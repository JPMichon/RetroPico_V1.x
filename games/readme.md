
## filemanager.py
Le programme filemanager.py est idéalement enregistré dans la mémoire Flash du RetroPico sous le nom de main.py (ce nom de fichier s'exécute automatiquement au démarrage).N'oubliez pas aussi de copier le répertoire /lib dans la Flash.Le programme FileManager permet de naviguer dans le répertoire racine de la carte MicroSD, puis de sélectionner et d'exécuter le programme MicroPython de votre choix.Les boutons P4 et P6 permettent de monter et descendre le curseur, et le bouton P5 permet de lancer le programme.La carte MicroSD doit obligatoirement être formatée en FAT32.

<img width="322" height="210" alt="image" src="https://github.com/user-attachments/assets/14f26b3f-6514-4073-9bbe-41a38137f779" />

## RetroPicoOS.py
Le programme RetroPicoOS.py est une version améliorée du FileManager. Il permet au choix de naviguer dans le système de fichiers (File System) de la Flash ou de la carte SD si elle est présente. Il permet également de copier des fichiers de la Flash vers la carte SD et vice-versa, en plus de pouvoir lancer les applications soit depuis la Flash, soit depuis la carte SD. Si vous sauvegardez le programme sous le nom de main.py dans la Flash, il s'exécutera automatiquement au démarrage du RetroPico.Autre note importante : vous aurez besoin de l'extension (Addon) I2C, car les deux applications requièrent un écran OLED et 3 boutons pour naviguer.
