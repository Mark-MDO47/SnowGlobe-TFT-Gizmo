#!/usr/bin/env python3
"""
CircleCapture.py - capture a square portion of an image, displaying the
   inscribed circle, and resize to 480x480 *.png for use on SnowGlobe
"""

# https://github.com/Mark-MDO47 and ChatGPT using GPT 5.5 2026-06-16
# https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/GO_BIG.md
# Inputs: JPG / PNG / BMP / HEIC / HEIF
# Outputs: 480x480 file in same directory as input named <original>_circle.png
#          *.txt with metadata named <original>_circle.txt
# Preview automatically scaled to fit screen
#     Full-resolution coordinate system
#
# | Control          | Function                |
# | ---------------- | ----------------------- |
# | Mouse drag       | Move circle             |
# | Mouse wheel      | Radius ±5 px            |
# | Arrow            | Move 100 px             |
# | Shift+Arrow      | Move 10 px              |
# | Ctrl+Shift+Arrow | Move 1 px               |
# | +                | Radius +1 px            |
# | Shift++          | Radius +10 px           |
# | -                | Radius -1 px            |
# | Shift+-          | Radius -10 px           |
# | M or m           | Center circle of max size |
# | Ctrl+S           | Save PNG + metadata TXT |

# LIBRARIES USED
# --------------
# tkinter
    # Standard Python GUI library.
    # Used for:
        # • window creation
        # • keyboard handling
        # • mouse handling
        # • drawing graphics overlays

# Pillow (PIL)
    # Python Imaging Library fork.
    # Used for:
        # • loading image files
        # • resizing images
        # • cropping images
        # • converting images for Tkinter display

# pillow-heif
    # Adds HEIC/HEIF support to Pillow.
    # Used so Apple iPhone images can be loaded directly.

# os
    # Used for file name manipulation.

# sys
    # Used for command-line argument handling.

# COORDINATE SYSTEM
# -----------------
# All coordinates are maintained in the ORIGINAL image coordinate space.
# A scaled preview image is displayed to fit the user's screen.
# Example:
    # Original image:
        # 8000 x 6000
    # Display preview:
        # 1600 x 1200
# The circle position and radius are stored in original-image pixels.
# This allows:
    # • accurate coordinates
    # • full-resolution crops
    # • responsive display

# The preview simply converts original coordinates using:
    # display_coordinate = original_coordinate * scale
# and mouse positions are converted back using:
    # original_coordinate = display_coordinate / scale

import os
import sys
import tkinter as tk

from PIL import Image, ImageTk
from pillow_heif import register_heif_opener

register_heif_opener()

# 
# ============================================================================ 
# USER CONFIGURATION 
# ============================================================================ 
# 
# All programmer-adjustable settings are collected here. 
# 
# Much future customization should require changing only these values. 
#
# ============================================================================
#
# Output PNG dimensions.
#
# The selected square is resampled to this size before saving.
#
OUTPUT_SIZE = 480

#
# Initial circle size.
#
# Radius is initialized to:
#
#     min(image_width, image_height) / INITIAL_RADIUS_DIVISOR
#
MAX_RADIUS_DIVISOR = 2     # gives maximum size circle to fit in current image
INITIAL_RADIUS_DIVISOR = MAX_RADIUS_DIVISOR # usually we want a maximum size circle

#
# Limits, move sizes, step sizes, and display feature sizes are given in pixels within the current image size

#
# Radius limits
#
MIN_RADIUS = 5

#
# Mouse wheel radius adjustment.
#
# Each wheel click changes radius by this amount.
#
MOUSE_WHEEL_RADIUS_STEP = 5

#
# Keyboard radius adjustment.
#
# example is +, but - is just the same
# +       => KEYBOARD_RADIUS_STEP pixels
# Shift+  => KEYBOARD_RADIUS_SHIFT_STEP pixels
#
KEYBOARD_RADIUS_STEP = 1
KEYBOARD_RADIUS_SHIFT_STEP = 10

