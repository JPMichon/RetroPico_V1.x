# 🕹️ RetroPico (v1.x)

[English version available here](./README.EN.md)

**retroPico** est une plateforme matérielle open-source complète basée sur le microcontrôleur **Raspberry Pi RP2040**. Conçue pour l'émulation rétro, les projets vidéo/audio vintage et l'expérimentation, elle s'accompagne d'un écosystème modulaire comprenant une carte mère, une extension d'Entrées/Sorties (IO) I2C et un micro-système d'exploitation dédié.<br>

> [!NOTE]
>_Ne soyez pas trop critique avec mes choix de conception et mes schématique qui relève du hobbisme. mes études en électronique remonte a plus de 40 ans et je n'ai jamais travailler en conception. ce projet est un défi personnel afin de me prouver que je maitrise encore un minimum de connaissance pour bricoler en électronique avec des composantes moderne. l'époque du Z80 monter sur un "protoboard" avec un sept segments, un eprom 2716, 2k de SDRAM et de surcroit coder en assembleur, semble tout droit venir de l'époque paléolithique._


⚠️  Vous comprendrez que ce PCB est de niveau lobbyistes, il n'est pas conçu pour intégrer des projets commerciaux. 

---

<img width="791" height="692" alt="image" src="https://github.com/user-attachments/assets/3cb99a51-60bd-45b2-b1b3-6a16bee65eb3" />

Version 1.3 sur la photo. 

---

_⚠️ **Important :** Je rend disponible le fichier Gerber du PCB vous permettant l'assemblage du **retroPico** ce qui requière une certaine expérience et dextérité. Néanmoins, il est possible d'utiliser un Raspberri PI Pico vanille et un panneau de prototypage pour obtenir un équivalent fonctionnel._

---

## 🤖 Assistant de Codage IA

Si vous utilisez un agent IA (comme ChatGPT, Claude ou GitHub Copilot) pour vous aider à développer des scripts pour la retroPico, copiez-collez le contenu de notre [Tuteur RetroPico](RETROPICO_MENTOR_PROMPT.md). Il configurera l'IA avec toutes les broches et adresses exactes de la carte pour vous guider pas à pas sans faire d'erreurs matérielles !

---

## 📌 Spécifications de la Carte Mère (v1.4)

Plusieurs révisions on été crée lors du développement. la version la plus abouti est la version 1.4. Les versions antérieurs sont en nombres très limités, c'est pour cette raison que je conserve ici l'historique du développement.

<img width="435" height="410" alt="image" src="https://github.com/user-attachments/assets/28c7ffd2-e0df-4d74-8cfb-f1193450a8a2" />

La révision **v1.4 (Stable)** de la carte mère intègre les caractéristiques suivantes :
* **Cœur de calcul** : Microcontrôleur **RP2040** épaulé par une mémoire Flash de **de 2-16 Mo (W25QxxFVSG)**.
* **Affichage Vidéo** : Sortie **VGA** (connecteur DB15). Configuration rapide de l'affichage via trois ponts de soudure (`SJ1`, `SJ2`, `SJ3`) pour basculer facilement d'un rendu **Monochrome** à un rendu **RGB basique**.
* **Stockage** : Lecteur de carte **MicroSD (TF Card)** avec broche de détection automatique (*Card Detect*) routée sur `GP11`.
* **Connectivité Sans-Fil** : Emplacement pour module **ESP-01S (Wi-Fi)** exploitant les broches `GP9` et `GP10`.
* **Audio & Effets** : Un **Buzzer magnétique (4000Hz)** intégré et une LED RGB adressable **WS2812B (NeoPixel)** gérée sur `GP23`.
* **Extensions** : Connecteur NeoPixel externe (configuré sur `GP24`) et connecteur d'extension I2C.
* **Alimentation & Connectivité** : Connecteur **USB Type-C** (6 broches) équipé d'un fusible de protection de 500 mA et d'un régulateur de tension **AP2114H-3.3**. Ce port USB femelle prend en charge le mode **USB Host**, permettant de connecter directement un **clavier standard** ou une **manette de jeu (Gamepad)** pour interagir avec vos programmes et émulateurs.

**Beaucoups de fonctionnalitées pour un minuscule PCB (60mm X 45mm).**

## 🛠️ Guide de Dépannage Matériel (Troubleshooting)

L'assemblage du **retroPico** est un défit en soit, le premier démarrage d'un PCB est l'épreuve ultime. Que vous soyez un constructeur chevronné ou que vous fassiez vos premiers pas avec le **RP2040**, les erreurs de soudure ou les composants capricieux font partie du processus.

