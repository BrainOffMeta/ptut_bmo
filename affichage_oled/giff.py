#!/usr/bin/env python3
from PIL import Image
import ST7789
import time
import sys

print("""
shapes.py - Display test shapes on the LCD using PIL.

If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the front slot.

Usage: {} <display_type>

Where <display_type> is one of:

  * square - 240x240 1.3" Square LCD
  * round  - 240x240 1.3" Round LCD (applies an offset)
  * rect   - 240x135 1.14" Rectangular LCD (applies an offset)
  * dhmini - 320x240 2.0" Display HAT Mini
""".format(sys.argv[0]))

try:
    display_type = sys.argv[1]
except IndexError:
    display_type = "square"

# Create ST7789 LCD display class.

if display_type in ("square", "rect", "round"):
    disp = ST7789.ST7789(
        height=135 if display_type == "rect" else 240,
        rotation=0 if display_type == "rect" else 90,
        port=0,
        cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=9,
        backlight=19,               # 18 for back BG slot, 19 for front BG slot.
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0 if display_type == "square" else 40,
        offset_top=53 if display_type == "rect" else 0
    )

elif display_type == "dhmini":
    disp = ST7789.ST7789(
        height=240,
        width=320,
        rotation=180,
        port=0,
        cs=1,
        dc=9,
        backlight=13,
        spi_speed_hz=60 * 1000 * 1000,
        offset_left=0,
        offset_top=0
   )

else:
    print ("Invalid display type!")

# Initialize display.
disp.begin()

width = disp.width
height = disp.height

# Load an image.
print('Loading gif: {}...'.format(image_file))
image = Image.open(image_file)

print('Drawing gif, press Ctrl+C to exit!')

frame = 0

while True:
    try:
        image.seek(frame)
        disp.display(image.resize((width, height)))
        frame += 1
        time.sleep(0.05)

    except EOFError:
        frame = 0
