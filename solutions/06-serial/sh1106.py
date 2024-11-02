"""
MicroPython module for I2C OLED display with SH1106 driver.

Components:
- ESP32-based board
- OLED display with SH1106 driver

Authors:
- Shujen Chen et al. Raspberry Pi Pico Interfacing and Programming with MicroPython
- MicroPython SH1106 OLED driver, I2C and SPI interfaces
- Tomas Fryza

Creation date: 2023-10-27
Last modified: 2024-11-02
"""

from machine import Pin
from machine import I2C
import framebuf
import utime as time


class SH1106_I2C(framebuf.FrameBuffer):
    DEV_ADDR = 0x3c
    WIDTH = 128
    HEIGHT = 64
    PAGES = HEIGHT // 8
    LOW_COLUMN_ADDR = 0x00
    HIGH_COLUMN_ADDR = 0x10
    PAGE_ADDRESS = 0xb0

    def __init__(self, i2c, width=WIDTH, height=HEIGHT, addr=DEV_ADDR):
        self.i2c = i2c
        self.addr = addr
        self._sh1106_init()
        self.buffer = bytearray(self.PAGES * self.WIDTH)
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)

    def write_cmd(self, cmd):
        """Write a byte of command to SH1106"""
        self.i2c.writeto(self.DEV_ADDR, bytearray([0x80, cmd]))

    def write_data(self, data):
        """Write a databuffer to SH1106"""
        self.i2c.writeto(self.DEV_ADDR, b"\x40"+data)

    def poweron(self):
        self.write_cmd(0xaf)

    def poweroff(self):
        self.write_cmd(0xae)

    def sleep(self, value):
        self.write_cmd(0xae | (not value))

    def contrast(self, val):
        self.write_cmd(0x81)
        self.write_cmd(val)

    def show(self):
        (w, p, buf) = (self.WIDTH, self.PAGES, self.buffer)
        for page in range(0, p):
            self.write_cmd(self.PAGE_ADDRESS | page)
            self.write_cmd(self.LOW_COLUMN_ADDR | 2)
            self.write_cmd(self.HIGH_COLUMN_ADDR | 0)
            # print(f"Updating page {page}")
            self.write_data(buf[(w*page):(w*page+w)])

    def _sh1106_init(self):
        """Initialize SH1106"""
        INIT_SEQ = (
            0xae,        # Turn off oled panel
            0x00,        # Set low column address
            0x10,        # Set high column address
            0x40,        # Set start line address
            0x20, 0x02,  # Page addressing mode
            0xc8,        # Top-down segment (4th segment)
            0x81,        # Set contrast control register
            0xcf, 0xa1,  # Set segment re-map 95 to 0
            0xa6,        # Set normal display
            0xa8,        # Set multiplex ratio(1 to 64)
            0x3f,        # 1/64 duty
            0xd3, 0x00,  # Set display offset: none
            0xd5,
            0x80,
            0xd9,
            0xf1, 0xda,
            0x12, 0xdb,
            0x40, 0x8d,
            0x14,
            0xaf         # Turn on oled panel
        )
        time.sleep_ms(100)

        for cmd in INIT_SEQ:
            self.write_cmd(cmd)


def demo():
    # Init I2C using pins GP22 & GP21 (default I2C0 pins)
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
    print(f"I2C configuration : {str(i2c)}")

    # Init OLED display
    oled = SH1106_I2C(i2c)
    oled.sleep(False)
    oled.contrast(100)
    oled.fill(0)

    # Add some text
    oled.text("Using OLED and", 0, 40)
    oled.text("ESP32", 50, 50)

    # Draw the logo
    # https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
    oled.fill_rect(0, 0, 32, 32, 1)
    oled.fill_rect(2, 2, 28, 28, 0)
    oled.vline(9, 8, 22, 1)
    oled.vline(16, 2, 22, 1)
    oled.vline(23, 8, 22, 1)
    oled.fill_rect(26, 24, 2, 4, 1)
    oled.text("MicroPython", 40, 0)
    oled.text("Brno, CZ", 40, 12)
    oled.text("RadioElect.", 40, 24)

    # Binary icon
    icon = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0]]
    # Copy icon to OLED display position pixel-by-pixel
    pos_x, pos_y = 100, 50
    for j, row in enumerate(icon):
        for i, val in enumerate(row):
            oled.pixel(i+pos_x, j+pos_y, val) 

    # Finally update the OLED display so the text is displayed
    oled.show()
    
    print("Check the OLED screen")


if __name__ == "__main__" :
    # Code that runs only if this script is executed directly
    demo()
