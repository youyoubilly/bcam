import cv2

class BaseCamConfig():

    def __init__(self):
        pass

    def init_camera(self):
        pass

    def device(self, device):
        self._device = device
        return self
    
    def disp_resolution(self, width, height):
        ''' Set display resolution'''
        self._width = width
        self._height = height
        return self

    def cap_resolution(self, capture_width, capture_height):
        ''' Set display resolution'''
        self._capture_width = capture_width
        self._capture_height = capture_height
        return self

    def brightness(self, brightness):
        self._brightness = brightness
        return self

    def fps(self, fps):
        sefl._fps = fps
        return self

class DefaultCamConfig(BaseCamConfig):
    
    def __init__(self):
        super(DefaultCamConfig, self).__init__()
        self._width = 640
        self._height = 480

    def init_camera(self):
        return cv2.VideoCapture(0)


class JetsonCamConfig(BaseCamConfig):

    def __init__(self):
        super(JetsonCamConfig, self).__init__()
        self._width = 224.0
        self._height = 224.0
        self._fps = 2.0
        self._capture_width = 3280
        self._capture_height = 2464
        self._brightness = 10.0
        self._flip = 0

    def _gst_str(self):
        return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, " + \
            "format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! " + \
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
        self._capture_width, self._capture_height, self._fps, self._flip, self._width, self._height)

    def init_camera(self):
        return cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)