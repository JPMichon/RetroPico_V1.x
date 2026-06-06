#----------------------------------------------------------
#RetroPico v1.x diag tools
#
#
# Identification de la version du PCB permettant la configuration adéquate certains IOs
RetroPico_PCB_REV = 1.2
#---------------------------------------------------------
from machine import I2C, Pin, PWM
from ssd1306 import SSD1306_I2C
from pcf8574 import PCF8574
from time import sleep
import utime, array
import EEPROM_CAT24C64 #For 32bit or 4KB EEPROM library. Change this according to your library name.
import sdcard
import uos, os


#
# Configuration des Ports pour le RetroPico 1.x
# Configure les ports en fonction de la revision du PCB
if RetroPico_PCB_REV==1.0:
    # v1.0 
    _I2C_SDA = 16 # définition de Data du I2C(0) (GP16)
    _I2C_SCL = 17 # définition de SCL du I2C(0) (GP17)

else:
    # v1.1 
    _I2C_SDA = 12 # définition de Data du I2C(0) (GP12)
    _I2C_SCL = 13 # définition de SCL du I2C(0) (GP13)
    
    
# Configuration commune    
_System_LED = 25 # définition du port  del systeme (GP25)        
_ESP_EN = 8 # ESP01 Enable
_ESP_RST = 7 # ESP01 Reset
_ESP_IO0 = 10  # disponible sur les versions > 1.3
_ESP_IO2 = 9   # disponible sur les versions > 1.3
_Buzzer = 6 # définition du  buzzer (GP6)
_Neo_LED = 23 # définition du port NeoPixel (GP23)
_Neo_LED_nbr = 1 # nombre de neopixel sur le port 
_Neo_PIN = 24 # définition du port NeoPixel (GP24) disponible sur les versions > 1.4
_Neo_PIN_nbr = 1 # nombre de neopixel sur le port disponible sur les versions > 1.4
_MicroSD_SEL = 5
_MicroSD_SCK = 2
_MicroSD_MOSI = 3
_MicroSD_MISO = 4
_MicroSD_DETECT = 11 # disponible sur les versions > 1.3
_User_BTN = 26
_VGA_VSYNC = 19
_VGA_HSYNC = 21
_VGA_R = 16
_VGA_G = 17
_VGA_B = 18
_VGA_Mono = 18
_TX_Pin = 0 # Pin TX
_RX_Pin = 1 # Pin RX
_BAUDRATE = 115200 # Baud rate du UART
brightness = 0.1

# devices I2C
_EEPROM_ADDR_PCB = 0x50 # adresse du eeprom du PCB
_EEPROM_ADDR_ADDON = 0x51 # adresse du eeprom duI2C Addon Board
_ATH20 = 0x38 # adresse du capteur
_BPM280 = 0x77 # adresse du capteur
_SSD1306 = 0x3C # adresse de l'ecran OLED
_PCF8574AT= 0x20 # adresse du multiplexeur

# Dictionnaire des fréquences des notes
NOTES = {
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'RE6': 1175, 'MI6': 1319,
    'SILENCE': 0
}

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, BLACK)

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()
 
 
# Create the StateMachine with the ws2812 program, outputting on Pin(##).
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(_Neo_LED))
 
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
 
# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(_Neo_LED_nbr)])

def TestEEPROM(i2caddr):
    eeprom = EEPROM_CAT24C64.CAT24C64(i2c,i2caddr)
    print('########## Début du test #############')
    print("Device: "+ str(i2caddr))
    print()
    print("-Lecture d'un bloc-")
    # Read and print 32Bytes starting from memory address 0
    print(eeprom.read(0, 24))
    print("-Effacement du EEPROM-")
    eeprom.wipe()
    print("-Lecture d'un bloc-")
    # Read and print 32Bytes starting from memory address 0
    print(eeprom.read(0, 24))
    print("-Ecriture d'un bloc-")
    # Write String to memory address 0
    eeprom.write(0, 'RetroPico V1.0x')
    # Read and print 32Bytes starting from memory address 0
    print("-Lecture d'un bloc-")
    print(eeprom.read(0, 24))
    print("-Effacement du EEPROM-")
    eeprom.wipe()
    print('########## Fin du test #############')

