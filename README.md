# bcam
bcam is an easy to use Python camera interface for NVIDIA Jetson.

This is forked form [jetcam](https://github.com/NVIDIA-AI-IOT/jetcam), intended to be used by BillioTech Team. 

Of course, You can clone and use it as well, if you find it convenient.

Quick guide is [here](notebook/single_usb_cam.ipynb)

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
import cv2


bcam = BCamera.builder() \
        .device(0) \
        .resolution(800, 600) \
        .fps(5) \
        .build()

bcam.start()

widget = widgets.Image(format='jpeg', width=400, height=400)

display(widget)

bcam.link(widget)
```

### Stop
```python
bcam.stop()
```
