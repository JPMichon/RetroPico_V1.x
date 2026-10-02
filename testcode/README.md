## 🛠️ Validation du Matériel : Scripts de Test (`testcode/`)

Le dossier `testcode/` contient des scripts MicroPython autonomes conçus pour tester individuellement chaque bloc de la carte **retroPico v1.4** et de son **I2C Addon**. C'est l'outil idéal pour diagnostiquer vos soudures juste après l'assemblage.

### 🔌 Tests des fonctionnalités de Base
* **`Test_GP25.py`** : Fait clignoter la LED système de la carte mère pour valider le bon fonctionnement général du RP2040.
* **`Test_NeoPixel.py`** : Allume et fait varier les couleurs de la DEL RGB adressable (WS2812B) sur la broche `GP23` (ou connecteur `GP24`).
* **`Piezo_JukeBox.py`** : Génère des mélodies sur le buzzer magnétique de 4000 Hz (`GP6`) pour tester le circuit audio de base.
* **`Test_RetroPico.py`** : Script de diagnostic global du matériel.

### 🌐 Tests du Bus I2C et de l'Addon
* **`Scan_I2C_OLED.py`** : Scanne le bus I2C (`GP12`/`GP13`) et affiche la liste des adresses détectées directement sur l'écran OLED. Utile pour vérifier si le PCF8574 (`0x20`) ou l'OLED (`0x3C`) répondent.
* **`I2C_MeteoStation_OLED.py`** : Initialise le capteur d'environnement optionnel **AHT20 + BMP280** et affiche la température, l'humidité et la pression en temps réel.
* **`FlashSize_OLED.py`** : Interroge la puce QFlash et affiche ses caractéristiques sur l'écran d'extension.

### 📡 Tests de la connectivité Wi-Fi (Module ESP-01S)
* **`ESP01_ScanAP.py`** : Active le module ESP-01S via les broches de contrôle et liste les réseaux Wi-Fi environnants détectés.
* **`ESP01_NTP_OLED.py`** : Connecte le module au Wi-Fi, récupère l'heure exacte sur Internet via un serveur NTP et l'affiche sur l'OLED.
* **`ESP01_WebServer.py`** : Démarre un micro-serveur web sur le RP2040 grâce au module Wi-Fi, permettant de contrôler la carte depuis un navigateur ou un smartphone.

### 📺 Tests de la Sortie Vidéo (Interface VGA)
* **`Test_VGA_Mono.py`** : Valide le circuit vidéo en mode monochrome (noir et blanc) afin de vérifier la synchronisation HSYNC/VSYNC et le rendu de base sur un moniteur VGA.
* **`test_vga_RGB.py`** : Teste la génération des signaux de couleur (Rouge, Vert, Bleu) sur la prise VGA pour s'assurer que toutes les lignes de couleur et leurs résistances associées fonctionnent correctement.


### 📂 Dossier `/lib`
Le sous-dossier `lib/` inclus dans ce répertoire contient les pilotes indispensables (`ssd1306.py`, `pcf8574.py`, `sdcard.py`). Pensez à copier ce dossier complet sur la Flash de votre carte pour que tous les scripts de test s'exécutent sans erreur.

---

## 🚀 Outils Système et Interface Graphique (GUI)

Le répertoire inclut deux scripts avancés pour exploiter pleinement l'interface utilisateur de la carte :

**`FileManager.py`** : Le programme filemanager.py est idéalement enregistré dans la mémoire Flash du RetroPico sous le nom de main.py (ce nom de fichier s'exécute automatiquement au démarrage).N'oubliez pas aussi de copier le répertoire /lib dans la Flash.Le programme FileManager permet de naviguer dans le répertoire racine de la carte MicroSD, puis de sélectionner et d'exécuter le programme MicroPython de votre choix.Les boutons P4 et P6 permettent de monter et descendre le curseur, et le bouton P5 permet de lancer le programme.La carte MicroSD doit obligatoirement être formatée en FAT32.
  
**`RetroPicoOS.py`** : Le programme RetroPicoOS.py est une version améliorée du FileManager. Il permet au choix de naviguer dans le système de fichiers (File System) de la Flash ou de la carte SD si elle est présente. Il permet également de copier des fichiers de la Flash vers la carte SD et vice-versa, en plus de pouvoir lancer les applications soit depuis la Flash, soit depuis la carte SD. Si vous sauvegardez le programme sous le nom de main.py dans la Flash, il s'exécutera automatiquement au démarrage du RetroPico.Autre note importante : vous aurez besoin de l'extension (Addon) I2C, car les deux applications requièrent un écran OLED et 3 boutons pour naviguer.

> ⚠️ **Note importante** : L'utilisation de ces deux applications requiert obligatoirement le module d'extension **RetroPico I2C Addon**, car elles utilisent l'écran OLED et les 3 boutons physiques pour la navigation.

### ⚙️ Guide d'installation rapide
1. Installez le firmware officiel **MicroPython** (version Raspberry Pi Pico / RP2040) sur votre retroPico.
2. Copiez les bibliothèques requises (`ssd1306.py`, `pcf8574.py` et `sdcard.py`) dans le dossier `/lib` de votre carte.
3. Téléversez le script de votre choix (`RetroPicoOS.py` ou `FileManager.py`) à la racine de la Flash. 
4. *Optionnel* : Si vous souhaitez que l'interface se lance automatiquement au démarrage de la console, renommez le script choisi en **`main.py`** sur la Flash.
5. Connectez le module **RetroPico I2C Addon**, insérez une carte MicroSD (formatée en FAT) et démarrez l'ensemble !
