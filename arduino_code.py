# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:17:39 2022

@author: cfgar
"""

from m5stack import *
import machine, os, time

import os
import time

class M5Stack : 
    def __init__(self, output, frequency, time_between_pulse):
        self.output = output
        self.pwm = machine.PWM(self.output)

        self.frequency = frequency
        self.pwm.freq(self.frequency)
        self.time_between_pulse = time_between_pulse

        lcd.clear()
        lcd.font(lcd.FONT_DejaVu18)
        lcd.text(0, 0,"Le script est lance")
        lcd.text(0, 20,'La sortie pwm est '+str(self.output))
        lcd.text(0, 40,"La frequence pwm est " + str(self.frequency))
        lcd.text(0, 60,"Le temps entre deux signaux est " + str(self.time_between_pulse))
        
    def signal_encoding(self, source, repetition):
        self.repetition=repetition
        lcd.text(0, 100,"Le signal sera répété " + str(self.repetition) +" fois")
        text_file = open(source, 'r')
        encodage = text_file.read().split(',')

        for j in range(repetition) :
            for i in range(len(encodage)) :
                if (i%2) == 0 :
                    self.pwm.duty(0)
                    time.sleep(self.time_between_pulse)
                self.pwm.duty(float(encodage[i]))
                time.sleep(self.time_between_pulse)

M5 = M5Stack(21,1500,7/1500)
M5.signal_encoding('./encodage.txt', 100000)