#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import datetime
import os
import sys

# Configuration
FAN_PIN = 21  # BCM pin used to drive transistor's base
WAIT_TIME = 2  # [s] Time to wait between each refresh
FAN_MIN = 25  # [%] Fan minimum speed.
PWM_FREQ = 25  # [Hz] Change this value if fan has strange behavior

# Configurable temperature and fan speed steps
tempSteps = [0, 40, 44, 45, 48, 50]  # [°C]
speedSteps = [0, 50, 63, 70, 85, 100]  # [%]

# Fan speed will change only of the difference of temperature is higher than hysteresis
hyst = 1

# Setup GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
fan.start(0)

i = 0
cpuTemp = 0
fanSpeed = 0
cpuTempOld = 0
fanSpeedOld = 0

# We must set a speed value for each temperature step
if len(speedSteps) != len(tempSteps):
    print("Numbers of temp steps and speed steps are different")
    exit(0)

filename = os.path.join("/","home","pi","Private","logs","fancontrol", "log.txt")
second_threshold = 5
countseconds = 0
try:
    while 1:
        # Read CPU temperature
        cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
        cpuTemp = float(cpuTempFile.read()) / 1000
        cpuTempFile.close()

        # Calculate desired fan speed
        if abs(cpuTemp - cpuTempOld) > hyst:
            if countseconds < second_threshold:
                countseconds += 1

                if os.path.exists(filename):
                    append_write = 'a' # append if already exists
                else:
                    append_write = 'w' # make a new file if not

                f = open(filename, append_write)
                f.write(str(datetime.datetime.now()) +" | Waiting for seconds to pass: "+ str(countseconds) +" \n\r")
                f.close()
                
                continue
            else:
                countseconds = 0
             
            # Below first value, fan will run at min speed.
            if cpuTemp < tempSteps[0]:
                fanSpeed = speedSteps[0]
            # Above last value, fan will run at max speed
            elif cpuTemp >= tempSteps[len(tempSteps) - 1]:
                fanSpeed = speedSteps[len(tempSteps) - 1]

            # Else set fan speed in steps
            else:
                for i in range(0, len(tempSteps) - 1):
                    if(cpuTemp >= tempSteps[len(tempSteps)-1-i]):
                        fanSpeed = speedSteps[len(tempSteps)-1-i]
                        break
                   

            if fanSpeed != fanSpeedOld:
                if (fanSpeed != fanSpeedOld
                        and (fanSpeed >= FAN_MIN or fanSpeed == 0)):
                    fan.ChangeDutyCycle(fanSpeed)
                    fanSpeedOld = fanSpeed

                    # filename = os.path.join(os.path.abspath(os.getcwd()), "log.txt")
                    print(filename)
                    if os.path.exists(filename):
                        append_write = 'a' # append if already exists
                    else:
                        append_write = 'w' # make a new file if not

                    f = open(filename, append_write)
                    f.write(str(datetime.datetime.now()) +" | Changing FanSpeed: CpuTemp: "+ str(cpuTemp) +", FanSpeed: "+str(fanSpeed)+"\n\r")
                    f.close()
            cpuTempOld = cpuTemp

        # Wait until next refresh
        time.sleep(WAIT_TIME)


# If a keyboard interrupt occurs (ctrl + c), the GPIO is set to 0 and the program exits.
except KeyboardInterrupt:
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
