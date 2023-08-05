#!/usr/bin/python3.7
import argparse
import binascii
import datetime
import hashlib
import dockerfile
import io
import json
import os
import paramiko
import requests
import shlex
import sseclient
import subprocess
import sys
import tempfile

from urllib.parse import urlparse

VISOR_DIR = os.path.expanduser('~/.visor')
VISOR_CONFIG = os.path.join(VISOR_DIR, 'config.json')
VISOR_TRANSMIT_DIR = os.path.join(VISOR_DIR, 'transmit')

# TODO: when running lots of builds in parallel, it seems like duplicate network
# ids can be created, despite the locks on _create_namespaced_network()
# TODO: make ctrl+c properly cancel a build
# TODO: don't take snapshots of very fast commands
# TODO: partition by team
# TODO: should be able to `visor console <container_id>` to recover from broken ssh
# TODO: REPEATABLE should be taking state of all required machines not just cur
# TODO: SNAPSHOT should be global/local to a machine
# TODO: --keep-running vms should auto-sleep after 20 mins of inactivity
# TODO: total time getting printed before error
# TODO: COPY semantics should match docker exactly
# TODO: clean up network after all containers in that network are gone
# TODO: host CPU going crazy even when guest cpu is close to idle
# TODO: make memory adjustable from inside visorfile
# TODO: server should be able to specify root dir

config = {}
if os.path.exists(VISOR_CONFIG):
  with open(VISOR_CONFIG, 'r') as f:
    config = json.loads(f.read())

def get_hash(string):
  return hashlib.sha256(string.encode('utf8')).hexdigest()[:30]

def get_command_value(command):
  return command.original[len(command.cmd):].strip()

def validate_server_url(server_url=None):
  if not server_url:
    if 'defaultServer' not in config:
      raise Exception('You need to run `visor login` first')
    return config['defaultServer']
  return server_url

def _api_call(*args, **kwargs):
  if 'timeout' not in kwargs:
    kwargs['timeout'] = 30
  server_url = validate_server_url(kwargs.get('server_url'))
  if 'server_url' in kwargs:
    del kwargs['server_url']
  if len(args) >= 2:
    args = list(args)
    args[1] = server_url + '/api/v1/' + args[1]
  if 'url' in kwargs:
    kwargs['url'] = server_url + '/api/v1/' + kwargs['url']
  return requests.request(*args, **kwargs)

exitcode = 0
def _stream(resp):
  global exitcode
  client = sseclient.SSEClient(resp)
  for event in client.events():
    if event.event == 'log':
      print(json.loads(event.data))
    elif event.event == 'error':
      print(json.loads(event.data))
      exitcode = 1
    else:
      print(event)
      raise Exception(f'Unknown event type {event.event}')

def safe_non_stream_api_call(*args, **kwargs):
  resp = _api_call(*args, **kwargs)
  if resp.status_code == 200:
    return resp.json()
  raise Exception('Server responded with %s: %s' % (resp.status_code, resp.text))

def safe_stream_api_call(*args, **kwargs):
  kwargs['stream'] = True
  if 'timeout' not in kwargs:
    kwargs['timeout'] = 1200
  resp = _api_call(*args, **kwargs)
  if resp.status_code == 200:
    return _stream(resp)
  raise Exception('Server responded with %s; %s' % (resp.status_code, resp.text))

def verify_login(server_url=None):
  if not server_url:
    if 'defaultServer' not in config:
      raise Exception('You need to run `visor login` first')
    server_url = config['defaultServer']
  if server_url not in config['auths']:
    raise Exception('You are not logged into server %s' % server_url)
  return server_url

