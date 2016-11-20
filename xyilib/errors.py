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


class CameraError(Exception):
    def __init__(self, rval):
        self.rval = rval

    def __str__(self):
        if hasattr(self, 'message'):
            return self.message
        else:
            return 'Camera returned error {}'.format(self.rval)


class Success(CameraError):
    message = 'Ok'


class FileNotFound(CameraError):
    message = 'File not found'


class OtherDeviceConnected(CameraError):
    message = 'Other device connected'


class Unauthorized(CameraError):
    message = 'Unauthorized'


class InvalidJson(CameraError):
    message = 'Received data is not JSON'


class InvalidArguments(CameraError):
    message = 'Invalid arguments'


class InvalidValue(CameraError):
    message = 'Invalid Value'


class ParamNotChanged(CameraError):
    message = 'Parameter already at requested value'


class ParamNotWritable(CameraError):
    message = 'Parameter is not writable'


class InvalidMessageId(CameraError):
    message = 'Invalid message id'


class InvalidPath(CameraError):
    message = 'Invalid path'


class ConnectionClosed(CameraError):
    message = 'Connection unexcpectedly closed'

ERR_SUCCESS = 0
ERR_FILE_NOT_FOUND = -1
ERR_OTHER_DEVICE_CONNECTED = -3
ERR_UNAUTHORIZED = -4
ERR_INVALID_JSON = -7
ERR_INVALID_ARGUMENTS = -9
ERR_INVALID_VALUE = -13
ERR_PARAM_NOT_CHANGED = -14
ERR_PARAM_NOT_WRITABLE = -15
ERR_INVALID_MESSAGE_ID = -23
ERR_INVALID_PATH = -26
ERR_CONNECTION_CLOSED = -10000

ERRORS = {
    ERR_SUCCESS: Success,
    ERR_FILE_NOT_FOUND: FileNotFound,
    ERR_OTHER_DEVICE_CONNECTED: OtherDeviceConnected,
    ERR_UNAUTHORIZED: Unauthorized,
    ERR_INVALID_JSON: InvalidJson,
    ERR_INVALID_ARGUMENTS: InvalidArguments,
    ERR_INVALID_VALUE: InvalidValue,
    ERR_PARAM_NOT_CHANGED: ParamNotChanged,
    ERR_PARAM_NOT_WRITABLE: ParamNotWritable,
    ERR_INVALID_MESSAGE_ID: InvalidMessageId,
    ERR_INVALID_PATH: InvalidPath,
    ERR_CONNECTION_CLOSED: ConnectionClosed,
}


def error_by_rval(rval, *args, **kwargs):
    error_cls = ERRORS.get(rval, CameraError)
    return error_cls(rval, *args, **kwargs)
