"""An example script that uses the functionality of robot_kit"""
from robot_kit.leds import NeoPixelStrip
from robot_kit.ultrasonic import Ultrasonic
import time


def clamp(color):
    """Clamp the color between 0 and 255"""
    return max(0, min(color, 255))


def range_color(distance, inverse=True):
    """Return the color based on the given range"""
    if inverse:
        return clamp(50-distance)
    else:
        return clamp(distance)


if __name__ == '__main__':
    """Run some of the basic commands for robot_kit"""

    # Create the LED strip class
    led_strip = NeoPixelStrip()

    # Get the distance from the Ultrasonic sensor
    dis_sensor = Ultrasonic()
    for i in range(50):
        distance = dis_sensor.get_distance()
        red = range_color(distance)
        green = range_color(distance, inverse=False)
        print(distance, red, green)
        led_strip.on(red, green, 0)
        time.sleep(0.25)

    # Okay all done so turn the LED strip off
    led_strip.off()
