import unittest

from tf2_vgpu.virtual_gpu import VirtualGPU


class TestVirtualGPU(unittest.TestCase):
    def test_create(self):
        gpu = VirtualGPU(512)

        self.assertIsNotNone(gpu)