#
# Circle movement increments.
#
# Arrow                => MOVE_COARSE
# Shift+Arrow          => MOVE_MEDIUM
# Ctrl+Shift+Arrow     => MOVE_FINE
#
MOVE_COARSE = 100
MOVE_MEDIUM = 10
MOVE_FINE = 1

#
# Preview sizing.
#
# Preview image is scaled so it occupies at most:
#
#     SCREEN_WIDTH  * PREVIEW_SCREEN_WIDTH_FRACTION
#     SCREEN_HEIGHT * PREVIEW_SCREEN_HEIGHT_FRACTION
#
PREVIEW_SCREEN_WIDTH_FRACTION = 0.90
PREVIEW_SCREEN_HEIGHT_FRACTION = 0.80

#
# Overlay colors.
#
CIRCLE_COLOR = "lime"
SQUARE_COLOR = "red"
CENTER_COLOR = "cyan"

#
# Overlay line thicknesses.
#
CIRCLE_LINE_WIDTH = 2
SQUARE_LINE_WIDTH = 2
CENTER_LINE_WIDTH = 2

#
# Center marker size.
#
CENTER_MARK_SIZE = 10

#
# Canvas background.
#
CANVAS_BACKGROUND = "black"

#
# Status line font.
#
STATUS_FONT = ("Consolas", 10)

#
# Window title.
#
WINDOW_TITLE = "Circle Capture"

#
# Extra pixels added to window height
# for status bar and decorations.
#
WINDOW_VERTICAL_MARGIN = 60

#
# Output Image and Metadata filename suffix.
#
OUTPUT_IMAGE_SUFFIX = "_circle.png"
OUTPUT_TEXT_SUFFIX = "_circle.txt"

#
# ============================================================================

class CircleSelector:

    def __init__(self, image, image_path):

        self.image = image
        self.image_path = image_path

        self.width, self.height = image.size

        self.cx = self.width // 2
        self.cy = self.height // 2

        self.radius = min(self.width, self.height) // INITIAL_RADIUS_DIVISOR

    def clamp_max(self):

        self.cx = self.width // 2
        self.cy = self.height // 2

        self.radius = min(self.width, self.height) // 2
        
    def clamp_radius(self):

        max_radius = min(
            self.cx,
            self.cy,
            self.width - 1 - self.cx,
            self.height - 1 - self.cy
        )

        self.radius = max(
            MIN_RADIUS,
            min(int(self.radius), int(max_radius))
        )

    def clamp_center(self):

        r = int(self.radius)

        self.cx = max(
            r,
            min(int(self.cx), self.width - 1 - r)
        )

        self.cy = max(
            r,
            min(int(self.cy), self.height - 1 - r)
        )

    def get_square(self):

        left = int(self.cx - self.radius)
        top = int(self.cy - self.radius)

        right = int(self.cx + self.radius)
        bottom = int(self.cy + self.radius)

        return left, top, right, bottom

    def save_square(self):

        left, top, right, bottom = self.get_square()

        crop = self.image.crop(
            (left, top, right, bottom)
        )

        crop = crop.resize(
            (OUTPUT_SIZE, OUTPUT_SIZE),
            Image.Resampling.LANCZOS
        )

        base = os.path.splitext(
            self.image_path
        )[0]

        png_file = base + OUTPUT_IMAGE_SUFFIX
        txt_file = base + OUTPUT_TEXT_SUFFIX

        crop.save(png_file)

        with open(
            txt_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "%s Metadata\n" % WINDOW_TITLE
            )

            f.write(
                "========================\n\n"
            )

            f.write(
                f"Original File: "
                f"{os.path.basename(self.image_path)}\n\n"
            )

            f.write(
                f"Center X: {self.cx}\n"
            )

            f.write(
                f"Center Y: {self.cy}\n\n"
            )

            f.write(
                f"Radius: {self.radius}\n\n"
            )

            f.write(
                "Bounding Square\n"
            )

            f.write(
                "---------------\n"
            )

            left, top, right, bottom = self.get_square()

            f.write(
                f"Left:   {left}\n"
            )

            f.write(
                f"Top:    {top}\n"
            )

            f.write(
                f"Right:  {right}\n"
            )

            f.write(
                f"Bottom: {bottom}\n\n"
            )

            f.write(
                f"Square Side: "
                f"{2 * self.radius}\n"
            )

            f.write(
                f"Output Size: "
                f"{OUTPUT_SIZE} x {OUTPUT_SIZE}\n"
            )

        print()
        print("Saved:")
        print("   ", png_file)
        print("   ", txt_file)
        print()


