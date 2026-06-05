from machine import Pin, I2C
import time
import ssd1306
import ahtx0  # Importation de la bibliothèque officielle
from bmp280 import BMP280

# uncomment based on version of the PCB
# v1.0 
#_I2C_SDA = 16 # définition de Data du I2C(0) (GP16)
#_I2C_SCL = 17 # définition de SCL du I2C(0) (GP17)
# v1.1 
_I2C_SDA = 12 # définition de Data du I2C(0) (GP12)
_I2C_SCL = 13 # définition de SCL du I2C(0) (GP13)

i2c=I2C(0,sda=Pin(_I2C_SDA), scl=Pin(_I2C_SCL), freq=200000)


# initialisation ssd1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Initialisation de l'AHT20
capteur_aht = ahtx0.AHT20(i2c)

# Initialisation du BMP280
# Utilisation du mode WEATHER (Idéal pour baromètre : basse consommation, suréchantillonnage optimal)
capteur_bmp = BMP280(i2c, addr=0x77)

print("Système démarré")

while True:
    try:
        # Lecture de l'AHT20
        temp_aht = capteur_aht.temperature
        humidite = capteur_aht.relative_humidity
        
        # Lecture du BMP280 (Appel des propriétés de la classe personnalisée)
        # La pression retournée par cette bibliothèque est déjà convertie en Pascals (Pa). 
        # On divise par 100 pour obtenir des Hectopascals (hPa).
        pression_hpa = capteur_bmp.pressure / 1000.0
        
        # Nettoyage de l'écran OLED
        oled.fill(0)
        
        # Structure de l'affichage
        oled.text("STATION METEO", 12, 0)
        oled.text("----------------", 0, 10)
        
        # Affichage des mesures formatées à une décimale
        oled.text("Temp: {:.1f} C".format(temp_aht), 0, 24)
        oled.text("Humid: {:.1f} %".format(humidite), 0, 38)
        oled.text("Press: {:.1f} kPa".format(pression_hpa), 0, 52)
        
        # Actualisation de l'écran
        oled.show()
        
    except Exception as e:
        # Gestion des erreurs de bus I2C ou de déconnexion de capteur
        oled.fill(0)
        oled.text("Erreur Lecture", 5, 20)
        oled.text("Verif. Cablage", 5, 36)
        oled.show()
        print("Erreur détectée :", e)
        
    # Intervalle de rafraîchissement de 2 secondes
    time.sleep(2)