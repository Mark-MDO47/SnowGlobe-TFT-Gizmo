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
# To make a Christmas ornament, modified again
#    removed touch controls


import displayio
from adafruit_qualia.graphics import Displays, Graphics
import io
import os

G_WHICH_IMAGE = 0 # index of which bin file to use next

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
# rd_dotbin_file(fname, numPxls, img_565)
#
# THIS IS FOR BIG-ENDIAN BINARY FILE
#
# fname   - path to *.bin file created by mdo_tablegen.py
#              arranged width-first then height
#              RGB 565 in big-endian format, two bytes per pixel
# numPxls - total number of pixels expected in *.bin file
# img_565 - buffer for RGB 565 pixels, arranged per .bin file which is width-first
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
def main():
    # For other displays:
    # 2.1" Round = Displays.ROUND21
    # 3.4" Square = Displays.SQUARE34
    # 320 x 820 Bar - Displays.BAR320X820
    graphics = Graphics(Displays.ROUND21, default_bg=None, auto_refresh=False)

    # prepare to read image map
    numPxls = graphics.display.width * graphics.display.height # 480 * 480 - make sure we have room

    # create buffer and don't let it go - don't want memory fragmentation
    img_565 = [0]*numPxls # make sure we have room

    pix_files = os.listdir("pix")
    list_of_bin = []
    for a_fn in pix_files:
       if (len(a_fn) > 4) and ((a_fn.rfind(".bin") + len(".bin")) == len(a_fn)):
           list_of_bin.append("pix" + os.sep + a_fn)

    bitmap = displayio.Bitmap(graphics.display.width, graphics.display.height, 65535)

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(
        bitmap,
        pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565)
    )

    # Add the TileGrid to the Group
    graphics.root_group.append(tile_grid)

    # Add the Group to the Display
    graphics.display.root_group = graphics.root_group

    current_color = displayio.ColorConverter().convert(0xFFFFFF)

    # cycle through images
    load_bitmap(bitmap, list_of_bin, 0, graphics.display.width, graphics.display.height, img_565)


    graphics.display.auto_refresh = True
    print("here I am")

    while True:
        pass


if __name__ == "__main__":
    main()
