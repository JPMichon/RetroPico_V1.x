from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep

# uncomment based on version of the PCB
# v1.0 
#_I2C_SDA = 16 # définition de Data du I2C(0) (GP16)
#_I2C_SCL = 17 # définition de SCL du I2C(0) (GP17)
# v1.1 
_I2C_SDA = 12 # définition de Data du I2C(0) (GP12)
_I2C_SCL = 13 # définition de SCL du I2C(0) (GP13)

i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)

# -----------------------------------
# Choisir la résolution du OLED
#
oled = SSD1306_I2C(128, 64, i2c)
#oled = SSD1306_I2C(128, 32, i2c)
#------------------------------------
#
#
#
# scan du bus I2C
#
#affichage la page d'accueil
oled.text('Scan i2c bus...', 10,25)
oled.show()
sleep(2) # attend 2sec
#efface l'ecran
oled.fill(0)
oled.show()

devices = i2c.scan()
pointeur=11 # permet d'incrémenter les lignes
if len(devices) == 0:
  oled.text('No i2c device !', 0,0)
  oled.show()  
else:
  oled.text('Device found:' +str(len(devices)), 3,1)
  oled.rect(0,0,128,10,1)
  oled.show()    
  for device in devices:  
    oled.text('Hex addr: '+str(hex(device)),0,pointeur)
    pointeur=pointeur+10
oled.show()   
#-------------------------------------------
# Registre des adresses i2c  
# 0x38  = AHT10/AHT20 temperature+humidity sensor
# 0x3c  = OLED SSD1306
# 0x40  = INA219 Current monitor
# 0x50  = EEPROM
# 0x68  = EEPROM
#
#------------------------------------------

