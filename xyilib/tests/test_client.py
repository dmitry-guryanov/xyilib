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

import logging
import unittest

from xyilib import client
from xyilib import errors
from xyilib.tests.fake_camera import FakeCamera

PORT = 9998


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.camera = FakeCamera(port=9998)
        self.camera.start()

    def tearDown(self):
        self.camera.stop()

    def test_auth(self):
        client.Camera('localhost', PORT)

    def test_get_param(self):
        c = client.Camera('localhost', PORT)
        param = c.get_param('serial_number')
        self.assertEqual(param, self.camera.conf()['serial_number'])

    def test_get_param_fail(self):
        c = client.Camera('localhost', PORT)
        with self.assertRaises(errors.ParamNotWritable):
            c.get_param('serial_numberx')

    def test_set_param(self):
        c = client.Camera('localhost', PORT)
        c.set_param('serial_number', 'xyz123')
        self.assertEqual(self.camera.conf()['serial_number'], 'xyz123')

    def test_set_param_fail(self):
        c = client.Camera('localhost', PORT)
        with self.assertRaises(errors.ParamNotWritable):
            c.set_param('serial_numberx', 'xyz123')

if __name__ == '__main__':
    logging.basicConfig(logging.DEBUG)
    unittest.main()
