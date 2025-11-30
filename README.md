# SnowGlobe TFT-Gizmo

My build of the Circuit Playground TFT Gizmo Snow Globe by Carter Nelson
- https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe/

Here are my extension ideas:
- I want the snow globe to cycle through several different background images
- I want to power it ultimately from AC so it can switch on and off with the Christmas tree

To see issues I had with my plan see https://github.com/Mark-MDO47/CircuitPlaygroundBLE_expts
**Table Of Contents**

## Preparation of the Electronics

First - go here [Update to Latest Firmware and CircuitPython](#update-to-latest-firmware-and-circuitpython "Update to Latest Firmware and CircuitPython")<br>
Next - store the **lib** files from the **Project Bundle** of **Simple Snow Globe** in the original **Circuit Playground TFT Gizmo Snow Globe** by Carter Nelson onto your **CIRCUITPY** drive - https://learn.adafruit.com/circuit-playground-tft-gizmo-snow-globe?view=all<br>
Next - assemble with TFT Gizmo - https://learn.adafruit.com/adafruit-tft-gizmo<br>
Finally - Store your boot.py and code.py onto your **CIRCUITPY** drive

### Update to Latest Firmware and CircuitPython

Good idea to do this when getting a new Circuit Playground Bluefruit.
- https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/downloads
- updating loader to 0.9.2 from 0.9.0
  - https://github.com/adafruit/Adafruit_nRF52_Bootloader/releases/tag/0.9.2
  - update-circuitplayground_nrf52840_bootloader-0.9.2_nosd.uf2
- Updating to CircuitPython 10.0.3
  - https://circuitpython.org/board/circuitplayground_bluefruit/
  - adafruit-circuitpython-circuitplayground_bluefruit-en_US-10.0.3.uf2
