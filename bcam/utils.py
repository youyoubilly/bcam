import cv2

def bgr8_to_jpeg(value):
    if value is None:
        return bytes()
    return bytes(cv2.imencode('.jpg', value)[1])