# RetroPico_V1.x
Un petit de développement basé sur un RP2040 comprenant un Port VGA, Wifi via un Module ESP-01, I2C, Lecteur MicroSD et plus.
Beaucoups de fonctionnalitées sur un minuscule PCB (60mm X 45mm).

<img width="1516" height="1355" alt="image" src="https://github.com/user-attachments/assets/b03b2323-4432-4850-8023-37b4b6e2cd66" />


## Compatibilité avec le projet Pico Micro Mac (pico-umac)

Ce projet permet de faire tourner l'émulateur de MAC 128K sur le PCB. A l'aide d'une simple modification Soit de retirer la résistance en reseau (RN1), uen résistance de 100ohm est installé en R19, SJ2 et SJ3 doivent être shorter.
https://github.com/evansm7/pico-mac



## L'alimentation:
En mode développement, l'alimentation ce fait par le connecteur USB Type-A situé en bas en utilisant un adapteur USB-A vers USB-C.

En mode autonome, l'alimentation ce fait via le connecteur USB-C situé en haut à droite et le port USB Type-A peut servire a connecter un périphérique comme une souris, clavier, manette de jeux etc.

## Assignation des IOs:
Le design a subit quelques modifications de design. Voici le tableau de l'assignation des ports en fonction des versions de PCB.
		
<img width="806" height="589" alt="image" src="https://github.com/user-attachments/assets/e96c0b7b-8d81-40d9-85a7-5135535c22ad" />


# RetroPico I2C Addon
Un module d'extension est en préparation permettant d'ajouter des entrées/Sorties et des modules I2C permettant de simplifier le dévelopepement.

<img width="1725" height="1100" alt="image" src="https://github.com/user-attachments/assets/1e9806a6-bb5b-4f73-8353-ba124eb9c725" />

