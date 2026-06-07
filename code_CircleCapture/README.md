# CircleCapture.py
**CircleCapture.py** is a utility to capture a square portion of an image, displaying the inscribed circle as if on a round display ornament, allow movement
and resize of the circle, and on command save the contents of the square, resized to 480x480 *.png
- Inputs: JPG / PNG / BMP / HEIC / HEIF
- Outputs: 480x480 file in same directory as input named <original>_circle.png *.txt with metadata named <original>_circle.txt
- Preview automatically scaled to fit screen with full-resolution coordinate system

The output of **CircleCapture.py** can be chained into **mdo_tablegen.py** to produce a *.bin for the 2.1 inch and 2.8 inch displays.

I used ChatGPT using GPT 5.5 to generate **CircleCapture.py**.

| Control          | Function                |
| ---------------- | ----------------------- |
| Mouse drag       | Move circle             |
| Mouse wheel      | Radius ±5 px            |
| Arrow            | Move 100 px             |
| Shift+Arrow      | Move 10 px              |
| Ctrl+Shift+Arrow | Move 1 px               |
| +                | Radius +1 px            |
| Shift++          | Radius +10 px           |
| -                | Radius -1 px            |
| Shift+-          | Radius -10 px           |
| Ctrl+S           | Save PNG + metadata TXT |

You can read about the hardware that uses these images here
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/GO_BIG.md

You can read about the program **mdo_tablegen.py** here
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/GO_BIG.md#software-starting-point---qualia_paintpy-and-tablegenpy

In order to run CircleCapture, there are some non-standard libraries to install. In the command below, replace **<your installer>** with your installer. It is likely to be either **pip** (standard Python package manager) or **conda** (Anaconda/Conda).

```
<your installer> install pillow pillow-heif
```

Here is an image of **CircleCapture.py** in action<br>
<img src="https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/resources/images/CircleSelector.jpg" width="400" alt="Circle Selector window">

