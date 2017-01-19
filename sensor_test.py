""" This is a string """

# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable-msg=E0611
# pylint: disable=maybe-no-member

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
output_pin1 = 11
output_pin2 = 13
output_pin3 = 15
output_pin4 = 16
trigger_pin = 18
echo_pin = 22
GPIO.setup(output_pin1, GPIO.OUT)
GPIO.setup(output_pin2, GPIO.OUT)
GPIO.setup(output_pin3, GPIO.OUT)
GPIO.setup(output_pin4, GPIO.OUT)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.output(trigger_pin, False)
time.sleep(2)


def turn_lv1_on():
    GPIO.output(output_pin1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin4, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(output_pin3, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(output_pin2, GPIO.LOW)
    time.sleep(0.1)

def turn_lv2_on():
    GPIO.output(output_pin1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin2, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin4, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(output_pin3, GPIO.LOW)
    time.sleep(0.1)

def turn_lv3_on():
    GPIO.output(output_pin1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin2, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin3, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin4, GPIO.LOW)
    time.sleep(0.1)

def turn_lv4_on():
    GPIO.output(output_pin1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin2, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin3, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(output_pin4, GPIO.HIGH)
    time.sleep(0.1)

def turn_all_off():
    GPIO.output(output_pin4, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(output_pin3, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(output_pin2, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(output_pin1, GPIO.LOW)
    time.sleep(0.1)

try:
    while True:
        time.sleep(0.5)
        GPIO.output(trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, False)
        start = time.time()
        end = start

        while GPIO.input(echo_pin) == 0:
            start = time.time()
            end = start

        while GPIO.input(echo_pin) == 1:
            end = time.time()

        total_duration = end - start
        distance = (total_duration * 34300) / 2
        distance = round(distance, 2)

        if distance <= 5:
            turn_lv4_on()
        elif distance <= 15:
            turn_lv3_on()
        elif distance <= 35:
            turn_lv2_on()
        elif distance <= 70:
            turn_lv1_on()
        else:
            turn_all_off()

        print "Distance: ", distance

except KeyboardInterrupt:
    print "Key has been noticed."

finally:
    GPIO.cleanup()
