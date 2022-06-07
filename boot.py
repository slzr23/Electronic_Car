#ESP32 Micropython Car Control 

#Made by SLZR, to a group of students of St Marie Highschool, with a big help by J.D Leroy (teacher)

import socket
import machine
import time
from machine import Pin, PWM, ADC, time_pulse_us
from time import sleep, sleep_us, sleep_ms

#Initialisation du r茅seau local sur la carte 
####################################################################
wifissid="yourwifiSSID"                                     
wifipass="yourwifiPassword" 
####################################################################

try:
  ENA.deinit()
except:
  pass
try:
  ENB.deinit()
except:
  pass
  
  
#ENA et ENB servent 脿 g茅rer l'amplitude de la tension d茅livr茅e au moteur 
ENA=PWM(Pin(14)) #Pin sur lequel ENA est branch茅
ENA.freq(1024)
ENB=PWM(Pin(18)) #Pin sur lequel ENB est branch茅 
ENB.freq(1024)

IN1 = Pin(26,Pin.OUT) #moteur 1
IN2 = Pin(25,Pin.OUT) #moteur 1
IN3 = Pin(2,Pin.OUT) #moteur 2
IN4 = Pin(4,Pin.OUT) #moteur 2

#initialisation des diff茅rents niveaux de vitesse de la voiture 
minSpeed = 300 #Vitesse 1
midSpeed = 700 #Vitesse 2
maxSpeed = 1000 #Vitesse 3
speed = midSpeed #Notre vitesse de base quand nous demanderont 脿 la voiture d'avancer sera Vitesse 2
action = 0 #on d茅finit une variable action qui servira plus tard 

#Print de d茅coration dans la console
print('/*----- Ouverture du panneau de controle: -----*/')
print(' ______ _           _                   _         _____ \n|  ____| |         | |                 (_)       / ____|\n| |__  | | ___  ___| |_ _ __ ___  _ __  _  ___  | |     __ _ _ __ \n|  __| | |/ _ \/ __| __|  __/ _ \|  _ \| |/ __| | |    / _` |  __| \n| |____| |  __/ (__| |_| | | (_) | | | | | (__  | |___| (_| | |  \n|______|_|\___|\___|\__|_|  \___/|_| |_|_|\___|  \_____\__,_|_|\n  ')


def setMotor(MotorPin, val):

  print('duty',val)
  MotorPin.duty(val)
  print('finsetmot:',MotorPin)

#Partie HTML: Panneau de controle, il est envoy茅 au navigateur de l'user qui tape l'IP dans son moteur de recherche 
html = """<!DOCTYPE html>
<html>
  <head>
    <title>Panneau de controle Electronic Car</title>
<h1>Panneau de Controle <b>Electronic Car </b> </h1>
<style>
body {background-color: black;
      font-family: monospace; 
      }
h1 {color:white;
    text-align: center; 
    font-size: :30px; 
}

h2 {color: white;} 
button {
        color: white;
        height: 200px;
        width: 200px;
        background:black;
        border: 3px solid #E60202; /* Green */
        border-radius: 50%;
        font-size: 200%;
        font-family: monospace;
        position: center;
}
</style>
</head>
<body>
  <center>
    <form>
      <h2><u>Direction</u></h2>
      <button name="CMD" value="forward" type="submit">Avancer</button>
      <div>
        <button name="CMD" value="left" type="submit">Gauche</button>
        <button name="CMD" value="stop" type="submit">STOP</button>
         <button name="CMD" value="right" type="submit">Droite</button>
      </div>
      <div>
        <button name="CMD" value="back" type="submit">Reculer</button>
      </div>
      <h2><u>Vitesse</u></h2>
      <div>
        <button name="CMD" value="slow" type="submit">Lent</button>
        <button name="CMD" value="mid" type="submit">Normal</button>
        <button name="CMD" value="fast" type="submit">Rapide</button>
    </form>
  </center>
</body>
</html>
"""

#Fonctions de direction de la voiture 

def stop(t=0):
  print('Arret des moteurs: ')
  print('Arret du moteur A')
  ENA.duty(0)
  print(ENA)
  print('Arret du moteur B')
  ENB.duty(0)
  print('pwm ok')
  IN1.value(0)
  IN2.value(0)
  IN3.value(0)
  IN4.value(0)
  print('in1234 ,ok')
  if t > 0 :
    sleep_ms(t)

