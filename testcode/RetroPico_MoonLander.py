#------------------------------------------------
#  Moon lander game
#               v1.0
#  JPMICHON  06/2026
# Identification de la version du PCB permettant la configuration adéquate certains IOs
RetroPico_PCB_REV = 1.2
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime
import math
import random

# variables permettant de tweeker le jeux 
Lander_X=50 # position initiale du lander
Lander_Y=8 # position initiale du lander
veloch=0 #Velocité horizontal initial
velocv=0 #Velocité vertical initial
Fuel=20 # réserve de carburant initial
trust_power=0.3 #puissance du moteur
gravity=0.10 # gravité de la planete
landingpad_X=0 # localiation du landing pad
WIDTH  = 128
HEIGHT = 64
# adresse des deivice I2C
_SSD1306 = 0x3C 
_PCF8574AT= 0x20 

if RetroPico_PCB_REV==1.0:
    _I2C_SDA = 16 
    _I2C_SCL = 17 
else:
    _I2C_SDA = 12 
    _I2C_SCL = 13 

i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
_Buzzer = 6 

pcf = PCF8574(i2c, address=_PCF8574AT)
pcf.port = 0x70 
# -----------------------------------
# Choisir la résolution du OLED
#
oled = SSD1306_I2C(128, 64, i2c)
#------------------------------------
#
NOTES = {
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319, 'SILENCE': 0}
   
def play_game_start():
    buzzer = PWM(Pin(_Buzzer))
    partition = ['DO5', 'MI5', 'SOL5', 'DO5', 'PAUSE', 'DO6']
    tempos = [0.10, 0.10, 0.10, 0.15, 0.05, 0.35]
    for note, duree in zip(partition, tempos):
        frequence = 0 if note == 'PAUSE' else NOTES[note]
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(0.01)
    buzzer.deinit()
    
def play_victory():
    buzzer = PWM(Pin(_Buzzer))
    # Mélodie triomphante, rapide et ascendante
    partition = ['DO5', 'DO5', 'DO5', 'DO5', 'PAUSE', 'SOL4', 'LA4', 'DO5', 'PAUSE', 'LA4', 'DO5']
    tempos = [0.10, 0.10, 0.10, 0.30, 0.05, 0.15, 0.15, 0.15, 0.05, 0.15, 0.50]
    
    for note, duree in zip(partition, tempos):
        frequence = 0 if note == 'PAUSE' else NOTES[note]
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(0.02)
    buzzer.deinit()
    
def play_game_over():
    buzzer = PWM(Pin(_Buzzer))
    partition = ['MI5', 'RE5', 'DO5', 'SI4', 'PAUSE', 'LA4']
    tempos = [0.15, 0.15, 0.15, 0.25, 0.10, 0.60]
    for note, duree in zip(partition, tempos):
        frequence = 0 if note == 'PAUSE' else NOTES[note]
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(0.02)
    buzzer.deinit()
    
def WaitAddonBTN():
    while True:
        if not pcf.pin(4) or not pcf.pin(5) or not pcf.pin(6):
            play_game_start()
            break 
        utime.sleep(.2)
        
def circle(x,y,r,color,fill=0):       #A circular function
    if(fill==0):
            for i in range(x-r,x+r+1):
                oled.pixel(i,int(y-math.sqrt(r*r-(x-i)*(x-i))),color)
                oled.pixel(i,int(y+math.sqrt(r*r-(x-i)*(x-i))),color)
            for i in range(y-r,y+r+1):
                oled.pixel(int(x-math.sqrt(r*r-(y-i)*(y-i))),i,color)
                oled.pixel(int(x+math.sqrt(r*r-(y-i)*(y-i))),i,color)
    else:
            for i in range(x-r,x+r+1):
                a=int(math.sqrt(r*r-(x-i)*(x-i)))
                oled.vline(i,y-a,a*2,color)

            for i in range(y-r,y+r+1):
                a=int(math.sqrt(r*r-(y-i)*(y-i)))
                oled.hline(x-a,i,a*2,color)
                
def draw_lander(x,y,trust):
    oled.rect(x, y, 16, 4, 1)
    oled.rect(x+3, y-4, 10, 4, 1)
    oled.line(x, y+3, x-2, y+6, 1)
    oled.line(x+15, y+3, x+16, y+6, 1)
    if trust==1:
        flame=random.randint(0, 1) #tire un chiffre au hazard afin de produire l'animation de la flamme
        if flame==0:
            oled.line(x+6, y+6, x+8, y+12, 1)
            oled.line(x+10, y+6, x+8, y+12, 1)
        elif flame==1:
            oled.line(x+6, y+6, x+8, y+14, 1)
            oled.line(x+10, y+6, x+8, y+14, 1)
 
def draw_gauge(level):
    if level<0.1:
        oled.text("Vide", 0,0)
    else:
        oled.line(3,20,3,20-int(level),1)
        oled.line(4,20,4,20-int(level),1)
        oled.line(3,20,6,20,1)
    oled.text('E',0,22)
        
# affiche l'écran d'acceuil
oled.fill(0)
oled.text("RetroPico",30,10)
oled.text("MoonLander",25,25)
oled.text("-Press key-",20,52)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.show()
# attend qu'un bouton soit enfoncé
WaitAddonBTN()
play_game_start()
oled.fill(0) # clear screen
utime.sleep(.2)
oled.show()


landingpad_X=random.randint(1, WIDTH-25)
# main loop 
while Lander_Y<HEIGHT-12:
    oled.fill(0) # clear screen
    animation=0
    oled.rect(landingpad_X, HEIGHT-2, 25, 2, 1) # dessine le landing pad
    
    if not pcf.pin(4):
        if Fuel>0: 
            veloch=veloch+trust_power
            Fuel=Fuel-(trust_power/2) # les thrusters latteraux consomme moins
    elif not pcf.pin(6):
        if Fuel>0:
            veloch=veloch-trust_power
            Fuel=Fuel-(trust_power/2) # les thrusters latteraux consomme moins
    elif not pcf.pin(5):
        if Fuel>0:
            velocv=velocv-trust_power
            Fuel=Fuel-trust_power
            animation=1 #fait apparaitre la flame
    velocv=velocv + gravity # effet de gravité     
    Lander_Y=int(Lander_Y+velocv) # effet de gravité  
    Lander_X=int(Lander_X+veloch)
    # boucle de doite a gauche
    if Lander_X> WIDTH:
        Lander_X=0
    elif Lander_X<1:
        Lander_X=WIDTH
    if Lander_Y < 4: # empeche de sortir de l'écran vers le haut
       Lander_Y =4
       velocv=0
    draw_lander(Lander_X,Lander_Y,animation)
    draw_gauge(Fuel)
    oled.show()
if velocv > 1.4 or veloch > 0.5 or Lander_X<landingpad_X-2 or Lander_X>landingpad_X+8:  # detection des conditions de crash
    # Crash!
    circle(Lander_X+6,Lander_Y-8,6,1,fill=1)
    oled.show()
    circle(Lander_X+12,Lander_Y-18,4,1,fill=1)
    oled.show()
    circle(Lander_X+15,Lander_Y-26,2,1,fill=1)
    oled.show()
    oled.text('KABOOM!',50,10)
    oled.show()
    play_game_over()
else:
    # Landed!
    oled.fill(0) # clear screen
    oled.text('HOURRA!',40,25)
    oled.text('Pointage:'+str(int(Fuel)),15,45) # le pointage est le carburant restant
    oled.show()
    play_victory()
