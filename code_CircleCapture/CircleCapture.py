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
# | Ctrl+S           | Save PNG + metadata TXT |

import os
import sys
import tkinter as tk

from PIL import Image, ImageTk
from pillow_heif import register_heif_opener

register_heif_opener()

OUTPUT_SIZE = 480


class CircleSelector:

    def __init__(self, image, image_path):

        self.image = image
        self.image_path = image_path

        self.width, self.height = image.size

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
            5,
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

        png_file = base + "_circle.png"
        txt_file = base + "_circle.txt"

        crop.save(png_file)

        with open(
            txt_file,
            "w",
            encoding="utf-8"
        ) as f:

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

            f.write("Square:\n")

            f.write(
                f"Left: {left}\n"
            )

            f.write(
                f"Top: {top}\n"
            )

            f.write(
                f"Right: {right}\n"
            )

            f.write(
                f"Bottom: {bottom}\n\n"
            )

            f.write(
                f"Square Side: "
                f"{right-left}\n"
            )

            f.write(
                f"Output Size: "
                f"{OUTPUT_SIZE}\n"
            )

        print(f"Saved: {png_file}")
        print(f"Saved: {txt_file}")


class App:

    def __init__(self, root, image_path):

        self.root = root

        self.original_image = Image.open(
            image_path
        ).convert("RGB")

        img_w, img_h = self.original_image.size

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()

        max_w = int(screen_w * 0.90)
        max_h = int(screen_h * 0.80)

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
            highlightthickness=0,
            bg="black"
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
            font=("Consolas", 10)
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

        root.geometry(
            f"{self.display_w}x"
            f"{self.display_h+60}"
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

        side = right - left

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
                outline="lime",
                width=2
            )
        )

        self.square_item = (
            self.canvas.create_rectangle(
                disp_left,
                disp_top,
                disp_right,
                disp_bottom,
                outline="red",
                width=2
            )
        )

        self.center_h = (
            self.canvas.create_line(
                disp_cx - 10,
                disp_cy,
                disp_cx + 10,
                disp_cy,
                fill="cyan",
                width=2
            )
        )

        self.center_v = (
            self.canvas.create_line(
                disp_cx,
                disp_cy - 10,
                disp_cx,
                disp_cy + 10,
                fill="cyan",
                width=2
            )
        )

        self.status.config(
            text=
            f"Center=({s.cx},{s.cy})   "
            f"Radius={s.radius}   "
            f"TL=({left},{top})   "
            f"BR=({right},{bottom})   "
            f"Side={side}px   "
            f"Output=480x480"
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
                self.selector.radius += 5
            else:
                self.selector.radius -= 5

        elif hasattr(event, "num"):

            if event.num == 4:
                self.selector.radius += 5

            elif event.num == 5:
                self.selector.radius -= 5

        self.selector.clamp_radius()

        self.redraw()

    def radius_key(self, event):

        shift = (
            event.state & 0x0001
        ) != 0

        step = 10 if shift else 1

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
            step = 1

        elif shift:
            step = 10

        else:
            step = 100

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

        print(
            "\nUsage:\n"
            "python circle_selector.py imagefile\n"
        )

        return

    image_path = sys.argv[1]

    root = tk.Tk()

    root.title(
        "Circle Selector"
    )

    App(
        root,
        image_path
    )

    root.mainloop()


if __name__ == "__main__":
    main()
