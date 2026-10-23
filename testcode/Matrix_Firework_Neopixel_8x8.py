# coder avec le System prompt RETROPICO_FreelanceCoder.md
# requete: "fait une animation de feux d'artifice"
#
# Projet: https://github.com/JPMichon/RetroPico_V1.x
#

import machine
import neopixel
import time
import random
import math

# --- CONFIGURATION MATÉRIELLE & PARAMÈTRES ---
PIN_NEOPIXEL = 23
NB_COLS = 8
NB_ROWS = 8
TOTAL_PIXELS = 1 + (NB_COLS * NB_ROWS)

# Niveau de luminosité globale (0.0 à 1.0)
BRIGHTNESS = 0.2

# Initialisation du ruban NeoPixel
np = neopixel.NeoPixel(machine.Pin(PIN_NEOPIXEL), TOTAL_PIXELS)

# --- PALETTE DE COULEURS POUR LES EXPLOSIONS ---
COLORS = [
    (255, 0, 0),     # Rouge
    (0, 255, 0),     # Vert
    (0, 0, 255),     # Bleu
    (255, 255, 0),   # Jaune
    (0, 255, 255),   # Cyan
    (255, 0, 255),   # Magenta
    (255, 128, 0),   # Orange
    (255, 255, 255)  # Blanc étincelant
]

def set_matrix_pixel(x, y, color):
    """ Allume un pixel de la matrice en appliquant la luminosité et en ignorant le PCB (index 0) """
    if 0 <= x < NB_COLS and 0 <= y < NB_ROWS:
        pixel_index = 1 + (int(y) * NB_COLS + int(x))
        r = int(color[0] * BRIGHTNESS)
        g = int(color[1] * BRIGHTNESS)
        b = int(color[2] * BRIGHTNESS)
        np[pixel_index] = (r, g, b)

def clear_matrix():
    """ Éteint la matrice et sécurise la DEL du PCB """
    for i in range(TOTAL_PIXELS):
        np[i] = (0, 0, 0)

# --- ANIMATION D'UN FEU D'ARTIFICE ---
def launch_firework():
    # 1. Choisir les paramètres du feu d'artifice
    start_x = random.randint(2, 5)        # Colonne de départ (centrée)
    target_y = random.randint(1, 3)       # Hauteur de l'explosion (haut de la matrice)
    color = random.choice(COLORS)         # Couleur de l'explosion
    
    # 2. Phase de montée (Fusée)
    for y in range(NB_ROWS - 1, target_y - 1, -1):
        clear_matrix()
        # Dessine la fusée (en blanc/jaune pendant la montée)
        set_matrix_pixel(start_x, y, (255, 240, 150))
        np.write()
        time.sleep_ms(80) # Vitesse de montée
        
    # 3. Phase d'explosion (Expansion des étincelles)
    # On simule des particules se propageant dans 8 directions (cercles concentriques)
    num_frames = 5 # Nombre d'étapes de l'explosion
    
    for frame in range(num_frames):
        clear_matrix()
        
        # Facteur d'atténuation de la couleur (fondu sortant)
        fade = (num_frames - frame) / num_frames
        faded_color = (int(color[0] * fade), int(color[1] * fade), int(color[2] * fade))
        
        # Rayon de l'explosion qui grandit à chaque frame
        radius = frame * 0.7
        
        # Calcul des positions des étincelles (angles de 0 à 360 degrés)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            # Calcul des coordonnées cartésiennes de la particule
            part_x = start_x + (radius * math.cos(rad))
            part_y = target_y + (radius * math.sin(rad))
            
            # Affichage si la particule est toujours dans les limites 8x8
            if 0 <= part_x < NB_COLS and 0 <= part_y < NB_ROWS:
                set_matrix_pixel(part_x, part_y, faded_color)
                
        np.write()
        time.sleep_ms(90) # Vitesse de l'explosion

# --- BOUCLE PRINCIPALE ---
while True:
    launch_firework()
    
    # Pause aléatoire entre deux tirs de feux d'artifice (0.3 à 1.5 seconde)
    clear_matrix()
    np.write()
    time.sleep_ms(random.randint(300, 1500))