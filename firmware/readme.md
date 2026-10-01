# 💾 Compilation du Firmware Custom (MicroPython) pour RetroPico

Par défaut, utiliser le firmware officiel du Raspberry Pi Pico "vanille" limite l'espace de stockage Flash à **2 Mo**, même si votre carte intègre une puce de 4 Mo, 8 Mo ou 16 Mo. 

Pour exploiter pleinement la mémoire de votre **RetroPico**, vous devez compiler votre propre firmware en ajustant la taille déclarée du Qflash. Les fichiers de configuration de ce dossier sont configurés pour une mémoire de **4 Mo**.

## 🛠️ Prérequis

Avant de commencer, vous devez configurer l'environnement de compilation officiel de MicroPython pour les puces RP2.

1. Installez les dépendances de build de votre système (CMake, GCC ARM Toolchain).
2. Clonez le dépôt officiel de MicroPython :
   ```bash
   git clone --recursive https://github.com/micropython/micropython
   ```
      ```bash
   cd micropython
   ```
3. Compilez la mpy-cross (nécessaire pour le build final) :
   ```bash
   make -C mpy-cross
   ```

## 🚀 Procédure de Compilation pour RetroPico (4 Mo)

1. Allez dans le répertoire dédié au portage du RP2040 :
   ```bash
   cd ports/rp2
   ```
2. Créez un nouveau profil de carte en copiant les fichiers fournis dans ce dépôt sous un dossier nommé `RETROPICO` :
   ```bash
   mkdir boards/RETROPICO
   # Copiez-y les fichiers : mpconfigboard.h, mpconfigboard.cmake, pins.csv
   ```
3. Lancez la compilation en spécifiant le nom de votre carte personnalisée :
   ```bash
   make BOARD=RETROPICO
   ```
4. Une fois la compilation terminée, récupérez votre fichier **`firmware.uf2`** fraîchement créé dans le dossier de build.

## ⚡ Installation du Firmware
1. Maintenez le bouton **BOOT** enfoncé sur votre RetroPico.
2. Connectez la carte à votre ordinateur via le port **USB Type-C**.
3. Glissez-déposez le fichier `firmware.uf2` compilé dans le lecteur virtuel. La carte redémarrera automatiquement avec **4 Mo** de stockage interne disponibles pour vos scripts et vos jeux !

