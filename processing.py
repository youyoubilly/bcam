import numpy as np
import cv2

def bgr8_to_jpeg(value, quality=10):
    return bytes(cv2.imencode('.jpg', value)[1])

def frame_dp(camera_image):
    image = np.copy(camera_image)
    jpeg_image = bgr8_to_jpeg(image)
    return jpeg_image