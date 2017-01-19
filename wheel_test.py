""" This is a string """

# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable-msg=E0611
# pylint: disable=maybe-no-member

import time
import random
import RPi.GPIO as gpio

input1 = 11
input2 = 13
input3 = 15
input4 = 16
led_pin1 = 37
led_pin2 = 31
led_pin3 = 35
led_pin4 = 36
trigger_pin = 18
echo_pin = 22
distance = 0

gpio.setmode(gpio.BOARD)
gpio.setup(input1, gpio.OUT)
gpio.setup(input2, gpio.OUT)
gpio.setup(input3, gpio.OUT)
gpio.setup(input4, gpio.OUT)
gpio.setup(led_pin1, gpio.OUT)
gpio.setup(led_pin2, gpio.OUT)
gpio.setup(led_pin3, gpio.OUT)
gpio.setup(led_pin4, gpio.OUT)
gpio.setup(trigger_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
gpio.output(trigger_pin, False)

def get_distance():
    gpio.output(trigger_pin, True)
    time.sleep(0.00001)
    gpio.output(trigger_pin, False)
    start = time.time()
    end = start

    while gpio.input(echo_pin) == 0:
        start = time.time()
        end = start

    while gpio.input(echo_pin) == 1:
        end = time.time()

    total_duration = end - start
    dist = (total_duration * 34300) / 2
    dist = round(dist, 2)

    print "Distance: ", dist
    return dist

def backwards():
    gpio.output(input1, True)
    gpio.output(input2, False)
    gpio.output(input3, True)
    gpio.output(input4, False)

def forward():
    gpio.output(input1, False)
    gpio.output(input2, True)
    gpio.output(input3, False)
    gpio.output(input4, True)

def pivot_left():
    gpio.output(input1, True)
    gpio.output(input2, False)
    gpio.output(input3, False)
    gpio.output(input4, True)
    time.sleep(0.4)
    forward()

def pivot_right():
    gpio.output(input1, False)
    gpio.output(input2, True)
    gpio.output(input3, True)
    gpio.output(input4, False)
    time.sleep(0.4)
    forward()

def turn_lv1_on():
    gpio.output(led_pin1, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin4, gpio.LOW)
    time.sleep(0.1)
    gpio.output(led_pin3, gpio.LOW)
    time.sleep(0.1)
    gpio.output(led_pin2, gpio.LOW)
    time.sleep(0.1)

def turn_lv2_on():
    gpio.output(led_pin1, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin2, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin4, gpio.LOW)
    time.sleep(0.1)
    gpio.output(led_pin3, gpio.LOW)
    time.sleep(0.1)

def turn_lv3_on():
    gpio.output(led_pin1, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin2, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin3, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin4, gpio.LOW)
    time.sleep(0.1)

def turn_lv4_on():
    gpio.output(led_pin1, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin2, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin3, gpio.HIGH)
    time.sleep(0.1)
    gpio.output(led_pin4, gpio.HIGH)
    time.sleep(0.1)

def turn_all_off():
    gpio.output(led_pin4, gpio.LOW)
    time.sleep(0.1)
    gpio.output(led_pin3, gpio.LOW)
    time.sleep(0.1)
    gpio.output(led_pin2, gpio.LOW)
    time.sleep(0.1)
    gpio.output(led_pin1, gpio.LOW)
    time.sleep(0.1)

forward()

try:
    while True:
        time.sleep(0.5)
        distance = get_distance()

        if distance <= 40:
            turn_lv4_on()
            if distance <= 30:
                if random.randint(0, 1):
                    pivot_right()
                    forward()
                else:
                    pivot_left()
                    forward()
        elif distance <= 55:
            turn_lv3_on()
        elif distance <= 65:
            turn_lv2_on()
        elif distance <= 75:
            turn_lv1_on()
        else:
            turn_all_off()

except KeyboardInterrupt:
    print "Key has been noticed."

finally:
    gpio.cleanup()
