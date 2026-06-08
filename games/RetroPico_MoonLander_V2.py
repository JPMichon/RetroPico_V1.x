#------------------------------------------------
#  Moon lander game - Graphiquement Amélioré
#               v2.0
#  JPMICHON   06/2026
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime
import math
import random

RetroPico_PCB_REV = 1.2

# Configuration des variables de jeu
Lander_X = 50 
Lander_Y = 6 
veloch = 0 
velocv = 0 
Fuel = 30 # Augmenté légèrement pour compenser le terrain
trust_power = 0.25 
gravity = 0.08 
WIDTH = 128
HEIGHT = 64

_SSD1306 = 0x3C 
_PCF8574AT = 0x20 

if RetroPico_PCB_REV == 1.0:
    _I2C_SDA = 16 
    _I2C_SCL = 17 
else:
    _I2C_SDA = 12 
    _I2C_SCL = 13 

i2c = I2C(0, sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
_Buzzer = 6 

pcf = PCF8574(i2c, address=_PCF8574AT)
pcf.port = 0x70 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

NOTES = {
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319, 'SILENCE': 0}

def play_sound(partition, tempos, gap=0.01):
    buzzer = PWM(Pin(_Buzzer))
    for note, duree in zip(partition, tempos):
        frequence = 0 if note == 'PAUSE' else NOTES.get(note, 0)
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(16384)
            utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(gap)
    buzzer.deinit()

def play_game_start():
    play_sound(['DO5', 'MI5', 'SOL5', 'DO5', 'PAUSE', 'DO6'], [0.1, 0.1, 0.1, 0.15, 0.05, 0.35])
    
def play_victory():
    play_sound(['DO5', 'DO5', 'DO5', 'DO5', 'PAUSE', 'SOL4', 'LA4', 'DO5', 'PAUSE', 'LA4', 'DO5'], 
               [0.1, 0.1, 0.1, 0.3, 0.05, 0.15, 0.15, 0.15, 0.05, 0.15, 0.5])
    
def play_game_over():
    play_sound(['MI5', 'RE5', 'DO5', 'SI4', 'PAUSE', 'LA4'], [0.15, 0.15, 0.15, 0.25, 0.1, 0.6])
    
def WaitAddonBTN():
    while True:
        if not pcf.pin(4) or not pcf.pin(5) or not pcf.pin(6):
            break 
        utime.sleep(0.1)

def circle(x, y, r, color, fill=0):
    if fill == 0:
        for i in range(x - r, x + r + 1):
            if 0 <= i < WIDTH:
                d = r*r - (x - i)*(x - i)
                if d >= 0:
                    sq = int(math.sqrt(d))
                    if 0 <= y - sq < HEIGHT: oled.pixel(i, y - sq, color)
                    if 0 <= y + sq < HEIGHT: oled.pixel(i, y + sq, color)
    else:
        for i in range(x - r, x + r + 1):
            if 0 <= i < WIDTH:
                d = r*r - (x - i)*(x - i)
                if d >= 0:
                    a = int(math.sqrt(d))
                    oled.vline(i, max(0, y - a), min(HEIGHT - 1, y + a) - max(0, y - a) + 1, color)

def draw_lander(x, y, thrust):
    # Capsule principale (Design adouci)
    oled.fill_rect(x + 3, y, 10, 5, 1)
    oled.rect(x + 4, y - 3, 8, 3, 1) # Hublot supérieur
    # Train d'atterrissage
    oled.line(x + 3, y + 5, x, y + 8, 1)
    oled.line(x + 12, y + 5, x + 15, y + 8, 1)
    oled.hline(x - 1, y + 8, 3, 1)
    oled.hline(x + 14, y + 8, 3, 1)
    # Flamme animée du moteur
    if thrust == 1:
        h = random.randint(5, 10)
        oled.line(x + 6, y + 5, x + 8, y + 5 + h, 1)
        oled.line(x + 9, y + 5, x + 8, y + 5 + h, 1)

# Génération dynamique du terrain lunaire
terrain = [0] * WIDTH
landingpad_X = random.randint(10, WIDTH - 35)
pad_width = 25
pad_height = HEIGHT - 6

def generate_terrain():
    # Crée une surface montagneuse fluide
    seed = random.uniform(0, 10)
    for x in range(WIDTH):
        if x >= landingpad_X and x < landingpad_X + pad_width:
            terrain[x] = pad_height
        else:
            # Combinaison d'ondes pour un look rocheux naturel
            height_offset = int(10 * math.sin(x * 0.05 + seed) + 4 * math.cos(x * 0.15))
            terrain[x] = HEIGHT - 8 + height_offset
            if terrain[x] < HEIGHT - 20: terrain[x] = HEIGHT - 20

def draw_terrain():
    for x in range(WIDTH):
        oled.vline(x, terrain[x], HEIGHT - terrain[x], 1)
    # Mettre en valeur la zone de d'atterrissage (ligne plate doublée)
    oled.hline(landingpad_X, pad_height, pad_width, 1)
    oled.hline(landingpad_X, pad_height + 1, pad_width, 1)

def draw_hud(fuel, v_speed):
    # Barre supérieure stylisée pour les statistiques
    oled.rect(0, 0, WIDTH, 10, 1)
    # Affichage du carburant numérique + mini barre de progression
    pct = max(0, min(100, int((fuel / 30) * 100)))
    oled.text("F:{}%".format(pct), 3, 1, 1)
    # Affichage de la vitesse verticale
    oled.text("V:{:.1f}".format(abs(v_speed)), 80, 1, 1)

# Écran d'accueil stylisé
oled.fill(0)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
for x in range(0, WIDTH, 4): # Petit motif de sol lunaire en bas
    oled.vline(x, HEIGHT - 5 - (x % 3), 5, 1)
oled.text("RETROPICO", 28, 12, 1)
oled.text("MOON LANDER", 20, 26, 1)
oled.text("- PRESS KEY -", 16, 46, 1)
oled.show()

WaitAddonBTN()
play_game_start()
generate_terrain()

# Boucle principale
game_over = False
landed = False

while not game_over:
    oled.fill(0)
    animation = 0
    
    # Lecture des entrées PCF8574
    btn_left = not pcf.pin(4)
    btn_down = not pcf.pin(5) # Moteur principal
    btn_right = not pcf.pin(6)
    
    if btn_left and Fuel > 0:
        veloch += trust_power * 0.6
        Fuel -= 0.08
    if btn_right and Fuel > 0:
        veloch -= trust_power * 0.6
        Fuel -= 0.08
    if btn_down and Fuel > 0:
        velocv -= trust_power
        Fuel -= 0.15
        animation = 1
        
    velocv += gravity
    Lander_Y += velocv
    Lander_X += veloch
    
    # Passage d'un côté à l'autre de l'écran (Wrap-around)
    if Lander_X > WIDTH - 16: Lander_X = 0
    elif Lander_X < 0: Lander_X = WIDTH - 16
    
    if Lander_Y < 11: # Limite haute sous le HUD
        Lander_Y = 11
        velocv = 0
        
    # Détection des collisions avec le sol
    # On vérifie les pieds du lander (x à x+15) au niveau du bas du sprite (y+8)
    check_y = int(Lander_Y + 8)
    collision = False
    for tx in range(int(Lander_X), int(Lander_X + 16)):
        px = tx % WIDTH
        if check_y >= terrain[px]:
            collision = True
            break
            
    if collision:
        game_over = True
        # Vérification des conditions strictes d'atterrissage sur le Pad
        on_pad = (Lander_X >= landingpad_X - 2) and (Lander_X + 16 <= landingpad_X + pad_width + 2)
        correct_y = (check_y <= pad_height + 3)
        
        if on_pad and correct_y and velocv <= 1.2 and abs(veloch) <= 0.4:
            landed = True
        else:
            landed = False
        break

    # Rendu graphique des éléments
    draw_terrain()
    draw_lander(int(Lander_X), int(Lander_Y), animation)
    draw_hud(Fuel, velocv)
    oled.show()
    utime.sleep(0.03)

# Séquence de fin de jeu
if landed:
    oled.fill(0)
    oled.rect(0, 0, WIDTH, HEIGHT, 1)
    oled.text('HOURRA !', 36, 18, 1)
    oled.text('Lander sauf', 20, 32, 1)
    score = max(0, int(Fuel * 10))
    oled.text('Score: {}'.format(score), 28, 46, 1)
    oled.show()
    play_victory()
else:
    # Animation d'explosion graphique
    cx, cy = int(Lander_X + 8), int(Lander_Y + 4)
    for r in range(4, 24, 4):
        circle(cx, cy, r, 1, fill=0)
        # Particules de débris éparpillées
        for _ in range(5):
            px = cx + random.randint(-r, r)
            py = cy + random.randint(-r, r)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT: oled.pixel(px, py, 1)
        oled.text('KABOOM!', 40, 15, 1)
        oled.show()
        utime.sleep(0.08)
    
    oled.fill(0)
    oled.rect(0, 0, WIDTH, HEIGHT, 1)
    oled.text('GAME OVER', 28, 24, 1)
    oled.text('Crash Lunaire', 12, 38, 1)
    oled.show()
    play_game_over()
