import unittest

from xyilib import client
from xyilib.tests.fake_camera import FakeCamera

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.camera = FakeCamera()
        self.camera.start()

    def tearDown(self):
        self.camera.stop()

    def test_auth(self):
        c = client.Camera('localhost', 9999)

if __name__ == '__main__':
    unittest.main()