Pour vous accompagner, le dépôt inclut un organigramme complet basé sur de nombreuses sessions de débogage réelles :

👉 **[Consulter le RetroPico RP2040 PCB Debug Flow](./hardware/RetroPico_DebugPCB.pdf)** 

## Spécificité du port VGA

 La RetroPico peut être configuré soit en mode monochrome ou en 3 bits permettant l'affichage de 8 couleurs 
 **Configuration couleur 3bits ou mode mono** : Le passage en mode mono ou couleur ce fait en changeant les points de soudure de **SJ1, SJ2 et SJ3**. 

Le port VGA du RetroPico utilise la technique de ce projet  [PICO-VGA-Micropython par HughMaingauche](https://github.com/HughMaingauche/PICO-VGA-Micropython/blob/main/VGA.py) tout en y ajoutant la possibilité de fonctionner en mode monochrome afin de libérer encore plus de RAM pour les projets.

En mode couleur, le buffer requière environ 120k de ram ce qui vous laisse environ 50k pour le programme.
en mode monochrome, la taille du buffer est d'environ 40k vous donnant beaucoup plus de latitude.
  
il est possible d'utiliser le port VGA en **MicroPython** bien que cette solution n'est pas optimale, quand mes tests seront terminés, j'ajouterais les exemples dans le répertoire **testcode**.  


---

## 📌 Table de Brochage des GPIO (Pinout Table)

Ce tableau récapitule l'affectation des broches du RP2040 au fil des révisions matérielles. Les zones grises indiquent qu'une option n'était pas disponible sur cette version.

<img width="730" height="568" alt="image" src="https://github.com/user-attachments/assets/1c53badb-5805-4934-ac96-cc5509bbca45" />

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

### 2. Portages et Émulation (C/C++)
La retroPico est une plateforme de développement polyvalente et versatile. Grâce à son port VGA intégré permettant un affichage monochrome ou en 8 couleurs (RGB basique), elle constitue une base matérielle idéale pour porter de nombreux autres émulateurs existants conçus pour le Raspberry Pi Pico (consoles 8/16-bit, ordinateurs vintage, etc.).

À titre d'exemple, son architecture lui permet d'accueillir nativement le projet de Matt Evans permettant de faire tourner un émulateur de Macintosh 128K/Plus sur le RP2040 :

* **Lien du projet d'origine** : [pico-mac (pico-umac) par evansm7](https://github.com/evansm7/pico-mac)
* **Démonstration Vidéo** : Vous pouvez visionner la vidéo complète de Jeff Geerling qui détaille l'installation et le rendu de cet émulateur sur le RP2040 : [Macintosh on a microcontroller (YouTube)]([https://youtube.com](https://www.youtube.com/watch?v=-gOS22wEpmU)).
* **Configuration en mode mono** : Le passage en mode mono ou couleur ce fait en changeant les points de soudure de **SJ1, SJ2 et SJ3**

### 3. Retro gaming plateform
A la base l'idée était de crée un projet doté d'une bonne flexibilité tant pour l'apprentissage qu'une base pour l'émulation rétro.
un simple recherche web avec les termes "**rp2040 retro emulator**" vous obtiendrez une multitude de projet de toutes sortes qu'il serait trop long a énumérer ici.

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

## 🎓 Accessibilité & Compatibilité avec le Raspberry Pi Pico

Si vous débutez en programmation ou en électronique, ne soyez pas intimidés ! Bien que la **RetroPico** intègre de nombreux composants sur un seul circuit imprimé (VGA, Wi-Fi, MicroSD, etc.), **son cœur reste un Raspberry Pi Pico standard**. 

Il y a en réalité **très peu de différences** fondamentales entre cette carte et un Pi Pico classique :
* **Même puce :** Le microcontrôleur principal est le RP2040. Tout code écrit pour un Pico standard fonctionnera ici.
* **Mêmes bases :** La logique de programmation, l'utilisation des broches (GPIO) et l'environnement restent identiques.

### 📚 Ressources pour les débutants

Puisque l'architecture est la même, vous pouvez utiliser à 100 % les guides, tutoriels et documentations officiels de la fondation Raspberry Pi pour apprendre à programmer votre RetroPico. 

Pour faire vos premiers pas, nous vous recommandons vivement le guide officiel :
👉 **[Getting started with the Raspberry Pi Pico (Raspberry Pi Projects)](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico)**

Ce guide vous apprendra pas à pas à :
1. Installer et configurer l'environnement de développement **Thonny**.
2. Connecter votre carte à votre ordinateur et y installer le micrologiciel **MicroPython**.
3. Écrire vos premiers scripts pour contrôler des entrées et des sorties.

Une fois que vous aurez compris les bases du clignotement d'une LED ou de la lecture d'un bouton avec ce guide, l'écosystème de la **RetroPico** et ses scripts de test (`testcode/`) vous permettront d'aller beaucoup plus loin (affichage graphique, son, jeux et réseau) sans changer de méthode de travail !

---

## 🚀 Démarrage Rapide avec RetroPicoOS (interface GUI)

L'application **RetroPicoOS**  permet au choix de naviguer dans le système de fichiers (File System) de la Flash ou de la carte SD si elle est présente. Il permet également de copier des fichiers de la Flash vers la carte SD et vice-versa, en plus de pouvoir lancer les applications soit depuis la Flash, soit depuis la carte SD. Si vous sauvegardez le programme sous le nom de main.py dans la Flash, il s'exécutera automatiquement au démarrage du RetroPico.Autre note importante : vous aurez besoin de l'extension (Addon) I2C, car les deux applications requièrent un écran OLED et 3 boutons pour naviguer.

1. Installez le firmware officiel **MicroPython** (version Raspberry Pi Pico / RP2040) sur votre retroPico.
2. Copiez les bibliothèques requises (`ssd1306.py`, `pcf8574.py` et `sdcard.py`) dans le dossier `/lib` de votre carte.
3. Téléversez le script de **RetroPicoOS** sous le nom `main.py` à la racine de la Flash.
4. Connectez le module **RetroPico I2C Addon**, insérez une carte MicroSD (FAT) et démarrez l'ensemble !

---

## 🎮 Logithèque : Les Jeux RetroPicoOS

Pour tester immédiatement les capacités matérielles du combo *RetroPico v1.4 + I2C Addon*, le dépôt intègre une suite de jeux rétro écrits en MicroPython. Ils utilisent l'écran OLED pour le rendu graphique et l'extenseur PCF8574 pour récupérer les actions des boutons.

### Jeux inclus dans le dépôt :
* **🚀 RetroPico_SpaceInvader.py** : Le grand classique spatial. Survivez aux vagues d'extraterrestres !
* **🛡️ RetroPico_SpaceCombat.py** : Un jeu de combat et d'esquive de tirs dans l'espace.
* **🌕 RetroPico_MoonLander_V2.py** : Dosé à la perfection. Utilisez vos propulseurs pour faire alunir votre module en douceur.
* **🧱 RetroPico_Breakout.py** : Un jeu de casse-briques dynamique exploitant les boutons pour déplacer la raquette.
* **🏓 RetroPico_PongGame.py** : L'indémodable jeu de tennis virtuel.
* **💥 RetroPico_Artillery.py** : Calculez votre angle de tir et votre puissance pour détruire la cible adverse.
* **🌀 RetroPico_GameofLife.py** : Une simulation graphique fluide du célèbre Jeu de la Vie de Conway.
* **🕹️ RetroPico_Pinball.py** : Une adaptation compacte de flipper sur écran OLED.

### 🕹️ Comment jouer ?
1. Copiez les fichiers `.py` des jeux de votre choix sur une carte **MicroSD (formatée en FAT32)** ou directement dans la mémoire Flash interne du RP2040.
2. Démarrez la console et sélectionnez votre espace de stockage (`FLASH` ou `SD`).
3. Naviguez dans la liste à l'aide des boutons **Haut (P4)** et **Bas (P6)**.
4. Appuyez sur **Sélection (P5)** sur le jeu choisi : `RetroPicoOS` chargera le code dynamiquement et lancera la partie !

---

## 📜 Licence

Le matériel (fichiers de conception, schémas, typons) et les logiciels de ce projet sont mis à disposition selon les termes de la Licence **Creative Commons Attribution - Pas d'Utilisation Commerciale - Partage dans les Mêmes Conditions 4.0 International (CC BY-NC-SA 4.0)**.

❌ **L'utilisation commerciale de ce projet (revente de PCBs nus, kits ou cartes retroPico assemblées) est strictement interdite sans autorisation préalable de l'auteur.**

Consultez le fichier [LICENSE](LICENSE) pour lire l'intégralité des termes.

## ☕ Soutenir le projet

Si vous appréciez mon travail et souhaitez m'offrir un café pour me soutenir bénévolement dans mes futurs projets de soudure et de code, vous pouvez me laisser un pourboire sur Ko-fi. C'est entièrement volontaire et grandement apprécié !
			


