import asyncio
import logging
from typing import List

from aio_wx_widgets.core.data_types import HorAlign
from aio_wx_widgets.frame import DefaultFrame
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets import text, AioButton, Text
from pyzbar.pyzbar import Decoded
from wxasync import WxAsyncApp

from qgrabber.controller import Controller
from qgrabber.model import ScannerModel
from qgrabber.view import ScannerView

_LOGGER = logging.getLogger(__name__)


class View(SimplePanel["Controller"]):
    def __init__(self, parent, controller: "Controller", view_width, view_height):
        super().__init__(parent, controller)

        view = ScannerView(
            self.ui_item, self.controller, width=view_width, height=view_height
        )

        self.add(view, create=False, hor_align=HorAlign.center)

        self.add(AioButton("start", self._on_start))
        self.add(AioButton("stop", self._on_stop))
        self.add(AioButton("start asyncio scanning task", self._on_start_scan_task))
        self.add(AioButton("cancel scan task", self._on_cancel_scan_task))
        self.scan_results: text.Text = self.add(Text("unknown"))

    def _on_scan(self, result: List[Decoded]):
        first_result = result[0]
        self.scan_results.set_text(str(first_result.data))

    async def _on_start(self, event):
        result = await self.controller.scan_code()
        self.scan_results.set_text(str(result))

    async def _on_start_scan_task(self, event):
        self.controller.start_scan_task()

    async def _on_cancel_scan_task(self, event):
        self.controller.cancel_scan_task()

    async def _on_stop(self, event):
        self.controller.stop_scan()
        print("stopping")


class MainWindow(DefaultFrame):
    view_width = 320
    view_height = 200

    def __init__(self):
        super().__init__("Main window")
        model = ScannerModel()
        controller = Controller(
            model, view_width=self.view_width, view_height=self.view_height
        )
        view = View(self, controller, self.view_width, self.view_height)
        view.populate()


#
#
#
# class MainWindow(DefaultFrame):
#     def __init__(self):
#         super().__init__("Main window")
#         model = ScannerModel()
#         # model.on_code_scanned.append(self._on_scan)
#
#         view_width = 320
#         view_height = 200
#
#         self.controller = Controller(
#             model, view_width=view_width, view_height=view_height
#         )
#


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
