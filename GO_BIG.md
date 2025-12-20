# GO BIG

I decided to make a bigger version of the Snow Globe based on the following hardware:

| Hardware | Description | URL |
| --- | --- | --- |
| Qualia ESP32-S3 RBG-666 40p TFT | Special TFT ESP32-S3 board | https://www.adafruit.com/product/5800 |
| 2.1 inch 480x480 Cap Display | TFT round display | https://www.adafruit.com/product/5792 |
| Clear Fillable Ornaments Balls 80mm/3.15" | Clear Plastic DIY Ornament 3.15 inch | https://www.amazon.com/dp/B0CF2GXVSN |

Note: even though the display itself is 2.1 inch there is some space around the edge so this ornament ball fits nicely on the display. I will have to make a cut and leave the rest of the electronics on the outside. I have ordered some 4 inch ornament balls but they won't be here before Christmas.

I had previously done some experiments with the electronics combination here and had no memory problems doing succesive images.
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display

**Table Of Contents**
* [Top](#go-big "Top")
* [Circuit Python First Steps](#circuit-python-first-steps "Circuit Python First Steps")
  * [CircUp tool for libraries](#circup-tool-for-libraries "CircUp tool for libraries")
  * [Settings toml File](#settings-toml-file "Settings toml File")

## The Plan

## Circuit Python First Steps
* [Top](#go-big "Top")<br>
Here is how to configure the Qualia ESP32-S3 for Circuit Python
| To Know | Where |
| --- | --- |
| Adafruit Qualia ESP32-S3 for RGB-666 Displays | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays |
| Adafruit Qualia ESP32-S3 - factory reset | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/factory-reset |
| UF2 Bootloader details | https://learn.adafruit.com/adafruit-hallowing/uf2-bootloader-details |
| settings.toml file | [settings toml file](#settings-toml-file "settings toml file") |

* [Top](#go-big "Top")<br>
I am following instructions here
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/overview
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/factory-reset 

I am using the latest *.uf2 from https://circuitpython.org/board/adafruit_qualia_s3_rgb666/
- Choose your board from https://circuitpython.org/downloads to get latest download
- I put the entire library into the ESP32-S3

Somehow my ESP32-S3 did not respond to a double-tap on reset, so I did a factory reset and reloaded the UF2 bootloader. I followed the instructions here and it worked the first time.
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/install-uf2-bootloader

I downloaded the **MU** editor as per instructions. It connected up to the ESP32-S3 board and its serial port. No red LED though.<BR>
Looks like sometimes I need to reset after saving new code MU.

### CircUp tool for libraries
* [Top](#go-big "Top")<br>
https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/circuitpython-libraries

Use the CircUp tool to update the libraries, or else copy the entire new Adafruit library.
- https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/usage

### Settings toml File
* [Top](#go-big "Top")<br>
Should probably set the following in **settings.toml** file; enclose strings within double-quotes ""
- https://docs.circuitpython.org/en/latest/docs/environment.html

| Parameter | Description | Comments |
| --- | --- | ---  |
| CIRCUITPY_WEB_API_PASSWORD | Password required to make modifications to the board from the Web Workflow | I just set this to nonsense so it won't connect |
| CIRCUITPY_WIFI_PASSWORD | Wi-Fi password used to auto connect to CIRCUITPY_WIFI_SSID | None |
| CIRCUITPY_WIFI_SSID | Wi-Fi SSID to auto-connect to even if user code is not running | None |
| CIRCUITPY_HEAP_START_SIZE | size of heap at startup | for qualia 3072000 seems good, but usually not needed |
| CIRCUITPY_PYSTACK_SIZE | size of stack at startup | for qualia 4000 seems good, but usually not needed |
