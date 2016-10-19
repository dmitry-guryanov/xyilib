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

import errno
import json
import socket
import threading

from six.moves import input

from xyilib import consts
from xyilib import errors
from xyilib import jsonutils


BUFSIZE = 65536


class FakeCamera(object):

    def __init__(self, port=9999):
        self.json_reader = jsonutils.MultiReader()
        self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ssock.bind(('localhost', port))
        self.ssock.listen(1)
        self.need_stop = False

        self.is_auth = False
        self.token = 451625

    def handle_request(self, obj):
        if 'msg_id' not in obj:
            self.csock.send(json.dumps({'rval': errors.ERR_UNAUTHORIZED,
                                        'msg_id': 0}))
            return

        msg_id = obj['msg_id']
        if msg_id == consts.YI_MSG_CREATE_TOKEN:
            self.is_auth = True
            self.csock.send(json.dumps({'rval': 0,
                                        'msg_id': consts.YI_MSG_CREATE_TOKEN,
                                        'param': self.token}))
            return

        if (not self.is_auth or 'token' not in obj or
                obj['token'] != self.token):
            self.csock.send(json.dumps({'msg_id': obj['msg_id'],
                                        'rval': errors.ERR_UNAUTHORIZED}))
            return

    def _thread(self):
        (self.csock, address) = self.ssock.accept()
        self.ssock.shutdown(socket.SHUT_RDWR)
        self.ssock.close()
        self.ssock = None

        while not self.need_stop:
            data = self.csock.recv(BUFSIZE)
            if len(data) == 0:
                break
            objs = self.json_reader.push_data(data)
            for obj in objs:
                self.handle_request(obj)

    def start(self, port=9999):
        self.thread = threading.Thread(target=self._thread)
        self.thread.start()

    def stop(self):
        if hasattr(self, 'csock') and self.csock:
            self.csock.shutdown(socket.SHUT_RDWR)
            self.csock.close()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 9999))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except socket.error as err:
            if err.errno != errno.ECONNREFUSED:
                raise

        self.thread.join()

if __name__ == '__main__':
    camera = FakeCamera()
    camera.start()
    input()
