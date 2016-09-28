# Copyright 2016 Dmitry Guryanov <dmitry.guryanov@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import logging
from six.moves import input

from client import Camera

loglevels = {0: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}


def get_loglevel(verbosity):
    if verbosity > max(loglevels.keys()):
        return logging.DEBUG
    if verbosity < 0:
        return logging.ERROR
    return loglevels[verbosity]


def do_shell(c, args):
    while True:
        try:
            cmd = input('>>> ')
        except (KeyboardInterrupt, EOFError):
            break
        if not cmd or cmd.isspace():
            continue
        try:
            cmd = json.loads(cmd)
        except ValueError as e:
            print('Invalid input: {}.'.format(e))
            continue
        if type(cmd) != dict:
            print('Command must be a dict.')
            continue
        if 'msg_id' not in cmd:
            print('Command must contain msg_id.')
        msg_id = cmd.pop('msg_id')
        resp = c._send_cmd(msg_id, **cmd)
        print(resp)


def do_get_all_params(c, args):
    params = c.get_params()
    for d in params:
        for k, v in d.items():
            print("{}: {}".format(k, v))


def do_get_param(c, args):
    val = c.get_param(args.param_name)
    print(val)


def do_set_param(c, args):
    c.set_param(args.param_name, args.param_value)


def do_get_choices(c, args):
    ret = c.get_choices(args.param_name)
    print('permission: {}'.format(ret['permission']))
    print('possible values:')
    for c in ret['choices']:
        print(c)


name = 'Xiaomi YI'
parser = argparse.ArgumentParser(
    description='{} camera command-line client.'.format(name))

parser.add_argument('--verbose', '-v', action='count')

parser.add_argument('-a', '--address', help='Camera IP address or hostname.')

subparsers = parser.add_subparsers()

p = subparsers.add_parser('shell')
p.set_defaults(func=do_shell)

p = subparsers.add_parser('get-all-params')
p.set_defaults(func=do_get_all_params)

p = subparsers.add_parser('get-param')
p.add_argument('param_name')
p.set_defaults(func=do_get_param)

p = subparsers.add_parser('set-param')
p.add_argument('param_name')
p.add_argument('param_value')
p.set_defaults(func=do_set_param)

p = subparsers.add_parser('get-choices')
p.add_argument('param_name')
p.set_defaults(func=do_get_choices)

args = parser.parse_args()

logging.basicConfig(level=get_loglevel(args.verbose))

c = Camera(args.address)
try:
    args.func(c, args)
finally:
    c.close()
