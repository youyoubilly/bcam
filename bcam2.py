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
        
    def config_builder(self, cam_type=DEFAULT_CAM):
        if cam_type == BCamera.JETSON_CAM:
            self.cam_config = JetsonCamConfig()
        elif cam_type == BCamera.JETSON_DUAL_CAM:
            pass
        elif cam_type == BCamera.PI_CAM:
            pass        
        elif cam_type == BCamera.USB_CAM:
            pass
        else:
            self.cam_config = DefaultCamConfig()

        return self.cam_config
        

    def _capture_frames(self):
        while True:
            print("6")
            re, image = self.cap.read()
            print("7", re)
            if re:
                print(image.shape)
                self.value = image
            else:
                self.cap.release()
                break

    def start(self):
        print("1")
        if not hasattr(self, 'cam_config'):
            self.cam_config = DefaultCamConfig()
        print("2")

        self.value = np.empty((int(self.cam_config._height), int(self.cam_config._width), 2), dtype=np.uint8)
        print("3")
        self.cap = self.cam_config.init_camera()
        print("4")
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            print("5")
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