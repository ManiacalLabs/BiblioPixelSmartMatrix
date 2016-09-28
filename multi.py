from BiblioPixelAnimations.matrix.bloom import Bloom
from BiblioPixelAnimations.matrix.Text import ScrollText, BounceText
from BiblioPixelAnimations.matrix.GameOfLife import GameOfLife, GameOfLifeRGB, GameOfLifeClock
from BiblioPixelAnimations.matrix.opencv_video import OpenCVVideo
from BiblioPixelAnimations.matrix.perlin_simplex import PerlinSimplex
from BiblioPixelAnimations.matrix.ScreenGrab import ScreenGrab
from BiblioPixelAnimations.matrix.LangtonsAnt import LangtonsAnt
from BiblioPixelAnimations.matrix.AnalogClock import AnalogClock
from BiblioPixelAnimations.matrix.ImageAnim import ImageAnim
from BiblioPixelAnimations.matrix.kimotion import Kimotion
from bibliopixel.drivers.serial_driver import DriverTeensySmartMatrix
from bibliopixel import LEDMatrix
import bibliopixel.colors as colors
from bibliopixel import MultiMapBuilder, mapGen
import bibliopixel.log as log
import time
from bibliopixel import font

log.setLogLevel(log.DEBUG)

w = 128
h = 32
dCount = 3
d_order = [10, 11, 12]

build = MultiMapBuilder()
drivers = []
for i in range(dCount):
    build.addRow(mapGen(w, h, serpentine=False))
    drivers.append(DriverTeensySmartMatrix(width=w, height=h, deviceID=d_order[i]))

led = LEDMatrix(drivers, width=w, height=h * dCount, coordMap=build.map,
                threadedUpdate=True, masterBrightness=128)

# anim = GameOfLife(led, color=colors.Red, bg=colors.Off, toroidal=False)
# anim = LangtonsAnt(led, antColor=colors.Green, pathColor=colors.Red)
# anim = OpenCVVideo(led, videoSource=None, mirror=True,
#                    offset=0.0, crop=True, useVidFPS=False)
# anim = ScreenGrab(led, bbox=[0 + 81, 0 + 52, 320 + 81, 240 + 52],
#                   mirror=False, offset=0.0, crop=True)

# anim = AnalogClock(led, aa=True)
anim = Bloom(led)
# anim = PerlinSimplex(led, freq=128, octaves=1, type=True)
# anim = ImageAnim(led, "G:/GitHub/AnimatedGifs/32x32", offset=(0, 0), bgcolor=colors.Off, brightness=255, cycles=1, random=True)
# anim = Kimotion(led, server="10.0.1.133:1337", mirror=True, crop=True, shader="Sandstorm",
#                 min_z=440, max_z=1100,
#                 near_color=[229, 107, 0], near_z=760,
#                 mid_color=[40, 0, 114],
#                 far_color=[2, 2, 12], far_z=1100)
# text = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
# anim = ScrollText(led, text, xPos=64, yPos=0, color=colors.Red, bgcolor=colors.Off,
#                   font_name='16x8', font_scale=2)
# anim = GameOfLifeClock(led, font_name='8x6', mil_time=False)
# anim = BounceText(led, "Hello Awesome!", xPos=64, yPos=40, color=colors.Red, font_name='16x8', font_scale=1)
try:
    anim.run(amt=6, fps=15)
except:
    raise
finally:
    anim.cleanup()
    time.sleep(1)
    led.all_off()
    led.update()
    time.sleep(1)
    led.all_off()
    led.update()


# try:
#     anim = Bloom(led)
#     anim.run(amt=6, fps=10)
# except:
#     time.sleep(1)
#     led.all_off()
#     led.update()
#     time.sleep(1)
#     led.all_off()
#     led.update()
#
# #anim = ScrollText(led, "Maniacal Labs Rules!", xPos = 128, yPos = 0, color = colors.Red, bgcolor = colors.Off, size = 4)
# # try:
# #     anim.run(amt=6, fps=30)
# # finally:
# #     led.all_off()
# #     led.update()
# #     time.sleep(1)
# #
# # led.all_off()
# # led.update()
# # time.sleep(1)
# # led.all_off()
# # led.update()
# # time.sleep(1)