def do_login(args):
  if not args.url.startswith('http'):
    raise argparse.ArgumentTypeError('url must start with http or https')
  resp = safe_non_stream_api_call(
    'post',
    'login',
    json={'username': args.username, 'password': args.password},
    server_url=args.url
  )
  if 'auths' not in config:
    config['auths'] = {}
  if args.url not in config['auths']:
    config['auths'][args.url] = {}
  config['auths'][args.url]['username'] = args.username
  config['auths'][args.url]['sshHost'] = urlparse(args.url).hostname
  config['auths'][args.url]['sshPort'] = resp['sshPort']
  config['auths'][args.url]['sshUsername'] = resp['username']
  config['auths'][args.url]['sshKey'] = resp['key']
  config['auths'][args.url]['sshTransmitDir'] = resp['repoPath']
  config['defaultServer'] = args.url
  os.makedirs(VISOR_DIR, exist_ok=True)
  with open(VISOR_CONFIG, 'w') as f:
    f.write(json.dumps(config, indent=2))

def find_context_dir(visorfile):
  ret = os.path.dirname(os.path.abspath(visorfile))
  cur = ret
  while cur != os.path.dirname(cur):
    if os.path.exists(os.path.join(cur, '.git')):
      return cur
    cur = os.path.dirname(cur)
  return ret

def add_all_files_and_subfiles(context_dir, files, path):
  if os.path.isdir(path):
    for root, dirs, fs in os.walk(path):
      for f in fs:
        name = os.path.abspath(os.path.join(root, f))
        if os.path.commonpath([name, context_dir]) != context_dir:
          raise Exception(f'Illegal COPY {name}')
        files.add(name)
      for d in dirs:
        name = os.path.abspath(os.path.join(root, d))
        if os.path.commonpath([name, context_dir]) != context_dir:
          raise Exception(f'Illegal COPY {name}')
        if os.path.islink(name):
          files.add(name)
  else:
    name = os.path.abspath(path)
    if os.path.commonpath([name, context_dir]) != context_dir:
      raise Exception(f'Illegal COPY {name}')
    files.add(name)

def find_context_files(visorfile):
  visorfile = os.path.abspath(visorfile)
  context_dir = find_context_dir(visorfile)
  cur_visorfile = visorfile
  files = {visorfile}
  for i in range(10):
    next_visorfile = None
    visorfile_dir = os.path.dirname(cur_visorfile)
    with open(cur_visorfile, 'r') as f:
      commands = dockerfile.parse_string(f.read())
      for command in commands:
        if command.cmd == 'inherit':
          base = get_command_value(command)
          if base.startswith('.'):
            next_visorfile = os.path.join(visorfile_dir, base)
            if os.path.isdir(next_visorfile):
              next_visorfile = os.path.join(next_visorfile, 'Visorfile')
            if os.path.commonpath([next_visorfile, context_dir]) != context_dir:
              raise Exception(f'Illegal INHERIT {base}')
            files.add(next_visorfile)
        elif command.cmd == 'copy':
          # TOOD escaped spaces won't work
          paths = get_command_value(command).split(' ')
          host_paths = paths[:-1]
          for host_path in host_paths:
            if host_path.startswith('/'):
              add_all_files_and_subfiles(
                context_dir, files, os.path.join(context_dir, host_path)
              )
            else:
              add_all_files_and_subfiles(
                context_dir, files, os.path.join(visorfile_dir, host_path)
              )
    if not next_visorfile:
      break
    cur_visorfile = next_visorfile
  else:
    raise Exception('FROM chain is too long')
  if os.path.exists(os.path.join(context_dir, '.git')):
    ignored = subprocess.check_output([
      'git', 'ls-files', '-o', '-i', '--exclude-standard'
    ], cwd=context_dir).decode('utf8').splitlines()
    # get all ignored files, recursively for all submodules, and write
    # paths rooted at the context_dir
    # HACK: need the command above separately because this call does not
    # include a call to the root repo
    ignored.extend(subprocess.check_output([
      'git', 'submodule', 'foreach', '--recursive',
      'git ls-files -o -i --exclude-standard | sed "s|^|$path/|"',
    ], cwd=context_dir).decode('utf8').splitlines())
    ignored = set([
      os.path.normpath(os.path.join(context_dir, x)) for x in ignored
    ])
    files = {os.path.normpath(x) for x in files}
    files = {x for x in files if x not in ignored}

  files = [os.path.relpath(x, start=context_dir) for x in files]
  return files

