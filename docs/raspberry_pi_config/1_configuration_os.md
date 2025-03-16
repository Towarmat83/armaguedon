# Configuration OS Raspberry Pi 4 Model B

## Prérequis

* Poste de travail
* Carte MicroSD (minimum 16Go de stockage)
* Raspberry Pi 4 Model B 4Go RAM au minimum
* Adaptateur microSD

## Étapes de mise en place

### Depuis votre poste de travail, installer [Imager](https://www.raspberrypi.com/software/).

1. Sélectionner le modèle de Raspberry Pi
2. Sélectionner le système d'exploitation : Raspberry Pi OS (64-bits)
3. Sélectionner votre stockage

![Imager1](./assets/imager_1.png)

4. Appliquer les réglages de personnalisation de l'OS

![Imager2](./assets/imager_2.png)

**Important :** Dans l'onglet `Services`, ne pas oublier de configurer l'accès SSH par mot de passe pour simplifer les futures configurations. 

5. Enregistrer les modifications

Cette partie peut prendre quelques minutes.

### Votre microSD contient désormais un OS Debian (bootfs + rootfs)

[Continuer la configuration](./2_yubikey_basic_configuration.md)