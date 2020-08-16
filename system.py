from axp202c import PMU
from machine import RTC
from micropython import const
from network import WLAN, STA_IF
from ntptime import settime
from time import sleep as sleep_delay

from config import WIFI_CONNECTIONS
from exceptions import (
    FailedToConnectToNetworkException,
    FailedCurrentTimeRequestException,
)


# Number of attempts of each saved network to
# connect before attempting a new one
NETWORK_RETRIES = const(5)


def connect_to_network():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)

    for essid, password in WIFI_CONNECTIONS:
        sta_if.connect(essid, password)

        current_try = 0
        while current_try < NETWORK_RETRIES:
            sleep_delay(2)

            if sta_if.isconnected():
                return sta_if

            current_try += 1

    if not sta_if.isconnected():
        raise FailedToConnectToNetworkException(
            'Unable to connect to any available network'
        )


class SystemManager:
    """
    Manager to store and update state of the system.
    """
    def __init__(self):
        self.wifi_connection = None
        self.power_manager = None

    def update_system(self):
        """
        High level task to re-trigger checks to keep system up to date.
        checks wifi connection, establishes system time etc.
        :return: None
        """
        self.reconnect_wifi_connection()
        self.update_system_time()
        self.power_manager = PMU()

    def reconnect_wifi_connection(self):
        """
        Attempt to connect and reconnect a wifi connection on
        nonexistence/connection failure.
        :return: None
        """
        if not self.wifi_connection or not self.wifi_connection.isconnected():
            try:
                self.wlan_connection = connect_to_network()
            except FailedToConnectToNetworkException:
                pass

    @staticmethod
    def update_system_time():
        """
        Pull down the latest NTP backed time and caches it locally.
        :return: None
        """
        try:
            settime()
        except FailedCurrentTimeRequestException:
            pass

    @property
    def system_time(self):
        return RTC().datetime()
