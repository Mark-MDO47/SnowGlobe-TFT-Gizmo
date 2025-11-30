# SnowGlobe TFT-Gizmo

My build of the Circuit Playground TFT Gizmo Snow Globe by Carter Nelson
- https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe/

Here are my extension ideas:
- I want the snow globe to cycle through several different background images
- I want to power it ultimately from AC so it can switch on and off with the Christmas tree

To see issues I had with my plan see https://github.com/Mark-MDO47/CircuitPlaygroundBLE_expts

**Table Of Contents**
* [Top](#snowglobe-tft\-gizmo "Top")
* [Preparation of the Electronics](#preparation-of-the-electronics "Preparation of the Electronics")
  * [Update to Latest Firmware and CircuitPython](#update-to-latest-firmware-and-circuitpython "Update to Latest Firmware and CircuitPython")

## Preparation of the Electronics
[Top](#snowglobe-tft\-gizmo "Top")<br>
First - go here [Update to Latest Firmware and CircuitPython](#update-to-latest-firmware-and-circuitpython "Update to Latest Firmware and CircuitPython")<br>
Next - store the **lib** files from the **Project Bundle** of **Simple Snow Globe** in the original **Circuit Playground TFT Gizmo Snow Globe** by Carter Nelson onto your **CIRCUITPY** drive - https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe?view=all<br>
Next - assemble with TFT Gizmo - https://learn.adafruit.com/adafruit-tft-gizmo<br>
Finally - Store your boot.py and code.py onto your **CIRCUITPY** drive

## References
[Top](#circuitplaygroundble_expts "Top")<br>

### From Nordic
[Top](#circuitplaygroundble_expts "Top")<br>
**nRF52840 Specs**
- https://docs.nordicsemi.com/bundle/ps_nrf52840/page/keyfeatures_html5.html
- https://docs-be.nordicsemi.com/bundle/ps_nrf52840/attach/nRF52840_PS_v1.11.pdf?_LANG=enus

### From Adafruit
[Top](#circuitplaygroundble_expts "Top")<br>

#### Circuit Playground Bluefruit - Bluetooth Low Energy
[Top](#circuitplaygroundble_expts "Top")<br>
- https://www.adafruit.com/product/4333
  - nRF52840 Cortex M4 processor with Bluetooth Low Energy
    - On-chip according to specification: 1 MBbyte FLASH and 256 kB RAM
    - When using CircuitPython, there is a 2 MByte USB filesystem FLASH disk. Maybe this comes from some other FLASH on the board?
  - https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/guided-tour
  - https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/pinouts

#### Circuit Playground TFT Gizmo
[Top](#circuitplaygroundble_expts "Top")<br>
- https://www.adafruit.com/product/4367
- https://learn.adafruit.com/adafruit-tft-gizmo

#### Update to Latest Firmware and CircuitPython
[Top](#circuitplaygroundble_expts "Top")<br>
Good idea to do this when getting a new Circuit Playground Bluefruit.
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/downloads
- updating loader to 0.9.2 from 0.9.0
  - https://github.com/adafruit/Adafruit_nRF52_Bootloader/releases/tag/0.9.2
  - update-circuitplayground_nrf52840_bootloader-0.9.2_nosd.uf2
- Updating to CircuitPython 10.0.3
  - https://circuitpython.org/board/circuitplayground_bluefruit/
  - adafruit-circuitpython-circuitplayground_bluefruit-en_US-10.0.3.uf2

#### Learn the basics of Circuit Playground Bluefruit
[Top](#circuitplaygroundble_expts "Top")<br>
From the Adafruit Learning System
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit

#### The Big Cahuna - the API registry.
[Top](#circuitplaygroundble_expts "Top")<br>
It is for all Circuit Playground and includes a section on the Bluefruit model.
- https://docs.circuitpython.org/projects/circuitplayground/en/latest/api.html

### Non-Official but Useful
Quick Reference Guide - Adafruit Circuit Playground Bluefruit (from Carnegie Mellon University)
- https://courses.ideate.cmu.edu/16-376/s2022/ref/text/code/cpb-quickref.html
