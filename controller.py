import time
from rpi_ws281x import *
from array import *
import argparse

# LED strip configuration:
LED_COUNT      = 70      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def colorWipe(s, c, p, b):
    """Wipe color across display a pixel at a time."""
    for i in range(s.numPixels()):
        if i % p == 0:
            s.setPixelColor(i, c)
    if b:
        s.show()

def patternWipe(s, c):
    cycle = 0
    for i in range(s.numPixels()):
        if cycle == len(c):
            cycle = 0
        s.setPixelColor(i, c[cycle])
        cycle += 1
    s.show()

def main():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-s', '--rgb', type=str, help='sets the color of strip with an rgb value r,g,b')
    parser.add_argument('-p', '--pattern', type=str, help='sets a pattern on the strip.')
    parser.add_argument('-q', '--colpattern', type=str, help='colored pattern on strip.')
    parser.add_argument('-b', '--brightness', type=str, help='brightness scale.')
    args = parser.parse_args()
    strlist = []
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    if not args.rgb and not args.colpattern:
        print('Please provide either an rgb value or a color pattern')
        exit()

    try:
        if args.rgb:
            strlist = args.rgb.split(',')
        pattern = 1

        if args.pattern:
            pattern = int(args.pattern)

        if not args.colpattern:
            colorWipe(strip, Color(int(strlist[0]), int(strlist[1]), int(strlist[2])), pattern, True)  # Orange
        elif args.colpattern:
            #Split color pattern into individual colors 'r,g,b','r,g,b'
            colors = args.colpattern.split('_')
            cList = [ ]
            convertedColors = [ ]
            #Split each individual color into a substring [[r,g,b],[r,g,b]]
            for i in range(len(colors)):
                cList.append(colors[i].split('*'))
                convertedColors.append(Color(int(cList[i][0]), int(cList[i][1]), int(cList[i][2])))
            patternWipe(strip, convertedColors)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

if __name__ == '__main__':
    main()
