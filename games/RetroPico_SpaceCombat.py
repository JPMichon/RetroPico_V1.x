#------------------------------------------------
#  Moon Lander -> Scroller "Space 1947"
#               v1.0
#  JPMICHON / AI  06/2026
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime
import math
import random

RetroPico_PCB_REV = 1.2

# Configuration système et écran
WIDTH  = 128
HEIGHT = 64
_SSD1306 = 0x3C 
_PCF8574AT= 0x20 

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

def play_sound(partition, tempos):
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
        utime.sleep(0.01)
    buzzer.deinit()

def play_shoot_sound():
    # Bruit de tir rapide
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(880)
    buzzer.duty_u16(8192)
    utime.sleep(0.03)
    buzzer.freq(440)
    utime.sleep(0.02)
    buzzer.duty_u16(0)
    buzzer.deinit()

def WaitAddonBTN():
    while True:
        if not pcf.pin(4) or not pcf.pin(5) or not pcf.pin(6):
            break 
        utime.sleep(0.1)

# --- Dessin des entités ---
def draw_player(x, y):
    # Dessin d'un chasseur spatial pointant vers la droite
    oled.fill_rect(x, y + 2, 12, 4, 1)
    oled.fill_rect(x + 4, y, 4, 8, 1)
    oled.pixel(x + 13, y + 3, 1)
    oled.pixel(x + 13, y + 4, 1)

def draw_enemy(x, y):
    # Dessin d'un vaisseau ennemi pointant vers la gauche
    oled.rect(x + 2, y, 8, 8, 1)
    oled.line(x + 2, y + 4, x, y + 2, 1)
    oled.line(x + 2, y + 4, x, y + 6, 1)
    oled.fill_rect(x + 5, y + 2, 3, 4, 1)

def draw_hud(score, shield):
    oled.hline(0, 9, WIDTH, 1)
    oled.text("SCR:{}".format(score), 2, 1, 1)
    oled.text("SHD:{}".format(shield), 80, 1, 1)

# --- Écran d'accueil ---
oled.fill(0)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.text("SPACE 1947", 24, 15, 1)
oled.text("- ARCADE MOD -", 12, 32, 1)
oled.text("PRESS ANY KEY", 16, 48, 1)
oled.show()
WaitAddonBTN()
play_sound(['DO5', 'MI5', 'SOL5', 'DO6'], [0.08, 0.08, 0.08, 0.2])

# --- Variables d'état du jeu ---
player_x = 15
player_y = 30
player_speed = 3
score = 0
shield = 3

# Listes d'objets [x, y] ou [x, y, type]
bullets = []
enemies = []
stars = [[random.randint(0, WIDTH), random.randint(11, HEIGHT - 2)] for _ in range(10)]

cooldown = 0
running = True
tick = 0

# --- Boucle principale ---
while running:
    oled.fill(0)
    tick += 1
    
    # Lecture des entrées
    move_up = not pcf.pin(4)
    shoot = not pcf.pin(5)
    move_down = not pcf.pin(6)
    
    # Déplacement joueur
    if move_up and player_y > 11:
        player_y -= player_speed
    if move_down and player_y < HEIGHT - 10:
        player_y += player_speed
        
    # Gestion du tir (avec délai antirebond/cooldown)
    if cooldown > 0:
        cooldown -= 1
    if shoot and cooldown == 0:
        bullets.append([player_x + 14, player_y + 3])
        play_shoot_sound()
        cooldown = 4 # Délai entre deux tirs
        
    # Défilement et rendu du fond étoilé
    for star in stars:
        star[0] -= 1 # Vitesse des étoiles
        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(11, HEIGHT - 2)
        oled.pixel(star[0], star[1], 1)
        
    # Mise à jour et dessin des tirs
    for b in bullets[:]:
        b[0] += 4 # Vitesse du laser
        if b[0] > WIDTH:
            bullets.remove(b)
        else:
            oled.hline(b[0], b[1], 4, 1)
            
    # Génération des ennemis
    if tick % 25 == 0 and len(enemies) < 4:
        enemies.append([WIDTH, random.randint(12, HEIGHT - 10), random.uniform(0.1, 0.3)])
        
    # Mise à jour et dessin des ennemis
    for e in enemies[:]:
        e[0] -= 2 # Vitesse d'avancée de l'ennemi
        # Trajectoire légèrement sinusoïdale pour simuler un vol d'esquive
        e[1] += int(1.5 * math.sin(e[0] * e[2]))
        
        # Rester dans les limites de l'écran de jeu
        if e[1] < 11: e[1] = 11
        if e[1] > HEIGHT - 10: e[1] = HEIGHT - 10
        
        if e[0] < -10:
            enemies.remove(e)
            continue
            
        draw_enemy(int(e[0]), int(e[1]))
        
        # Test collision : Tir contre Ennemi
        enemy_rect = (e[0], e[1], 10, 8)
        for b in bullets[:]:
            if (e[0] <= b[0] <= e[0] + 10) and (e[1] <= b[1] <= e[1] + 8):
                # Explosion rapide
                oled.fill_rect(int(e[0]), int(e[1]), 10, 8, 1)
                score += 10
                bullets.remove(b)
                enemies.remove(e)
                break
                
        # Test collision : Joueur contre Ennemi
        if (e[0] < player_x + 12 and e[0] + 10 > player_x and
            e[1] < player_y + 8 and e[1] + 8 > player_y):
            shield -= 1
            enemies.remove(e)
            # Flash écran blanc pour notifier le dégât
            oled.fill(1)
            oled.show()
            utime.sleep(0.05)
            if shield <= 0:
                running = False
                
    # Rendu final du joueur et de l'interface
    draw_player(player_x, player_y)
    draw_hud(score, shield)
    oled.show()
    utime.sleep(0.02)

# --- Écran Game Over ---
oled.fill(0)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.text("MISSION ECHOUER", 4, 16, 1)
oled.text("FINAL SCR: {}".format(score), 12, 36, 1)
oled.show()
play_sound(['MI5', 'RE5', 'DO5', 'LA4'], [0.2, 0.2, 0.2, 0.5])
