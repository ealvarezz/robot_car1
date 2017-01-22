""" This is a string """

# pylint: disable=C0121
# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable-msg=E0611
# pylint: disable=maybe-no-member

import time
import numpy as np
import RPi.GPIO as gpio

quater_turn = 0.32
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

def check_distance():
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


def get_correct_dist():
    while True:
        crct_distance = check_distance()
        if crct_distance < 1000:
            break

    print "Distance: ", crct_distance
    return crct_distance

def scan():
    dist_list = []
    stop()
    dist_list.append(get_correct_dist())
    pivot_left(0.14)
    stop()
    dist_list.append(get_correct_dist())
    pivot_left(0.14)
    stop()
    dist_list.append(get_correct_dist())
    pivot_left(0.14)
    stop()
    dist_list.append(get_correct_dist())
    pivot_left(0.14)
    stop()
    dist_list.append(get_correct_dist())
    np_list = np.array(dist_list)

    max_index = np_list.argmax()
    print "Maximum index: ", max_index, "\n"
    if dist_list[max_index] <= 40:
        return False
    multiplier = 4 - max_index
    pivot_right(0.14 * multiplier)
    stop()
    return True

def completeScan():
    print "Seems to be stuck, scanning...\n"
    pivot_right(quater_turn)
    if scan():
        return

    print "Crap! still stuck, 360 time!"
    print "Scanning again ..."
    scan()

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

def pivot_left(val):
    gpio.output(input1, True)
    gpio.output(input2, False)
    gpio.output(input3, False)
    gpio.output(input4, True)
    time.sleep(val)
    forward()

def pivot_right(val):
    gpio.output(input1, False)
    gpio.output(input2, True)
    gpio.output(input3, True)
    gpio.output(input4, False)
    time.sleep(val)
    forward()

def stop():
    gpio.output(input1, False)
    gpio.output(input2, False)
    gpio.output(input3, False)
    gpio.output(input4, False)
    time.sleep(0.1)

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
        distance = check_distance()

        if distance <= 40:
            turn_lv4_on()
            if distance <= 30:
                backwards()
                time.sleep(0.2)
                completeScan()
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
