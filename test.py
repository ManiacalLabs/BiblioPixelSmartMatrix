from BiblioPixelAnimations.matrix.bloom import Bloom
from BiblioPixelAnimations.matrix.Text import ScrollText
from bibliopixel.drivers.serial_driver import *
import time

w = 128
h = 32
driver = DriverSerial(LEDTYPE.GENERIC, w * h, hardwareID="16C0:0483", dev="")

import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

import bibliopixel.colors as colors

# load the LEDStrip class
from bibliopixel.led import *
led = LEDMatrix(driver, width=w, height=h,
                serpentine=False, threadedUpdate=False)


#load channel test animation
# from bibliopixel.animation import MatrixCalibrationTest
# anim = MatrixCalibrationTest(led)
# anim.run(fps=30)

try:
    anim = Bloom(led)
    anim.run(amt=6, fps=30)
except:
    led.all_off()
    led.update()
    time.sleep(1)
    led.all_off()
    led.update()

#anim = ScrollText(led, "Maniacal Labs Rules!", xPos = 128, yPos = 0, color = colors.Red, bgcolor = colors.Off, size = 4)
# try:
#     anim.run(amt=6, fps=30)
# finally:
#     led.all_off()
#     led.update()
#     time.sleep(1)
#
# led.all_off()
# led.update()
# time.sleep(1)
# led.all_off()
# led.update()
# time.sleep(1)
