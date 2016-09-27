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


YI_JSON_PORT = 7878


# These consts are almost copied from
# https://github.com/jnordberg/yichan/blob/master/src/index.coffee
# git repo: https://github.com/jnordberg/yichan
# Great thanks to Johan Nordberg https://github.com/jnordberg !

YI_MSG_GET_PARAM = 1  # type: setting name
YI_MSG_SET_PARAM = 2  # type = name, param = value
# restore_factory_settings, param: on
# buzzer_ring param: on/off
# dev_reboot param: on

YI_MSG_GET_ALL_PARAMS = 3
YI_MSG_FORMAT_DRIVE = 4  # param can be disk drive letter, e.g. 'D:'
YI_MSG_GET_SPACE = 5  # type: total/free
# UNKNOWN =  6 rval: -13, {'type':'%s','param':'%s','param_size':%d}
# NOT USED = 7
# UNKNOWN =  8 # rval: -13

YI_MSG_GET_PARAM_CHOICES = 9
# UNKNOWN = 0x0A # rval: 0
YI_MSG_GET_SYSTEM_INFO = 0x0B
YI_MSG_GET_BATTERY_INFO = 0x0C
# UNKNOWN = 14 # rval -1 if param and type set
# UNKNOWN = 15 # rval -24 if type set
# UNKNOWN = 16 # rval 0 or -14

YI_MSG_CREATE_TOKEN = 0x101
YI_MSG_RELEASE_TOKEN = 0x102
YI_MSG_START_PREVIEW = 0x103
YI_MSG_STOP_PREVIEW = 0x104

YI_MSG_START_VIDEO_RECORD = 0x201
YI_MSG_STOP_VIDEO_RECORD = 0x202
YI_MSG_GET_RECORDED_LENGTH = 0x203
# UNKNOWN = 0x204 # ? rval 0 if recording error otherwise

YI_MSG_PHOTO_CAPTURE = 0x301
YI_MSG_STOP_PHOTO_CAPTURE = 0x302

YI_MSG_GET_THUMB = 0x401  # param: filename, type: any string?
# > {"msg_id": 1025, "param": "/tmp/fuse_d/DCIM/129MEDIA/YDXJ2007.jpg",
#    "type": "foo"}
# < {rval: 0, msg_id: 1025, size: 1673, type: 'thumb',
#    md5sum: '5f4eb3f0743b2c2cf718a8399828053e' }
# sends data over transfer socket

YI_MSG_GET_MEDIA_INFO = 0x402  # param: filename
# > {"msg_id": 1026, "param": "/tmp/fuse_d/DCIM/129MEDIA/YDXJ2007.jpg"}
# < { rval: 0, msg_id: 1026, size: 2711430, date: '2016-06-17 02:28:12',
#     resolution: '4608x2592', media_type: 'img' }

# UNKNOWN           = 0x403 # param: filename, type: any integer?
# > {"msg_id": 1027, "param": "/tmp/fuse_d/DCIM/129MEDIA/YDXJ2007.jpg",
#    "type": 100}
# < { rval: 0, msg_id: 1027 }

YI_MSG_DEL_FILE = 0x501
YI_MSG_LS = 0x502
YI_MSG_CD = 0x503
YI_MSG_PWD = 0x504
YI_MSG_GET_FILE = 0x505
YI_MSG_PUT_FILE = 0x506
YI_MSG_CANCEL_FILE = 0x507

YI_MSG_WIFI_RESTART = 0x601
# 0x701 - accepted but no response sent

# 0x1000001  sdcard type? { rval: 0, msg_id: 16777217, param: 'sd_hc' }
# 0x1000002  -13
# 0x1000003  -30 with param, -25 no param
# 0x1000004  -13
# 0x1000005  start quick record
# 0x1000006  -14 with param, -13 no param
# 0x1000007  -14 with param, -13 no param
# 0x1000008  another wifi restart?
# 0x1000009  ? rval 0
# 0x100000A  ? rval 0
# 0x100000B  take photo while video is recording - event piv_complete
# 0x100000C  configure capture mode - param: precise quality cont.;5.0 sec
# 0x100000D  ?? sent with no
# 0x100000E  ?? stop mabye?
# 0X100000F  bind bluetooth devices?
# 0x1000010  unbind bluetooth devices?
#            { type: 'btc_delete_all_binded_dev', param: '3' }
# 0x1000011  -13
# 0x1000012  ? rval 0
# 0x1000013  unzip firmware?
# 0x1000014  last captured photo?
#            {rval: 0, msg_id: 16777236,
#             param: '/tmp/fuse_d/DCIM/100MEDIA/YDXJ0003.jpg' }
# 0x1000015  { rval: 0, msg_id: 16777237, param: '7743' }
# 0x1000016  -14
# 0x1000017  invalid message id -23
# 0x1000018  invalid message id -23
# 0x1000019  -14
# 0x100001A  dumps firmware log to /DCIM/firmware.log
#            { rval: 0, msg_id: 16777242, error: '-2' }
#            { rval: 0, msg_id: 16777242, param: '/DCIM/firmware.log' }

YI_MSG_LINUX_SET_SOFTAP_CONFIG = 0x2000001  # does not work?
YI_MSG_LINUX_GET_SOFTAP_CONFIG = 0x2000002  # sends invalid JSON
YI_MSG_LINUX_RESTART_WEB_SERVER = 0x2000006

# something to do with firmware updates
# 0x4000001 - ?
# 0x4000002 - ?
# 0x4000003 - rval 0
# 0x4000004 - rval 0
