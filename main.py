#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

CHAIN_MOTOR_PCT = 90
LOADINGDOCK_MOTOR_PCT = 60

# Init the EV3 brick
ev3 = EV3Brick()

# Init motors
chainMotor = Motor(Port.A)
loadingDockMotor = Motor(Port.B)

# Init sensors
loadingDockSenor = ColorSensor(Port.S1)
# loadingDockSenor._mode('COL-REFLECT')
# chainSensor = ColorSensor(Port.S2)
# chainSensor._mode('REFLECT')

# Init the stopwatch
loadingDockTimer = StopWatch()

# Play a sound
ev3.speaker.beep()

loadingDockFull = False

# Start the loading dock motor
loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)

while True:
    # Start the chain motor
    # chainMotor.dc(CHAIN_MOTOR_PCT)

    # If loading dock sensor changes to desired value, stop the loading dock motor
    colorVal1 = loadingDockSenor.color()
    print('Color: ', colorVal1)
    print('loadingDockFull', loadingDockFull)
    print('Timer:', loadingDockTimer.time(), 'ms')
    wait(500)

    if colorVal1 != Color.BLACK and loadingDockFull == False:
        loadingDockMotor.stop()
        loadingDockFull = True
        loadingDockTimer.reset()

    if loadingDockTimer.time() >= 10000:
        # Restart the loading dock motor
        loadingDockMotor.dc(LOADINGDOCK_MOTOR_PCT)
        wait(10000)
        loadingDockFull = False




