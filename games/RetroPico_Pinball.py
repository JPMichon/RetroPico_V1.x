#------------------------------------------------
#  RetroPinball -> Cibles Latérales & 3 Bumpers
#               v1.0
#Version du  RetroPico 
RetroPico_PCB_REV = 1.2
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime
import math
import random



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
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA4': 440, 'SI5': 988,
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

def play_bump_sound():
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(650)
    buzzer.duty_u16(8192)
    utime.sleep(0.015)
    buzzer.duty_u16(0)
    buzzer.deinit()

def play_target_sound():
    buzzer = PWM(Pin(_Buzzer))
    buzzer.freq(950)
    buzzer.duty_u16(8192)
    utime.sleep(0.02)
    buzzer.duty_u16(0)
    buzzer.deinit()

def WaitAddonBTN():
    while True:
        if not pcf.pin(4) or not pcf.pin(5) or not pcf.pin(6):
            break 
        utime.sleep(0.1)

# --- Dessin de la table graphique ---
def draw_table():
    oled.vline(22, 0, HEIGHT, 1)
    oled.vline(24, 0, HEIGHT, 1)
    oled.vline(106, 0, HEIGHT, 1)
    oled.vline(108, 0, HEIGHT, 1)
    oled.hline(22, 0, 86, 1)
    oled.hline(22, 1, 86, 1)
    oled.vline(98, 12, HEIGHT - 12, 1)
    
    # Roto-déflecteur à 90° (/)
    oled.line(98, 2, 106, 10, 1)
    oled.line(99, 2, 106, 9, 1)
    
    oled.line(24, 44, 35, 56, 1)
    oled.line(98, 44, 93, 56, 1)
    oled.vline(20, 0, HEIGHT, 1)

# --- Dessin d'un bumper détaillé ---
def draw_bumper(x, y, flash):
    if flash > 0:
        oled.fill_rect(x-4, y-4, 9, 9, 1)
        oled.fill_rect(x-2, y-2, 5, 5, 0)
        oled.pixel(x, y, 1)
    else:
        oled.pixel(x, y, 1)
        oled.pixel(x-2, y-1, 1); oled.pixel(x-2, y, 1); oled.pixel(x-2, y+1, 1)
        oled.pixel(x+2, y-1, 1); oled.pixel(x+2, y, 1); oled.pixel(x+2, y+1, 1)
        oled.pixel(x-1, y-2, 1); oled.pixel(x, y-2, 1); oled.pixel(x+1, y-2, 1)
        oled.pixel(x-1, y+2, 1); oled.pixel(x, y+2, 1); oled.pixel(x+1, y+2, 1)

# --- Gestion physique des collisions avec un segment statique ---
def collide_with_wall(x1, y1, x2, y2, bounce_coeff):
    global ball
    wx = x2 - x1
    wy = y2 - y1
    w_len = math.sqrt(wx*wx + wy*wy)
    if w_len == 0: return
    wux = wx / w_len
    wuy = wy / w_len
    bx = ball[0] - x1
    by = ball[1] - y1
    proj = bx * wux + by * wuy
    if 0 <= proj <= w_len:
        nx = -wuy
        ny = wux
        dist_x = bx - proj * wux
        dist_y = by - proj * wuy
        dist = math.sqrt(dist_x*dist_x + dist_y*dist_y)
        if dist < (radius + 1.0):
            dot = ball[2] * nx + ball[3] * ny
            if dot > 0: # La bille va vers la paroi
                ball[2] -= 2.0 * dot * nx
                ball[3] -= 2.0 * dot * ny
                ball[2] *= bounce_coeff
                ball[3] *= bounce_coeff
                ball[0] += nx * (radius + 1.5 - dist)
                ball[1] += ny * (radius + 1.5 - dist)
                play_bump_sound()
                
# --- Écran d'accueil ---
oled.fill(0)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.rect(3, 3, WIDTH-6, HEIGHT-6, 1)
oled.text("RetroPico", 30, 10, 1)
oled.text("PINBALL", 40, 20, 1)
oled.text("PRESS ANY KEY", 12, 49, 1)
oled.show()
WaitAddonBTN()
play_sound(['DO5', 'MI5', 'SOL5', 'DO6'], [0.08, 0.08, 0.08, 0.2])

