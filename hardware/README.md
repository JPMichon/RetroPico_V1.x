# 🛠️ Matériel & Circuits Imprimés (Hardware) - RetroPico

Ce répertoire regroupe l'intégralité des fichiers de conception matérielle de l'écosystème **RetroPico**. Vous y trouverez les schémas électriques, les fichiers de fabrication Gerber ainsi que la liste des composants nécessaires pour assembler votre propre console de développement rétro.

## 📂 Structure du Répertoire

Le dossier est divisé en sous-modules correspondant aux différentes cartes du projet :

* **`main-board-retroPico/`** : Fichiers sources de la carte mère principale basée sur le microcontrôleur RP2040 (Révision stable v1.4).
* **`addon-i2c/`** : Fichiers de conception de la carte fille d'extension d'Entrées/Sorties comprenant l'écran OLED, les boutons et les capteurs (Révision v1.1).

---

## 📐 Schémas Électriques & Fabrication (Gerber)

Pour permettre une consultation rapide et simplifier la commande de vos circuits imprimés (PCB) chez des fabricants comme JLCPCB, PCBWay ou d'autres, les fichiers de production ont été exportés et centralisés ci-dessous :

### 🕹️ 1. Carte Mère Principale (v1.4)
* **Schéma PDF :** [Consulter le schéma de la Carte Mère](Schematic_uRetroputer_1.4.pdf) *(Assurez-vous de nommer votre PDF ainsi dans le dossier)*
* **Production PCB :** 📦 **[Télécharger le fichier Gerber ZIP de la Carte Mère](PCB_uRetroputer_V1.4_2026-06-14.zip)**

### 🔌 2. Module d'Extension I2C Addon (v1.1)
* **Schéma PDF :** [Consulter le schéma de l'I2C Addon](Schematic_I2C-IO_Board_1.1.pdf) *(Assurez-vous de nommer votre PDF ainsi dans le dossier)*
* **Production PCB :** 📦 **[Télécharger le fichier Gerber ZIP de l'I2C Addon](Gerber_I2C-IO_Board_PCB_I2C-IO_Board_V1.1.zip)**

> 📥 **Comment commander vos PCB ?** Téléchargez le fichier `.zip` correspondant à la carte souhaitée et téléversez-le directement sur le site de votre fabricant de circuits imprimés favori sans le décompresser.

---

## 📋 Liste des Composants (BOM - Bill of Materials)

Pour vous faciliter l'approvisionnement des composants électroniques nécessaires à l'assemblage de la carte mère, une nomenclature officielle et datée est disponible en libre téléchargement :

👉 **[Consulter le fichier de nomenclature (CSV)](BOM_RetroPico_v1.4_2026-10-01.csv)**

### 📌 Composants stratégiques de la Carte Mère v1.4

| Catégorie | Composant / Référence | Boîtier / Spécificité | Rôle sur la RetroPico |
| :--- | :--- | :--- | :--- |
| **Cœur** | Microcontrôleur **RP2040** | QFN-56 | Microcontrôleur principal double cœur. |
| **Mémoire** | Flash **W25QxxFVSG** | SOIC-8 | Stockage du code et du système (2 à 16 Mo supportés). |
| **Alimentation** | Régulateur **AP2114H-3.3** | SOT-223 | Convertisseur de tension linéaire pour un 3.3V stable. |
| **Sécurité** | Fusible réarmable PTC 500mA | 1206 (SMD) | Protection du bus d'alimentation USB-C. |
| **Vidéo** | Connecteur VGA Femelle | DB15 Traversant | Sortie écran analogique (Monochrome ou 8 couleurs). |
| **Sans-fil** | Connecteur femelle 2x4 | Pas de 2.54 mm | Accueil du module Wi-Fi ESP-01S. |
| **Audio/Visuel**| LED RGB Adressable **WS2812B** | SMD 5050 | Indicateur lumineux d'état (NeoPixel interne). |
| **Audio** | Buzzer magnétique | 4000 Hz | Génération d'effets sonores et de musique 8-bits. |

---

## ⚠ Note importante sur l'assemblage

Le soudage de la carte mère **RetroPico** requiert une certaine expérience en microsoudure de composants montés en surface (CMS/SMT), notamment pour le boîtier QFN-56 du RP2040 et le port USB Type-C. 

En cas de problème au premier démarrage, référez-vous au guide de dépannage de la page principale :

👉 **[RetroPico RP2040 PCB Debug Flow](RetroPico_DebugPCB.pdf)**
