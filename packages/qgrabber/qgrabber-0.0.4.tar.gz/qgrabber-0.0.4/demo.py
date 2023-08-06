import asyncio
import logging
from typing import List

import wx
from aio_wx_widgets.frame import DefaultFrame
from aio_wx_widgets.widgets import button, text
from pyzbar.pyzbar import Decoded
from wx.core import wxdate2pydate
from wxasync import WxAsyncApp

from qgrabber.controller import Controller
from qgrabber.model import ScannerModel
from qgrabber.view import ScannerView

_LOGGER = logging.getLogger(__name__)


class MainWindow(DefaultFrame):
    def __init__(self):
        super().__init__("Main window")
        model = ScannerModel()
        # model.on_code_scanned.append(self._on_scan)

        view_width = 320
        view_height = 200

        self.controller = Controller(
            model, view_width=view_width, view_height=view_height
        )
        view = ScannerView(self, self.controller, width=view_width, height=view_height)

        self.add(view, layout=wx.ALIGN_CENTER, create=False)

        self.add(button.async_button("start", self._on_start))
        self.add(button.async_button("stop", self._on_stop))
        self.scan_results: text.Text = self.add(text.Text("unknown"))

    def _on_scan(self, result: List[Decoded]):
        first_result = result[0]
        self.scan_results.set_text(str(first_result.data))

    async def _on_start(self, event):
        result = await self.controller.scan_code()
        self.scan_results.set_text(str(result))

    async def _on_stop(self, event):
        self.controller.stop_scan()
        print("stopping")


async def run_app():
    app = WxAsyncApp()
    main_window = MainWindow()
    main_window.Show()
    app.SetTopWindow(main_window)
    await app.MainLoop()


if __name__ == "__main__":
    # os.environ["DEBUGGING"] = "1"
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(run_app())
