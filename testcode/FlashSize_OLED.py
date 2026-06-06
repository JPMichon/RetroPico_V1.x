import os
from machine import Pin, I2C
import ssd1306
import time

# 1. Configuration du matériel (Broches et I2C)
# SDA = Pin 12 (GP12), SCL = Pin 13 (GP13) -> Bus matériel I2C(0)
i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)

# Initialisation de l'écran SSD1306 (128x64 pixels)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def compter_fichiers(chemin='/'):
    """Compte récursivement tous les fichiers de la flash (MicroPython friendly)."""
    total_fichiers = 0
    try:
        for entree in os.listdir(chemin):
            # Recréer le chemin complet de l'élément
            suffixe = '' if chemin == '/' else '/'
            chemin_complet = f"{chemin}{suffixe}{entree}"
            
            try:
                # Récupérer les métadonnées (os.stat sur Pico renvoie des infos de type tuple)
                # Le premier élément indique s'il s'agit d'un dossier (0x4000) ou d'un fichier (0x8000)
                mode = os.stat(chemin_complet)[0]
                if mode & 0x4000:  # C'est un répertoire/dossier
                    total_fichiers += compter_fichiers(chemin_complet)
                else:  # C'est un fichier
                    total_fichiers += 1
            except:
                # Sécurité si un fichier système est inaccessible
                pass
    except:
        pass
    return total_fichiers

def obtenir_espace_flash():
    """Récupère l'espace de stockage et compte les fichiers."""
    info = os.statvfs('/')
    
    # Extraction des valeurs numériques du tuple (AJOUTER LES CORCHETS [])
    taille_bloc = info[0]   # Taille du bloc (ex: 4096)
    blocs_totaux = info[2]  # Nombre total de blocs
    blocs_libres = info[3]  # Nombre de blocs libres
    
    # Le reste des calculs fonctionne maintenant parfaitement
    total = (blocs_totaux * taille_bloc) / 1024
    libre = (blocs_libres * taille_bloc) / 1024
    utilise = total - libre
    
    pct_utilise = (utilise / total) * 100 if total > 0 else 0
    nb_fichiers = compter_fichiers('/')
    
    return total, libre, pct_utilise, nb_fichiers

def dessiner_interface(total, libre, pct_utilise, nb_fichiers):
    """Dessine une interface graphique claire et professionnelle."""
    # Effacer l'écran
    oled.fill(0)
    
    # --- EN-TÊTE ---
    oled.text("MEMOIRE FLASH", 12, 2, 1)
    oled.hline(0, 13, 128, 1) # Ligne de séparation
    
    # --- TEXTE DES DONNÉES ---
    oled.text(f"Total: {total:.0f} Ko", 0, 18, 1)
    oled.text(f"Libre: {libre:.0f} Ko", 0, 27, 1)
    oled.text(f"Fichiers: {nb_fichiers}", 0, 36, 1) # Nouvelle ligne ajoutée
    
    # --- SECTION GRAPHIQUE (Barre de progression) ---
    oled.text(f"Utilise: {pct_utilise:.1f}%", 0, 46, 1)
    
    # Dessin du contour de la jauge
    oled.rect(0, 56, 128, 8, 1)
    
    # Remplissage de la jauge
    largeur_barre = int((pct_utilise / 100) * 124)
    if largeur_barre > 0:
        oled.fill_rect(2, 58, largeur_barre, 4, 1)
        
    # Envoyer le dessin à l'écran
    oled.show()

# Boucle principale de rafraîchissement
print("Affichage mis a jour sur l'ecran SSD1306...")
try:
    while True:
        # Récupération des données globales
        total, libre, pct_utilise, nb_fichiers = obtenir_espace_flash()
        
        # Mise à jour graphique
        dessiner_interface(total, libre, pct_utilise, nb_fichiers)
        
        # Pause de 5 secondes pour économiser les ressources de calcul
        time.sleep(5)
        
except KeyboardInterrupt:
    print("Programme arrete.")
    oled.fill(0)
    oled.show()
