#------------------------------------------------
#  Artillery game for RetroPico
#  Controls: P6 Angle+, P4 Angle-, P5 Hold Power/Release to Shoot
#
RetroPico_PCB_REV = 1.2
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime
import math
import random

WIDTH  = 128
HEIGHT = 64

# Configuration matérielle

if RetroPico_PCB_REV == 1.0:
    _I2C_SDA, _I2C_SCL = 16, 17
else:
    _I2C_SDA, _I2C_SCL = 12, 13
    
i2c = I2C(0, sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
_Buzzer = 6

pcf = PCF8574(i2c, address=0x20)
pcf.port = 0x70 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Sons
NOTES = {'DO4': 262, 'MI5': 659, 'SOL5': 784, 'DO6': 1047, 'SI4': 494, 'LA4': 440}

def play_sound(melody, tempos):
    buzzer = PWM(Pin(_Buzzer))
    for note, duree in zip(melody, tempos):
        if note in NOTES:
            buzzer.freq(NOTES[note])
            buzzer.duty_u16(32768)
        else:
            buzzer.duty_u16(0)
        utime.sleep(duree)
        buzzer.duty_u16(0)
        utime.sleep(0.01)
    buzzer.deinit()

# Écran d'accueil
oled.fill(0)
oled.text("RetroPico", 30, 10)
oled.text("ARTILLERY", 28, 25)
oled.text("-Press key-", 20, 52)
oled.rect(0, 0, WIDTH, HEIGHT, 1)
oled.show()

# Attente d'un bouton
while pcf.pin(4) and pcf.pin(5) and pcf.pin(6):
    utime.sleep(0.1)
play_sound(['DO4', 'SOL5', 'DO6'], [0.1, 0.1, 0.2])

# --- PARAMÈTRES DU JEU ---
terrain_h = [HEIGHT - 5] * WIDTH
center = WIDTH // 2
mountain_height = random.randint(20, 35)
for i in range(WIDTH):
    dist_from_center = abs(i - center)
    if dist_from_center < 30:
        terrain_h[i] -= int(mountain_height * (1 - (dist_from_center / 30)))

player_x, target_x = 10, 115
player_y = terrain_h[player_x] - 2
target_y = terrain_h[target_x] - 2

angle = 45
power = 5
score = 0
game_over = False

# Boucle principale
while not game_over:
    oled.fill(0)
    
    # Dessiner le terrain
    for x in range(WIDTH):
        oled.line(x, HEIGHT, x, terrain_h[x], 1)
        
    # Dessiner le joueur (Carré) et la cible (Croix)
    oled.fill_rect(player_x - 2, player_y - 2, 5, 5, 1)
    oled.line(target_x - 3, target_y - 3, target_x + 3, target_y + 3, 1)
    oled.line(target_x - 3, target_y + 3, target_x + 3, target_y - 3, 1)
    
    # Afficher l'interface (HUD)
    oled.text(f"A:{angle}", 0, 0)
    oled.text(f"P:{power}", 50, 0)
    oled.text(f"S:{score}", 100, 0)
    
    # Dessiner la ligne du canon
    rad = math.radians(angle)
    gun_x = int(player_x + 6 * math.cos(rad))
    gun_y = int(player_y - 6 * math.sin(rad))
    oled.line(player_x, player_y, gun_x, gun_y, 1)
    
    # --- GESTION DES ENTRÉES ---
    if not pcf.pin(6):  # P6 augmente l'angle
        if angle < 90: angle += 2
        utime.sleep(0.05)
    elif not pcf.pin(4):  # P4 diminue l'angle
        if angle > 0: angle -= 2
        utime.sleep(0.05)
        
    elif not pcf.pin(5):  # P5 enfoncé : on charge la puissance
        power_charging = True
        while not pcf.pin(5):  # Boucle tant que P5 reste enfoncé
            power += 1
            if power > 25: 
                power = 5  # Recommence si on dépasse la puissance max
                
            # Mise à jour rapide de l'affichage de la puissance pendant la charge
            oled.fill_rect(50, 0, 40, 10, 0)
            oled.text(f"P:{power}", 50, 0)
            oled.show()
            utime.sleep(0.1)
            
        # --- TIR (Déclenché dès que P5 est relâché) ---
        play_sound(['DO4'], [0.1])
        
        rad = math.radians(angle)
        shell_x = float(player_x)
        shell_y = float(player_y)
        vx = power * math.cos(rad) * 0.4
        vy = -power * math.sin(rad) * 0.4
        gravity = 0.08
        
        flying = True
        while flying:
            shell_x += vx
            vy += gravity
            shell_y += vy
            
            curr_x, curr_y = int(shell_x), int(shell_y)
            
            if curr_x < 0 or curr_x >= WIDTH:
                flying = False
                break
                
            if 0 <= curr_y < HEIGHT:
                oled.pixel(curr_x, curr_y, 1)
                oled.show()
                oled.pixel(curr_x, curr_y, 0)
                
            if curr_y >= terrain_h[max(0, min(curr_x, WIDTH - 1))]:
                if abs(curr_x - target_x) < 4 and abs(curr_y - target_y) < 4:
                    score += 1
                    oled.fill(0)
                    oled.text("TOUCHE !", 35, 25)
                    oled.show()
                    play_sound(['MI5', 'SOL5', 'DO6'], [0.1, 0.1, 0.3])
                    
                    # Nouveau terrain et nouvelle cible
                    mountain_height = random.randint(20, 35)
                    for i in range(WIDTH):
                        dist = abs(i - center)
                        terrain_h[i] = HEIGHT - 5
                        if dist < 30:
                            terrain_h[i] -= int(mountain_height * (1 - (dist / 30)))
                    target_x = random.randint(70, 120)
                    target_y = terrain_h[target_x] - 2
                else:
                    play_sound(['SI4', 'LA4'], [0.1, 0.1])
                flying = False
                
            utime.sleep(0.02)
            
        # Réinitialisation de la puissance de départ après le tir
        power = 5
            
    oled.show()
