# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# https://github.com/Mark-MDO47 made choices for Circuit Playground Bluefruit
#   and added delay before the read. Maybe not needed.

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
# switch = digitalio.DigitalInOut(board.D2)

# For Feather M0/M4 Express
# switch = digitalio.DigitalInOut(board.D5)

# For Circuit Playground Express, Circuit Playground Bluefruit
switch = digitalio.DigitalInOut(board.D7)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Delay for 10 milliseconds (0.01 seconds)
time.sleep(0.01)

# If the switch pin is connected to ground CircuitPython can write to the drive
storage.remount("/", readonly=switch.value)