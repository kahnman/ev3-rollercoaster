#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
# from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

CHAIN_MOTOR_PCT = 90
LOADINGDOCK_MOTOR_PCT = -80

# Init the EV3 brick
ev3 = EV3Brick()

# Init motors
chainMotor = Motor(Port.A)
loadingDockMotor = Motor(Port.B)

# Init sensors
loadingDockSenor = ColorSensor(Port.S1)
# loadingDockSenor._mode('COL-REFLECT')
# chainSensor = LightSensor(Port.S2)
chainSensor = InfraredSensor(Port.S2)
# chainSensor._mode('REFLECT')

# Init the stopwatch
loadingDockTimer = StopWatch()
sensorCheckTimer = StopWatch()

# Play a sound
ev3.speaker.beep()

loadingDockFull = False
trainEnteringLoadingDock = False

# Start the loading dock motor
loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)

while True:
    # Start the chain motor
    # chainMotor.dc(CHAIN_MOTOR_PCT)

    loadingDockColorValue = loadingDockSenor.color()
    print('LoadingDock Color: ', loadingDockColorValue)

    # loadingDockReflectionColorValue = loadingDockSenor.reflection()

    # chainSensorValue = chainSensor.distance()

    # If loading dock sensor changes to desired value, stop the loading dock motor
    # if sensorCheckTimer.time() >= 1000:

    # print('Chain Sensor: ', chainSensorValue)
    # print('loadingDockFull', loadingDockFull)
    # print('Timer:', loadingDockTimer.time(), 'ms')
    sensorCheckTimer.reset()

    # train entering loading dock
    if trainEnteringLoadingDock == False and loadingDockColorValue != Color.BLACK:
        trainEnteringLoadingDock = True

    if trainEnteringLoadingDock == True and loadingDockColorValue == Color.BLACK:
        ev3.speaker.beep()
        print('LoadingDock Color: ', loadingDockColorValue)

        loadingDockFull = True
        loadingDockTimer.reset()
        trainEnteringLoadingDock = False
        # wait(50)
        loadingDockMotor.stop()

    # if loadingDockColorValue != Color.BLACK and loadingDockFull == False:
    #     loadingDockMotor.stop()
    #     loadingDockFull = True
    #     loadingDockTimer.reset()

    if loadingDockTimer.time() >= 10000:
        # Restart the loading dock motor
        loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)
        wait(10000)
        loadingDockFull = False

    # Wait a bit in between each cycle of code
    wait(100)
