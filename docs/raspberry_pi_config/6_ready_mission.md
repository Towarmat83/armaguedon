# Mise en place de la mission

## Prérequis

* [Configuration OS](1_configuration_os.md)
* [Configuration basique Yubikey](2_yubikey_basic_configuration.md)
* [Configuration LUKS](3_configuration_luks.md)
* [Configuration du login](4_login_authentication.md)
* [Configuration Service Détection / Cas critique](/docs/raspberry_pi_config/5_automatic_detection.md)


## Étapes de mise en place

### Votre Raspberry Pi est maintenant équipée, voici les étapes à suivre pour configurer correctement les configurations système à votre code métier.

Pour la réalisation de ce POC, notre code métier correspond à un timestamps s'écrivant toutes les secondes de manière sécurisée dans un fichier situé dans la partition LUKS. 

C'est le fichier [`log_script.py`](../../src/log_script.py).

Toutes les secondes, ce programme va écrire chiffré le timestamps dans le fichier `logs.txt`.
Pour assurer une sécurité optimale, une clé asymétrique est utilisée et c'est la clé publique qui est utilisée pour chiffrer la donnée. 

De ce fait, il est nécessaire de créer cette paire de clé asymétrique sur votre PC et non sur la Raspberry Pi. 
Il ne vous reste qu'à partager votre clé publique pour chiffrer la donnée durant la mission et à utiliser votre clé privée pour déchiffrer la donnée au retour de mission.

Le tout étant stocké sur la partition chiffrée LUKS dévérouillable uniquement via votre Yubikey. 

1. Création de la clé asymétrique sur votre PC

[Lien utile](https://support.yubico.com/hc/en-us/articles/360013790259-Using-Your-YubiKey-with-OpenPGP)

```bash
gpg --full-generate-key
# Sélectionner 1 (RSA and RSA)
# 4096
# 2y
# Saisir les informations manquantes

# Vérifier la présence de la clé publique et privée
gpg --list-keys
gpg --list-secret-keys
```

**Conseil :** Il n'est pas nécessaire d'importer la clé privée sur votre Yubikey comme réalisé dans le lien. 

2. Importer votre clé publique sur votre partition sécurisée LUKS

```bash
# Exporter la clé sur le PC
gpg --export --armor <ID_DE_TA_CLÉ> > public_key.asc

# Transférer votre clé publique dans votre partition sécurisée.
```

3. Lancement du code métier au dévérouillage de la session
```bash
# Ajouter dans le .bashrc à la fin du fichier
/usr/bin/python3 /mnt/log_script.py & 

# Ce code correspond à notre code pour notre POC
```

3. Désactivation du port Ethernet + micro-HDMI
```bash
# Création d'un crontab
sudo crontab -e

# Ajout de cette ligne à la fin du fichier
@reboot /sbin/ip link set dev eth0 down

# Modification du fichier config.txt
sudo vim /boot/firmware/config.txt

# Ajout de cette ligne
hdmi_blanking=1
```


4. Désactivation du port USB dès que la Yubikey est débranchée. 

* Reconnaissance du Bus utilisé
```bash
lsusb
# Résultat possible
# Bus 001 Device 004: ID 1050:0407 Yubico Yubikey 4
```

* Reconnaissance plus poussée
```bash
# Cette commande permet de contrôler tous le traffic pour les `usb`
sudo udevadm monitor --subsystem-match=usb --property

# Vérifier que ACTION = remove
# Vérifier que le PRODUCT correspond bien à 1050/407/XXX
```

* Création d'un [script sh](./conf/disable-usb-port.sh)
```bash
sudo vim /usr/local/bin/disable-usb-port.sh
```

* Rendre exécutable le script
```bash
sudo chmod +x /usr/local/bin/disable-usb-port.sh
```

* Création d'un [service](./conf/99-yubikey-remove.rules)
```bash
sudo vim /etc/udev/rules.d/99-yubikey-remove.rules
```
* Chargement de la règle
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```
* Rendre persistant cette étape à chaque redémarrage
```bash
# Ajout dans le crontab
sudo crontab -e

# Ajout de cette ligne à la fin du fichier
@reboot /usr/local/bin/disable-usb-port.sh
```


5. Désactivation du SSH pour limiter l'accès uniquement au TTY1.
```bash
sudo systemctl disable ssh
sudo systemctl stop ssh
```

6. Redémarrage complet pour tester
```bash
sudo reboot
```

### L'accès en SSH et par microHDMI sont désormais indisponibles.

### Vous êtes prêt à utiliser notre POC. 