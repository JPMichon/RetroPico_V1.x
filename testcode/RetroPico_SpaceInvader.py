#------------------------------------------------
#  Galaga / Space Invaders game
#               v1.0
#  Adapté pour RetroPico - 06/2026
#------------------------------------------------
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import utime
import random

RetroPico_PCB_REV = 1.2
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


oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
#initialisation du multiplexeur pour que les boutons fonctionnent
pcf = PCF8574(i2c, address=_PCF8574AT)
# Étape essentielle pour le PCF8574 : écrire des '1' sur les broches en entrée
# pour activer leur fonctionnement en lecture / pull-up interne.
# Masque pour isoler les broches P4, P5, P6
# P4 = 1<<4 (0x10), P5 = 1<<5 (0x20), P6 = 1<<6 (0x40) -> Total = 0x70
pcf.port = 0x70 # activation des pins pour les boutons

NOTES = {
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319, 'SILENCE': 0
}
   
def play_sound(note, duree):
    if _Buzzer is None: return
    try:
        buzzer = PWM(Pin(_Buzzer))
        freq = NOTES.get(note, 0)
        if freq == 0:
            buzzer.duty_u16(0)
        else:
            buzzer.freq(freq)
            buzzer.duty_u16(1000)
        utime.sleep(duree)
        buzzer.deinit()
    except:
        pass

# --- Variables du joueur ---
player_x = WIDTH // 2
player_y = HEIGHT - 8
player_speed = 3

# --- Projectiles (Balles) ---
bullets = []       # Balles du joueur: [x, y]
alien_bullets = [] # Balles des ennemis: [x, y]

# --- Liste des Aliens ---
# Chaque alien: [x, y, type, direction_animation]
aliens = []
alien_rows = 2
alien_cols = 6
alien_w = 8
alien_h = 6

def init_aliens():
    aliens.clear()
    for row in range(alien_rows):
        for col in range(alien_cols):
            x = 15 + col * 16
            y = 10 + row * 10
            aliens.append([x, y, row]) # row sert de type/visuel

init_aliens()

alien_dir = 1
alien_speed = 1
alien_move_delay = 10
alien_timer = 0

score = 0
lives = 3
game_over = False

# Code de démarrage
play_sound('DO5', 0.1)
play_sound('MI5', 0.1)
play_sound('SOL5', 0.2)

# --- Boucle Principale ---
while not game_over and lives > 0:
    oled.fill(0)
    
    # 1. Lecture des entrées PCF8574
    inputs = pcf.port
    btn_left  = not pcf.pin(6) # P6
    btn_right = not pcf.pin(4) # P4
    btn_fire  = not pcf.pin(5) # P4
    
    # 2. Mouvement du joueur
    if btn_left and player_x > 4:
        player_x -= player_speed
    if btn_right and player_x < WIDTH - 12:
        player_x += player_speed
        
    # 3. Gestion du tir joueur
    if btn_fire and len(bullets) < 3:
        # Limite la cadence en vérifiant la distance de la dernière balle
        if not bullets or bullets[-1][1] < player_y - 15:
            bullets.append([player_x + 4, player_y - 2])
            play_sound('SI5', 0.02)
            
    # 4. Dessin du joueur (Vaisseau type Galaga)
    oled.rect(player_x + 3, player_y, 3, 6, 1)
    oled.rect(player_x, player_y + 3, 9, 3, 1)
    oled.pixel(player_x + 4, player_y - 1, 1)

    # 5. Déplacement et dessin des aliens
    alien_timer += 1
    shift_down = False
    
    if alien_timer >= alien_move_delay:
        alien_timer = 0
        # Vérifier si un alien touche les bords latéraux
        for al in aliens:
            al[0] += alien_dir * alien_speed
            if al[0] <= 2 or al[0] >= WIDTH - 10:
                shift_down = True
                
        if shift_down:
            alien_dir *= -1
            for al in aliens:
                al[1] += 4
                if al[1] >= player_y - 4:
                    game_over = True # Les aliens ont envahi la base

    # Dessin des aliens et tirs aléatoires
    for al in aliens:
        ax, ay, a_type = al[0], al[1], al[2]
        if a_type == 0:
            # Alien Type 1: Forme de crabe
            oled.rect(int(ax+1), int(ay), 6, 4, 1)
            oled.pixel(int(ax), int(ay+4), 1)
            oled.pixel(int(ax+7), int(ay+4), 1)
        else:
            # Alien Type 2: Forme de pieuvre
            oled.rect(int(ax+2), int(ay), 4, 5, 1)
            oled.rect(int(ax), int(ay+2), 8, 2, 1)
            
        # Tir aléatoire des aliens
        if random.randint(0, 400) == 7:
            alien_bullets.append([ax + 4, ay + 6])

    # 6. Mise à jour des projectiles du joueur
    new_bullets = []
    for b in bullets:
        b[1] -= 4 # Monte vers le haut
        if b[1] > 0:
            new_bullets.append(b)
            oled.line(int(b[0]), int(b[1]), int(b[0]), int(b[1]+2), 1)
            
            # Collision balle joueur -> Alien
            for al in aliens:
                if (al[0] <= b[0] <= al[0] + alien_w) and (al[1] <= b[1] <= al[1] + alien_h):
                    aliens.remove(al)
                    new_bullets.remove(b)
                    score += 20
                    play_sound('FA4', 0.03)
                    break
    bullets = new_bullets

    # 7. Mise à jour des projectiles ennemis (Aliens)
    new_alien_bullets = []
    for ab in alien_bullets:
        ab[1] += 3 # Descend vers le bas
        if ab[1] < HEIGHT:
            new_alien_bullets.append(ab)
            oled.pixel(int(ab[0]), int(ab[1]), 1)
            
            # Collision balle alien -> Joueur
            if (player_x <= ab[0] <= player_x + 9) and (player_y <= ab[1] <= player_y + 6):
                lives -= 1
                new_alien_bullets.remove(ab)
                play_sound('DO4', 0.2)
                utime.sleep_ms(500) # Petite pause lors de l'impact
                break
    alien_bullets = new_alien_bullets

    # 8. Condition de victoire de la vague
    if not aliens:
        score += 200
        alien_speed += 1
        if alien_move_delay > 2:
            alien_move_delay -= 2
        init_aliens()
        play_sound('SOL5', 0.1)
        play_sound('DO6', 0.2)

    # Affichage de l'interface (Score et Vies)
    oled.text(f"S:{score}", 0, 0, 1)
    oled.text(f"V:{lives}", WIDTH - 30, 0, 1)
    
    oled.show()
    utime.sleep_ms(20)

# --- Écran de fin de partie ---
oled.fill(0)
oled.text("GAME OVER", 28, 20, 1)
oled.text(f"Score: {score}", 32, 40, 1)
oled.show()
play_sound('DO4', 0.6)
