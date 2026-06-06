import time
import utime
from machine import UART, Pin

# Initialiser le port série (UART) sur le Pico
# Broches par défaut : GP0 (TX) et GP1 (RX)

_TX_Pin = 0 # Pin TX
_RX_Pin = 1 # Pin RX
_ESP_EN = 8 # ESP01 Enable
_ESP_RST = 7 # ESP01 Reset
_BAUDRATE = 115200 # Baud rate du UART
_Debugverbose = False

# Initialize UART on Pico pour le ESP
uart = UART(0, baudrate=_BAUDRATE, tx=Pin(_TX_Pin), rx=Pin(_RX_Pin), rxbuf=2048)
#Initialisation des PINs pour le controle du ESP
ESP01_EN = Pin(_ESP_EN,Pin.OUT) # ESP01 Enable
ESP01_RST = Pin(_ESP_RST,Pin.OUT) # ESP01 Reset

def _init_esp01():
    #active le ESP01 en resettant le ESP01 et en activant la pin enable
    ESP01_RST.value(0)  # reset
    utime.sleep(2.0) # reset 1sec
    ESP01_RST.value(1)  # reset
    utime.sleep(3.0)
    ESP01_EN.value(1) # enable ESP01
    
def _send_at(cmd, back='OK', timeout=3000):
    uart.write(cmd)
    utime.sleep_ms(timeout)
    toto=_Wait_ESP_Rsp(uart, timeout)
    print(toto)

def _Wait_ESP_Rsp(uart=uart, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    try:
            return resp.decode()
    except UnicodeError:
            if _Debugverbose:
                print(resp)

def afficher_reseaux_wifi(reponse_at):
    print(reponse_at)
    # En-tête mis à jour avec toutes les colonnes possibles
    print(f"{'SSID (Nom)':<20} | {'RSSI':<8} | {'BSSID (MAC)':<18} | {'Canal':<6} | {'Sécurité (ECN)':<15} | {'Offset/Calval':<13}")
    print("-" * 92)

    # Dictionnaire pour traduire le type de sécurité (ECN)
    secu_types = {
        "0": "Ouvert", "1": "WEP", "2": "WPA_PSK", 
        "3": "WPA2_PSK", "4": "WPA_WPA2_PSK",
        "5": "WPA2_Enterprise", "6": "WPA3_PSK", "7": "WPA2_WPA3_PSK"
    }

    # Traignement ligne par ligne
    for ligne in reponse_at.split("\n"):
        if "+CWLAP:(" in ligne:
            try:
                # Extraction du contenu entre les parenthèses
                contenu = ligne.split("(")[1].split(")")[0]
                donnees = [param.strip().strip('"') for param in contenu.split(",")]
                
                # Assignation dynamique selon le nombre d'éléments renvoyés par le module
                # Format standard complet (7 éléments) ou simplifié (5 éléments)
                ecn_code = donnees[0]
                ssid = donnees[1] if donnees[1] else "<Masqué>"
                rssi = donnees[2] + " dBm"
                bssid = donnees[3]
                canal = donnees[4]
                
                # Gère l'affichage si les options de fréquence spécifiques (6 et 7) sont absentes
                freq_info = f"{donnees[5]}/{donnees[6]}" if len(donnees) >= 7 else "-"
                
                # Traduction du protocole de sécurité
                securite = secu_types.get(ecn_code, f"Inconnu ({ecn_code})")
                
                # Affichage aligné dans le tableau
                print(f"{ssid:<20} | {rssi:<8} | {bssid:<18} | {canal:<6} | {securite:<15} | {freq_info:<13}")
                
            except (IndexError, ValueError):
                # Ignore les lignes mal formées ou coupées
                continue    

#Initialise le module, le met en mode Station et scanne les réseaux.
print("Initialisation de l'ESP-01S...")

_init_esp01() # initialisation du ESP    
# 1. Vérifier si l'ESP répond
_send_at('AT\r\n', timeout=2000)

    
# 2. Configurer le mode Wi-Fi sur Station (1)
print("Configuration en mode Station...")
_send_at('AT+CWMODE=1\r\n', timeout=2000)

    
# 3. Lancer la commande de scan des réseaux (AT+CWLAP)
print("Recherche des réseaux Wi-Fi (2.4GHz 802.11 b/g/n) (Veuillez patienter quelques secondes)...")
#_send_at('AT+CWLAP\r\n', timeout=10000)
uart.write('AT+CWLAP\r\n')
utime.sleep_ms(8000)
# 4. Afficher et filtrer les résultats
afficher_reseaux_wifi(_Wait_ESP_Rsp(uart,5000))




