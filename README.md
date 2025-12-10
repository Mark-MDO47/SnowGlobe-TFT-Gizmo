# SnowGlobe TFT-Gizmo

My build of the Circuit Playground TFT Gizmo Snow Globe by Carter Nelson
- https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe/

Here are my extension ideas:
- I want the snow globe to cycle through several different background images
- I want to power it ultimately from AC so it can switch on and off with the Christmas tree
- I want to have some control of loading the background images

To see issues I had with my plan see https://github.com/Mark-MDO47/CircuitPlaygroundBLE_expts

**Table Of Contents**
* [Top](#snowglobe-tft\-gizmo "Top")
* [v1.0.0 Snow Globe Behavior](#v100-snow-globe-behavior "v1.0.0 Snow Globe Behavior")
* [Preparation of the Electronics](#preparation-of-the-electronics "Preparation of the Electronics")
* [Preparation of Plastic Ornament Globe](#preparation-of-plastic-ornament-globe "Preparation of Plastic Ornament Globe")
* [Software](#software "Software")
* [Parts List](#parts-list "Parts List")
* [References](#references "References")
  * [From Nordic](#from-nordic "From Nordic")
  * [From Adafruit](#from-adafruit "From Adafruit")
    * [Circuit Playground Bluefruit - Bluetooth Low Energy](#circuit-playground-bluefruit-\--bluetooth-low-energy "Circuit Playground Bluefruit - Bluetooth Low Energy")
    * [Circuit Playground TFT Gizmo](#circuit-playground-tft-gizmo "Circuit Playground TFT Gizmo")
    * [Update to Latest Firmware and CircuitPython](#update-to-latest-firmware-and-circuitpython "Update to Latest Firmware and CircuitPython")
    * [Learn the basics of Circuit Playground Bluefruit](#learn-the-basics-of-circuit-playground-bluefruit "Learn the basics of Circuit Playground Bluefruit")
    * [The Big Kahuna - the API registry.](#the-big-kahuna-\--the-api-registry "The Big Kahuna - the API registry.")
  * [Non-Official but Useful](#non\-official-but-useful "Non-Official but Useful")

## v1.0.0 Snow Globe Behavior
[Top](#snowglobe-tft\-gizmo "Top")<br>
As of v1.0.0:
- At startup, a psuedo-random number is used to choose the background image and load it up
- Snowfall starts
- If either a SHAKE is detected or 300 seconds pass - REBOOT

## Preparation of the Electronics
[Top](#snowglobe-tft\-gizmo "Top")<br>
- First - go here [Update to Latest Firmware and CircuitPython](#update-to-latest-firmware-and-circuitpython "Update to Latest Firmware and CircuitPython")<br>
- Next - store the **lib** files from the **Project Bundle** (I am in version 10x of CircuitPython) of **Simple Snow Globe** in the original **Circuit Playground TFT Gizmo Snow Globe** by Carter Nelson onto your **CIRCUITPY** drive - https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe?view=all<br>
- Next - mechanically assemble Circuit Playground Bluefruit with TFT Gizmo - https://learn.adafruit.com/adafruit-tft-gizmo<br>
- Finally - Connect USB to your computer and store your boot.py and code.py onto your **CIRCUITPY** drive

## Preparation of Plastic Ornament Globe
[Top](#snowglobe-tft\-gizmo "Top")<br>
I am using a USB cable plugged into a wall charger to power the Snow Globe. That way it can be powered on/off with the rest of the Christmas tree lights.

I needed a way to get the USB cable into the plastic globe. Ideally I would put a 7/16 inch hole and add a rubber grommet. However, with my slow-speed electric drill, any bit larger than 7/32 inch would grab as it went through and shatter the plastic.

Eventually I used the slow-speed electric drill and a 7/32 inch pilot hole, followed by a grinding attachment from my Dremel tool again with the slow-speed electric drill to get about a 3/8 inch hole. I finished up with a smaller grinding tool on the actual Dremel tool to slot out the sides. Not pretty, but it fits the cable and it is on the backside of the ornament.

## Software
[Top](#snowglobe-tft\-gizmo "Top")<br>
See the following to examine the code.py and boot.py I am using.
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/tree/master/code
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/code/README.md

The code.py software I am using is based on the **Circuit Playground TFT Gizmo Snow Globe** by Carter Nelson. This is a CircuitPython program.
- https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe/

Because the latest stable version of CircuitPython was 10.0.3 when I did this project, I started from the "simple" version of Carter's Snow Globe for CircuitPython 10.x. The original version is here in addition to the Adafruit Learning address above.
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/code/code.original.simple.10x.py

My version of the code is here:
- https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/code/code.py

I did a little code re-arranging to suit my style. I was hoping to be able to have it load a sequence of background images but found it would hit memory limitations after anywhere from 2 to 5 images in my various attempts to solve it. I am not sure if the issue is a memory leak or memory fragmentation. As Christmas was approaching, I opted to do a reboot to load the next background image to avoid memory issues.

I was hoping to use the FLASH in the form of a filesystem that CircuitPython provides to be able to sequence through the images. I made some attempts using the methods described here, but was not able to make that work:
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython-storage

Maybe I just need to RTFM! The above says (and I paraphrase): boot.py only runs after a power-cycle or hard reset, not a soft reboot. Duh.

Since I had not figured out writing to the FLASH filesystem and Christmas was still approaching, I decided to use a psuedo-random number generator to choose the background image after reboot. I didn't use the standard randrange() method - that is fine for controlling the snowflakes but I didn't want to have a predictable sequence of background images. Eventually I used the least significant portion of the count of nanoseconds since power-on as my "random" number.

If you are interested in reading about some of the things I tried or my thoughts on random numbers, see here:
- https://github.com/Mark-MDO47/CircuitPlaygroundBLE_expts

I still might use the conductive tape to allow touch control of some portion of the Snow Globe.

## Parts List
[Top](#snowglobe-tft\-gizmo "Top")<br>
| Qty | Description | URL |
| --- | --- | --- |
| 1 | Adafruit Circuit Playground Bluefruit - Bluetooth® Low Energy | https://www.adafruit.com/product/4333 |
| 1 | Adafruit Circuit Playground TFT GIZMO | https://www.adafruit.com/product/4367 |
| 1 | Adafruit DIY Ornament Kit - 6cm Diameter - Perfect for Circuit Playground | https://www.adafruit.com/product/4036 |
| 1 | Itramax Micro USB Extension Cable 20FT (note: flat cable USB-A to USB-MicroB) | https://www.amazon.com/Itramax-Charging-Charger-Camera-Controller/dp/B07ZGCV1S1?th=1 |
| 1 | USB C Charger Block, Dual Port Type C Wall Charger Fast Charging 20W Power Adapter Cube (note: also has USB-A output) | https://www.amazon.com/dp/B0CPSBD68W?th=1 |
| 1 | Ornament hook | https://www.amazon.com/dp/B0G1CNB86G |
| 1 | 5mm x 20M (0.2in x 65ft) Conductive Cloth Fabric Adhesive Tape | https://www.amazon.com/dp/B01ALDR0D0 |


## References
[Top](#snowglobe-tft\-gizmo "Top")<br>

### From Nordic
[Top](#snowglobe-tft\-gizmo "Top")<br>
**nRF52840 Specs**
- https://docs.nordicsemi.com/bundle/ps_nrf52840/page/keyfeatures_html5.html
- https://docs-be.nordicsemi.com/bundle/ps_nrf52840/attach/nRF52840_PS_v1.11.pdf?_LANG=enus

### From Adafruit
[Top](#snowglobe-tft\-gizmo "Top")<br>

#### Circuit Playground Bluefruit - Bluetooth Low Energy
[Top](#snowglobe-tft\-gizmo "Top")<br>
- https://www.adafruit.com/product/4333
  - nRF52840 Cortex M4 processor with Bluetooth Low Energy
    - On-chip according to specification: 1 MBbyte FLASH and 256 kB RAM
  - Schematic here: https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/downloads
    - When using CircuitPython, there is a 2 MByte USB filesystem FLASH disk. This comes from a FLASH part on the board.
  - https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/guided-tour
  - https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/pinouts

#### Circuit Playground TFT Gizmo
[Top](#snowglobe-tft\-gizmo "Top")<br>
- https://www.adafruit.com/product/4367
- https://learn.adafruit.com/adafruit-tft-gizmo
- https://learn.adafruit.com/circuitpython-display-support-using-displayio

#### Update to Latest Firmware and CircuitPython
[Top](#snowglobe-tft\-gizmo "Top")<br>
Good idea to do this when getting a new Circuit Playground Bluefruit.
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/downloads
- updating loader to 0.9.2 from 0.9.0
  - https://github.com/adafruit/Adafruit_nRF52_Bootloader/releases/tag/0.9.2
  - update-circuitplayground_nrf52840_bootloader-0.9.2_nosd.uf2
- Updating to CircuitPython 10.0.3
  - https://circuitpython.org/board/circuitplayground_bluefruit/
  - adafruit-circuitpython-circuitplayground_bluefruit-en_US-10.0.3.uf2

#### Learn the basics of Circuit Playground Bluefruit
[Top](#snowglobe-tft\-gizmo "Top")<br>
From the Adafruit Learning System
- https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit

#### The Big Kahuna - the API registry.
[Top](#snowglobe-tft\-gizmo "Top")<br>
It is for all Circuit Playground and includes a section on the Bluefruit model.
- https://docs.circuitpython.org/projects/circuitplayground/en/latest/api.html

### Non-Official but Useful
Quick Reference Guide - Adafruit Circuit Playground Bluefruit (from Carnegie Mellon University)
- https://courses.ideate.cmu.edu/16-376/s2022/ref/text/code/cpb-quickref.html
