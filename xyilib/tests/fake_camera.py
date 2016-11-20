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
CONF = {
    'app_status': 'idle',
    'auto_low_light': 'on',
    'auto_power_off': 'off',
    'burst_capture_number': '7 p \\/ s',
    'buzzer_ring': 'off',
    'buzzer_volume': 'low',
    'camera_clock': '2016-11-20 08:08:19',
    'capture_default_mode': 'precise quality',
    'capture_mode': 'precise quality',
    'dev_functions': '7743',
    'dual_stream_status': 'on',
    'emergency_file_backup': 'off',
    'hw_version': 'YDXJ_v25L',
    'led_mode': 'all enable',
    'loop_record': 'off',
    'meter_mode': 'spot',
    'osd_enable': 'off',
    'photo_quality': 'S.Fine',
    'photo_size': '16M (4608x3456 4:3)',
    'photo_stamp': 'off',
    'piv_enable': 'on',
    'precise_cont_capturing': 'off',
    'precise_cont_time': '0.5 sec',
    'precise_self_remain_time': '0',
    'precise_self_running': 'off',
    'precise_selftime': '3s',
    'preview_status': 'on',
    'quick_record_time': '0',
    'rc_button_mode': 'mode_shutter',
    'rec_default_mode': 'record',
    'rec_mode': 'record',
    'record_photo_time': '5',
    'save_log': 'off',
    'sd_card_status': 'insert',
    'sdcard_need_format': 'no-need',
    'serial_number': 'Z25L622ACN4547421',
    'start_wifi_while_booted': 'off',
    'streaming_status': 'on',
    'support_auto_low_light': 'on',
    'sw_version': 'YDXJv22L_1.3.0_build-20160524143845_b1049_i841_s1125',
    'system_default_mode': 'record',
    'system_mode': 'record',
    'timelapse_photo': 'off',
    'timelapse_video': '0.5',
    'timelapse_video_duration': 'off',
    'timelapse_video_resolution': '1920x1080 60P 16:9',
    'video_output_dev_type': 'off',
    'video_quality': 'S.Fine',
    'video_resolution': '1920x1080 30P 16:9',
    'video_rotate': 'off',
    'video_stamp': 'off',
    'video_standard': 'NTSC',
    'warp_enable': 'off',
    'wifi_password': '12345678',
    'wifi_ssid': 'YDXJ_4547421'
}


class FakeCamera(object):

    def __init__(self, port=9999):
        self.json_reader = jsonutils.MultiReader()
        self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.ssock.bind(('localhost', self.port))
        self.ssock.listen(1)
        self.need_stop = False

        self.is_auth = False
        self.token = 451625
        self.config = CONF.copy()

    def handle_request(self, obj):
        if 'msg_id' not in obj:
            self.csock.send(json.dumps({'rval': errors.ERR_UNAUTHORIZED,
                                        'msg_id': 0}))
            return

        msg_id = obj.pop('msg_id')
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
        obj.pop('token')

        if msg_id == consts.YI_MSG_GET_PARAM:
            if 'type' not in obj:
                self.csock.send(json.dumps(
                    {'msg_id': msg_id,
                     'rval': errors.ERR_INVALID_ARGUMENTS}))
            type_ = obj.pop('type')
            if type_ not in self.config:
                self.csock.send(json.dumps(
                    {'msg_id': msg_id,
                     'rval': errors.ERR_PARAM_NOT_WRITABLE}))
            else:
                self.csock.send(json.dumps(
                    {'msg_id': msg_id,
                     'rval': 0,
                     'type': type_,
                     'param': self.config[type_]}))

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
                try:
                    self.handle_request(obj)
                except Exception as e:
                    print("Exception in camera thread!")
                    print(e)
                    self.need_stop = True
                    self.csock.shutdown(socket.SHUT_RDWR)
                    self.csock.close()

    def start(self):
        self.thread = threading.Thread(target=self._thread)
        self.thread.start()

    def stop(self):
        if hasattr(self, 'csock') and self.csock:
            self.csock.shutdown(socket.SHUT_RDWR)
            self.csock.close()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', self.port))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except socket.error as err:
            if err.errno != errno.ECONNREFUSED:
                raise

        self.thread.join()

    def get_fake_config(self):
        return self.config

if __name__ == '__main__':
    camera = FakeCamera()
    camera.start()
    input()
