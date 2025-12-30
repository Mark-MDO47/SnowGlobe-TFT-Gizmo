# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple painting demo that works with on any touch display
"""

# https://github.com/Mark-MDO47 2025-12-20
# https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/GO_BIG.md
#
# Re-organized to be a  snow-globe ornament
#    used to be qualia_paint.py https://docs.circuitpython.org/projects/qualia/en/latest/examples.html
#    modified by me https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/README.md#mdo_qualia_paint
#       now uses binary file for image load, can load one image after another
#
# This code now includes concepts and some code from the Circuit Playground TFT Gizmo Snow Globe by Carter Nelson
#       https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe/
#
# To make a Christmas ornament, modified again
#    removed touch controls
#    save img_565 (type list) in scope at all times so it doesn't fragment memory, also it is background image
#


from random import randrange
import displayio
from adafruit_qualia.graphics import Displays, Graphics
import io
import os
import time

GC_TIME_TILL_NEXT_BG = 30            # time in seconds till load next background
GC_SNOW_COLOR = 0xFFFF                # snow color
GC_NUM_FLAKES = 70                    # total number of snowflakes
GC_MAX_SIZE_FLAKE = 6                 # max size of square for pixels
GC_MIN_SIZE_FLAKE = 3                 # max size of square for pixels

G_GRAPHICS = None

# get these structures defined so always in scope to avoid memory fragmentation
G_FLAKE_REGIONS = [[0 for _ in range(4)] for _ in range(GC_NUM_FLAKES)] # region of this flake

G_WHICH_IMAGE = 0 # index of which .bin file to use as next background

############################################################
# within_region(x,y, region)
#
# INPUTS:
#    x, y   - coordinates to check
#    region - indexes to bitmap: (x_bgn, x_end, y_bgn, y_end)
#
# returns True or False, True if coordinates within region
#
def within_region(x,y, region):
    x_bgn, x_end, y_bgn, y_end = region
    my_rtn = True
    if (x < x_bgn) or (x >= x_end):
        my_rtn = False
    if (y < y_bgn) or (y >= y_end):
        my_rtn = False
    return my_rtn
    # end within_region()

############################################################
# color_region(bitmap, color, region)
#
# INPUTS:
#    bitmap - RGB 565 that refreshes into the screen; width-first then height
#    color  - RGB 565 color to use
#    region - indexes to bitmap: (x_bgn, x_end, y_bgn, y_end)
#
def color_region(bitmap, color, region):
    x_bgn, x_end, y_bgn, y_end = region
    for i in range(x_bgn, x_end):
        for j in range(y_bgn, y_end):
            bitmap[i, j] = color
    # end color_region()

############################################################
# restore_region(bitmap, img_565, region, wd, ht)
#
# INPUTS:
#    bitmap - RGB 565 that refreshes into the screen; width-first then height
#    region - indexes to bitmap: (x_bgn, x_end, y_bgn, y_end)
#    wd, ht         - total width and height of the screen bitmap area
#    img_565 - buffer for RGB 565 pixels, arranged per .bin file which is width-first
#
def restore_region(bitmap, img_565, region, wd, ht):
    x_bgn, x_end, y_bgn, y_end = region
    for i in range(x_bgn, x_end):
        for j in range(y_bgn, y_end):
            bitmap[i, j] = img_565[i + j*wd]
    # end restore_region()

############################################################
# start_snow(bitmap, wd, ht)
#    puts initial set of snowflakes onto background
#
# INPUTS:
#    bitmap - RGB 565 that refreshes into the screen; width-first then height
#    wd, ht         - total width and height of the screen bitmap area
#
# GLOBAL CONSTANTS:
#    GC_MAX_SIZE_FLAKE - maximum size of flake in pixels
#    GC_MIN_SIZE_FLAKE - minimum size of flake in pixels
#    GC_NUM_FLAKES     - total number of snowflakes
#    GC_SNOW_COLOR     - snow color
#
# GLOBAL STRUCTURES:
#    G_FLAKE_REGIONS   - x,y position of this flake
#
def create_flake_region(bitmap, wd, ht):
    x_bgn = randrange(0,wd)
    y_bgn = randrange(0,ht)
    size = randrange(GC_MIN_SIZE_FLAKE, GC_MAX_SIZE_FLAKE+1)
    x_end = min(x_bgn+size,wd-1)
    y_end = min(y_bgn+size,ht-1)
    return [x_bgn, x_end, y_bgn, y_end]
    # end create_flake_region()

############################################################
# start_snow(bitmap, wd, ht)
#    puts initial set of snowflakes onto background
#
# INPUTS:
#    bitmap - RGB 565 that refreshes into the screen; width-first then height
#    wd, ht         - total width and height of the screen bitmap area
#
# GLOBAL CONSTANTS:
#    GC_MAX_SIZE_FLAKE - maximum size of flake in pixels
#    GC_MIN_SIZE_FLAKE - minimum size of flake in pixels
#    GC_NUM_FLAKES     - total number of snowflakes
#    GC_SNOW_COLOR     - snow color
#
# GLOBAL STRUCTURES:
#    G_FLAKE_REGIONS   - x,y position of this flake
#
def start_snow(bitmap, wd, ht):
    global G_FLAKE_REGIONS

    for flake_idx in range(GC_NUM_FLAKES):
        G_FLAKE_REGIONS[flake_idx] = create_flake_region(bitmap, wd, ht)
        color_region(bitmap, GC_SNOW_COLOR, G_FLAKE_REGIONS[flake_idx])
    # end start_snow()

############################################################
# move_snow(bitmap, wd, ht, img_565)
#    lets snow fall down a bit
#
# INPUTS:
#    bitmap  - RGB 565 that refreshes into the screen; width-first then height
#    wd, ht  - total width and height of the screen bitmap area
#    img_565 - buffer for RGB 565 pixels, arranged per .bin file which is width-first
#
# GLOBAL CONSTANTS:
#    GC_NUM_FLAKES     - total number of snowflakes
#    GC_SNOW_COLOR     - snow color
#    GC_MIN_SIZE_FLAKE - minimum size of flake in pixels
#
# GLOBAL STRUCTURES:
#    G_FLAKE_REGIONS   - x,y position of this flake
#
def move_snow(bitmap, wd, ht, img_565):
    global G_FLAKE_REGIONS

    for flake_idx in range(GC_NUM_FLAKES):
        restore_region(bitmap, img_565, G_FLAKE_REGIONS[flake_idx], wd, ht)
        x_bgn, x_end, y_bgn, y_end = G_FLAKE_REGIONS[flake_idx]
        down = max(((y_end - y_bgn) * 2) // GC_MIN_SIZE_FLAKE, GC_MIN_SIZE_FLAKE)
        y_bgn_moved = y_bgn + down
        y_end_moved = min(y_end+down, ht-1)
        if ((y_bgn_moved+1) >= y_end_moved):
            x_bgn, x_end, y_bgn, y_end = create_flake_region(bitmap, wd, ht)
            y_bgn_moved = y_bgn // 8 # put them up near the top
            y_end_moved = min(y_bgn_moved-y_bgn+y_end, ht-1)
            G_FLAKE_REGIONS[flake_idx] = [x_bgn, x_end, y_bgn_moved, y_end_moved]
        else:
            G_FLAKE_REGIONS[flake_idx] = [x_bgn, x_end, y_bgn_moved, y_end_moved]
        color_region(bitmap, GC_SNOW_COLOR, G_FLAKE_REGIONS[flake_idx])
    # end move_snow()

############################################################
# rd_dotbin_file(fname, numPxls, img_565)
#
# THIS IS FOR BIG-ENDIAN BINARY FILE
#    see https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/README.md#mdo_qualia_paint
#        for mdo_tablegen.py which can produce these files
#    The original Adafruit tablegen.py (basis for mdo_tablegen.py) can be found here:
#        https://github.com/adafruit/Uncanny_Eyes commit d2103e84aa33da9f6924885ebc06d880af8deeff
#
# INPUTS:
#    fname   - path to *.bin file created by mdo_tablegen.py
#              arranged width-first then height
#              RGB 565 in big-endian format, two bytes per pixel
#    numPxls - total number of pixels expected in *.bin file
#    img_565 - buffer for RGB 565 pixels, arranged per .bin file which is width-first
#
def rd_dotbin_file(fname, numPxls, img_565):
    fptr = io.open(fname,'rb')
    ba = bytearray(fptr.read())
    fptr.close()
    foundPxls = int(len(ba) / 2) # two bytes per pixel 16 bits
    oddBytes = len(ba) % 2       # must be an even number of pixels
    if (foundPxls != numPxls) or (0 != oddBytes):
        raise RuntimeError("pxl found=%d expected %d oddBytes %d." % (foundPxls,numPxls,oddBytes))
    # convert bytes (big-endian) into 16 bit RGB 565 (aka 666)
    for i, j in enumerate(range(0,foundPxls*2,2)):
        img_565[i] = int(ba[j]<<8) | int(ba[j+1])
    del ba
    # end rd_dotbin_file()

############################################################
# load_bitmap(bitmap, list_of_bin, skipleft_width, wd, ht, img_565)
#
# INPUTS:
#    bitmap         - RGB 565 that refreshes into the screen; width-first then height
#    list_of_bin    - list of paths to *.bin files to display
#    skipleft_width - width of the color palette on the left, in pixels
#    wd, ht         - total width and height of the screen bitmap area
#    img_565        - type=list; buffer for the matched set of pixels, arranged width-first
#
# INFO:
#    left half of screen is first skipleft_width pixels
#    right have of screen is from coordinate (wd-skipleft_width) to wd
#    total screen is wd width by ht height pixels
#
# GLOBAL:
#    G_WHICH_IMAGE contains index within list_of_bin to use for display
#
def load_bitmap(bitmap, list_of_bin, skipleft_width, wd, ht, img_565):
    global G_WHICH_IMAGE
    # get img_565 and prepare G_WHICH_IMAGE for next call
    rd_dotbin_file(list_of_bin[G_WHICH_IMAGE], (wd-skipleft_width)*ht, img_565)
    G_WHICH_IMAGE += 1
    if G_WHICH_IMAGE >= len(list_of_bin):
        G_WHICH_IMAGE = 0
    # copy img_565 into left half of bitmap
    for i in range(skipleft_width,wd):
        for j in range(ht):
            """
            # debug checking code
            if (i < skipleft_width) or (i > wd):
                raise RuntimeError("i(%d) out of range." % i)
            if (j < 0) or (j > ht):
                raise RuntimeError("j(%d) out of range." % j)
            if ((i - skipleft_width + j*(wd-skipleft_width)) < 0) or ((i - skipleft_width + j*(wd-skipleft_width)) >= numPxls):
                raise RuntimeError("i(%d) j(%d) calc(%d) out of range." % (i, j, i + j*(wd-skipleft_width)))
            """
            bitmap[i, j] = img_565[i - skipleft_width + j*(wd-skipleft_width)]
    # end load_bitmap()

############################################################
# Main Program
#
# GLOBAL STRUCTURES:
#    G_GRAPHICS        - Graphics display structure
#
def main():
    # For other displays:
    # 2.1" Round = Displays.ROUND21
    # 3.4" Square = Displays.SQUARE34
    # 320 x 820 Bar - Displays.BAR320X820
    G_GRAPHICS = Graphics(Displays.ROUND21, default_bg=None, auto_refresh=False)

    # prepare to read image map - get number of pixels for our display
    numPxls = G_GRAPHICS.display.width * G_GRAPHICS.display.height # 480 * 480 - make sure we have room

    # create pixel buffer for TFT 16-bit values and don't let it go - we don't want memory fragmentation
    # this buffer is just a Python list
    img_565 = [0]*numPxls # make sure we have room

    # do a directory of /pix and make list of *.bin files
    pix_files = os.listdir("pix")
    list_of_bin = []
    for a_fn in pix_files:
       if (len(a_fn) > 4) and ((a_fn.rfind(".bin") + len(".bin")) == len(a_fn)):
           list_of_bin.append("pix" + os.sep + a_fn)
    list_of_bin = sorted(list_of_bin)

    # create the bitmap for the display
    bitmap = displayio.Bitmap(G_GRAPHICS.display.width, G_GRAPHICS.display.height, 65535)

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(
        bitmap,
        pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565)
    )

    # Add the TileGrid to the Group
    G_GRAPHICS.root_group.append(tile_grid)

    # Add the Group to the Display
    G_GRAPHICS.display.root_group = G_GRAPHICS.root_group

    # load the first background image
    load_bitmap(bitmap, list_of_bin, 0, G_GRAPHICS.display.width, G_GRAPHICS.display.height, img_565)
    start_snow(bitmap, G_GRAPHICS.display.width, G_GRAPHICS.display.height)

    # for now we will just let it auto-refresh and see if that is a problem
    G_GRAPHICS.display.auto_refresh = True

    start_time = time.time() # time in seconds since 1970 as an int
    #  ESP32 boards should support arbitrarily large integers in CircuitPython
    while True:
        if (time.time() - start_time) > GC_TIME_TILL_NEXT_BG:
            # cycle through images
            load_bitmap(bitmap, list_of_bin, 0, G_GRAPHICS.display.width, G_GRAPHICS.display.height, img_565)
            G_GRAPHICS.display.auto_refresh = False
            start_snow(bitmap, G_GRAPHICS.display.width, G_GRAPHICS.display.height)
            G_GRAPHICS.display.auto_refresh = True
            start_time = time.time() # time in seconds
        else:
            G_GRAPHICS.display.auto_refresh = False
            move_snow(bitmap, G_GRAPHICS.display.width, G_GRAPHICS.display.height, img_565)
            G_GRAPHICS.display.auto_refresh = True
        G_GRAPHICS.display.refresh()

if __name__ == "__main__":
    main()
