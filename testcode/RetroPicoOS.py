# ---------------------------------------------------------
# RetroPicoOS
# Identification de la version du PCB pour la configuration des IOs
RETROPICO_PCB_REV = 1.2
# ---------------------------------------------------------
from machine import I2C, Pin, SPI
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
import time
import sdcard
import os

# --- CONFIGURATION MATÉRIELLE ---
if RETROPICO_PCB_REV == 1.0:
    _I2C_SDA, _I2C_SCL = 16, 17
else:
    _I2C_SDA, _I2C_SCL = 12, 13
    
_SYSTEM_LED = 25
_BUZZER = 6
_SSD1306_ADDR = 0x3C
_PCF8574_ADDR = 0x20

# --- INITIALISATION ---
i2c = I2C(0, sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
oled = SSD1306_I2C(128, 64, i2c)

# Lecteur MicroSD (SPI)
SPI_SCK, SPI_MOSI, SPI_MISO, SPI_CS = 2, 3, 4, 5
spi = SPI(0, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))

try:
    sd = sdcard.SDCard(spi, Pin(SPI_CS))
except Exception:
    sd = None
    print("No SD Card detected")
    
# Initialisation des boutons (PCF8574)
pcf = PCF8574(i2c, address=_PCF8574_ADDR)
pcf.port = 0x70  # Activation des pull-ups sur P4, P5, P6

# --- FONCTIONS ---
def sd_available():
    if sd is None:
        return False
    try:
        os.mount(sd, "/sd")
        os.umount("/sd")
        return True
    except OSError as e:
        return e.args[0] == 17  # Déjà monté (EEXIST)
    except Exception:
        return False

def draw_header(title):
    oled.fill(0)
    oled.text(title, 20, 0)
    oled.line(0, 10, 128, 10, 1)

def splash_screen():
    info = os.statvfs('/')
    # Extraction des valeurs numériques du tuple (AJOUTER LES CORCHETS [])
    taille_bloc = info[0]   # Taille du bloc (ex: 4096)
    blocs_totaux = info[2]  # Nombre total de blocs
    blocs_libres = info[3]  # Nombre de blocs libres
    Flashtotal = (blocs_totaux * taille_bloc) / 1024
    Flashlibre = (blocs_libres * taille_bloc) / 1024
    
    oled.fill(0)
    oled.rect(0, 0, 128, 13, 1)
    oled.line(0, 55, 128, 55, 1)
    oled.text('RetroPico_OS', 15, 3)
    oled.text(str(os.uname().version)[:16], 1, 15)
    oled.text(f"Flash:{Flashlibre:.0f}/{Flashtotal:.0f}K0", 0, 30, 1)
    oled.text("Navigation", 25, 45)
    oled.text("Flash        SD" if sd_disponible else "Flash", 1, 57)
    oled.show()

def read_keys():
    if not pcf.pin(6): return 'down'
    if not pcf.pin(5): return 'select'
    if not pcf.pin(4): return 'up'
    return 'null'

def afficher_menu():
    draw_header("FileManager")
    if not files:
        oled.text("Aucun script .py", 0, 20)
    else:
        start_idx = (selected_index // 5) * 5
        for i in range(start_idx, min(start_idx + 5, len(files))):
            prefix = "> " if i == selected_index else "  "
            oled.text(prefix + files[i][:14], 0, 15 + (i % 5) * 10)
    oled.show()

def copier_fichier(source, destination):
    try:
        with open(source, "rb") as f_src:
            with open(destination, "wb") as f_dest:
                while True:
                    bloc = f_src.read(512)
                    if not bloc: break
                    f_dest.write(bloc)
        return True
    except Exception as e:
        print(f"Erreur copie: {e}")
        return False
    
def selected_file(nom_fichier):
    draw_header("FileManager")
    oled.text(nom_fichier[:16], 0, 30)
    oled.line(0, 55, 128, 55, 1)
    
    if storage == "FLASH":
        fichier_source, fichier_dest = f"/{nom_fichier}", f"/sd/{nom_fichier}"
        oled.text("CP>SD EXEC   RET" if sd_disponible else "      EXEC   RET", 1, 57)
    else:
        fichier_source, fichier_dest = f"/sd/{nom_fichier}", f"/{nom_fichier}"
        oled.text("CP>\ EXEC   RET" if sd_disponible else "     EXEC   RET", 1, 57)
          
    oled.show()
    time.sleep(0.5)
    
    while True:
        key = read_keys()
        if key == 'down' and sd_disponible:
            draw_header("FileManager")
            oled.text("Copie de...", 0, 20)
            oled.text(nom_fichier[:16], 0, 32)
            oled.show()
            
            if copier_fichier(fichier_source, fichier_dest):
                oled.text("Done !", 0, 48)
            else:
                oled.text("Echec copie", 0, 48)
            oled.show()
            time.sleep(2)
            break
        
        elif key == 'up':
            break
        
        elif key == 'select':    
            try:
                with open(fichier_source, "r") as f:
                    draw_header("FileManager")
                    oled.text("Execution de...", 0, 20)
                    oled.text(nom_fichier[:16], 0, 35)
                    oled.line(0, 50, 128, 50, 1)
                    oled.show()
                    time.sleep(0.5)
                    code = f.read()
                    exec(code, globals())
            except Exception as e:
                oled.fill(0)
                oled.text("ERREUR :", 0, 0)
                oled.text(str(e)[:16], 0, 16)
                oled.show()
                time.sleep(3)
            break
        time.sleep_ms(50)

# --- BOUCLE PRINCIPALE ---
sd_disponible = sd_available()
splash_screen()

# Choix de l'espace de stockage
storage = None
while storage is None:
    key_input = read_keys()
    if key_input == 'down':
        storage = "FLASH"
        files = [f for f in os.listdir("/") if f.endswith(".py")]
    elif key_input == 'up' and sd_disponible:
        storage = "SD"
        os.mount(sd, "/sd")
        files = [f for f in os.listdir("/sd") if f.endswith(".py")]
    time.sleep_ms(50)

files.sort()
selected_index = 0
afficher_menu()

# Boucle de navigation du menu
while True:
    key_input = read_keys()
    
    if key_input == 'up' and files:
        selected_index = (selected_index - 1) % len(files)
        afficher_menu()
        time.sleep_ms(200)  # Anti-rebond/ralentisseur de défilement
        
    elif key_input == 'down' and files:
        selected_index = (selected_index + 1) % len(files)
        afficher_menu()
        time.sleep_ms(200)
        
    elif key_input == 'select' and files:
        selected_file(files[selected_index])
        afficher_menu()  # Réaffiche le menu après action
        time.sleep_ms(200)
        
    time.sleep_ms(50)
