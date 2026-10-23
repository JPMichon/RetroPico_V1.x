import machine
import neopixel
import time
import random

# --- CONFIGURATION MATÉRIELLE & PARAMÈTRES ---
PIN_NEOPIXEL = 23
NB_COLS = 8
NB_ROWS = 8
# 1 pixel PCB + 64 pixels matrice = 65 pixels au total
TOTAL_PIXELS = 1 + (NB_COLS * NB_ROWS)

# Niveau de luminosité globale (0.0 à 1.0)
BRIGHTNESS = 0.1

# Initialisation du ruban NeoPixel
np = neopixel.NeoPixel(machine.Pin(PIN_NEOPIXEL), TOTAL_PIXELS)

# --- STRUCTURE DES GOUTTES (MATRIX) ---
# Correction de la syntaxe d'initialisation de la liste pour MicroPython
drops = [0] * NB_COLS
speeds = [random.randint(1, 3) for _ in range(NB_COLS)]

def init_drops():
    """Initialise les positions de départ des gouttes au-dessus de l'écran"""
    for i in range(NB_COLS):
        drops[i] = random.randint(-4, 0)

def set_matrix_pixel(x, y, color):
    """
    Allume un pixel de la matrice 8x8 en sautant le pixel 0 (DEL PCB)
    et applique le coefficient de luminosité globale.
    """
    if 0 <= x < NB_COLS and 0 <= y < NB_ROWS:
        # Calcul de l'index : +1 pour ignorer la DEL du PCB à l'index 0
        pixel_index = 1 + (y * NB_COLS + x)
        
        # Application de la luminosité (conversion en entier obligatoire)
        r = int(color[0] * BRIGHTNESS)
        g = int(color[1] * BRIGHTNESS)
        b = int(color[2] * BRIGHTNESS)
        
        np[pixel_index] = (r, g, b)

def update_matrix():
    """Calcule l'effet de pluie Matrix et met à jour l'affichage"""
    # Assurer que la DEL du PCB reste éteinte (Sécurité)
    np[0] = (0, 0, 0)
    
    # Nettoyer le reste de la matrice
    for i in range(1, TOTAL_PIXELS):
        np[i] = (0, 0, 0)
        
    for x in range(NB_COLS):
        head_y = int(drops[x])
        
        # Dessine le corps de la goutte avec un dégradé de vert vers le haut
        for length in range(4):
            current_y = head_y - length
            if 0 <= current_y < NB_ROWS:
                if length == 0:
                    # Tête de la goutte (Vert vif/blanc)
                    color = (50, 250, 50)
                elif length == 1:
                    # Corps brillant
                    color = (0, 255, 0)
                elif length == 2:
                    # Corps moyen
                    color = (0, 140, 0)
                else:
                    # Traîne sombre
                    color = (0, 60, 0)
                    
                set_matrix_pixel(x, current_y, color)
        
        # Fait descendre la goutte
        drops[x] += speeds[x] * 0.4
        
        # Réinitialisation si la traîne sort de l'écran
        if drops[x] - 4 >= NB_ROWS:
            drops[x] = random.randint(-3, 0)
            speeds[x] = random.randint(1, 3)

    # Envoi des données aux NeoPixels
    np.write()

# --- BOUCLE PRINCIPALE ---
init_drops()

while True:
    update_matrix()
    time.sleep_ms(90) # Ajuste la fluidité de l'animation