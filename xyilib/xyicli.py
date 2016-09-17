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
import logging

from client import Camera

loglevels = {0: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}


def get_loglevel(verbosity):
    if verbosity > max(loglevels.keys()):
        return logging.DEBUG
    if verbosity < 0:
        return logging.ERROR
    return loglevels[verbosity]


def do_timeget(c, args):
    t = c.get_clock()
    print(t.ctime())


name = 'Xiaomi YI'
parser = argparse.ArgumentParser(
    description='{} camera command-line client.'.format(name))

parser.add_argument('--verbose', '-v', action='count')

parser.add_argument('-a', '--address', help='Camera IP address or hostname.')

subparsers = parser.add_subparsers()

parser_timeget = subparsers.add_parser('time-get')
parser_timeget.set_defaults(func=do_timeget)

args = parser.parse_args()

logging.basicConfig(level=get_loglevel(args.verbose))

c = Camera(args.address)
try:
    args.func(c, args)
finally:
    c.close()
