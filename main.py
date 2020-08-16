from apps.watch import WatchDisplay
from lcd_display import LcdDisplay
from system import SystemManager

# Setup internal system
system_manager = SystemManager()
system_manager.update_system()

# Setup LCD and eventsB
lcd_display = LcdDisplay(system_manager).setup()
lcd_display.register_touch_event()

# Display initial app
WatchDisplay(system_manager, lcd_display).run()
