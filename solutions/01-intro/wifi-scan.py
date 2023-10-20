"""
MicroPython Wi-Fi access point scanner

This MicroPython script scans for nearby Wi-Fi access points
(APs) using an ESP32 microcontroller and displays their SSID,
channel index, and signal strength (RSSI).

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Run the current script
2. Wait for results

Author: Wokwi, Tomas Fryza
Date: 2023-09-21
"""

import network
from machine import Pin

status_led = Pin(2, Pin.OUT)

# Initialize the Wi-Fi interface in station (client) mode
wifi = network.WLAN(network.STA_IF)
# Activate the interface
wifi.active(True)

# Perform the Wi-Fi APs scan
status_led.on()
print("Scanning for Wi-Fi networks...")
available_networks = wifi.scan()
status_led.off()

# Print the list of available Wi-Fi networks
print("SSID              | Channel | Signal Strength (dBm)")
print("------------------+---------+----------------------")
for network in available_networks:
    ssid = network[0].decode("utf-8")
    channel = network[2]
    rssi = network[3]
    print(f"{ssid:17s} | {channel:7d} | {rssi:10d}")
