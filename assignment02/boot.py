import os
import pycom
from machine import UART

uart = UART(0, 115200)
os.dupterm(uart)
pycom.heartbeat(False)
