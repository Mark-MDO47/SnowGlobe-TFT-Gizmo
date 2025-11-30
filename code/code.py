# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# https://github.com/Mark-MDO47 2025-11-21
#
# Re-organized to have a "main" function
# Display random background images based on nanosecond time since power-on
#    when there is a "shake"
#    after a set amount of time
#
# Doesn't work as expected:
#
# * Have not gotten CIRCUITPY file system writes to succeed yet...
#       therefore have not implemented the "sequential" image mode
#       I guess that will be version 2
#
# * Tried multiple things to load another image without rebooting,
#   but they all eventually got an error saying out of RAM.
#   Did not try every possible combination of these.
#     - displayio.release_displays()
#     - display.root_group = None
#     - snow_bmp = None
#     - bg_palette = None
#     - bg_bitmap = None
#     - gc.collect()
#

from random import randrange
import board
import busio
import digitalio  # so we can read/write the file system
import supervisor # so we can reboot
import time       # so we can get nanosecond count for "random" number (I don't trust PRN)
import displayio
from adafruit_gizmo import tft_gizmo
import adafruit_imageload
import adafruit_lis3dh

#---| User Config |---------------
BACKGROUND = "/mdo_%02d.bmp"       # specify color or background BMP file template
BACKGROUND_RANGE = [1, 14]         # range of numbered background files
TIME_TILL_NEXT_BG = 300            # time in seconds till load next background
NUM_FLAKES = 50                    # total number of snowflakes
SNOW_COLOR = 0xFFFFFF              # snow color
SHAKE_THRESHOLD = 27               # shake sensitivity, lower=more sensitive
#---| User Config |---------------

# Snowflakes
FLAKES = (
    0, 0, 0, 0,    0, 0, 0, 0,    1, 1, 1, 1,
    0, 0, 0, 0,    1, 1, 1, 0,    1, 1, 1, 1,
    0, 1, 1, 0,    1, 1, 1, 0,    1, 1, 1, 1,
    0, 1, 1, 0,    1, 1, 1, 0,    1, 1, 1, 1,
)
flakes = None
flake_pos = [0.0] * NUM_FLAKES
snow_depth = 0
snow_bmp = None
bg_bitmap = None
bg_palette = None

