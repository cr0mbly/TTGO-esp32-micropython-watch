from micropython import const
import network
import time

from config import WIFI_CONNECTIONS
from exceptions import FailedToConnectToNetworkException

# Number of attempts of each saved network to
# connect before attempting a new one
NETWORK_RETRIES = const(5)


def connect_to_network():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    for essid, password in WIFI_CONNECTIONS:
        sta_if.connect(essid, password)

        current_try = 0
        while current_try < NETWORK_RETRIES:
            time.sleep(2)

            if sta_if.isconnected():
                return sta_if

            current_try += 1

    if not sta_if.isconnected():
        raise FailedToConnectToNetworkException(const('Unable to connect to any available network'))
