from st7789 import BLACK, WHITE
import vga1_8x8 as font

from apps.utils import BaseApp


SECOND_TO_TRIGGER_DISPLAY_UPDATE = 59
SECOND_TO_RESET_DISPLAY_UPDATE = 0


class WatchDisplay(BaseApp):
    has_already_updated = False

    def setup(self):
        self.lcd_display.enable_screen()
        self.display_time()

    def loop(self):
        if self.current_second == SECOND_TO_TRIGGER_DISPLAY_UPDATE:
            if self.has_already_updated:
                return
            else:
                self.display_time()
                self.has_already_updated = True
        elif self.current_second == SECOND_TO_RESET_DISPLAY_UPDATE:
            self.has_already_updated = False
        else:
            return

    @property
    def current_year(self):
        return self.system_manager.system_time[0]

    @property
    def current_month(self):
        return self.system_manager.system_time[1]

    @property
    def current_day(self):
        return self.system_manager.system_time[2]

    @property
    def current_hour(self):
        return self.system_manager.system_time[4]

    @property
    def current_minute(self):
        return self.system_manager.system_time[5]

    @property
    def current_second(self):
        return self.system_manager.system_time[6]

    @property
    def current_ms(self):
        return self.system_manager.system_time[7]

    @property
    def formatted_time(self):
        return str(self.current_hour) + ':' + str(self.current_minute)

    def display_time(self):
        self.lcd_display.st7789_display.text(
            font,
            self.formatted_time,
            104,
            1,
            WHITE
        )
