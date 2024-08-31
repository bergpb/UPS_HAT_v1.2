import smbus2
import struct
import time
from datetime import datetime as dt


def read_voltage(bus):
    address = 0x36
    read = bus.read_word_data(address, 0X02)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 / 1000 / 16
    return voltage


def read_capacity(bus):
    address = 0x36
    read = bus.read_word_data(address, 0X04)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256
    return capacity


def quick_start(bus):
    address = 0x36
    bus.write_word_data(address, 0x06, 0x4000)


def power_on_reset(bus):
    address = 0x36
    bus.write_word_data(address, 0xfe, 0x0054)


bus = smbus2.SMBus(1)
power_on_reset(bus)
quick_start(bus)
previous_voltage = read_voltage(bus)

current_voltage = read_voltage(bus)
capacity = read_capacity(bus)

while capacity == 0 or current_voltage == 0:
    current_voltage = read_voltage(bus)
    capacity = read_capacity(bus)
 
datetime = dt.now().strftime('%Y-%m-%d %H:%M:%S')
print("++++++++++++++++++++")
print("Battery:%4i%% %5.2fV" % (read_capacity(bus), current_voltage))
if current_voltage > previous_voltage:
    print("     Charging")
elif current_voltage < previous_voltage:
    print("    Discharging")
previous_voltage = current_voltage
if capacity >= 100:
    print("----Battery FULL----")
elif capacity <= 15 and capacity > 5:
    print("----Battery LOW-----")
elif capacity <= 5:
    print("  D A N G E R !!!")
    print("BATTERY RUNNING OUT")
print(f"Datetime: {datetime}")