def ScanI2C():
    print('####Liste des adresses du RetroPico et du I2C Addon Board#######')
    print('# 0x20  = PCF8574AT Multiplex 8 ports')
    print('# 0x38  = AHT20')
    print('# 0x3c  = OLED SSD1306')
    print('# 0x50  = EEPROM')
    print('# 0x51  = EEPROM on Addon Board')
    print('# 0x77  = BMP280')
    print('################################################################')
    print('Scan i2c bus...')
    print('')
    devices = i2c.scan()
    if len(devices) == 0:
          print('No i2c device !')
    else:
        print('Device found:' +str(len(devices)))
        for device in devices:  
            print('         Hex addr: '+str(hex(device)))
    print('--------------')         
    print('Fin du scan')    

def TestMicroSD():
    #cette sous routine teste le bon fonctionnement de la carte microSD
    MicroSD_Detect = Pin(_MicroSD_DETECT,Pin.IN)
    
    if MicroSD_Detect.value()==0 or RetroPico_PCB_REV < 1.3: # si la carte est présente, j'accède a la carte  
        CS = machine.Pin(_MicroSD_SEL, machine.Pin.OUT)
        spi = machine.SPI(0,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(_MicroSD_SCK),mosi=machine.Pin(_MicroSD_MOSI),miso=machine.Pin(_MicroSD_MISO))
        sd = sdcard.SDCard(spi,CS)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
        _temp = "Size:{} MB".format(sd.sectors/2048)
        print(_temp)
        print("Create file: RetroPico.log")

        with open("/sd/RetroPico.log", "w") as file:
            file.write("Welcome RetroPico World!\r\n\n")
            file.write("https://github.com/JPMichon/\r\n\n")
            file.write(b'RetroPico system environment\n\r')
            file.write(str(os.uname().machine))
            file.write(b' @ ')
            file.write(str(int((machine.freq()/1000000))))
            file.write(b' Mhz\n\r')
            file.write(str(os.uname().version))
        print("Saved")
                   
    else:
        print('Carte SD absente')

def play_level_up():
    buzzer = PWM(Pin(_Buzzer))
    
    # Suite rapide de notes ascendantes, se terminant par une note finale éclatante
    partition = ['SOL5', 'LA5', 'SI5', 'DO6', 'RE6', 'MI6']
    tempos = [0.06, 0.06, 0.06, 0.06, 0.06, 0.40]
    
    for note, duree in zip(partition, tempos):
        frequence = NOTES[note]
        
        if frequence == 0:
            buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            buzzer.freq(frequence)
            buzzer.duty_u16(32768)  # Volume optimal
            utime.sleep(duree)
        
        # Micro-pause minimale pour lier l'effet de montée
        buzzer.duty_u16(0)
        utime.sleep(0.01)
        
    buzzer.deinit()

def play_mario():
    Buzzer = PWM(Pin(_Buzzer))
    
    # Partition du thème principal de Mario
    partition = [
        'MI5', 'MI5', 'SILENCE', 'MI5', 'SILENCE', 'DO5', 'MI5', 'SILENCE',
        'SOL5', 'SILENCE', 'SOL4', 'SILENCE',
        'DO5', 'SILENCE', 'SOL4', 'SILENCE', 'MI4', 'SILENCE',
        'LA4', 'SILENCE', 'SI4', 'SILENCE', 'SIB4', 'LA4', 'SILENCE',
        'SOL4', 'MI5', 'SOL5', 'LA5', 'SILENCE', 'FA5', 'SOL5',
        'SILENCE', 'MI5', 'SILENCE', 'DO5', 'RE5', 'SI4'
    ]
    
    # Durées correspondantes (en secondes)
    tempos = [
        0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
        0.12, 0.36, 0.12, 0.36,
        0.18, 0.18, 0.18, 0.18, 0.18, 0.18,
        0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
        0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
        0.12, 0.12, 0.12, 0.12, 0.12, 0.24
    ]
    
    # Note intermédiaire manquante (le La bémol / Si bémol) ajoutée dynamiquement
    NOTES['SIB4'] = 466
    
    for note, duree in zip(partition, tempos):
        frequence = NOTES[note]
        
        if frequence == 0:
            Buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            Buzzer.freq(frequence)
            Buzzer.duty_u16(1500)  # Volume légèrement réduit pour les notes aiguës
            utime.sleep(duree)
            
        # Micro-pause obligatoire pour détacher les notes identiques qui se suivent
        Buzzer.duty_u16(0)
        utime.sleep(0.03)
        
    Buzzer.duty_u16(0)
    
    
