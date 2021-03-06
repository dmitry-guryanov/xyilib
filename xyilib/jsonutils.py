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

import json
import string


class MultiReader(object):

    def __init__(self):
        self.buf = ''
        self.decoder = json.JSONDecoder()

    def push_data(self, data):
        objs = []
        self.buf += data
        while True:
            try:
                (obj, idx) = self.decoder.raw_decode(self.buf)
                try:
                    idx += next(i for i, j in enumerate(self.buf[idx:])
                                if j not in string.whitespace)
                    self.buf = self.buf[idx:]
                except StopIteration:
                    self.buf = ''
                objs.append(obj)
            except ValueError:
                break

        return objs
