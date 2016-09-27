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

from collections import deque
from datetime import datetime
import json
import logging
import socket
import threading

import consts
import jsonutils


log = logging.getLogger('xyilib.client')
BUFSIZE = 65536


class Camera(object):

    def __init__(self, address, port=consts.YI_JSON_PORT):
        self.address = address
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))
        self.fsock = self.sock.makefile()

        self.json_reader = jsonutils.MultiReader()
        self.msgs = {}

        log.debug("Starting receiver thread for %s", address)
        self.thread = threading.Thread(target=self._receive,
                                       name="receiver-{}".format(address))
        self.thread.start()
        self.token = None

        self.do_auth()

    def do_auth(self):
        log.debug('Trying to authenticate to %s', self.address)
        resp = self._send_cmd(
            {'msg_id': consts.YI_MSG_CREATE_TOKEN, 'token': 0})
        log.info('do_auth: got {}'.format(resp))
        self.token = resp['param']

    def _send_cmd(self, obj):
        if self.token:
            obj['token'] = self.token

        log.info('Send object: %r', obj)
        s = json.dumps(obj)
        self.sock.send(s + '\n')

        cv, q = self.msgs.setdefault(obj['msg_id'],
                                     (threading.Condition(), deque()))
        with cv:
            if not q:
                cv.wait()
            resp = q.popleft()
        return resp

    def _receive(self):
        name = threading.current_thread().name
        while True:
            log.debug('[%s]: Waiting for data from camera', name)
            s = self.sock.recv(BUFSIZE)
            if len(s) == 0:
                log.info('[%s]: Received an empty string, terminating', name)
                break

            log.debug('[%s]: Got data: %s', name, s)

            objs = self.json_reader.push_data(s)
            for obj in objs:
                log.info('[%s]: Got object: %r', name, obj)
                cv, q = self.msgs.get(obj['msg_id'], (None, None))
                if cv:
                    with cv:
                        q.append(obj)
                        cv.notify()

    def close(self):
        log.info("Closing connection to %s", self.address)
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.thread.join()

    def get_clock(self):
        resp = self._send_cmd({'type': 'camera_clock', 'msg_id': 1})
        return datetime.strptime(resp['param'], '%Y-%m-%d %H:%M:%S')