def forward(t=0):
  global ENA,ENB
  ENA.duty(speed)
  print(speed)
  IN1.value(1)
  IN2.value(0)
  ENB.duty(speed)
  print(speed)
  IN3.value(1)
  IN4.value(0)
  print(ENA,ENB)
  if t > 0 :
    sleep_ms(t)


def back(t=0):
  global ENA,ENB
  ENA.duty(speed)
  print(speed)
  IN1.value(0)
  IN2.value(1)
  ENB.duty(speed)
  print(speed)
  IN3.value(0)
  IN4.value(1)
  print(ENA,ENB)
  if t > 0 :
    sleep_ms(t)



def left (t=0):
  
  global ENA,ENB
  ENA.duty(speed)
  print(speed)
  IN1.value(0)
  IN2.value(1)
  ENB.duty(speed)
  print(speed)
  IN3.value(1)
  IN4.value(0)
  print(ENA,ENB)
  if t > 0 :
    sleep_ms(t)


def right (t=0):
  
  global ENA,ENB
  ENA.duty(speed)
  print(speed)
  IN1.value(1)
  IN2.value(0)
  ENB.duty(speed)
  print(speed)
  IN3.value(0)
  IN4.value(1  )
  print(ENA,ENB)
  if t > 0 :
    sleep_ms(t)



def left_cruise (t=0):
  setMotor(IN1, 0)
  setMotor(IN2, 0)
  setMotor(IN3, speed)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)

def right_cruise (t=0):
  setMotor(IN1, speed)
  setMotor(IN2, 0)
  setMotor(IN3, 0)
  setMotor(IN4, 0)
  if t > 0 :
    sleep_ms(t)


def remoteControl () :
    global auto, s, action, speed
    conn, addr = s.accept()
    print("Signal per莽u depuis %s" % str(addr))
    request = conn.recv(1024)
    print("Requete = %s" % str(request))
    request = str(request)

    if request.find('/?CMD=forward') == 6: 
        print('+La voiture avance')
        action = 1
    elif request.find('/?CMD=back') == 6: 
        print('+La voiture recule')
        action = 2
    elif request.find('/?CMD=left') == 6: 
        print('+La voiture tourne 脿 gauche')
        action = 3
    elif request.find('/?CMD=right') == 6:  
        print('+La voiture tourne 脿 droite')
        action = 4
    elif request.find('/?CMD=l') == 6:
        print('+L')
        action = 5
    elif request.find('/?CMD=r') == 6:
        print('+R')
        action = 6
    elif request.find('/?CMD=stop') == 6: 
        print('+stop')
        action = 0
    elif request.find('/?CMD=fast') == 6: 
        print('+fast=')
        speed = maxSpeed
        print (speed)
    elif request.find('/?CMD=slow') == 6: 
        print('+slow=')
        speed = minSpeed
        print (speed)
    elif request.find('/?CMD=mid') == 6:  
        print('+mid=')
        speed = midSpeed
        print (speed)
    elif request.find('/?CMD=man') == 6:
        auto=False
        action = 0
        print('+manual=')
    elif request.find('/?CMD=auto') == 6:
        auto=True
        action = 0
        print('+autoDrive')
    
    
    if action == 0:
        stop()
    elif action == 1:
        forward()
    elif action == 2:
        back()
    elif action == 3:
        left()
    elif action == 4:
        right()
    elif action == 5:
        left_cruise()
    elif action == 6:
        right_cruise()

    response = html
    conn.send(response)
    conn.close()

def autoDrive():
  print("fonction auto")
stop()

import network

# Connexion de l'appareil au r茅seau wifi 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifissid,wifipass)
count = 7
while not wifi.isconnected() and count > 0 : #chargement 
    count -= 1
    print ('.')
    time.sleep(1)

if wifi.isconnected() :
    print('Configuration du r茅seau: ', wifi.ifconfig())
    #Configuration du Socket WebServer
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()


    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(('', 80))
    s.listen(5)
    print("Vous pouvez d茅sormais vous connecter 脿 l'IP de la voiture")
else  :
    print('No Wifi. Auto Mode')
    auto = True


while True:

    if auto :
        autoDrive()
    elif wifi.isconnected()  :
        remoteControl()






