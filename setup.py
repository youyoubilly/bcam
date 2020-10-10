from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bcam',
    version='0.0.7',
    author='Kevin Peng, Billy Wang',
    description='An easy to use camera interface for NVIDIA Jetson and raspberry pi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['ipywidgets','imutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
