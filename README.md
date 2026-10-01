# RetroPico_V1.x



## Compatibilité avec le projet Pico Micro Mac (pico-umac)

Ce projet permet de faire tourner l'émulateur de MAC 128K sur le PCB. A l'aide d'une simple modification Soit de retirer la résistance en reseau (RN1), uen résistance de 100ohm est installé en R19, SJ2 et SJ3 doivent être shorter.
https://github.com/evansm7/pico-mac



# 🕹️ retroPico (v1.4)

[![Licence](https://shields.io)](https://spdx.org)

**retroPico** est une plateforme matérielle open-source complète basée sur le microcontrôleur **Raspberry Pi RP2040**. Conçue pour l'émulation rétro, les projets vidéo/audio vintage et l'expérimentation, elle s'accompagne d'un écosystème modulaire comprenant une carte mère, une extension d'Entrées/Sorties (IO) I2C et un micro-système d'exploitation dédié.
Beaucoups de fonctionnalitées sur un minuscule PCB (60mm X 45mm).

En mode monochrome, la carte mère est entièrement compatible avec le célèbre projet d'émulation Macintosh [**pico-mac (pico-umac)** d'evansm7](https://github.com).

---

## 📌 Spécifications de la Carte Mère (v1.4)

La révision **v1.4 (Stable)** de la carte mère intègre les caractéristiques suivantes :

<img width="875" height="819" alt="image" src="https://github.com/user-attachments/assets/28c7ffd2-e0df-4d74-8cfb-f1193450a8a2" />

* **Cœur de calcul** : Microcontrôleur **RP2040** épaulé par une mémoire Flash de **de 2-16 Mo (W25QxxFVSG)**.
* **Affichage Vidéo** : Sortie **VGA** (connecteur DB15). Configuration rapide de l'affichage via trois ponts de soudure (`SJ1`, `SJ2`, `SJ3`) pour basculer facilement d'un rendu **Monochrome** à un rendu **RGB basique**.
* **Stockage** : Lecteur de carte **MicroSD (TF Card)** avec broche de détection automatique (*Card Detect*) routée sur `GP11`.
* **Connectivité Sans-Fil** : Emplacement pour module **ESP-01S (Wi-Fi)** exploitant les broches `GP9` et `GP10`.
* **Audio & Effets** : Un **Buzzer magnétique (4000Hz)** intégré et une LED RGB adressable **WS2812B (NeoPixel)** gérée sur `GP23`.
* **Extensions** : Connecteur NeoPixel externe (configuré sur `GP24`) et connecteur d'extension I2C.
* **Alimentation** : Connecteur **USB Type-C** (6 broches), fusible de protection de 500 mA et régulateur de tension **AMS1117-3.3V**.

---

## 📌 Table de Brochage des GPIO (Pinout Table)

Ce tableau récapitule l'affectation des broches du RP2040 au fil des révisions matérielles. Les zones grises indiquent qu'une option n'était pas disponible sur cette version.

| Fonctionnalité | Signal / Périphérique | v1.0 | v1.1 | v1.2 | v1.3 | v1.4 (Stable) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Indicateur** | System LED | < colspan=5 align=center> **GP25** |
| **Bouton** | User Button | < colspan=5 align=center> **GP26** |
| **Audio** | Buzzer | < colspan=5 align=center> **GP6** |
| **LED Adressable** | NeoPixel (PCB) | < colspan=5 align=center> **GP23** |
| | NeoPixel (Connecteur broche) | 🚫 | 🚫 | 🚫 | 🚫 | **GP24** |
| **Vidéo VGA** | VGA V-SYNC | < colspan=5 align=center> **GP19** |
| | VGA H-SYNC | < colspan=5 align=center> **GP21** |
| | VGA R (Rouge) | 🚫 | < colspan=4 align=center> **GP16** |
| | VGA G (Vert) | 🚫 | < colspan=4 align=center> **GP17** |
| | VGA B (Bleu) / Mode Mono | < colspan=5 align=center> **GP18 / Mono** |
| **Stockage SD** | MicroSD Select (CS) | < colspan=5 align=center> **GP5** |
| | MicroSD SCK | < colspan=5 align=center> **GP2** |
| | MicroSD MOSI | < colspan=5 align=center> **GP3** |
| | MicroSD MISO | < colspan=5 align=center> **GP4** |
| | MicroSD Detect | 🚫 | 🚫 | 🚫 | < colspan=2 align=center> **GP11** |
| **Bus I2C** | I2C SDA | < colspan=2 align=center> GP16 | < colspan=3 align=center> **GP12** |
| | I2C SCL | < colspan=2 align=center> GP17 | < colspan=3 align=center> **GP13** |
| **Extension Wi-Fi** | ESP Enable | < colspan=5 align=center> **GP8** |
| *(Module ESP-01S)* | ESP Reset | < colspan=5 align=center> **GP7** |
| | ESP TX | < colspan=5 align=center> **GP0** |
| | ESP RX | < colspan=5 align=center> **GP1** |
| | ESP IO0 | 🚫 | 🚫 | 🚫 | < colspan=2 align=center> **GP10** |
| | ESP IO2 | 🚫 | 🚫 | 🚫 | < colspan=2 align=center> **GP9** |

---

## 🔌 Module d'Extension : RetroPico I2C Addon (v1.1)

Pour enrichir l'interface utilisateur, le projet intègre un second PCB optionnel qui se connecte directement sur le port I2C principal : le **RetroPico I2C Addon**.

* **Interface Visuelle** : Support pour un écran **OLED SSD1306** connecté en I2C.
* **Entrées Utilisateur** : **3 boutons poussoirs** (`BTN1`, `BTN2`, `BTN3`) gérés via un extenseur de broches **PCF8574AT** (économie de broches sur le RP2040).
* **Capteurs Environnementaux** : Emplacement pour un capteur combiné température/humidité/pression **AHT20 + BMP280**.
* **Stockage embarqué** : Une mémoire EEPROM **CAT24Cxxx** dédiée au module.
* **Cavalier WRITE** : Permet de relier la broche `WP` (Write Protect) à la masse (GND) pour **autoriser l'écriture** sur l'EEPROM. Non court-circuité, l'EEPROM reste verrouillée en lecture seule.
* **Chaînage** : Intègre un port `I2C-INPUT` (protégé par un fusible) et **deux ports de sortie** (`I2C-OUT1`, `I2C-OUT2`) pour ajouter d'autres modules.

<img width="510" height="335" alt="image" src="https://github.com/user-attachments/assets/47bdc560-c56a-44de-9372-f5a676f50c30" />

## tableau des adresses I2C du module

<img width="256" height="154" alt="image" src="https://github.com/user-attachments/assets/037f8af3-744b-4097-852c-e45279ffd713" />

---

## 💻 Écosystème Logiciel (Firmwares supportés)

### 1. RetroPicoOS (MicroPython)
Un micro-système d'exploitation et gestionnaire de fichiers conçu sur mesure en **MicroPython** pour le combo *Carte Mère + I2C Addon*.
* **Gestionnaire de fichiers (FileManager)** : Liste et trie les scripts `.py` sur l'écran OLED.
* **Exécution dynamique** : Permet de naviguer avec les boutons physiques et de lancer directement un script en mémoire (`exec()`).
* **Copie Inter-Stockage** : Permet de dupliquer un fichier à la volée de la mémoire Flash interne vers la carte MicroSD (et vice-versa).
* **Diagnostic** : Calcule et affiche l'espace Flash total et disponible au démarrage.

### 2. Émulation Macintosh : pico-mac (C/C++)
Le matériel de la carte retroPico a été spécifiquement routé pour accueillir nativement le projet **pico-mac**.
* **Configuration** : Fermez le pont de soudure monochrome (`SJ1`) pour lier les lignes vidéo. 
* Le firmware d'origine s'associe automatiquement avec le brochage vidéo (`GP18`, `GP19`, `GP21`) et le lecteur SD de la carte retroPico.

---

## 📂 Structure du Dépôt

```text
├── hardware/
│   ├── main-board-retroPico/   # Schémas et Gerbers de la carte mère RP2040 (v1.4)
│   └── addon-i2c/              # Schémas et Gerbers du module d'extension IO (v1.1)
├── firmware/				    # Version Compilé de Micropython pour prendre en charge la taille de la Qflash
├── testcode/					# Code en Micropython permetant de tester les différentes composantes
└── games/          			# des jeux un micropython tournant sur le I2C Addon.
    
```

---

## 🚀 Démarrage Rapide avec RetroPicoOS

1. Installez le firmware officiel **MicroPython** (version Raspberry Pi Pico / RP2040) sur votre retroPico.
2. Copiez les bibliothèques requises (`ssd1306.py`, `pcf8574.py` et `sdcard.py`) dans le dossier `/lib` de votre carte.
3. Téléversez le script de **RetroPicoOS** sous le nom `main.py` à la racine de la Flash.
4. Connectez le module **RetroPico I2C Addon**, insérez une carte MicroSD (FAT) et démarrez l'ensemble !

---

## 🤝 Contributions

Les contributions (suggestions de boîtiers imprimés en 3D, optimisations de routage ou applications logicielles additionnelles) sont les bienvenues. N'hésitez pas à ouvrir une *Issue* ou à soumettre une *Pull Request*.

---

## 📜 Licence

Le matériel informatique de ce projet est publié sous licence **CERN Open Hardware Licence Version 2 - Weakly Reciprocal (CERN-OHL-W-2.0)**. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.
			


