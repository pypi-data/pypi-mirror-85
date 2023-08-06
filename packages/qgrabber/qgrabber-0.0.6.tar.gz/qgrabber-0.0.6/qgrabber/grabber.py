import logging

import numpy as np

from qgrabber.pygrabber.dshow_graph import SampleGrabberCallback

_LOGGER = logging.getLogger(__name__)


class WxGrabber(SampleGrabberCallback):
    def BufferCB(self, this, SampleTime, pBuffer, BufferLen):
        img = np.ctypeslib.as_array(
            pBuffer, shape=(self.image_resolution[1], self.image_resolution[0], 3)
        )
        self.callback(img)
