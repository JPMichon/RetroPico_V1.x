#------------------------------------------------
#  Breakout
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
    
# Variables de jeu
BALL_SIZE = 3 
BALL_SPEED = 1 
PAD_WIDTH = 25 
PAD_HEIGHT = 2
PAD_STEP = 5

# Configuration des briques
BRICK_ROWS = 3
BRICK_COLS = 7
BRICK_WIDTH = 16
BRICK_HEIGHT = 4
BRICK_PADDING = 2
BRICK_OFFSET_X = 2
BRICK_OFFSET_Y = 10

# Génération de la matrice de briques [y][x] -> 1 = présente, 0 = détruite
bricks = [[1 for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)]

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Écran d'accueil
oled.fill(0)
oled.text("RetroPico", 30, 10)
oled.text("BREAKOUT", 32, 25)
oled.text("-Press key-", 20, 52)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.show()

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

def play_brick_hit():
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(NOTES['SOL5'])
    buzzer.duty_u16(16384)
    utime.sleep(0.05)
    buzzer.deinit()

def draw_ball():
    oled.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, 1) 

def draw_bricks():
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            if bricks[row][col] == 1:
                bx = BRICK_OFFSET_X + col * (BRICK_WIDTH + BRICK_PADDING)
                by = BRICK_OFFSET_Y + row * (BRICK_HEIGHT + BRICK_PADDING)
                oled.fill_rect(bx, by, BRICK_WIDTH, BRICK_HEIGHT, 1)

def WaitAddonBTN():
    while True:
        if not pcf.pin(4) or not pcf.pin(5) or not pcf.pin(6):
            play_game_start()
            break 
        utime.sleep(.2)

# Attente du démarrage
WaitAddonBTN()

oled.fill(0) 
utime.sleep(.2)

x = 52 # Position initiale de la palette
ball_x = int(WIDTH / 2)
ball_y = 40  # Commencer sous les briques
ball_x_dir = 1
ball_y_dir = -1  # Lancer vers le haut
score = 0
GameOver = False
Victory = False

while not GameOver and not Victory:
    oled.fill(0) 
    
    # Murs extérieurs
    oled.rect(0, 0, 1, HEIGHT, 1)
    oled.rect(0, 0, WIDTH, 1, 1)
    oled.rect(WIDTH-1, 0, 1, HEIGHT, 1)
    
    # Lecture des boutons pour la palette
    if not pcf.pin(4):
        if x < (WIDTH - PAD_WIDTH - 2):  
            x = x + PAD_STEP
    elif not pcf.pin(6):
        if x > 2: 
            x = x - PAD_STEP
        
    # Affichage des éléments
    oled.fill_rect(x, 60, PAD_WIDTH, PAD_HEIGHT, 1) 
    draw_bricks()
    draw_ball()

    # Déplacement de la balle
    ball_x = ball_x + (ball_x_dir * BALL_SPEED)
    ball_y = ball_y + (ball_y_dir * BALL_SPEED)
    
    # Collisions avec les murs
    if ball_x > WIDTH - BALL_SIZE - 1:
        ball_x_dir = -1
        ball_x = WIDTH - BALL_SIZE - 1
    if ball_x < 1:
        ball_x_dir = 1       
        ball_x = 1
    if ball_y < 1:
        ball_y_dir = 1
        ball_y = 1
    
    # Collision avec les briques
    remaining_bricks = 0
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            if bricks[row][col] == 1:
                remaining_bricks += 1
                bx = BRICK_OFFSET_X + col * (BRICK_WIDTH + BRICK_PADDING)
                by = BRICK_OFFSET_Y + row * (BRICK_HEIGHT + BRICK_PADDING)
                
                # Vérification de la boîte de collision overlap
                if (ball_x + BALL_SIZE >= bx and ball_x <= bx + BRICK_WIDTH and
                    ball_y + BALL_SIZE >= by and ball_y <= by + BRICK_HEIGHT):
                    
                    bricks[row][col] = 0 # Détruire la brique
                    score += 10
                    play_brick_hit()
                    
                    # Inversion de direction simple
                    ball_y_dir = -ball_y_dir
                    
                    # Sortir de la boucle pour éviter de détruire plusieurs briques à la fois
                    break 
        else:
            continue
        break

    if remaining_bricks == 0:
        Victory = True

    # Collision avec la palette
    if ball_y + BALL_SIZE >= 60: 
        if ball_x + BALL_SIZE >= x and ball_x <= x + PAD_WIDTH:
            ball_y_dir = -1
            ball_y = 60 - BALL_SIZE
        else:
            if ball_y > HEIGHT:
                GameOver = True 
                
    # Vitesse progressive selon les briques cassées
    BALL_SPEED = (score // 100) + 1         
    oled.show()

# Fin de partie
oled.fill(0)
if Victory:
    oled.text("VICTOIRE !", 25, 15)
else:
    oled.text("Game Over", 30, 15)

oled.text("Score: " + str(score), 30, 40)
oled.show()
play_game_over()
