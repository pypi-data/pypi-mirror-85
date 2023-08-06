import asyncio
import logging
from asyncio import CancelledError
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
        self._scan_task=None

    def start_scan_task(self):
        loop= asyncio.get_running_loop()
        self._scan_task = loop.create_task(self.scan_code())
        self._scan_task.add_done_callback(self._scan_callback)

    def _scan_callback(self,future:asyncio.Future):
        future.result()

    def cancel_scan_task(self):
        if self._scan_task:
            self._scan_task.cancel()

    def stop_scan(self):
        self._model.stop()

    async def scan_code(self):
        try:
            return await self._model.scan(
                self._on_stream_data, self._view_width, self._view_height
            )
        except Exception:
            # _LOGGER.exception(err)
            self.stop_scan()
            raise

    def subscribe_to_frame_data(self, stream_handler):
        self._on_stream_data = stream_handler

    def code_scanned(self, result: Optional["Decoded"] = None):
        """Called when a qr code has been detected."""
        if result:
            print(result)

