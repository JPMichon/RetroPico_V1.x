
## filemanager.py
Le programme filemanager.py est idéalement enregistré dans la flash du RetroPico sous le nom de main.py (ce nom de ficher s'exécute automatiquement au démarrage)
N'oublier pas aussi de copier le repertoire /lib dans la flash. 

Le programme Filemanager permet de naviger dans le répertoire racine de la carte MicroSD et de sélectionner et d'executer le programme micropython de votre choix.
Les boutons P4 et P6 pour monter et dessendre le curseur et P5 pour lancer le programme.
La carte MicroSD doit obligatoirement être formater en FAT32.

<img width="322" height="210" alt="image" src="https://github.com/user-attachments/assets/14f26b3f-6514-4073-9bbe-41a38137f779" />

## RetroPicoOS.py
Le programme RetroPicoOS.py est une version ameliorer du filemanager. il permet aux choix de naviger dans le filesystem de la flash ou de la carteSD si présente et permet de copier des fichiers de la Flash vers la carteSD et vice-versa en plus de pouvoir lancer les applications soit de la flash ou de la carteSD. Si vous sauvegarder le programme sou sle nom de main.py dansla flash, il s'executera automatiquement au démarage du Retropico.

Autre note importante, cela vous prend le Addon I2C car les deux applcations requières un écran OLED et 3 bouttons pour naviguer.
