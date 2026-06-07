#------------------------------------------------
#  Game of Life
#  JPMICHON  06/2026
# Identification de la version du PCB permettant la configuration adéquate certains IOs
RetroPico_PCB_REV = 1.2
#------------------------------------------------
from machine import Pin, I2C, PWM
import utime
import urandom
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574

# --- Conway Configuration ---
CELL_SIZE = 4 # Largeur et hauteur d'une cellule en pixels

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
    
# --- OLED Configuration ---
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# devices I2C
_SSD1306 = 0x3C # adresse de l'ecran OLED
_PCF8574AT= 0x20 # adresse du multiplexeur

i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
_Buzzer = 6 # définition du  buzzer (GP6)
display = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

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
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319, 'SILENCE': 0}

# Utilisation de la division entière (//) pour obtenir des nombres entiers
# 128 // 3 = 42 colonnes, 64 // 3 = 21 lignes
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE   
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE 

# Création de la grille (1 est vivant, 0 est mort)
board = [[0 for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

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
    
def conway_step():
    changed = False
    # Grille temporaire basée sur la taille réelle du jeu (GRID_HEIGHT x GRID_WIDTH)
    new_board = [[board[x][y] for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
    
    for x in range(GRID_HEIGHT):
        for y in range(GRID_WIDTH):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    # Effet toroïdal (boucle) basé sur les dimensions de la grille
                    nx = (x + dx) % GRID_HEIGHT
                    ny = (y + dy) % GRID_WIDTH
                    count += board[nx][ny]
            
            # Règles de Conway
            self = board[x][y]
            if self and not (2 <= count <= 3):
                new_board[x][y] = 0
                changed = True
            elif not self and count == 3:
                new_board[x][y] = 1
                changed = True
                
    # Mise à jour de la grille principale
    for x in range(GRID_HEIGHT):
        for y in range(GRID_WIDTH):
            board[x][y] = new_board[x][y]
            
    return changed

def conway_rand():
    print("Generate New Life!")
    for x in range(GRID_HEIGHT):
        for y in range(GRID_WIDTH):
            board[x][y] = urandom.randint(0, 1)

def draw_board():
    display.fill(0) # Efface l'écran
    
    for x in range(GRID_HEIGHT):
        for y in range(GRID_WIDTH):
            if board[x][y] == 1:
                # Dessine un carré plein de CELL_SIZE x CELL_SIZE pour la cellule vivante
                for dx in range(CELL_SIZE):
                    for dy in range(CELL_SIZE):
                        px = (y * CELL_SIZE) + dx
                        py = (x * CELL_SIZE) + dy
                        # Protection pour éviter tout pixel en dehors des limites de l'écran
                        if px < SCREEN_WIDTH and py < SCREEN_HEIGHT:
                            display.pixel(px, py, 1)
                        
    display.show() # Affiche le rendu sur l'OLED

refresh_needed = True

# --- Main Loop ---
# splash screen
display.fill(0)
display.text("RetroPico",30,10)
display.text("Conway",40,25)
display.text("GameofLife",25,35)
display.text("-Press key-",20,52)
display.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 1)
display.show()
WaitAddonBTN()

while True:
    if refresh_needed:
        conway_rand()
        refresh_needed = False

    draw_board()
    
    if not conway_step():
        refresh_needed = True # Pattern stabilized, generate new life
        play_game_over()
    utime.sleep_ms(50) # Control the speed of the simulation
