import RPi.GPIO as GPIO
import time

from gpiozero import DistanceSensor
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

duty_cycle = 0
LED = 7
Taster = 5

Motor1_PWM = 18
Motor1_IN1 = 17
Motor1_IN2 = 22

Motor2_PWM = 19
Motor2_IN1 = 24
Motor2_IN2 = 4

#SR04
trigger=25
echo=27

sensor = DistanceSensor(echo=27, trigger=25)


def M1_forward():
    GPIO.output(Motor1_IN2,GPIO.LOW)
    GPIO.output(Motor1_IN1,GPIO.HIGH)
    
def M1_backward():
    GPIO.output(Motor1_IN1,GPIO.LOW)
    GPIO.output(Motor1_IN2,GPIO.HIGH)

def M2_forward():
    GPIO.output(Motor2_IN2,GPIO.LOW)
    GPIO.output(Motor2_IN1,GPIO.HIGH)
    
def M2_backward():
    GPIO.output(Motor2_IN1,GPIO.LOW)
    GPIO.output(Motor2_IN2,GPIO.HIGH)
    
def straight(): #function to move straight forward
    while( sensor.distance * 100 > 40):
       print("Distance: ",sensor.distance*100, "cm")
       GPIO.output(LED, GPIO.HIGH)
       PWM_1.ChangeDutyCycle(100)
       M1_forward()
       PWM_2.ChangeDutyCycle(80)    # for rotor staright move not use 100
       M2_forward()
       time.sleep(0.175)
       PWM_1.ChangeDutyCycle(0)
       PWM_2.ChangeDutyCycle(0)
       time.sleep(0.175)
       GPIO.output(LED, GPIO.LOW)
       if (sensor.distance * 100 < 40):
           back()

def back():  #function to take a small reverse to turn
   if (sensor.distance*100 < 40):
       print("Distance: ",sensor.distance*100, "cm")
       PWM_1.ChangeDutyCycle(30)
       M1_backward()
       PWM_2.ChangeDutyCycle(30)
       M2_backward()
       time.sleep(0.5)
       PWM_1.ChangeDutyCycle(0)
       PWM_2.ChangeDutyCycle(0)
       time.sleep(0.175)
       turn()
       
def turn():  #function to turn either left or right
    while(sensor.distance *100 <40):
     print("Distance: ",sensor.distance*100, "cm")
     GPIO.output(LED, GPIO.HIGH)

     PWM_1.ChangeDutyCycle(25)        #turn right
     M1_forward()
     PWM_2.ChangeDutyCycle(0)
     M2_forward()
     time.sleep(0.7)                  #angle 90 degree rotate

     PWM_1.ChangeDutyCycle(0)
     PWM_2.ChangeDutyCycle(0)
     time.sleep(0.175)
     
     if (sensor.distance *100 < 40):  #if wrong direction turned
        PWM_1.ChangeDutyCycle(0)      #turn left
        M1_forward()
        PWM_2.ChangeDutyCycle(25)
        M2_forward()
        time.sleep(1.31)              #angle 180 degree rotate
            
        PWM_1.ChangeDutyCycle(0)
        PWM_2.ChangeDutyCycle(0)
        time.sleep(0.175)             
     
    straight()
          
    
GPIO.setup(Motor1_IN1,GPIO.OUT)
GPIO.setup(Motor1_IN2,GPIO.OUT)
GPIO.setup(Motor1_PWM,GPIO.OUT)
PWM_1 = GPIO.PWM(Motor1_PWM, 90) #GPIO als PWM mit Frequenz 90Hz
PWM_1.start(0) #Duty Cycle = 0

GPIO.setup(Motor2_IN1,GPIO.OUT)
GPIO.setup(Motor2_IN2,GPIO.OUT)
GPIO.setup(Motor2_PWM,GPIO.OUT)
PWM_2 = GPIO.PWM(Motor2_PWM, 90) #GPIO als PWM mit Frequenz 90Hz
PWM_2.start(0) #Duty Cycle = 0

GPIO.setup(LED, GPIO.OUT)

d = sensor.distance * 100

if (d< 40):
    back()
    
else:
    straight()