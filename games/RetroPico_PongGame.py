#------------------------------------------------
#  Pong game
#  JPMICHON  06/2026
# Identification de la version du PCB permettant la configuration adéquate certains IOs
RetroPico_PCB_REV = 1.2
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime

WIDTH  = 128
HEIGHT = 64

# devices I2C
_SSD1306 = 0x3C # adresse de l'ecran OLED
_PCF8574AT= 0x20 # adresse du multiplexeur

#
# Configuration des Ports pour le RetroPico 1.x
# Configure les ports en fonction de la revision du PCB
if RetroPico_PCB_REV==1.0:
    # v1.0
    _I2C_SDA = 16 # définition de Data du I2C(0) (GP16)
    _I2C_SCL = 17 # définition de SCL du I2C(0) (GP17)

else:
    # v1.1 and up
    _I2C_SDA = 12 # définition de Data du I2C(0) (GP12)
    _I2C_SCL = 13 # définition de SCL du I2C(0) (GP13)
    

i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
_Buzzer = 6 # définition du  buzzer (GP6)

#initialisation du multiplexeur pour que les boutons fonctionnent
pcf = PCF8574(i2c, address=_PCF8574AT)
# Étape essentielle pour le PCF8574 : écrire des '1' sur les broches en entrée
# pour activer leur fonctionnement en lecture / pull-up interne.
# Masque pour isoler les broches P4, P5, P6
# P4 = 1<<4 (0x10), P5 = 1<<5 (0x20), P6 = 1<<6 (0x40) -> Total = 0x70
pcf.port = 0x70 # activation des pins pour les boutons
    
# Variables
BALL_SIZE = 3 # 2X2 pixels
BALL_SPEED = 1 # permet d'accelerer la balle
PAD_WIDTH = 25 # largeur de la palette
PAD_HEIGHT = 2
PAD_STEP =5
HALF_PAD_WIDTH = int(PAD_WIDTH / 2)
HALF_PAD_HEIGHT = int(PAD_HEIGHT / 2)

# -----------------------------------
# Choisir la résolution du OLED
#
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
#------------------------------------
#
oled.fill(0)
oled.text("RetroPico",30,10)
oled.text("PONG",50,25)
oled.text("-Press key-",20,52)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.show()

NOTES = {
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319, 'SILENCE': 0}
   
def play_game_start():
    buzzer = PWM(Pin(_Buzzer))
    
    # Mélodie dynamique et rythmée qui monte vers une note finale aiguë
    partition = ['DO5', 'MI5', 'SOL5', 'DO5', 'PAUSE', 'DO6']
    tempos = [0.10, 0.10, 0.10, 0.15, 0.05, 0.35]
    
    for note, duree in zip(partition, tempos):
        if note == 'PAUSE':
            frequence = 0
        else:
            frequence = NOTES[note]
        
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        
        # Micro-pause nette pour un effet saccadé et énergique
        buzzer.duty_u16(0)
        utime.sleep(0.01)
        
    buzzer.deinit()
    
def play_game_over():
    buzzer = PWM(Pin(_Buzzer))
    
    # Suite descendante, triste et ralentie sur la fin
    partition = ['MI5', 'RE5', 'DO5', 'SI4', 'PAUSE', 'LA4']
    tempos = [0.15, 0.15, 0.15, 0.25, 0.10, 0.60]
    
    for note, duree in zip(partition, tempos):
        # Gestion de la pause dans la partition
        if note == 'PAUSE':
            frequence = 0
        else:
            frequence = NOTES[note]
        
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)
            utime.sleep(duree)
        
        # Micro-pause entre les notes
        buzzer.duty_u16(0)
        utime.sleep(0.02)
        
    buzzer.deinit()
    
def draw_ball():
    oled.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, 1) 

def WaitAddonBTN():

    while True:
        P4 = pcf.pin(4)
        P5 = pcf.pin(5)
        P6 = pcf.pin(6)
        # Les boutons force la pin a 0 (False) par defaut, ils sont a 1 (True) 
        if not P4 or not P5 or not P6:
            #print("Bouton détecté ! [" + str(P6)+str(P5)+str(P4)+"]") # affichage du status des boutons
            play_game_start()
            break # On sort de la boucle pour continuer le script
        utime.sleep(.2)

    
# attend qu'un bouton soit enfoncé
WaitAddonBTN()

oled.fill(0) # clear screen
utime.sleep(.2)
reading_key=65534
x=64 # set la valeur initial de la position du curseur
# Lance la balle a partir du centre
ball_x = int(WIDTH / 2)
ball_y = int(HEIGHT / 2)
# Initialise le mouvement de la balle
ball_x_dir = 1
ball_y_dir = 1
score=0
GameOver=False

while GameOver==False: #Boucle infini
    oled.fill(0) # clear screen
    oled.rect(0, 0, 1, HEIGHT, 1)
    oled.rect(0, 0, WIDTH, 1, 1)
    oled.rect(WIDTH-1,0 ,1,HEIGHT, 1)
    
    if not pcf.pin(4):
        if x < (WIDTH - PAD_WIDTH/2 -PAD_STEP):  
            x=x+PAD_STEP
    elif not pcf.pin(6):
        if x > (PAD_STEP-PAD_WIDTH/2): 
            x=x-PAD_STEP
        
    oled.fill_rect(x,  62, PAD_WIDTH, PAD_HEIGHT, 1) # dessine la palette
    draw_ball()

    # Déplacement de la balle
    ball_x = ball_x + (ball_x_dir*BALL_SPEED)
    ball_y = ball_y + (ball_y_dir*BALL_SPEED)
    
    # Détection des collisions avec les parois et fait rebondir la balle
    if ball_y < 0:
        ball_y_dir = 1
    if ball_x > WIDTH - 3:
        ball_x_dir = -1
    if ball_x  < 0:
        ball_x_dir = 1       
    
    # Détection de la palette
    if ball_y > 62: # si la balle est au niveau de la palette, je valide s'il y a collision
        if ball_x > x and ball_x < (x+PAD_WIDTH): # si vrai, la palette a touché la balle
            ball_y_dir = -1
            ball_y = ball_y-2
            score=score+1  # j'incrémente le score a chaque rebond sur la palette
        else:
            GameOver=True # partie fini
    BALL_SPEED = (score//10)+1 # a chaque tranche de 10, la balle augmente la vitesse de la balle         
    oled.show() # rafraichi l'image

# si j'arrive ici c'est que la partie est fini
oled.fill(0)
oled.text("Game Over",30,15)
oled.text("Score: " +str(score),30,55)
oled.show()
play_game_over()