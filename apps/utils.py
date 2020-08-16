class BaseApp:
    """
    Base class per app that provides the core interface and system interaction
    """

    def __init__(self, system_manager, lcd_display):
        self.system_manager = system_manager
        self.lcd_display = lcd_display

    def loop(self):
        """
        Individual apps main program loop goes here. The individual app just
        needs to be written so as to work repeatedly in a looping cycle, the
        app BaseApp will handle repeated call within the run method
        :return:
        """
        raise NotImplemented(
            'loop method must be defined for main app logic'
        )

    def setup(self):
        """
        Optional work defined before main program loop begins
        """
        pass

    def run(self):
        """
        App entrypoint beings the program loop and boots the application.
        """
        self.setup()

        while True:
            if self.lcd_display.is_display_enabled:
                self.lcd_display.disable_screen()
            else:
                self.lcd_display.enable_screen()

            self.loop()
