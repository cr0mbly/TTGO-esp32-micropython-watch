# TTGO-esp32-micropython-watch
Playground ESP32 based micropython watch based utilising the TTGO 2020 watches
hardware



# Setup

To setup the install for the environment you'll need to first install the
micropython firmware included in this repo to the board. There's a good doc
[here](https://tasmota.github.io/docs/Esptool/) which oultlines how to install
the ESP32 flashing tool we'll use during development. Once it's installed we can
flash the firmware and get the environment running.

Firstly we'll wipe the inital flash envrionment to clear anything that might be
on the watch

NOTE these docs assume a linux environment if your developing on mac/windows
there's other readme's  out there you can follow.

```Bash
sudo esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

This should take about 30 seconds and dump return a sucess status on completion.
Next we need to flash the base firmware, you can do this by running

```Bash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 ~/<relative-directory>/TTGO-micropython-watch/firmware/TTGO_watch_2020_esp32.bin

```

This takes about 2 minutes and on completion have the full micropython environment
installed and ready to connect too.

We can test this by connecting to the REPL by going


```Bash
picocom /dev/ttyUSB0 -b115200
```

Depending on how your permissions are setup you may need to change the
permission setting to make it readable

```Bash
sudo chmod 777 /dev/ttyUSB0
```

here you should be greeted with the terminal.

If you want to do a simple hello world of the hardware you can run

```
from time import sleep
from machine import Pin

vibrator = Pin(4, Pin.OUT)
vibrator.on()
sleep(1)
vibrator.off()
```

Which will cycle the vibrator motor on the watch on or off.


# Flashing the app

To flash the development code I personally use [IDEA's pycharm micropython plugin](https://plugins.jetbrains.com/plugin/9777-micropython),
as it takes care of ignoring the non project python files and allows you to
whitelist/blacklist files/folders that are included for upload on the watch.

If your wanting to stick to the command line approach I'd suggest using ampy to
do it which would have been installed during the esptool.py setup, there's a
good overview of commands [here](https://pythonforundergradengineers.com/upload-py-files-to-esp8266-running-micropython.html)


### Project structure


 - `main.py` Entrypoint for script, sets up drivers and any pre app code
    that needs to be initialized
 - `system.py` Contains shared app state settings class, and connectors
    for network
 - `config.py` Ommited from the app contains private settings variables we want
    included in the app but don't want uploaded to git
 - `apps` Contains the watch apps, also contains a shared base class new apps
    can be based off of.
 - `firmware` packaged Micropython firmware from RussHuges containing a few
    prebuild libraries we want to use.
 - `libs` vendor code or snippets taken from other libraries


### Config with config.py

TODO this will be changed but serves it's purpose for now. On build we'll need
to add a config.py file containing our private wifi key plus any other configuration.

At the moment this project only expects a single variable

```Python
WIFI_CONNECTIONS = [('WIFI-AP-name', 'password')]
```

You can add multiple AP configs to this and the app will try to connect to one
of them on first boot, this will be changed in the future.

### Thanks

 - https://github.com/russhughes/st7789_mpy (For his excellent bundling of the micropython firmware and extension of the st7789 display library)
