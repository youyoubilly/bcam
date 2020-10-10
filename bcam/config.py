import cv2
import ipywidgets.widgets as widgets
    
class BaseCamConfig():

    def __init__(self, camera):
        self.camera = camera

    def init_camera(self):
        pass

    def device(self, value):
        self._device = value
        return self

    def resolution(self, width, height):
        ''' Set display resolution'''
        self._width = width
        self._height = height
        return self

    def cap_resolution(self, width, height):
        ''' Set display resolution'''
        self._capture_width = width
        self._capture_height = height
        return self

    def brightness(self, value):
        self._brightness = value
        return self
    
    def contrast(self, value):
        self._contrast = value
        return self
    
    def saturation(self, value):
        self._saturation = value
        return self
    
    def hue(self, value):
        self._hue = value
        return self
    
    def rotate_270(self):
        self._rotate_angle = 270
        return self
    
    def rotate_clockwise(self):
        return self.rotate_270()

    def rotate_90(self):
        self._rotate_angle = 90
        return self
    
    def rotate_counterclockwise(self):
        return self.rotate_90()
    
    def rotate_180(self):
        self._rotate_angle = 180
        return self
    
    def rotate_angle(self):
        return self._rotate_angle if hasattr(self, '_rotate_angle') else 0
    
    def auto_wb(self, value):
        self._auto_white_balance = value
        
    def auto_exposure(self, value):
        self._auto_exposure = value
        return self
    
    def gamma(self, value):
        self._gamma = value
        return self
    
    def gain(self, value):
        self._gain = value
        return self
    
    def wb_temp(self, value):
        self._white_balance_temperature = value
        return self
    
    def sharpness(self, value):
        self._sharpness = value
        return self
    
    def bl_compensation(self, value):
        self._backlight_compensation = value
        return self
    
    def fps(self, value):
        self._fps = value
        return self
    
    def verbose(self, value):
        self._verbose = value
        return self
    
    def show_panel(self, value):
        self._show_panel = value
        return self
    
    def is_verbose(self):
        return hasattr(self, '_verbose') and self._verbose
    
    def is_show_panel(self):
        return hasattr(self, '_show_panel') and self._show_panel
    
    def do_verbose(self):
        if hasattr(self, '_verbose') and self._verbose:
            print("Fourcc: {}, Auto exposure: {}, Format: {}, Mode: {}".format(\
                  self.camera.cap.get(cv2.CAP_PROP_FOURCC), \
                  self.camera.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE), \
                  self.camera.cap.get(cv2.CAP_PROP_FORMAT), \
                  self.camera.cap.get(cv2.CAP_PROP_MODE)))

            print("FPS: {}, Brightness: {}, Contrast: {}, Hue: {}, Gain: {}, Sharpness: {}".format(\
                  self.camera.cap.get(cv2.CAP_PROP_FPS), \
                  self.camera.cap.get(cv2.CAP_PROP_BRIGHTNESS), \
                  self.camera.cap.get(cv2.CAP_PROP_CONTRAST), \
                  self.camera.cap.get(cv2.CAP_PROP_HUE), \
                  self.camera.cap.get(cv2.CAP_PROP_GAIN), \
                  self.camera.cap.get(cv2.CAP_PROP_SHARPNESS)))
            
    def do_show_panel(self):
        if hasattr(self, '_show_panel') and self._show_panel:
            self.build_panel_item(cv2.CAP_PROP_BRIGHTNESS, "Brightness:", -64, 64, 0)
            self.build_panel_item(cv2.CAP_PROP_CONTRAST, "Contrast:", 0, 100, 33)
            self.build_panel_item(cv2.CAP_PROP_SATURATION, "Saturation:", 0, 100, 46)
            self.build_panel_item(cv2.CAP_PROP_HUE, "Hue:", -2000, 2000, 0, 10)
            self.build_panel_item(cv2.CAP_PROP_HUE, "Gamma:",100, 300, 100)
            self.build_panel_item(cv2.CAP_PROP_HUE, "Gain:",0, 2, 0)
            self.build_panel_item(cv2.CAP_PROP_SHARPNESS, "Sharpness:",0, 16, 8)
            self.build_rotate_panel()
            
            
    def build_panel_item(self, cv_value, description, min_val, max_val, value=0, step=1):
            brightness_w = widgets.IntSlider(min=min_val, max=max_val, value=value, step=step, description=description)
            def on_value_change(change):
                self.camera.cap.set(cv_value, change['new'])
            brightness_w.observe(on_value_change, names='value')
            
            display(brightness_w)
            
    def build_rotate_panel(self):
            brightness_w = widgets.IntSlider(min=0, max=270, value=0, step=90, description="Rotate:")
            def on_value_change(change):
                self._rotate_angle = -1 * change['new']
            brightness_w.observe(on_value_change, names='value')
            
            display(brightness_w)
            
    
class DefaultCamConfig(BaseCamConfig):
    
    def __init__(self, camera):
        super(DefaultCamConfig, self).__init__(camera)

        self._device = 0

    def build(self):
        self.camera.cap = cv2.VideoCapture(self._device)
        
        if hasattr(self, '_fps'):
            self.camera.cap.set(cv2.CAP_PROP_FPS, self._fps)
        
        if hasattr(self, '_height') and hasattr(self, '_width'):
            self.camera.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
            self.camera.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
            
        if hasattr(self, '_brightness'):
            self.camera.cap.set(cv2.CAP_PROP_BRIGHTNESS, self._brightness)

        if hasattr(self, '_contrast'):
            self.camera.cap.set(cv2.CAP_PROP_CONTRAST, self._contrast)
            
        if hasattr(self, '_saturation'):
            self.camera.cap.set(cv2.CAP_PROP_SATURATION, self._saturation)
            
        if hasattr(self, '_hue'):
            self.camera.cap.set(cv2.CAP_PROP_HUE, self._hue)

        if hasattr(self, '_gain'):
            self.camera.cap.set(cv2.CAP_PROP_GAIN, self._gain)

        if hasattr(self, '_sharpness'):
            self.camera.cap.set(cv2.CAP_PROP_SHARPNESS, self._sharpness)

        if hasattr(self, '_auto_exposure'):
            self.camera.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1 if self._auto_exposure else 0)
        
        self.do_verbose()
        self.do_show_panel()
        
        return self.camera
    
class JetsonCamConfig(BaseCamConfig):

    def __init__(self, camera):
        super(JetsonCamConfig, self).__init__(camera)
        self._width = 224.0
        self._height = 224.0
        self._fps = 2.0
        self._capture_width = 3280
        self._capture_height = 2464
        self._brightness = 10.0
        self._flip = 0

    def _gst_str(self):
        return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, ' % (self._capture_width, self._capture_height) + \
            'format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! ' % (self._fps, self._flip)+ \
            'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (self._width, self._height)

    def build(self):
        if self.rotate_angle() == 90:
            self._flip = 3
        elif self.rotate_angle() == 180:
            self._flip = 2
        elif self.rotate_angle() == 270:
            self._flip = 1
        
        print(self._gst_str())
        self.camera.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)
        
        self.do_verbose()
        self.do_show_panel()
        return self.camera