import gc
import utime
import micropython
#https://github.com/hakierspejs/pico-vga-driver/tree/master
from vga_Framebuffer import TinyVgaDriver

led = machine.Pin(25, machine.Pin.OUT)
COLOR_RED = 0b1
COLOR_BLACK = 0b0
#vga = TinyVgaDriver(gpio_pin_hsync=2,gpio_pin_vsync=3,gpio_pin_color=5) #Config pour UCompute and VGA Adaptor
vga = TinyVgaDriver(gpio_pin_hsync=21,gpio_pin_vsync=19,gpio_pin_color=18)
#vga.stop_synchronisation()
print(micropython.mem_info())
vga.start_synchronisation()
print(micropython.mem_info())

vga.fbuf.fill(vga.COLOR_BLACK)
utime.sleep_ms(100)
for i in range(4):
        vga.fbuf.fill(vga.COLOR_RED)
        utime.sleep_ms(500)
        print(i)
        vga.fbuf.fill(vga.COLOR_BLACK)
        utime.sleep_ms(500)
        
#vga.fbuf.line(100, 100, 300, 300, COLOR_RED)
#utime.sleep_ms(1000)
vga.fbuf.text('MicroPython!', 1, 10)

utime.sleep_ms(5000)     # CRITICAL: Sleep to allow the background system to breathe
vga.stop_synchronisation()