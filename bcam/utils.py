import cv2

def bgr8_to_jpeg(value):
    return bytes(cv2.imencode('.jpg', value)[1])