class App:

    def __init__(self, root, image_path):

        self.root = root

        self.original_image = Image.open(
            image_path
        ).convert("RGB")

        img_w, img_h = self.original_image.size

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()

        max_w = int(
            screen_w *
            PREVIEW_SCREEN_WIDTH_FRACTION
        )

        max_h = int(
            screen_h *
            PREVIEW_SCREEN_HEIGHT_FRACTION
        )

        self.scale = min(
            max_w / img_w,
            max_h / img_h,
            1.0
        )

        self.display_w = int(
            img_w * self.scale
        )

        self.display_h = int(
            img_h * self.scale
        )

        self.display_image = (
            self.original_image.resize(
                (
                    self.display_w,
                    self.display_h
                ),
                Image.Resampling.LANCZOS
            )
        )

        self.photo = ImageTk.PhotoImage(
            self.display_image
        )

        self.selector = CircleSelector(
            self.original_image,
            image_path
        )

        self.dragging = False

        self.canvas = tk.Canvas(
            root,
            width=self.display_w,
            height=self.display_h,
            bg=CANVAS_BACKGROUND,
            highlightthickness=0
        )

        self.canvas.pack()

        self.canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.photo
        )

        self.status = tk.Label(
            root,
            anchor="w",
            font=STATUS_FONT
        )

        self.status.pack(
            fill=tk.X
        )

        self.circle_item = None
        self.square_item = None
        self.center_h = None
        self.center_v = None

        self.canvas.bind(
            "<ButtonPress-1>",
            self.mouse_down
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.mouse_up
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.mouse_drag
        )

        self.canvas.bind(
            "<MouseWheel>",
            self.mouse_wheel
        )

        self.canvas.bind(
            "<Button-4>",
            self.mouse_wheel
        )

        self.canvas.bind(
            "<Button-5>",
            self.mouse_wheel
        )

        root.bind(
            "<Left>",
            self.key_move
        )

        root.bind(
            "<Right>",
            self.key_move
        )

        root.bind(
            "<Up>",
            self.key_move
        )

        root.bind(
            "<Down>",
            self.key_move
        )

        root.bind(
            "<KeyPress-plus>",
            self.radius_key
        )

        root.bind(
            "<KeyPress-minus>",
            self.radius_key
        )

        root.bind(
            "<KeyPress-equal>",
            self.radius_key
        )

        root.bind(
            "<Control-s>",
            self.save
        )

        root.bind(
            "m",
            self.max_key
        )

        root.bind(
            "M",
            self.max_key
        )

        root.geometry(
            f"{self.display_w}x"
            f"{self.display_h + WINDOW_VERTICAL_MARGIN}"
        )

        self.redraw()

    def redraw(self):

        s = self.selector

        left, top, right, bottom = (
            s.get_square()
        )

        disp_left = left * self.scale
        disp_top = top * self.scale

        disp_right = right * self.scale
        disp_bottom = bottom * self.scale

        disp_cx = s.cx * self.scale
        disp_cy = s.cy * self.scale

        disp_r = s.radius * self.scale

        for item in (
            self.circle_item,
            self.square_item,
            self.center_h,
            self.center_v
        ):
            if item:
                self.canvas.delete(item)

        self.circle_item = (
            self.canvas.create_oval(
                disp_cx - disp_r,
                disp_cy - disp_r,
                disp_cx + disp_r,
                disp_cy + disp_r,
                outline=CIRCLE_COLOR,
                width=CIRCLE_LINE_WIDTH
            )
        )

        self.square_item = (
            self.canvas.create_rectangle(
                disp_left,
                disp_top,
                disp_right,
                disp_bottom,
                outline=SQUARE_COLOR,
                width=SQUARE_LINE_WIDTH
            )
        )

        self.center_h = (
            self.canvas.create_line(
                disp_cx - CENTER_MARK_SIZE,
                disp_cy,
                disp_cx + CENTER_MARK_SIZE,
                disp_cy,
                fill=CENTER_COLOR,
                width=CENTER_LINE_WIDTH
            )
        )

        self.center_v = (
            self.canvas.create_line(
                disp_cx,
                disp_cy - CENTER_MARK_SIZE,
                disp_cx,
                disp_cy + CENTER_MARK_SIZE,
                fill=CENTER_COLOR,
                width=CENTER_LINE_WIDTH
            )
        )

        self.status.config(
            text=
            f"Center=({s.cx},{s.cy})   "
            f"Radius={s.radius}   "
            f"TL=({left},{top})   "
            f"BR=({right},{bottom})   "
            f"Side={2 * s.radius}px   "
            f"Output={OUTPUT_SIZE}x{OUTPUT_SIZE}"
        )

    def mouse_down(self, event):

        self.dragging = True

        self.selector.cx = int(
            event.x / self.scale
        )

        self.selector.cy = int(
            event.y / self.scale
        )

        self.selector.clamp_center()

        self.redraw()

    def mouse_up(self, event):

        self.dragging = False

    def mouse_drag(self, event):

        if not self.dragging:
            return

        self.selector.cx = int(
            event.x / self.scale
        )

        self.selector.cy = int(
            event.y / self.scale
        )

        self.selector.clamp_center()

        self.redraw()

    def mouse_wheel(self, event):

        if hasattr(event, "delta") and event.delta:

            if event.delta > 0:
                self.selector.radius += (
                    MOUSE_WHEEL_RADIUS_STEP
                )
            else:
                self.selector.radius -= (
                    MOUSE_WHEEL_RADIUS_STEP
                )

        elif hasattr(event, "num"):

            if event.num == 4:
                self.selector.radius += (
                    MOUSE_WHEEL_RADIUS_STEP
                )

            elif event.num == 5:
                self.selector.radius -= (
                    MOUSE_WHEEL_RADIUS_STEP
                )

        self.selector.clamp_radius()

        self.redraw()

    def max_key(self, event):

        self.selector.clamp_max()

        self.redraw()

    def radius_key(self, event):

        shift = (
            event.state & 0x0001
        ) != 0

        step = (
            KEYBOARD_RADIUS_SHIFT_STEP
            if shift
            else KEYBOARD_RADIUS_STEP
        )

        if event.keysym in (
            "plus",
            "equal"
        ):
            self.selector.radius += step

        elif event.keysym == "minus":
            self.selector.radius -= step

        self.selector.clamp_radius()

        self.redraw()

    def key_move(self, event):

        shift = (
            event.state & 0x0001
        ) != 0

        ctrl = (
            event.state & 0x0004
        ) != 0

        if shift and ctrl:
            step = MOVE_FINE

        elif shift:
            step = MOVE_MEDIUM

        else:
            step = MOVE_COARSE

        if event.keysym == "Left":
            self.selector.cx -= step

        elif event.keysym == "Right":
            self.selector.cx += step

        elif event.keysym == "Up":
            self.selector.cy -= step

        elif event.keysym == "Down":
            self.selector.cy += step

        self.selector.clamp_center()

        self.redraw()

    def save(self, event=None):

        self.selector.save_square()


def main():

    if len(sys.argv) != 2:

        print()
        print(
            "Usage:"
        )

        print(
            "    python CircleCapture.py imagefile"
        )

        print()

        return

    image_path = sys.argv[1]

    root = tk.Tk()

    root.title(
        WINDOW_TITLE
    )

    App(
        root,
        image_path
    )

    root.mainloop()


if __name__ == "__main__":
    main()
