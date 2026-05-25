#--------------------------------------------------------
#RetroPico
# 
# Web server
# 
#
#                                  JP Michon 05/2026
#--------------------------------------------------------
"""
NOTE:
Les modules ESP-01(S) Sont assez capricieux et instable causé par la sensibilité aux fluctuations du VCC.
L'ajout d'un condensateur de découplage entre le VCC et le GND règle souvent les problèmes.     
Un condensateur electrolitique de 470uf 10V entre le VCC et le GND du module fait la job.
"""
# Identification de la version du PCB permettant la configuration adéquate certains IOs
RetroPico_PCB_REV = "1.1"


_Debugverbose = False
#-------------------------------------------------------

from machine import UART,Pin, I2C
import math
import utime
import time
import struct
from ssd1306 import SSD1306_I2C
from SECRET import _SSID, _WifiPWD
"""
Le fichier SECRET est dans le répertoire lib.
Il est constitué des deux lignes suivante:
_SSID = "SSID de votre réseau"
_WifiPWD = "Mot de passe du Wifi"
ceci permet de ne pas hardcoder le mot de passe dans le code.
"""
#
# Configuration des Ports pour le RetroPico 1.x
# Configure les ports en fonction de la revision du PCB
if RetroPico_PCB_REV=="1.0":
    # v1.0 
    _I2C_SDA = 16 # définition de Data du I2C(0) (GP16)
    _I2C_SCL = 17 # définition de SCL du I2C(0) (GP17)

else:
    # v1.1 
    _I2C_SDA = 12 # définition de Data du I2C(0) (GP12)
    _I2C_SCL = 13 # définition de SCL du I2C(0) (GP13)
    
    
# Configuration commune    
_Led_System = 25 # définition du port  del systeme (GP25)        
_ESP_EN = 8 # ESP01 Enable
_ESP_RST = 7 # ESP01 Reset
_Buzzer = 6 # définition du  buzzer (GP11)
_NeoPixel = 23 # définition du port NeoPixel (GP23)
_NeoPixel_nbr = 1 # nombre de neopixel sur le port
_EEPROM_ADDR = 0x50 # adresse du eeprom
_TX_Pin = 0 # Pin TX
_RX_Pin = 1 # Pin RX
_BAUDRATE = 115200 # Baud rate du UART
# --- CONFIGURATION Pour le time server ---
_NTPServer="pool.ntp.org"
#_NTPServer="time.google.com"
# ajustement du timezone en fonction de la localisation ou de l'heure d'ete
_TimeZone_Offset=4 #ajustement timezone GMT-4
#
#---------------------------------------------------------------------------
# Initialisation 
i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
rtc = machine.RTC() # j'initialise le RTC interne du Pico

# Initialize UART on Pico pour le ESP
uart = UART(0, baudrate=_BAUDRATE, tx=Pin(_TX_Pin), rx=Pin(_RX_Pin))
#Initialisation des PINs pour le controle du ESP
ESP01_EN = Pin(_ESP_EN,Pin.OUT) # ESP01 Enable
ESP01_RST = Pin(_ESP_RST,Pin.OUT) # ESP01 Reset
# -----------------------------------
# Choisir le type de OLED
#
oled = SSD1306_I2C(128, 64, i2c)
#oled = SSD1306_I2C(128, 32, i2c)
#------------------------------------
#

def _init_esp01():
    #active le ESP01 en resettant le ESP01 et en activant la pin enable
    ESP01_RST.value(0)  # reset
    utime.sleep(2.0) # reset 1sec
    ESP01_RST.value(1)  # reset
    utime.sleep(3.0)
    ESP01_EN.value(1) # enable ESP01
    
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
                print("Except!")
                #print(resp)
                
def _Print_AT_Firmware(uart=uart,timeout=3000):
    uart.write('AT+GMR\r\n')
    utime.sleep_ms(timeout)
    toto=_Wait_ESP_Rsp(uart, timeout)
    print("Version: "+ toto)
    
def _send_at(cmd, back='OK', timeout=3000):
    uart.write(cmd)
    if _Debugverbose:
        print("CMD: "+cmd)
    
    utime.sleep_ms(timeout)
    toto=_Wait_ESP_Rsp(uart, timeout)
    if _Debugverbose:
        print("test:",toto)
#---------------------------------------------------------------------
# code principale
#

oled.text('----------------', 0, 0)
oled.text('WEB Server', 25, 10)
oled.text('----------------', 0, 20)
oled.show()
_init_esp01() # initialisation du ESP
if _send_at('AT\r\n'):
    print("OK")

_Print_AT_Firmware()
_send_at('AT+CWMODE=1\r\n', timeout=2000)

oled.text("WiFi...", 0, 30)
oled.show()
print("Connexion au WiFi...")
if _send_at('AT+CWJAP="' + _SSID + '","' + _WifiPWD + '"\r\n',timeout=10000):
    print("Connecté !")
oled.text("OK", 80, 30)
oled.show()
# obtenir l'IP
uart.write('AT+CIFSR\r\n')
data = _Wait_ESP_Rsp(uart, timeout=2000)
print("IP:", data.split('"')[1])
oled.text('IP:'+data.split('"')[1], 0, 40)
oled.show()
print("MAC:", data.split('"')[-2])
print()
# demarre le webserver sur le port 80
print("Start Listening")
_send_at("AT+CIPMUX=1\r\n")
_send_at("AT+CIPSERVER=1,80\r\n")
print("loop")
oled.text("Server Listening", 0, 55)
oled.show()

while True:
    if uart.any() > 0:
        request = uart.read()
        print("Received:", request)    
        
        # 1. Check using bytes
        if b"+IPD" in request:
            print("Incoming Web Request detected!")
                
            # 2. Extract ID using bytes, then decode just the ID
            try:
                conn_id = request.split(b"+IPD,")[1].split(b",")[0].decode('utf-8')
            except (IndexError, ValueError):
                conn_id = "0"
                
            # 3. Clean, predictable HTML string
            html = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" \
                   "<!DOCTYPE html><html><body><h1>Hello from RetroPico!</h1></body></html>"
                
            # 4. Send length command
            _send_at(f"AT+CIPSEND={conn_id},{len(html)}\r\n")
            time.sleep(0.1)
                
            # 5. Send payload as bytes
            uart.write(html.encode('utf-8'))
            time.sleep(0.2)
                
            # 6. Close connection
            _send_at(f"AT+CIPCLOSE={conn_id}\r\n")