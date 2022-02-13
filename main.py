#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

CHAIN_MOTOR_PCT = 90
LOADINGDOCK_MOTOR_PCT = -80

# Init the EV3 brick
ev3 = EV3Brick()

# Init motors
loadingDockMotor = Motor(Port.A)
chainMotorFront = Motor(Port.B)
chainMotorBack = Motor(Port.C)

# Init sensors
loadingDockSensor = ColorSensor(Port.S1)
# loadingDockSensor._mode('COL-REFLECT')
# chainSensor = LightSensor(Port.S2)
# chainSensor = InfraredSensor(Port.S2)
chainSensor = LightSensor(Port.S2)
# chainSensor._mode('REFLECT')

# Init the stopwatch
loadingDockTimer = StopWatch()
# sensorCheckTimer = StopWatch()

# Play a sound
ev3.speaker.beep(100)

loadingDockFull = False
trainLeftLoadingDock = False
trainWaitingAtFrontHill = False

# Start the loading dock motor
loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)

# Start the chain motors
chainMotorBack.dc(CHAIN_MOTOR_PCT)
chainMotorFront.dc(CHAIN_MOTOR_PCT)

# Get the beginning distance for the chain sensor
# chainSensorStartingValue = chainSensor.distance()
chainSensorStartingValue = chainSensor.ambient()
dockSensorStartingValue = loadingDockSensor.ambient()

while True:
    # loadingDockColorValue = loadingDockSensor.color()
    loadingDockAmbientValue = loadingDockSensor.ambient()
    # chainSensorValue = chainSensor.distance()
    chainSensorValue = chainSensor.ambient()

    # print('LoadingDock Color: ', loadingDockColorValue)
    # print('Chain Ambient Start: ', chainSensorStartingValue)
    # print('Chain Ambient: ', chainSensorValue)
    # print('Chain Sensor: ', chainSensorValue)
    # print('loadingDockFull', loadingDockFull)
    # print('Timer:', loadingDockTimer.time(), 'ms')
    # sensorCheckTimer.reset()

    # Determine if a train has entered loading dock
    # if loadingDockColorValue != Color.BLACK and loadingDockFull == False:
    if loadingDockAmbientValue < (dockSensorStartingValue-5) and loadingDockFull == False:
        wait(400)
        loadingDockMotor.stop()
        # chainMotorFront.dc(CHAIN_MOTOR_PCT)
        loadingDockTimer.reset()
        loadingDockFull = True
        ev3.speaker.beep(200)
        wait(50)
        ev3.speaker.beep(200)

    # After 10 seconds of a train being in the loading dock, release it
    if loadingDockTimer.time() >= 10000 and loadingDockFull == True:
        # Restart the loading dock motor
        loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)
        ev3.speaker.beep(600)
        loadingDockFull = False
        trainLeftLoadingDock = True
        wait(5000)

    if chainSensorValue < (chainSensorStartingValue-10) and trainLeftLoadingDock == False:
        chainMotorFront.stop()
        trainWaitingAtFrontHill = True

    if trainWaitingAtFrontHill == True and trainLeftLoadingDock == True:
        chainMotorFront.dc(CHAIN_MOTOR_PCT)
        wait(10000) # Give the train time to pass the sensor on the hill
        trainLeftLoadingDock = False
        trainWaitingAtFrontHill = False

    # if chainSensorValue < chainSensorStartingValue:
    #     if loadingDockFull == False:
    #         chainMotorFront.stop()
    #     else:
    #         # Restart the loading dock motor
    #         loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)
    #         ev3.speaker.beep(600)
    #         wait(1000)
    #         # ev3.speaker.beep(600)
    #         loadingDockFull = False

    # Wait a bit in between each cycle of code
    wait(10)
