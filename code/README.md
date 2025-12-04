# Code

**Table Of Contents**
* [Top](#code "Top")
* [code.py](#codepy "code.py")
* [boot.py](#bootpy "boot.py")

## code.py
[Top](#code "Top")<br>
The software I am using is based on the **Circuit Playground TFT Gizmo Snow Globe** by Carter Nelson. This is a CircuitPython program.
- https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe/

Because the latest stable version of CircuitPython was 10.0.3 when I did this project, I started from the "simple" version of Carter's Snow Globe for CircuitPython 10.x. The original version is here in addition to the Adafruit Learning address above.
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/code/code.original.simple.10x.py

My version of the code is here:
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/code/code.py

I did a little code re-arranging to suit my style. I was hoping to be able to have it load a sequence of background images but found it would hit memory limitations after anywhere from 2 to 5 images in my various attempts to solve it. I am not sure if the issue is a memory leak or memory fragmentation. As Christmas was approaching, I opted to do a reboot to load the next background image to avoid memory issues.

I was hoping to use the FLASH in the form of a filesystem that CircuitPython provides to be able to sequence through the images. I made some attempts using the methods described here, but was not able to make that work:
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-storage

Since I had not figured out writing to the FLASH filesystem and Christmas was still approaching, I decided to use a psuedo-random number generator to choose the background image. I didn't use the standard randrange() method - that is fine for controlling the snowflakes but I didn't want to have a predictable sequence of background images. Eventually I used the least significant portion of the count of nanoseconds since power-on as my "random" number.

If you are interested in reading about some of the things I tried or my thoughts on random numbers, see here:
- https://github.com/Mark-MDO47/CircuitPlaygroundBLE_expts

I still might use the conductive tape to allow touch control of some portion of the Snow Globe.

## boot.py
[Top](#code "Top")<br>
