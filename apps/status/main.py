from st7789 import WHITE
import vga1_16x16 as font

from apps.utils import BaseApp
from apps.status.status_types import BatterPercentStatus


class StatusApp(BaseApp):
    STATUS_CLASSES = [
        BatterPercentStatus,
    ]

    def setup(self):
        self.display_header()

    def display_header(self):
        self.lcd_display.st7789_display.hline(40, 20, 200, WHITE)
        self.lcd_display.st7789_display.text(
            font,
            'System Statuses',
            60,
            0,
            WHITE,
        )
