import RPi.GPIO as GPIO
import time
import datetime
import urllib2
import urllib
from firebase import firebase
firebase=firebase.FirebaseApplication('https://raspberrypi/**************************************')
GPIO.setmode(GPIO.BOARD)
n=0
controlpin=[7,11,13,15]
for pin in controlpin:
GPIO.setup(pin,GPIO.OUT)
GPIO.output(pin,0)
seq=[[1,0,0,0],
[1,1,0,0],
[0,1,0,0],
[0,1,1,0],
[0,0,1,0],
[0,0,1,1],
[0,0,0,1],
[1,0,0,1]]
sensor=16
buzzer=18
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,False)
dat=raw_input("input")
while(1):
print('checking')
y= datetime.datetime.now()
y=str(y)
y=y[11:16]
y=y.replace(':','')
if(y==dat):
for i in range(116):
for halfstep in range(8):
for pin in range(4):
GPIO.output(controlpin[pin],seq[halfstep][pin])
time.sleep(0.001)
n=n+1
result1=firebase.put('med_disp',n,y)
result2=firebase.put('med_disp','date',y)
take=firebase.get('/med_disp/number of medicine left',None)
#print(take)
#take=take[1:3]
take=int(take)
no_of_med=take-1
result3=firebase.put('med_disp','number of medicine left',no_of_med)
try:
while True:
if GPIO.input(sensor) != 1:
GPIO.output(buzzer,True)
print ("Object Detected")
else:
GPIO.output(buzzer,False)
break
except KeyboardInterrupt:
GPIO.cleanup()
time.sleep(60)
