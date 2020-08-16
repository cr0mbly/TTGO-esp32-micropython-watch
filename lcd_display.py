from axp202c import AXP202_LDO2, PMU
from libs.focaltouch import FocalTouch
from libs.debounce_irq import DebouncedSwitch, HALF_SECOND_DELAY
from machine import I2C, SPI, Pin
from st7789 import ST7789, BLACK, WHITE

# SPI settings
SPI_INTEFACE = 2
SPI_BAUDRATE = 32000000

# Hardcoded Pins for lcd integration
DISPLAY_SCK_PIN = 18
DISPLAY_MOSI_PIN = 19
DISPLAY_CS_PIN = 5
DISPLAY_DC_PIN = 27
DISPLAY_BACKLIGHT_PIN = 12

# Hardcoded Pins for touch integration
TOUCH_SCL_PIN = 32
TOUCH_SDA_PIN = 23
TOUCH_INTERRUPT_PIN = 38

# LCD configuration
LCD_DIMENSION_X = 240
LCD_DIMENSION_Y = 240
DEFAULT_ROTATION = 2


class LcdDisplay:
    # Component interface objects
    st7789_display = None
    st7789_touch = None

    def __init__(self, system_manager):
        self.system_manager = system_manager
        self.is_display_enabled = False

    def setup(self):
        """
        Handles all of the initialization of the
        LCD screen/power management and touch interface.
        :return: LcdDisplay class
        """
        # initialize display spi port
        spi = SPI(
            SPI_INTEFACE,
            baudrate=SPI_BAUDRATE,
            polarity=1,
            phase=0,
            bits=8,
            firstbit=0,
            sck=Pin(DISPLAY_SCK_PIN, Pin.OUT),
            mosi=Pin(DISPLAY_MOSI_PIN, Pin.OUT),
        )

        # Setup lcd screen
        self.st7789_display = ST7789(
            spi,
            LCD_DIMENSION_X,
            LCD_DIMENSION_Y,
            cs=Pin(DISPLAY_CS_PIN, Pin.OUT),
            dc=Pin(DISPLAY_DC_PIN, Pin.OUT),
            backlight=Pin(DISPLAY_BACKLIGHT_PIN, Pin.OUT),
            rotation=DEFAULT_ROTATION
        )

        # setup touch interface
        touch_i2c = I2C(
            scl=Pin(TOUCH_SCL_PIN),
            sda=Pin(TOUCH_SDA_PIN),
        )
        self.st7789_touch = FocalTouch(touch_i2c)

        # initialize display.
        self.st7789_display.init()
        return self

    def disable_screen(self):
        """Disable screen backlight and set status"""
        if self.is_display_enabled:
            self.system_manager.power_manager.disablePower(AXP202_LDO2)

    def enable_screen(self):
        """Enable screen backlight and set status"""
        if not self.is_display_enabled:
            self.system_manager.power_manager.enablePower(AXP202_LDO2)

    def _touch_callback(self, t):
        self.is_display_enabled = not self.is_display_enabled

    def register_touch_event(self, debounce_ms=HALF_SECOND_DELAY):
        """Set the callback event on a touch event"""
        touch_interrupt = Pin(TOUCH_INTERRUPT_PIN, Pin.IN, Pin.PULL_UP)
        DebouncedSwitch(touch_interrupt, self._touch_callback, delay=debounce_ms)