def splashscreen():
    oled.text('RetroPico', 30,15)
    oled.text('RP2040', 40,25)
    oled.text('Diag Tools', 25,45)
    oled.text('V1.0', 90,55)
    oled.show()
    sleep(2) # attend 2sec
    oled.fill(0)
    oled.show()
    
def testGP25():
    GP25_led = Pin(_System_LED,Pin.OUT)
    GP25_led.value(0) # led GP25
    for i in range(10):
        GP25_led.toggle()
        utime.sleep(.2)
        
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(_Neo_LED_nbr)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    utime.sleep(.1)
    
def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
 
def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)
        
def flash_led_P7():
    pcf = PCF8574(i2c, address=_PCF8574AT)
    pcf.pin(7, 0)  # Allume (ou éteint selon le câblage de la LED)
    for i in range(20):
        pcf.toggle(7)
        utime.sleep(.2)
    
def testNEOPIXEL():
    for color in COLORS:
        pixels_fill(color)
        pixels_show()
        utime.sleep(.5)
        
def ReadUserButton():
    print("enfoncer le bouton noir")
    Ubutton = Pin(_User_BTN,Pin.IN)
    while Ubutton.value()==1:
        utime.sleep(.1)
    print("Détecté")    
    play_level_up()
    
        
def AfficheMenu():
    print('--------------')
    print('') 
    print('Liste des tests diponibles:')
    print('1 - Test du led GP25')
    print('2 - Test du led NEOPIXEL(GP23)')
    print('3 - Test de la carte MicroSD')
    print('4 - Test du Led P7 (Addon board)')
    print('5 - Test des boutons(Addon board)')
    print('6 - Scan du I2C')
    print("7 - Test du Piezo")
    print("8 - Test du EEPROM")
    print("9 - Test du EEPROM (I2C Addon board)")
    print("10 - User Button")
    print('--------------')            
#---------------------------------------------------------------------------
# Initialisation 
i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)
# -----------------------------------
# Choisir le modele de OLED
#
oled = SSD1306_I2C(128, 64, i2c)
#oled = SSD1306_I2C(128, 32, i2c)

#------------------------------------

#-------------------------------------------------------------------
splashscreen()

print('Cette application permet de tester les composantes du RetroPico')
print('-------------------------------------------------------------------')
print('')
while True:
    AfficheMenu()
    choice = input('Votre choix (1-10):')
    if choice=='1':
        print('Test du led GP25')
        testGP25()
    elif choice=='2':
        print('Test du led NEOPIXEL(GP23)')
        testNEOPIXEL()
    elif choice=='3':
        print('Test de la carte MicroSD')
        TestMicroSD()
    elif choice=='4':
        print('I2C Addon LED P7 flashing')
        flash_led_P7()
    elif choice=='5':
        print('*Le test des boutons est en boucle infinie, vous devrez redémarrer le programme')        
        testButons()
    elif choice=='6':
        print('Scan du port I2C')        
        ScanI2C()
    elif choice=='7':
        print("Test Piezo")        
        play_mario()
    elif choice=='8':
        print("Test du EEPROM")        
        TestEEPROM(_EEPROM_ADDR_PCB)
    elif choice=='9':
        print("Test du EEPROM (I2C Addon board)")        
        TestEEPROM(_EEPROM_ADDR_ADDON)
    elif choice=='10':
        print("User Button")           
        ReadUserButton()