from pyA20.gpio import gpio, port
from orangepwm import *
import time as tm
import database as db

carId = 1

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
def move(leftSpeed, rightSpeed):
	""" 
		Forward: value > 0 (max 100)
		Reverse: value < 0 (min -100)
		Brake: value == 0
	"""
	leftPwm.changeDutyCycle(abs(leftSpeed))
	rightPwm.changeDutyCycle(abs(rightSpeed))
	
	if leftSpeed > 0:
		gpio.output(leftForwardPin, True)
		gpio.output(leftReversePin, False)
	elif leftSpeed == 0:
		gpio.output(leftForwardPin, False)
		gpio.output(leftReversePin, False)
	else:
		gpio.output(leftForwardPin, False)
		gpio.output(leftReversePin, True)
	
	if rightSpeed > 0:
		gpio.output(rightForwardPin, True)
		gpio.output(rightReversePin, False)
	elif rightSpeed == 0:
		gpio.output(rightForwardPin, False)
		gpio.output(rightReversePin, False)
	else:
		gpio.output(rightForwardPin, False)
		gpio.output(rightReversePin, True)


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
data = db.getData(carId)
move(data["leftspeed"], data["rightspeed"])

while True:
	newData = db.getData(carId)

	if data["leftspeed"] != newData["leftspeed"] or data["rightspeed"] != newData["rightspeed"]:
		move(newData["leftspeed"], newData["rightspeed"])
		data = newData
	
	db.updateData(newData.update({
		"leftlinesensor": readLineSensors()[0], 
		"rightlinesensor": readLineSensors()[1], 
		"ultrasonicsensor": readUltrasonicSensor()
	}))