def transmit_context(visorfile, archive, server_url=None):
  server_url = verify_login(server_url)
  c = config['auths'][server_url]
  with tempfile.NamedTemporaryFile('w', delete=False) as f:
    f.write(c['sshKey'])
    f.flush()
    env = os.environ.copy()
    env['BORG_RELOCATED_REPO_ACCESS_IS_OK'] = 'yes'
    env['BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK'] = 'yes'
    args = [
      'borg',
      'create',
      '--stats',
      '--lock-wait', '120',
      '--rsh', 'ssh -i %s -o "StrictHostKeyChecking no" -o "IdentitiesOnly=yes"' % f.name,
      'ssh://%s@%s:%s%s::%s' % (
        c['sshUsername'],
        c['sshHost'],
        c['sshPort'],
        c['sshTransmitDir'],
        archive
      ),
    ]
    args.extend(find_context_files(visorfile))
    #print(' '.join([shlex.quote(x) for x in args]))
    subprocess.check_call(args, env=env, cwd=find_context_dir(visorfile))
  return

def do_build_base(args):
  safe_stream_api_call(
    'post',
    'build_base',
    json={
      'os': args.os,
    },
  )

def do_build(args):
  nonce = binascii.b2a_hex(os.urandom(15)).decode('utf8')
  archive = '%s-%s' % (datetime.datetime.now().strftime('%Y%m%d'), nonce)
  print('Sending build context...')
  server_url = verify_login()
  visorfile = args.visorfile
  if os.path.isdir(visorfile):
    visorfile = os.path.join(visorfile, 'Visorfile')
  transmit_context(visorfile, archive)
  context_dir = find_context_dir(visorfile)
  print('Done sending build context\n')

  safe_stream_api_call(
    'post',
    'build',
    json={
      'archive': archive,
      'visorfileRelpath': os.path.relpath(visorfile, start=context_dir),
      'keepRunning': args.keep_running,
    },
  )

def do_run(args):
  resp = safe_non_stream_api_call(
    'post', 'run', json={'imageId': args.image_id}
  )
  print(resp['containerId'])

def do_ssh(args, server_url=None):
  guest_ssh_args = safe_non_stream_api_call(
    'get', 'guest_ssh_args', json={'containerId': args.container_id}
  )
  server_url = verify_login(server_url)
  c = config['auths'][server_url]
  with tempfile.NamedTemporaryFile('w', delete=False) as f:
    f.write(c['sshKey'])
    f.flush()
    subcmd = 'ssh -t -p %s -i %s -o "StrictHostKeyChecking no" %s@localhost %s' % (
      str(guest_ssh_args['port']),
      guest_ssh_args['keyFile'],
      guest_ssh_args['username'],
      shlex.quote(args.cmd) if args.cmd else ''
    )
    cmd = [x for x in [
      'ssh',
      '-t',
      '-p', str(c['sshPort']),
      '-i', f.name,
      '-o', 'StrictHostKeyChecking no',
      '%s@%s' % (c['sshUsername'], c['sshHost']),
      subcmd
    ] if x]
    os.execvp('ssh', cmd)

def do_console(args):
  guest_console_args = safe_non_stream_api_call(
    'get', 'guest_console_args', json={'containerId': args.container_id}
  )
  server_url = verify_login(server_url)
  c = config['auths'][server_url]
  with tempfile.NamedTemporaryFile('w', delete=True) as f:
    f.write(c['sshKey'])
    f.flush()
    subcmd = 'telnet localhost {port}'
    # TODO: LOH not sure how to make telnet secure

def do_ps(args):
  resp = safe_non_stream_api_call('get', 'ps')
  for container in resp['containers']:
    print(container)

def do_stop(args):
  raise Exception('Not implemented')

def do_start(args):
  raise Exception('Not implemented')

def do_rm(args):
  resp = safe_non_stream_api_call(
    'post', 'rm', json={'containerId': args.container_id}
  )
  print(resp['containerId'])

