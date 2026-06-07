#----------------------------------------------------------
#RetroPico v1.x diag tools
#
#
# Identification de la version du PCB permettant la configuration adéquate certains IOs
RetroPico_PCB_REV = 1.2
#---------------------------------------------------------
from machine import I2C, Pin, SPI, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import time
import utime, array
import EEPROM_CAT24C64 #For 32bit or 4KB EEPROM library. Change this according to your library name.
import sdcard
import sys, os

# --- CONFIGURATION MATÉRIELLE ---
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
    
    
# Configuration commune    
_System_LED = 25 # définition du port  del systeme (GP25)        
_Buzzer = 6 # définition du  buzzer (GP6)

#default addresse
_SSD1306 = 0x3C # adresse de l'ecran OLED
_PCF8574AT= 0x20 # adresse du multiplexeur

#---------------------------------------------------------------------------
# Initialisation 
i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
# -----------------------------------
# Choisir le modele de OLED
#
oled = SSD1306_I2C(128, 64, i2c)
#oled = SSD1306_I2C(128, 32, i2c)

#------------------------------------

# 2. Lecteur MicroSD (SPI)
SPI_SCK = 2
SPI_MOSI = 3
SPI_MISO = 4
SPI_CS = 5
spi = SPI(0, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
sd = sdcard.SDCard(spi, Pin(SPI_CS))

pcf = PCF8574(i2c, address=_PCF8574AT)
# Étape essentielle pour le PCF8574 : écrire des '1' sur les broches en entrée
# pour activer leur fonctionnement en lecture / pull-up interne.
# Masque pour isoler les broches P4, P5, P6
# P4 = 1<<4 (0x10), P5 = 1<<5 (0x20), P6 = 1<<6 (0x40) -> Total = 0x70
pcf.port = 0x70 # activation des pins pour les boutons
# 3. Boutons (Actifs à l'état bas - GND)


# --- LOGIQUE DU MENU ---

# Monter la carte SD
os.mount(sd, "/sd")
files = [f for f in os.listdir("/sd") if f.endswith(".py")]
files.sort()

selected_index = 0

def afficher_menu():
    oled.fill(0)
    oled.text("FileManager", 20, 0)
    oled.line(0, 10, 128, 10, 1)

    if not files:
        oled.text("Aucun script .py", 0, 20)
    else:
        # Afficher jusqu'à 5 fichiers
        start_idx = (selected_index // 5) * 5
        for i in range(start_idx, min(start_idx + 5, len(files))):
            prefix = "> " if i == selected_index else "  "
            oled.text(prefix + files[i][:14], 0, 15 + (i % 5) * 10)

    oled.show()

def executer_script(nom_fichier):
    chemin = f"/sd/{nom_fichier}"
    oled.fill(0)
    oled.text("Execution de...", 0, 0)
    oled.text(nom_fichier[:16], 0, 16)
    oled.show()
    time.sleep(0.5)

    try:
        # Exécuter le fichier en conservant l'environnement global
        with open(chemin, "r") as f:
            code = f.read()
            exec(code, globals())
    except Exception as e:
        oled.fill(0)
        oled.text("ERREUR :", 0, 0)
        oled.text(str(e)[:16], 0, 16)
        oled.show()
        time.sleep(3)

# --- BOUCLE PRINCIPALE ---

# État anti-rebond pour les boutons
last_press = 0
afficher_menu()
if not files:
    oled.text("Carte vide", 0, 0)
    oled.show()

while True:
    current_time = time.ticks_ms()
 
    # Lecture des boutons (anti-rebond de 200ms)
    if time.ticks_diff(current_time, last_press) > 200:
        if not pcf.pin(4) and files:
            selected_index = (selected_index - 1) % len(files)
            afficher_menu()
            last_press = current_time
        elif not pcf.pin(6) and files:
            selected_index = (selected_index + 1) % len(files)
            afficher_menu()
            last_press = current_time
        elif not pcf.pin(5) and files:
            script_a_lancer = files[selected_index]
            executer_script(script_a_lancer)
            # Retour au menu après l'exécution du script
            afficher_menu()
            last_press = current_time

    # Petit délai pour économiser les ressources du CPU
    time.sleep_ms(50)
