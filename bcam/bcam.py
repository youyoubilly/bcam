#Update:2020.09.1
#Inspired by jetcam: https://github.com/NVIDIA-AI-IOT/jetcam
#Modified by Kevin Pang, Billy Wang, Shawn Ling

import traitlets
from traitlets.config.configurable import SingletonConfigurable
import threading
import numpy as np
import cv2
import time
import imutils
from imutils.video import FPS
from .config import *

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
        self.links = []
        self._running = False
        
    @classmethod
    def builder(cls, cam_type=DEFAULT_CAM):
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
            if self.cam_config.rotate_angle() != 0:
                (h, w) = image.shape[:2]
                # calculate the center of the image
                center = (w / 2, h / 2)
                M = cv2.getRotationMatrix2D(center, self.cam_config.rotate_angle(), 1.0)
                self.value = cv2.warpAffine(image, M, (h, w))
                
        return self.value
                
    def _capture_frames(self):
        _fps = FPS()
        _fps.start()
        _counter = 0
        
        current_fps = 0
        
        while self._running:
            if self.cap is None:
                time.sleep(0.5)
                continue
                
            re, image = self.cap.read()
            
            angle = self.cam_config.rotate_angle()
            if angle != 0 and image is not None:
                if isinstance(self.cam_config, JetsonCamConfig):
                    pass
                else:
                    (h, w) = image.shape[:2]
                    # calculate the center of the image
                    center = (w / 2, h / 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    image = cv2.warpAffine(image, M, (h, w))
            
            if re:                
                if self.cam_config.is_verbose():
                    image=cv2.putText(image,'FPS: {:.2f}'.format(current_fps),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
                    
                if _counter >= 100:
                    _fps.stop()
                    current_fps = _fps.fps()
                    _fps = FPS()
                    _counter = 0
                    _fps.start()
                    
                self.value = image
                _fps.update()
                
                _counter+=1
            else:
                print("Cam error, will realase the camera.")
                self.cap.release()
                break

    def start(self, with_threading=True):
        if not hasattr(self, 'cam_config'):
            self.cam_config = DefaultCamConfig()

        self.value = np.empty((int(self.cam_config._height), int(self.cam_config._width), 3), dtype=np.uint8)        
        
        if with_threading and (not hasattr(self, 'thread') or not self.thread.isAlive()):
            self._running = True
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def jpeg(self):
        return self.bgr8_to_jpeg(self.value)
    
    def stop(self):
        if hasattr(self, 'cap'):
            self._running = False
            self.cap.release()
        if hasattr(self, 'thread'):
            self.thread.join()

    def restart(self):
        self.stop()
        self.start()
        for link in self.links:
            link.release()
            
    def bgr8_to_jpeg(self, value):
        return bytes(cv2.imencode('.jpg', value)[1])
    
    def link(self, widget):
        link = traitlets.dlink((self,'value'), (widget, 'value'), transform=self.bgr8_to_jpeg)
        self.links.append(link)
        


       