# --- Initialisation de la physique ---
ball = [102, 50, 0.0, 0.0]
ball_in_play = False
radius = 1.5

# Configuration de 3 Bumpers centraux : [X, Y, Points, TimerFlash]
bumpers = [
    [48, 18, 10, 0],
    [72, 18, 10, 0],
    [60, 30, 15, 0]
]
bump_radius = 3.0

# Configuration des 4 cibles latérales : [X, Y, Largeur, Hauteur, Points, TimerFlash]
targets = [
    [25, 14, 2, 8, 50, 0],  # Gauche Haute
    [25, 28, 2, 8, 50, 0],  # Gauche Basse
    [95, 14, 2, 8, 50, 0],  # Droite Haute
    [95, 28, 2, 8, 50, 0]   # Droite Basse
]

flipper_y = 56
score = 0
lives = 3
running = True

# Gestion du lanceur analogique
launch_charge = 0.0
max_charge = 30.0  
prev_launch_button = False

# --- Boucle principale ---
while running:
    oled.fill(0)
    
    # 1. Traitement des entrées utilisateur
    flipper_L_active = not pcf.pin(6)
    launch_button    = not pcf.pin(5)
    flipper_R_active = not pcf.pin(4)
    
    # 2. Logique de charge mécanique et vélocité du lanceur
    if not ball_in_play:
        if launch_button:
            if launch_charge < max_charge:
                launch_charge += 1.2
                ball[1] = 50 + int(launch_charge * 0.2)
        elif prev_launch_button and not launch_button:
            velocity_y = -3.5 - (launch_charge / max_charge) * 4.0
            ball = [102, ball[1], 0.0, velocity_y]
            ball_in_play = True
            launch_charge = 0.0
            play_sound(['SOL5', 'DO6'], [0.04, 0.04])
            
    prev_launch_button = launch_button
        
    # 3. Traitement de la physique dynamique
    if ball_in_play:
        ball[1] += 0.24  # Gravité
        
        ball[0] += ball[2]  # Intégration VX
        ball[1] += ball[3]  # Intégration VY
        
        ball[2] *= 0.992  # Friction X
        ball[3] *= 0.992  # Friction Y

        # --- Rebond angulaire sur le déflecteur de sortie ---
        if ball[0] - ball[1] >= 94 and ball[0] >= 98 and ball[1] <= 12:
            temp_vy = ball[3]
            ball[2] = abs(temp_vy) * -0.82 
            ball[3] = abs(temp_vy) * 0.15   
            ball[0] = 96
            ball[1] = 4
            play_bump_sound()

        # --- Collisions parois de la table ---
        if ball[0] - radius < 24:
            ball[0] = 24 + radius
            ball[2] = -ball[2] * 0.60
        
        if ball[1] > 12:
            if ball[0] + radius > 98 and ball[0] < 102:
                ball[0] = 98 - radius
                ball[2] = -ball[2] * 0.60
            elif ball[0] + radius > 106:
                ball[0] = 106 - radius
                ball[2] = -ball[2] * 0.60
        else:
            if ball[0] + radius > 106:
                ball[0] = 106 - radius
                ball[2] = -ball[2] * 0.60
                
        if ball[1] - radius < 2:
            ball[1] = radius + 2
            ball[3] = -ball[3] * 0.60
        # --- Collisions physiques avec les parois inférieures adjacentes ---
        # Paroi oblique gauche : de (24, 44) à (35, 56)
        collide_with_wall(24, 44, 35, 56, bounce_coeff=0.65)
        # Paroi oblique droite : de (98, 44) à (93, 56) (inversée géométriquement pour la normale)
        collide_with_wall(93, 56, 98, 44, bounce_coeff=0.65)
        
        # --- Collisions Cibles Latérales ---
        for t in targets:
            if t[5] > 0: t[5] -= 1  # Gère l'effet d'extinction temporaire
            
            # Détection de collision AABB simple entre la bille et les rectangles des cibles
            if (t[0] <= ball[0] <= t[0] + t[2]) and (t[1] <= ball[1] <= t[1] + t[3]):
                score += t[4]
                t[5] = 12  # Désactive et fait clignoter la cible pendant 12 frames
                ball[2] = -ball[2] * 1.1  # Renvoie vigoureusement la bille horizontalement
                play_target_sound()

        # --- Collisions Bumpers ---
        for b in bumpers:
            if b[3] > 0: b[3] -= 1
            
            dx = ball[0] - b[0]
            dy = ball[1] - b[1]
            dist = math.sqrt(dx*dx + dy*dy)
            min_dist = radius + bump_radius
            
            if dist < min_dist:
                if dist == 0: dist = 0.1
                ball[0] = b[0] + (dx / dist) * min_dist
                ball[1] = b[1] + (dy / dist) * min_dist
                ball[2] = (dx / dist) * 4.2
                ball[3] = (dy / dist) * 4.2
                score += b[2]
                b[3] = 4
                play_bump_sound()

        # --- Traitement géométrique des Flippers ---
        fl_x1, fl_y1 = 35, flipper_y
        fl_x2, fl_y2 = 51, flipper_y - (5 if flipper_L_active else -2)
        fr_x1, fr_y1 = 93, flipper_y
        fr_x2, fr_y2 = 77, flipper_y - (5 if flipper_R_active else -2)

        if flipper_y - 5 <= ball[1] <= flipper_y + 4:
            if fl_x1 <= ball[0] <= fl_x2:
                ball[1] = flipper_y - radius
                ball[3] = -abs(ball[3]) * 0.85 - (1.8 if flipper_L_active else 0)
                ball[2] += (1.4 if flipper_L_active else -0.4)
                if flipper_L_active: play_bump_sound()
                
            elif fr_x2 <= ball[0] <= fr_x1:
                ball[1] = flipper_y - radius
                ball[3] = -abs(ball[3]) * 0.85 - (1.8 if flipper_R_active else 0)
                ball[2] += (-1.4 if flipper_R_active else 0.4)
                if flipper_R_active: play_bump_sound()

        # --- Perte de bille ---
        if ball[1] > HEIGHT:
            lives -= 1
            ball_in_play = False
            ball = [102, 50, 0.0, 0.0]
            play_sound(['MI4', 'DO4'], [0.1, 0.2])
            if lives <= 0:
                running = False

    # 4. Rendu de l'interface graphique (UI)
    draw_table()
    
    # Section HUD
    oled.text("S", 0, 2, 1)
    oled.text("{}".format(score), 0, 12, 1)
    oled.text("B", 0, 30, 1)
    for l in range(lives):
        oled.fill_rect(2 + (l * 6), 42, 4, 4, 1)
    
    # Rendu des 3 bumpers
    for b in bumpers:
        draw_bumper(b[0], b[1], b[3])

    # Rendu des cibles latérales (uniquement si elles ne sont pas en refroidissement/clignotement)
    for t in targets:
        if t[5] % 3 == 0:  # Effet d'alternance/clignotement si touché
            oled.fill_rect(t[0], t[1], t[2], t[3], 1)

    # Rendu dynamique des structures des Flippers
    fl_y2_d = flipper_y - (5 if flipper_L_active else -2) if ball_in_play else flipper_y + 2
    fr_y2_d = flipper_y - (5 if flipper_R_active else -2) if ball_in_play else flipper_y + 2
    
    oled.line(35, flipper_y, 51, fl_y2_d, 1)
    oled.line(93, flipper_y, 77, fr_y2_d, 1)
    
    # Rendu de la bille
    oled.fill_rect(int(ball[0])-1, int(ball[1])-1, 2, 2, 1)
    
    # Ressort mécanique adaptatif selon la jauge de charge
    if not ball_in_play:
        spring_top = 56 + int(launch_charge * 0.2)
        oled.rect(100, spring_top, 5, HEIGHT - spring_top, 1)
        oled.line(100, spring_top + 2, 105, spring_top + 4, 1)
        
    oled.show()
    utime.sleep(0.008)

# --- Écran Game Over ---
oled.fill(0)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.rect(4, 4, WIDTH-8, HEIGHT-8, 1)
oled.text("GAME OVER", 28, 16, 1)
oled.line(20, 28, 108, 28, 1)
oled.text("SCORE: {}".format(score), 20, 38, 1)
oled.show()
play_sound(['MI5', 'RE5', 'DO5', 'LA4'], [0.2, 0.2, 0.2, 0.5])