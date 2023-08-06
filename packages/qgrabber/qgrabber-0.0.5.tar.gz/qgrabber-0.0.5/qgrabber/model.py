import logging
from asyncio.locks import Event
from typing import List, Optional

from pyzbar.pyzbar import Decoded, decode

from qgrabber.grabber import WxGrabber
from qgrabber.pygrabber.dshow_graph import FilterGraph, FilterType
from qgrabber.pygrabber.dshow_ids import MediaSubtypes, MediaTypes

_LOGGER = logging.getLogger(__name__)


def cropper(frame, width, height):
    if width is None:
        return frame
    y, x = frame.shape[:2]
    startx = x // 2 - width // 2
    starty = y // 2 - height // 2
    return frame[starty : starty + height, startx : startx + width].copy(order="C")


class ScannerModel:
    """Scanner model managing the webcam.

    Use the start function to start scanning with callbacks carrying results.
    Use the async scan function to start scanning a wait for a scanned result.
    """

    def __init__(self):
        self._graph = None
        self._crop_x = None
        self._crop_y = None
        self._camera_callback = None
        self.on_code_scanned = []
        self._evt = Event()

    async def scan(self, camera_call_back, crop_x=None, crop_y=None) -> Optional[str]:
        self._evt = Event()
        _result = None

        def _on_code_scanned(result):
            nonlocal _result
            _result = result
            self._evt.set()

        self.start(camera_call_back, _on_code_scanned, crop_x, crop_y)

        await self._evt.wait()
        self.stop()
        return _result

    def start(self, camera_callback, on_code_scanned, crop_x=None, crop_y=None):
        """Start the scanner.

        Args:
            camera_callback: Callable whenever image data from the camera is received.
                Use this call to populate your view with the image data.
            on_code_scanned: Called when a code is detected.
            crop_x: image data crop_x
            crop_y: image data crop_y

        Returns:

        """
        self._camera_callback = camera_callback
        self._crop_x = crop_x
        self._crop_y = crop_y
        self.on_code_scanned.append(on_code_scanned)

        self._graph = FilterGraph()
        self._graph.add_video_input_device(0)
        filter_type = FilterType.sample_grabber

        _filter = self._graph.filter_factory.build_filter(filter_type, None)
        self._graph.filters[filter_type] = _filter
        self._graph.filter_graph.AddFilter(_filter.instance, _filter.Name)

        sample_grabber = self._graph.filters[FilterType.sample_grabber]
        sample_grabber_cb = WxGrabber(self.call_back)

        sample_grabber.set_callback(sample_grabber_cb, 1)
        sample_grabber.set_media_type(MediaTypes.Video, MediaSubtypes.RGB24)

        self._graph.add_null_render()
        self._graph.prepare_preview_graph()
        self._graph.run()

    def stop(self):
        """Stop the webcam."""

        if self._graph:
            self._graph.stop()
            self._graph=None
        self._evt.set()

    def decode(self, frame):
        codes = decode(frame)
        if codes:
            _LOGGER.debug(codes)
            for scanned_callback in self.on_code_scanned:
                scanned_callback(codes)

    def call_back(self, frame):
        """Process incoming frame data."""
        _LOGGER.debug("Calling back")
        frame = cropper(frame, self._crop_x, self._crop_y)
        self.decode(frame)
        self._camera_callback(frame)
