from setuptools import setup, find_packages

setup(
    name='bcam',
    version='0.0.1',
    description='An easy to use camera interface for NVIDIA Jetson and raspberry pi',
    packages=find_packages(),
    install_requires=['ipywidgets','imutils'
    ],
)
