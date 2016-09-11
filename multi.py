from BiblioPixelAnimations.matrix.bloom import Bloom
# from BiblioPixelAnimations.matrix.Text import ScrollText
# from BiblioPixelAnimations.matrix.GameOfLife import GameOfLife, GameOfLifeRGB
# from BiblioPixelAnimations.matrix.opencv_video import OpenCVVideo
# from BiblioPixelAnimations.matrix.perlin_simplex import PerlinSimplex
# from BiblioPixelAnimations.matrix.ScreenGrab import ScreenGrab
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE
from bibliopixel import LEDMatrix
import bibliopixel.colors as colors
from bibliopixel import MultiMapBuilder, mapGen
import bibliopixel.log as log
import time

log.setLogLevel(log.DEBUG)

w = 128
h = 32
dCount = 3
d_order = [1, 2, 3]

build = MultiMapBuilder()
drivers = []
for i in range(dCount):
    build.addRow(mapGen(w, h, serpentine=False))
    drivers.append(DriverSerial(LEDTYPE.GENERIC, w * h,
                                hardwareID="16C0:0483", deviceID=d_order[i]))

led = LEDMatrix(drivers, width=w, height=h * dCount, coordMap=build.map,
                threadedUpdate=True, masterBrightness=128)

# anim = GameOfLife(led, color=colors.Red, bg=colors.Off, toroidal=False)
# anim = OpenCVVideo(led, videoSource=None, mirror=True,
#                    offset=0.0, crop=True, useVidFPS=False)
# anim = ScreenGrab(led, bbox=[0, 0 + 52, 640, 480 + 52],
#                   mirror=False, offset=0.0, crop=True)

anim = Bloom(led)
try:
    anim.run(amt=6, fps=10)
except:
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
