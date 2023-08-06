# QGrabber

Scan QR codes using your webcam, pyzbar and wxpython. No usage of opencv

There are many tuturials available that explain how to scan a barcode with python.
Unfortunately they all make use of opencv for camera access. To me, the downside is the size of opencv.
So I tried to find an alternative. Which was hard.

I finallly settled with:
https://github.com/andreaschiavinato/python_grabber
Currently it is vendored inside this repo until a version will be available on pypi.

## Installation

`pip install qgrabber`

## Usage

See the demo.py file.