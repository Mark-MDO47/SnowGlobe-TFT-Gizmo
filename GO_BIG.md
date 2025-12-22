# GO BIG

I decided to make a bigger version of the Snow Globe

**Table Of Contents**
* [Top](#go-big "Top")
* [The Plan](#the-plan "The Plan")
  * [Starting Point - qualia_paint.py and tablegen.py](#starting-point-\--qualia_paintpy-and-tablegenpy "Starting Point - qualia_paint.py and tablegen.py")
  * [mdo_big_round_ornament.py](#mdo_big_round_ornamentpy "mdo_big_round_ornament.py")
    * [Performance](#performance "Performance")
    * [Memory](#memory "Memory")
* [Circuit Python First Steps](#circuit-python-first-steps "Circuit Python First Steps")
  * [CircUp tool for libraries](#circup-tool-for-libraries "CircUp tool for libraries")
  * [Settings toml File](#settings-toml-file "Settings toml File")
* [Parts List](#parts-list "Parts List")

## The Plan
[Top](#go-big "Top")<br>

### Starting Point - qualia_paint.py and tablegen.py
[Top](#go-big "Top")<br>
I will start from my versions of some things taken from Adafruit libraries as described here in my experiments.
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/README.md#mdo_qualia_paint

I made **mdo_** versions of the Adafruit examples **qualia_paint.py** and **tablegen.py**
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/tree/master/mdo_qualia_paint

The original Adafruit **qualia_paint.py** can be found here:
- https://docs.circuitpython.org/projects/qualia/en/latest/examples.html

The original Adafruit **tablegen.py** can be found here:
- https://github.com/adafruit/Uncanny_Eyes commit d2103e84aa33da9f6924885ebc06d880af8deeff

When I started on **mdo_qualia_paint.py** I used **mdo_tablegen.py** to read an image file (.bmp, .png, .jpg) and create the C-language ***.h** file for the 16-bit RBG 565 format, then read that *.h file in **mdo_qualia_paint.py** and convert it to binary on the board. This took about 2.5 minutes to boot **mdo_qualia_paint.py** even after cropping the left 1/3 of the picture that is used for its controls.

I modified **mdo_tablegen.py** to also create a **.bin** file that is a big-endian version of the data in raw binary. It now takes about 15 seconds to boot **mdo_qualia_paint.py** reading this **.bin** file.

This **mdo_tablegen.py** will work for the Snow Globe project too.

## mdo_big_round_ornament.py
[Top](#go-big "Top")<br>
I decided to call this program **mdo_big_round_ornament.py**

### Performance
[Top](#go-big "Top")<br>
It still takes 15 seconds to load the **.bin**; I expected longer since we aren't cropping off 1/3 of the picture like mdo_qualia_paint. It takes 25 seconds from power-on but 15 seconds from storing program on USB drive.

Maybe I will make **mdo_big_round_ornament** not write all the pixels that are not actually on the round display to speed things up. But first let's get it working, then we can optimize.

### Memory
[Top](#go-big "Top")<br>
I am creating the list ([]) img_565 early on and keeping it in scope so we don't fragment RAM by allocating/deallocating it over and over.
- This stores the 16-bit pixel information of the current background image. That will be a handy thing to have around as we move the snow sprites around.

### 01 - Test of Memory Usage Robustness
[Top](#go-big "Top")<br>
My hope is that by starting with this code which is closer to the metal, I can avoid the memory problems I had with the TFT-Gizmo version. The problem is my lack of background knowledge in the display routines used. I was just using a shotgun approach to debug it. Admittedly I did find some issues and got it to last through 5 background changes instead of 2, but eventually I just used the reboot option.

With **mdo_qualia_paint** I had never noticed this issue. However, the background switches were manually invoked and I had never tested the limits to see if there was a latent problem.

The file **01_RobustnessTest.py** (an early version of mdo_big_round_ornament.py) changes the background every 10 seconds. I ran it for 20 hours and it was still going without a problem.

## Parts List
[Top](#go-big "Top")<br>
| Hardware | Description | URL |
| --- | --- | --- |
| Qualia ESP32-S3 RBG-666 40p TFT | Special TFT ESP32-S3 board | https://www.adafruit.com/product/5800 |
| 2.1 inch 480x480 Cap Display | TFT round display | https://www.adafruit.com/product/5792 |
| Clear Fillable Ornaments Balls 80mm/3.15" | Clear Plastic DIY Ornament 3.15 inch | https://www.amazon.com/dp/B0CF2GXVSN |
| Itramax Micro USB Extension Cable 20FT (note: flat cable USB-A to USB-MicroB) | USB cable | https://www.amazon.com/Itramax-Charging-Charger-Camera-Controller/dp/B07ZGCV1S1?th=1 |
| USB C Charger Block, Dual Port Type C Wall Charger Fast Charging 20W Power Adapter Cube (note: also has USB-A output) | USB charger | https://www.amazon.com/dp/B0CPSBD68W?th=1 |

Note: even though the display itself is 2.1 inch there is some space around the edge so this ornament ball fits nicely on the display. I will have to make a cut and leave the rest of the electronics on the outside. I have ordered some 4 inch ornament balls but they won't be here before Christmas.

## First Steps - Factory Reset and Install Circuit Python
[Top](#go-big "Top")<br>
Here is how to configure the Qualia ESP32-S3 for Circuit Python<br>

| To Know | Where |
| --- | --- |
| Adafruit Qualia ESP32-S3 for RGB-666 Displays | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays |
| Adafruit Qualia ESP32-S3 - factory reset | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/factory-reset |
| UF2 Bootloader details | https://learn.adafruit.com/adafruit-hallowing/uf2-bootloader-details |
| settings.toml file | [settings toml file](#settings-toml-file "settings toml file") |

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
[Top](#go-big "Top")<br>

https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/circuitpython-libraries

Use the CircUp tool to update the libraries, or else copy the entire new Adafruit library.
- https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/usage

### Settings toml File
[Top](#go-big "Top")<br>

Should probably set the following in **settings.toml** file; enclose strings within double-quotes ""
- https://docs.circuitpython.org/en/latest/docs/environment.html

| Parameter | Description | Comments |
| --- | --- | ---  |
| CIRCUITPY_WEB_API_PASSWORD | Password required to make modifications to the board from the Web Workflow | I just set this to nonsense so it won't connect |
| CIRCUITPY_WIFI_PASSWORD | Wi-Fi password used to auto connect to CIRCUITPY_WIFI_SSID | None |
| CIRCUITPY_WIFI_SSID | Wi-Fi SSID to auto-connect to even if user code is not running | None |
| CIRCUITPY_HEAP_START_SIZE | size of heap at startup | for qualia 3072000 seems good, but usually not needed |
| CIRCUITPY_PYSTACK_SIZE | size of stack at startup | for qualia 4000 seems good, but usually not needed |
