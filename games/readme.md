
## filemanager.py
Le programme filemanager.py est idéalement enregistré dans la mémoire Flash du RetroPico sous le nom de main.py (ce nom de fichier s'exécute automatiquement au démarrage).N'oubliez pas aussi de copier le répertoire /lib dans la Flash.Le programme FileManager permet de naviguer dans le répertoire racine de la carte MicroSD, puis de sélectionner et d'exécuter le programme MicroPython de votre choix.Les boutons P4 et P6 permettent de monter et descendre le curseur, et le bouton P5 permet de lancer le programme.La carte MicroSD doit obligatoirement être formatée en FAT32.

<img width="322" height="210" alt="image" src="https://github.com/user-attachments/assets/14f26b3f-6514-4073-9bbe-41a38137f779" />

## RetroPicoOS.py
Le programme RetroPicoOS.py est une version améliorée du FileManager. Il permet au choix de naviguer dans le système de fichiers (File System) de la Flash ou de la carte SD si elle est présente. Il permet également de copier des fichiers de la Flash vers la carte SD et vice-versa, en plus de pouvoir lancer les applications soit depuis la Flash, soit depuis la carte SD. Si vous sauvegardez le programme sous le nom de main.py dans la Flash, il s'exécutera automatiquement au démarrage du RetroPico.Autre note importante : vous aurez besoin de l'extension (Addon) I2C, car les deux applications requièrent un écran OLED et 3 boutons pour naviguer.

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
