# bcam
bcam is an easy to use Python camera interface for NVIDIA Jetson.

This is forked form [jetcam](https://github.com/NVIDIA-AI-IOT/jetcam), intended to be used by BillioTech Team. 

Of course, You can clone and use it as well, if you find it convenient.

Quick guide is [here](demo.ipynb)

If you find an issue, please [let us know](../..//issues)!

## Install 

```bash
pip3 install bcam
```

## Usage

### Start camera from Jupyter Notebook
```python
from bcam import BCamera
import traitlets
import ipywidgets.widgets as widgets

def bgr8_to_jpeg(value):
    return bytes(cv2.imencode('.jpg', value)[1])

bcam = BCamera.builder() \
        .device(0) \
        .resolution(800, 600) \
        .fps(5) \
        .build()

bcam.start()

image_widget1 = widgets.Image(format='jpeg', width=400, height=400)

display(image_widget)

camera_link = traitlets.dlink((bcam, 'value'), (image_widget, 'value'), transform=bgr8_to_jpeg)
```

### Stop
```python
camera_link.release()
bcam.stop()
```
