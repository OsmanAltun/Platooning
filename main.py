from pyA20.gpio import gpio, port
from orangepwm import *
import time as tm

# motor speed pins
leftPwmPin = port.PA12
rightPwmPin = port.PA11

# motor direction pins
leftForwardPin = port.PG7
leftReversePin = port.PG6
rightForwardPin = port.PA0
rightReversePin = port.PA1

# ultrasonic sensor pins
triggerPin = port.PA15 # output
echoPin = port.PA16 # input

# line sensor pins
leftLineSensorPin = port.PA13
rightLineSensorPin = port.PA10

# initialize gpio library
gpio.init()

# motor configuration
gpio.setcfg(leftForwardPin, gpio.OUTPUT)
gpio.setcfg(leftReversePin, gpio.OUTPUT)
gpio.setcfg(rightForwardPin, gpio.OUTPUT)
gpio.setcfg(rightReversePin, gpio.OUTPUT)
leftPwm = OrangePwm(500, leftPwmPin)
rightPwm = OrangePwm(500, rightPwmPin)
leftPwm.start(0)
rightPwm.start(0)

# ultrasonic sensor configuration
gpio.setcfg(triggerPin, gpio.OUTPUT)
gpio.setcfg(echoPin, gpio.INPUT)

# line sensor configuration
gpio.setcfg(leftLineSensorPin, gpio.INPUT)
gpio.setcfg(rightLineSensorPin, gpio.INPUT)



# functions

def forward(leftSpeed, rightSpeed):
	"""
		Function sets speed of both dc motors and drives forward.

		Args:
		  leftSpeed: A number between 0 and 100
		  rightSpeed: A number between 0 and 100
	"""
	leftPwm.changeDutyCycle(leftSpeed)
	rightPwm.changeDutyCycle(rightSpeed)
	gpio.output(leftForwardPin, True)
	gpio.output(leftReversePin, False)
	gpio.output(rightForwardPin, True)
	gpio.output(rightReversePin, False)

def reverse(leftSpeed, rightSpeed):
	"""
		Function sets speed of both dc motors and drives backward.

		Args:
			leftSpeed: A number between 0 and 100
			rightSpeed: A number between 0 and 100
	"""
	leftPwm.changeDutyCycle(leftSpeed)
	rightPwm.changeDutyCycle(rightSpeed)
	gpio.output(leftForwardPin, False)
	gpio.output(leftReversePin, True)
	gpio.output(rightForwardPin, False)
	gpio.output(rightReversePin, True)

def brake():
	"""Function stops the motors"""
	#leftPwm.changeDutyCycle(0)
	#rightPwm.changeDutyCycle(0)
	gpio.output(leftForwardPin, False)
	gpio.output(leftReversePin, False)
	gpio.output(rightForwardPin, False)
	gpio.output(rightReversePin, False)

def readUltrasonicSensor():
	"""
		Function reads ultrasonic sensor

		Returns:
			Distance in meters
	"""
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

def readLineSensors():
	"""
		Function reads line sensors

		Returns:
			A tuple containing booleans
	"""
	return gpio.input(leftLineSensorPin), gpio.input(rightLineSensorPin)




# main loop

while True:
	tm.sleep(1)
	if all(x==1 for x in readLineSensors()):
		forward(50, 50)
	else:
		brake()

