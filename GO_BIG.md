# GO BIG

I decided to make a bigger version of the Snow Globe. 
- **GO BIG** uses the round 2.1" 480x480 TFT display. I used the touchscreen version since that was what I had in the bin.
- **GO BIGGER** will use the round 2.8" 480x480 TFT display. This one is not a touchscreen version since in this application we cannot touch the screen.

| 2.1 display on the table | 2.1 display on the tree |
| --- | --- |
| <img src="https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/resources/images/GoBig_OnTable_smudged.jpg" width="300" alt="Go Big Snowglobe on table - smudged to protect the guilty"> | <img src="https://github.com/Mark-MDO47/SnowGlobe-TFT-Gizmo/blob/master/resources/images/GoBig_BarefootFormal_1020x768_smudge.png" width="400" alt="Go Big Snowglobe - smudged to protect the guilty"> |
 
**Table Of Contents**
* [Top](#go-big "Top")
* [The Plan](#the-plan "The Plan")
  * [Hardware for **GO BIG** and **GO BIGGER**](#hardware-for-**go-big**-and-**go-bigger** "Hardware for **GO BIG** and **GO BIGGER**")
* [Software Starting Point - qualia_paint.py and tablegen.py](#software-starting-point-\--qualia_paintpy-and-tablegenpy "Software Starting Point - qualia_paint.py and tablegen.py")
* [Software Changes](#software-changes "Software Changes")
  * [Image File Format](#image-file-format "Image File Format")
  * [Overall Organization](#overall-organization "Overall Organization")
  * [Performance](#performance "Performance")
  * [Memory](#memory "Memory")
    * [01 - Test of Memory Usage Robustness](#01-\--test-of-memory-usage-robustness "01 - Test of Memory Usage Robustness")
* [Parts List](#parts-list "Parts List")
* [First Steps - Factory Reset and Install Circuit Python](#first-steps-\--factory-reset-and-install-circuit-python "First Steps - Factory Reset and Install Circuit Python")
  * [CircUp tool for libraries](#circup-tool-for-libraries "CircUp tool for libraries")
  * [Settings toml File](#settings-toml-file "Settings toml File")
  * [2.8 inch Display](#28-inch-display "2.8 inch Display")

## The Plan
[Top](#go-big "Top")<br>

### Hardware for **GO BIG** and **GO BIGGER**
[Top](#go-big "Top")<br>
The display for the 2.1" is found at https://www.adafruit.com/product/5792.

The display for the 2.8" is found at https://www.adafruit.com/product/5852.

It seems probable that I won't have to modify the program at all to switch between these two displays.
- Ha ha! That was incorrect. The two displays use a different controller chip with different initialization etc.
- When all is said and done, just one line needed changing. Adafruit added the 2.8 to their list of supported displays.
- See [2.8 inch Display](#28-inch-display "2.8 inch Display")

## Software Starting Point - qualia_paint.py and tablegen.py
[Top](#go-big "Top")<br>
I will start from my versions of some things taken from Adafruit libraries as described here in my experiments.
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/README.md#mdo_qualia_paint

I made **mdo_** versions of the Adafruit examples **qualia_paint.py** and **tablegen.py**
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/tree/master/mdo_qualia_paint
- **mdo_tablegen.py** creates a .bin file from any of .jpg, .png or .bmp. The .bin is in exactly the correct format for use on these TFT displays.
- **mdo_qualia_paint.py** reads these .bin files and can swap between them (plus other functionality not used for the SnowGlobe).

The original Adafruit **qualia_paint.py** can be found here:
- https://docs.circuitpython.org/projects/qualia/en/latest/examples.html
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/mdo_qualia_paint/fromAdafruit_examples/qualia_paint__latest_2025-12-19.py

The original Adafruit **tablegen.py** and **hextable.py** can be found here:
- https://github.com/adafruit/Uncanny_Eyes commit d2103e84aa33da9f6924885ebc06d880af8deeff
- https://github.com/Mark-MDO47/expt_AdaFruit_TTL666_display/blob/master/mdo_qualia_paint/fromAdafruit_Uncanny_Eyes/tablegen.py and hextable.py

## Software Changes
[Top](#go-big "Top")<br>
I decided to call these programs **mdo_2.1_round_ornament.py** and **mdo_2.8_round_ornament.py**

### Image File Format
[Top](#go-big "Top")<br>
When I started on **mdo_qualia_paint.py** I used **mdo_tablegen.py** to read an image file (.bmp, .png, .jpg) and create the C-language ***.h** file for the 16-bit RBG 565 format, then read that *.h file in **mdo_qualia_paint.py** and convert it to binary on the board. This took about 2.5 minutes to boot **mdo_qualia_paint.py** even after cropping the left 1/3 of the picture that is used for its controls.

I modified **mdo_tablegen.py** to also create a **.bin** file that is a big-endian version of the data in raw binary. It now takes about 15 seconds to boot **mdo_qualia_paint.py** reading this **.bin** file.

This **mdo_tablegen.py** will work for the Snow Globe project too. Maybe some minor changes...

### Overall Organization
[Top](#go-big "Top")<br>
The program starts running the **main()** routine.<br>
```python
if __name__ == "__main__":
    main()
```

**main()** gets the display hardware initialized and holds several key structures
- **img_565** - a preallocated buffer for RGB 565 pixels, arranged per .bin file which is width-first
  - this will hold the unmodified background image
- **bitmap** - this is the image as displayed. If pixels are filled in here and auto_refresh set to True, it will show on the screen.
- **list_of_bin** - list of .bin files in **pix** directory, sorted alphabetically 
- **G_FLAKE_REGIONS** - list of [x_bgn, x_end, y_bgn, y_end] regions for snowflakes. Size and position are somewhat random.

The primary actions of **main()** are
- load_bitmap() - loads the first background image
- start_snow() - puts "random-sized" snowflakes on "random-locations" in entire range of background image
- while True:
  - if time for this background image has expired, pick next image and do load_bitmap() and start_snow()
  - else do move_snow(), which will refresh snowflakes in top region that hit the bottom. Snowflakes move proportional to linear size (eat your heart out Isaac Newton!).

### Performance
[Top](#go-big "Top")<br>
It still takes 15 seconds to load the **.bin**; I expected longer since we aren't cropping off 1/3 of the picture like mdo_qualia_paint. It takes 25 seconds from power-on but 15 seconds from storing program on USB drive. When looping with a 5 second delay for snow movement it takes 12 seconds, so it seems to take about 7 seconds to actually read .bin, display it, and start snow once the program is initialized.
- This process shows as the snow holding still while reading .bin followed by a sweep across the screen replacing the background image, then appearance of snowflakes.

Maybe I will make **mdo_x.x_round_ornament** not write all the pixels that are not actually on the round display to speed things up. From a visual standpoint, the snow stops moving momentarily and then the image wipes across in about 2 to 3 seconds. Seems to work fine.

On the other hand, the snow movement is definitely jerky compared to the TFT-Gizmo version.

### Memory
[Top](#go-big "Top")<br>
One of the issues with the TFT-Gizmo version that I have not resolved is that if it tries to load background images one after another it will eventually crash from not being to allocate the memory. This was something I wanted to absolutely not allow in this version.

I create the python list - [] - img_565 early on and keep it in scope so we don't fragment RAM by allocating/deallocating it over and over.
- This retains the 16-bit pixel information of the current background image. That will be a handy thing to have around as we move the snow sprites around.
- This seems to be working - no RAM crashes - see below.

#### 01 - Test of Memory Usage Robustness
[Top](#go-big "Top")<br>
My hope is that by starting with this code which is closer to the metal, I can avoid the memory problems I had with the TFT-Gizmo version.
- The problem with debugging the TFT-Gizmo version is my lack of background knowledge in the display routines used. I was just using a shotgun approach to debug it. Admittedly I did find some issues and got it to last through 5 background changes instead of 2, but eventually I just used the reboot option.

With **mdo_qualia_paint** I had never noticed this issue. However, the background switches were manually invoked and I had never tested the limits to see if there was a latent problem.

The file **01_RobustnessTest.py** (an early version of mdo_x.x_round_ornament.py) changes the background every 10 seconds. I ran it for 20 hours and it was still going without a problem.

Now that it is hanging on the tree with snow falling I have not yet seen any indication of a memory problem or other crashing issue.

## Parts List
[Top](#go-big "Top")<br>
| GO BIG Hardware | Description | URL |
| --- | --- | --- |
| Qualia ESP32-S3 RBG-666 40p TFT | Special TFT ESP32-S3 board | https://www.adafruit.com/product/5800 |
| 2.1 inch 480x480 Cap Display | TFT round display 2.1" | https://www.adafruit.com/product/5792 |
| Clear Fillable Ornaments Balls 80mm/3.15" | Clear Plastic DIY Ornament 3.15 inch | https://www.amazon.com/dp/B0CF2GXVSN |
| Itramax Micro USB Extension Cable 20FT (note: flat cable USB-A to USB-C) | USB cable | https://www.amazon.com/dp/B0DFPPSPTW&th=1 |
| USB C Charger Block, Dual Port Type C Wall Charger Fast Charging 20W Power Adapter Cube (note: also has USB-A output) | USB charger | https://www.amazon.com/dp/B0CPSBD68W?th=1 |

Note: even though the **GO BIG** display itself is 2.1 inch there is some device space surrounding the display edge so this ornament ball fits nicely on top of the display. To use the back part of the ornament ball I will have to make a cut and leave the rest of the electronics on the outside. I have ordered some 4 inch ornament balls but they won't be here before Christmas.
- For now I just folded the display and ESP32-S3 over into one-half of the globe with bubble-wrap to maintain electrical isolation, then used foam and tape to hold it in. I thought I had destroyed it but it still worked. Had to pay attention so that the USB connection could be made but it looks surprisingly good!

| GO BIGGER Hardware | Description | URL |
| --- | --- | --- |
| Qualia ESP32-S3 RBG-666 40p TFT | Special TFT ESP32-S3 board | https://www.adafruit.com/product/5800 |
| 2.8 inch 480x480 Cap Display | TFT round display 2.8" | https://www.adafruit.com/product/5852 |
| Clear Fillable Ornaments Balls 90mm | 90,80,70mm plastic DIY ornament 24Pack | https://www.amazon.com/dp/B0FQJL6NLH |
| Option-A: Itramax Micro USB Extension Cable 20FT 2Pack (note: flat cable USB-A to USB-C) | USB cable | https://www.amazon.com/dp/B0DFPPSPTW |
| Option-B: Itramax USB Extension Cable White Flat 10FT 2Pack | USB-A extender cable | https://www.amazon.com/Itramax-Extension-USB-Compatible-Weatherproof/dp/B0DCNJCSS3/?th=1 |
| Option-B: Smays Short 1ft USB C Cable USB A to Type C 20-Pack white | Short USB-A to USB-C cable | https://www.amazon.com/dp/B0DMSPR6XF |
| USB C Charger Block, Dual Port Type C Wall Charger Fast Charging 20W Power Adapter Cube (note: also has USB-A output) | USB charger | https://www.amazon.com/dp/B0CPSBD68W?th=1 |

## First Steps - Factory Reset and Install Circuit Python
[Top](#go-big "Top")<br>
Here is how to configure the Qualia ESP32-S3 for Circuit Python<br>

| Step | Description | URL |
| --- | --- | --- |
| 1 | Factory Reset* | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/factory-reset |
| 2 | Tiny UF2 reload | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/factory-reset |
| 3 | FW Update | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/install-uf2-bootloader |
| 4 | Install CircuitPython | https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/circuitpython-display-setup<br>https://circuitpython.org/board/adafruit_qualia_s3_rgb666/ |
| 5 | Install Library Bundle | https://docs.circuitpython.org/projects/qualia/en/latest/<br>https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/circuitpython-libraries<br>https://circuitpython.org/libraries |

Note *
- Be aware that the "learn" for factory reset says "The Qualia ESP32-S3 microcontroller ships running a circular rainbow gradient example for the round 480x480 display". They are talking about a display such as the 2.1 inch round using the TL021WVC02CT-B1323 controller, not the 2.8 inch round using the TL028WVC01-B1621A controller.
- May need to use the Adafruit WebSerial ESPTool to do Factory Reset and Tiny UF2 reload.
  - https://adafruit.github.io/Adafruit_WebSerial_ESPTool/

After copying entire Adafruit bundle into /lib, there is room for 20 image 480x480 *.bin files in the pix directory.
- Note that if there are 20 *.bin files there and you try to over-write, it will say not enough room. In that case you must delete the file you are going to over-write first, then copy.

| To Know | Where |
| --- | --- |
| UF2 Bootloader details | https://learn.adafruit.com/adafruit-hallowing/uf2-bootloader-details |
| settings.toml file | [settings toml file](#settings-toml-file "settings toml file") |
| USB drive CIRCUITPY is read-only | Linux: (A) eject CIRCUITPY (B) unplug, delay 5 sec, plug-in Qualia |

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

### 2.8 inch Display
[Top](#go-big "Top")<br>
This requires specific setup; see example here (I later found easier ways to do this)
- https://learn.adafruit.com/adafruit-qualia-esp32-s3-for-rgb666-displays/qualia-rgb666-with-tl028wvc01-2-8-round-display
- The above is maybe out of date with latest Circuitpython libraries. It led me down the rabbit hole for about a week.

There is an example pointed to below that shows that ROUND28 is now an available option to Qualia (search for **ROUND28** or **Wed Nov 06, 2024 10:06 am** by adafruit_support_carter
- https://forums.adafruit.com/viewtopic.php?p=1034614&hilit=tl028wvc01+2.8+480x480#p1034614

This means I can use the 2.8 inch display by changing one line. All the magic initialization and usage of a new controller chip are taken care of automagically.

```python
<<<2.1 inch display>>>
    G_GRAPHICS = Graphics(Displays.ROUND21, default_bg=None, auto_refresh=False)
<<<2.8 inch display>>>
    G_GRAPHICS = Graphics(Displays.ROUND28, default_bg=None, auto_refresh=False)
```