# For Circuit Playground Express, Circuit Playground Bluefruit - this is the slide slide_switch
slide_switch = digitalio.DigitalInOut(board.D7)
slide_switch.direction = digitalio.Direction.INPUT
slide_switch.pull = digitalio.Pull.UP

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
# load_background(display, fname)
#
# NOTE FIXME TODO: I have not yet fixed the memory leaks so cannot load sequence of images without running out of RAM.
#    see https://github.com/Mark-MDO47/CircuitPlaygroundBLE_expts for a description of what was tried
#
# This routine loads the background image named in fname and assembles the snow globe elements root_goup into display
#
def load_background(display, fname):
    #pylint: disable=global-statement, redefined-outer-name
    global flakes, flake_pos, snow_depth, snow_bmp, bg_bitmap, bg_palette

    # Load background image
    try:
        bg_bitmap, bg_palette = adafruit_imageload.load(fname,
                                                        bitmap=displayio.Bitmap,
                                                        palette=displayio.Palette)
    # Or just use solid color
    except (OSError, TypeError, AttributeError):
        fname = fname if isinstance(fname, int) else 0x000000
        bg_bitmap = displayio.Bitmap(display.width, display.height, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = fname
    background = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)

    # Shared palette for snow bitmaps
    palette = displayio.Palette(2)
    palette[0] = 0xADAF00   # transparent color
    palette[1] = SNOW_COLOR # snow color
    palette.make_transparent(0)

    # Snowflake setup
    flake_sheet = displayio.Bitmap(12, 4, len(palette))
    for i, value in enumerate(FLAKES):
        flake_sheet[i] = value
    flakes = displayio.Group()
    for _ in range(NUM_FLAKES):
        flakes.append(displayio.TileGrid(flake_sheet, pixel_shader=palette,
                                         width = 1,
                                         height = 1,
                                         tile_width = 4,
                                         tile_height = 4 ) )

    # Snowfield setup
    snow_depth = [display.height] * display.width
    snow_bmp = displayio.Bitmap(display.width, display.height, len(palette))
    snow = displayio.TileGrid(snow_bmp, pixel_shader=palette)

    # Add everything to display
    splash = displayio.Group()
    splash.append(background)
    splash.append(flakes)
    splash.append(snow)
    display.root_group = splash

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
# clear_the_snow(display)
#
# This routine clears the accumulated snow from the display
#
def clear_the_snow(display):
    #pylint: disable=global-statement, redefined-outer-name
    global flakes, flake_pos, snow_depth, snow_bmp

    display.auto_refresh = False
    for flake in flakes:
        # set to a random sprite
        flake[0] = randrange(0, 3)
        # set to a random x location
        flake.x = randrange(0, display.width)
    # set random y locations, off screen to start
    flake_pos = [-1.0*randrange(0, display.height) for _ in range(NUM_FLAKES)]
    # reset snow level
    snow_depth = [display.height] * display.width
    # and snow bitmap
    for i in range(display.width * display.height):
        snow_bmp[i] = 0
    display.auto_refresh = True

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
# add_snow(display, index, amount, steepness)
#
# This routine accumulates snow onto the bottom of the display
#
def add_snow(display, index, amount, steepness=2):
    #pylint: disable=global-statement, redefined-outer-name
    global flakes, flake_pos, snow_depth, snow_bmp

    location = []
    # local steepness check
    for x in range(index - amount, index + amount):
        add = False
        if x == 0:
            # check depth to right
            if snow_depth[x+1] - snow_depth[x] < steepness:
                add = True
        elif x == display.width - 1:
            # check depth to left
            if snow_depth[x-1] - snow_depth[x] < steepness:
                add = True
        elif 0 < x < display.width - 1:
            # check depth to left AND right
            if snow_depth[x-1] - snow_depth[x] < steepness and \
               snow_depth[x+1] - snow_depth[x] < steepness:
                add = True
        if add:
            location.append(x)
    # add where snow is not too steep
    for x in location:
        new_level = snow_depth[x] - 1
        if new_level >= 0:
            snow_depth[x] = new_level
            snow_bmp[x, new_level] = 1

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
# get_background_index(sequential)
#
# Gets count to use this time and (possibly) stores count for next time
# Two modes - sequential or random
#
# Circuit Playground Bluefruit has FLASH that is set up as a file system, so we use that if it is available.
#    We can also use the last bits of the nanosecond time count as a random choice.
#
# NOTE FIXME TODO: as of now I have not been able to make writes to the file system work.
#
# The slide_switch determines if we can write to file system, because of our boot.py.
#   If slide_switch == False, we cannot save state to file system.
#   see https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-storage for a description of this scheme & boot.py
#
# Most of the time sequential is False and we use the random number.
# If sequential is True, we can only truly implement that when file system access is allowed.
#
# Behavior if slide_switch == True
#    if sequential == True
#       read index file.
#         If previous mode was random (sequential == False), set current index to start
#         else set current index to next sequential index, including wraparound
#    else
#         set current index to randomized index
#    write file with index and current mode
#    return calculated current index
# Behavior if slide_switch == False
#    set current index to randomized index
#    return calculated current index
# 
BACKGROUND_INDEX_FNAME = "background_index.txt"
def get_background_index(sequential=False):
    global slide_switch

    file_system_access = str(slide_switch.value)
    nanosec_rand = 1 + (time.monotonic_ns() % (BACKGROUND_RANGE[1]-BACKGROUND_RANGE[0]))
    print("DEBUG Slide Switch reads %s rand = %d" % (file_system_access, nanosec_rand))

    current_index = nanosec_rand # default and in case of error
    file_system_error = False
    if "True" == file_system_access:
        try:
            with open(BACKGROUND_INDEX_FNAME, "r") as f:
                line = f.read()
                a_split = line.split(",")
                current_index = int(a_split[0])
                file_mode = a_split[1].lower()
                # print("DEBUG read success! |%s| %d %s" % (line, current_index, file_mode))
        except OSError:
            # print("DEBUG open/read OSError")
            file_system_error = True
        except:
            # print("DEBUG open/read unknown error")
            file_system_error = True

    if True == sequential:
        current_index = current_index + 1
        if current_index > BACKGROUND_RANGE[1]:
            current_index = BACKGROUND_RANGE[0]

    # print("DEBUG before last if fs_access=%s fs_error=%s" % (file_system_access, str(file_system_error)))
    if ("True" == file_system_access) and (False == file_system_error):
        mode = "r" # random mode is default
        if True == sequential:
            mode = "s" # sequential mode
        try:
            with open(BACKGROUND_INDEX_FNAME, "w") as f:
                f.write("%s,%s", (str(current_index), mode))
            # print("DEBUG wrote %s,%s", (str(current_index), mode))
        except:
            # print("DEBUG write failed, file_system_error = %s" % str(file_system_error))
            pass

    return current_index

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
# main()
#
# This routine is the "main" for the snow globe program
#
# It sets up the accelerometer and display, then calls load_background() with a "randomly" chosen image
# It loops
#    It adds snowflakes at the top and then accumulates them onto the bottom of the background image
#    If it sees a shake or a touch on pin A1 or it times out for this image, it reboots
#
def main():
    #pylint: disable=global-statement, redefined-outer-name
    global flakes, flake_pos, snow_depth, snow_bmp

    # Accelerometer setup
    accelo_i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    accelo = adafruit_lis3dh.LIS3DH_I2C(accelo_i2c, address=0x19)

    # Create the TFT Gizmo display
    display = tft_gizmo.TFT_Gizmo()

    # The background filename changes every time we reboot.
    load_background(display, BACKGROUND % get_background_index())

    start_time = time.monotonic() # time in seconds
    while True:
        clear_the_snow(display)
        # loop until globe is full of snow
        while snow_depth.count(0) < (display.width)/3:
            # check for shake
            if accelo.shake(SHAKE_THRESHOLD, 5, 0) or ((time.monotonic() - start_time) > TIME_TILL_NEXT_BG):
                # Did not find mem leak; just reboot
                supervisor.reload()
                break # not really but...
            # update snowflakes
            for i, flake in enumerate(flakes):
                # speed based on sprite index
                flake_pos[i] += 1 - flake[0] / 3
                # check if snowflake has hit the ground
                if int(flake_pos[i]) >= snow_depth[flake.x]:
                    # add snow where it fell
                    add_snow(display, flake.x, flake[0] + 2)
                    # reset flake to top
                    flake_pos[i] = 0
                    # at a new x location
                    flake.x = randrange(0, display.width)
                flake.y = int(flake_pos[i])
            display.refresh()

if __name__ == "__main__":
    main()
