import logging
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from pyzbar.pyzbar import Decoded

    from qgrabber.model import ScannerModel

_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, model: "ScannerModel", view_width, view_height):
        self._model = model
        self._view_width = view_width
        self._view_height = view_height
        self._on_stream_data: Optional[Callable[[bytearray], None]] = None

    def start_scan(self):
        self._model.start(
            self._on_stream_data,
            on_code_scanned=self.code_scanned,
            crop_x=self._view_width,
            crop_y=self._view_height,
        )

    def stop_scan(self):
        self._model.stop()

    async def scan_code(self):
        return await self._model.scan(
            self._on_stream_data, self._view_width, self._view_height
        )

    def subscribe_to_frame_data(self, stream_handler):
        self._on_stream_data = stream_handler

    def code_scanned(self, result: Optional["Decoded"] = None):
        """Called when a qr code has been detected."""
        if result:
            print(result)
