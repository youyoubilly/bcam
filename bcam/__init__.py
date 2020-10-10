from .bcam import BCamera
from .config import *

DEFAULT_CAM = 0
JETSON_CAM = 1
JETSON_DUAL_CAM = 2
PI_CAM = 3
USB_CAM = 4
    
def builder(cam_type=DEFAULT_CAM):
    return BCamera.builder(cam_type)