from pyA20.gpio import gpio, port
from orangepwm import *
import time as tm

# setup

# pins for controlling motor speed
leftPwmPin = port.PA12
rightPwmPin = port.PA11

# pins for controlling motor direction
leftForwardPin = port.PG7
leftReversePin = port.PG6
rightForwardPin = port.PA0
rightReversePin = port.PA1

# pins for communication with the ultrasonic sensor
triggerPin = port.PA15 # output
echoPin = port.PA16 # input

# gpio configuration
gpio.init()
gpio.setcfg(leftForwardPin, gpio.OUTPUT)
gpio.setcfg(leftReversePin, gpio.OUTPUT)
gpio.setcfg(rightForwardPin, gpio.OUTPUT)
gpio.setcfg(rightReversePin, gpio.OUTPUT)
gpio.setcfg(triggerPin, gpio.OUTPUT)
gpio.setcfg(echoPin, gpio.INPUT)
leftPwm = OrangePwm(500, leftPwmPin)
rightPwm = OrangePwm(500, rightPwmPin)
leftPwm.start(0)
rightPwm.start(0)

# functions

def forward(leftSpeed, rightSpeed):
	leftPwm.changeDutyCycle(leftSpeed)
	rightPwm.changeDutyCycle(rightSpeed)
	gpio.output(leftForwardPin, True)
	gpio.output(leftReversePin, False)
	gpio.output(rightForwardPin, True)
	gpio.output(rightReversePin, False)

def reverse(leftSpeed, rightSpeed):
	leftPwm.changeDutyCycle(leftSpeed)
	rightPwm.changeDutyCycle(rightSpeed)
	gpio.output(leftForwardPin, False)
	gpio.output(leftReversePin, True)
	gpio.output(rightForwardPin, False)
	gpio.output(rightReversePin, True)

def brake():
	leftPwm.changeDutyCycle(0)
	rightPwm.changeDutyCycle(0)
	gpio.output(leftForwardPin, False)
	gpio.output(leftReversePin, False)
	gpio.output(rightForwardPin, False)
	gpio.output(rightReversePin, False)

def distance():
	gpio.output(triggerPin, gpio.HIGH)
	tm.sleep(0.01)
	gpio.output(triggerPin, gpio.LOW)

	while gpio.input(echoPin) == gpio.LOW:
		pass
	oldTime = tm.time()
	while gpio.input(echoPin) == gpio.HIGH:
		pass
	deltaTime = tm.time() - oldTime
	return deltaTime/2 * 343

# main loop

while True:
	tm.sleep(1)
	print(distance())
	pass