def do_images(args):
  resp = safe_non_stream_api_call('get', 'images')
  for image in resp['images']:
    print(image)

def do_rmi(args):
  resp = safe_non_stream_api_call(
    'post', 'rmi', json={'imageId': args.image_id}
  )
  print(resp['imageId'])

def do_view(args):
  resp = safe_non_stream_api_call(
    'post', 'view', json={'publishableId': args.publishable_id}
  )
  print(f'Published guest port {resp["guestPort"]} on localhost:{resp["hostPort"]}')

def do_clean(args):
  safe_stream_api_call(
    'post',
    'clean',
    json={
      'includeBases': args.include_bases,
    },
  )

class Unbuffered(object):
  def __init__(self, stream):
    self.stream = stream
  def write(self, data):
    self.stream.write(data)
    self.stream.flush()
  def writelines(self, datas):
    self.stream.writelines(datas)
    self.stream.flush()
  def __getattr__(self, attr):
    return getattr(self.stream, attr)

def main():
  sys.stdout = Unbuffered(sys.stdout)

  main_parser = argparse.ArgumentParser(description='Visor client')
  subparsers = main_parser.add_subparsers(dest='subparser')
  subparsers.required = True

  login_parser = subparsers.add_parser('login', help='Log into a visor server')
  login_parser.add_argument('url')
  login_parser.add_argument('username')
  login_parser.add_argument('password')
  login_parser.set_defaults(func=do_login)

  build_base_parser = subparsers.add_parser(
    'build-base', help='Build a base image'
  )
  build_base_parser.add_argument(
    'os', choices=['ubuntu16', 'ubuntu18', 'ubuntu20']
  )
  build_base_parser.set_defaults(func=do_build_base)

  build_parser = subparsers.add_parser('build', help='Build a Visorfile')
  build_parser.add_argument('--keep-running', action='store_true')
  build_parser.add_argument('visorfile', help='The Visorfile to build')
  build_parser.set_defaults(func=do_build)

  run_parser = subparsers.add_parser('run', help='Run an instance of image_id')
  run_parser.add_argument('image_id', type=str)
  run_parser.set_defaults(func=do_run)

  ssh_parser = subparsers.add_parser('ssh', help='SSH to a running container')
  ssh_parser.add_argument('container_id', type=str)
  ssh_parser.add_argument('cmd', type=str, nargs='?', default=None)
  ssh_parser.set_defaults(func=do_ssh)

  console_parser = subparsers.add_parser(
    'console', help='Display the console to a running container'
  )
  console_parser.add_argument('container_id', type=str)
  console_parser.set_defaults(func=do_console)

  ps_parser = subparsers.add_parser('ps', help='List running containers')
  ps_parser.set_defaults(func=do_ps)

  stop_parser = subparsers.add_parser('stop', help='Stop a running container')
  stop_parser.set_defaults(func=do_stop)

  start_parser = subparsers.add_parser('start', help='Start a stopped container')
  start_parser.set_defaults(func=do_start)

  rm_parser = subparsers.add_parser('rm', help='Kill a container')
  rm_parser.add_argument('container_id', type=str)
  rm_parser.add_argument('--force', type=bool, default=False)
  rm_parser.set_defaults(func=do_rm)

  images_parser = subparsers.add_parser('images', help='List all images')
  images_parser.set_defaults(func=do_images)

  rmi_parser = subparsers.add_parser('rmi', help='Delete an image')
  rmi_parser.add_argument('image_id', type=str)
  rmi_parser.set_defaults(func=do_rmi)

  view_parser = subparsers.add_parser('view', help='View a published id')
  view_parser.add_argument('publishable_id', type=str)
  view_parser.set_defaults(func=do_view)

  clean_parser = subparsers.add_parser('clean', help='Wipe all images and vms')
  clean_parser.add_argument('--include-bases', action='store_true')
  clean_parser.set_defaults(func=do_clean)

  args = main_parser.parse_args()
  args.func(args)

  sys.exit(exitcode)

if __name__ == '__main__':
  main()
