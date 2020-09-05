#Update:2020.09.1
#Inspired by jetcam: https://github.com/NVIDIA-AI-IOT/jetcam
#Modified by Kevin Pang, Billy Wang, Shawn Ling

import traitlets
from traitlets.config.configurable import SingletonConfigurable
import atexit
import threading
import numpy as np
import enum
import cv2
import time
from config import *

class BCamera(SingletonConfigurable):

    value = traitlets.Any()

    DEFAULT_CAM = 0
    JETSON_CAM = 1
    JETSON_DUAL_CAM = 2
    PI_CAM = 3
    USB_CAM = 4
    

    def __init__(self, *args, **kwargs):
        super(BCamera, self).__init__(*args, **kwargs)
        self.cap = None
        
    @staticmethod
    def builder(cam_type=DEFAULT_CAM):
        camera = BCamera()
        if cam_type == BCamera.JETSON_CAM:
            camera.cam_config = JetsonCamConfig(camera)
        elif cam_type == BCamera.JETSON_DUAL_CAM:
            pass
        elif cam_type == BCamera.PI_CAM:
            pass        
        elif cam_type == BCamera.USB_CAM:
            pass
        else:
            camera.cam_config = DefaultCamConfig(camera)

        return camera.cam_config
    
    def capture_frame(self):
        re, image = self.cap.read()
        if re:
            self.value = image
        
        return self.value
                

    def _capture_frames(self):
        while True:
            if self.cap is None:
                time.sleep(0.5)
                continue
            re, image = self.cap.read()
            if re:
                self.value = image
            else:
                self.cap.release()
                break

    def start(self, with_threading=True):
        if not hasattr(self, 'cam_config'):
            self.cam_config = DefaultCamConfig()

        self.value = np.empty((int(self.cam_config._height), int(self.cam_config._width), 3), dtype=np.uint8)        
        
        if with_threading and (not hasattr(self, 'thread') or not self.thread.isAlive()):
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def stop(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'thread'):
            self.thread.join()

    def restart(self):
        self.stop()
        self.start()