# Authentification du Login pour Raspberry Pi 4 Model B 

## Prérequis

* [Configuration OS](1_configuration_os.md)
* [Configuration basique Yubikey](2_yubikey_basic_configuration.md)
* [Configuration LUKS](3_configuration_luks.md)
* Cable microHDMI
* Clavier

## Étapes de mise en place


### Seul l'accès via TTY1 doit être activé sur la Raspberry Pi, ce document vous permet de configurer correctement l'accès au terminal.

1. Retirer l'interface graphique et les différents TTY (TeleTYpewriter)

```bash
sudo systemctl disable lightdm
sudo systemctl stop lightdm

sudo nano /etc/systemd/logind.conf

# Modifier ces deux lignes
NAutoVTs=1
ReserveVT=1

sudo systemctl daemon-reexec

# Vérifier que la Raspberry Pi démarre bien en mode console (CLI)
sudo systemctl set-default multi-user.target

# Redémarre la Raspberry Pi
sudo reboot
```

Brancher votre cable mircoHDMI et votre clavier, l'autologin de la raspberry Pi devrait directement vous connecter sans demander de mot de passe, la session devrait etre ouverte.
Les tty2 à 7 devraient être indisponibles. (ATL + F2, etc...)

2. Vérifier que l'interface tty1 esy en mode CLI 

Cela permet d'avoir une seule et unique console, sans interface graphique, rendant donc plus simple à protéger et à contrôler.

```bash
# Vérifier que aucun fichier n'existe dans /etc/systemd/system/getty@tty1.service.d/
ls /etc/systemd/system/getty@tty1.service.d/

# Créer le fichier 'autologin.conf' si aucun fichier n'existe sinon override le ficher existant
sudo vim /etc/systemd/system/getty@tty1.service.d/autologin.conf
```

Remplir ce fichier avec le contenu suivant:
```bash
[Service]
ExecStart=
ExecStart=-/sbin/agetty -o '-p -- username' --noclear --skip-login -  %I $TERM

# Remplacer le nom de l'utilisateur par celui que vous souhaitez
```

Ce fichier permet de configurer l'interface tty1 en mode CLI uniquement et de demander le mot de passe sans demander le login.

```bash
# Recharger la configuration et rédemarrer la Raspberry Pi
sudo systemctl daemon-reload
sudo reboot
```

### Dans cette configuration, dès la mise sous tension de la Raspberry Pi, l'interface tty1 sera automatiquement configurée en mode CLI et demandant le mot de passe de l'utilisateur 'username' pour acceder au terminal.


3. Mettre en place l'authentification via Yubikey

[Tutoriel utile](https://sysadmin102.com/2023/07/enable-2-factor-authentication-2fa-or-passwordless-on-kali-linux-with-the-yubikey/)

Créer ce dossier sur la Raspberry Pi
```bash
mkdir -p ~/.config/Yubico
```

Associer la Yubikey
```bash
pamu2fcfg > ~/.config/Yubico/u2f_keys
# La Yubikey clignote, veuillez la toucher.
```

Associer la seconde Yubikey
```bash
pamu2fcfg -n >> ~/.config/Yubico/u2f_keys
# La Yubikey clignote, veuillez la toucher.
```



Modifier ce fichier:

```bash
sudo vim /etc/pam.d/login 
```

Ajouter cette ligne à la ligne 55.

```bash
auth required pam_u2f.so cue [cue_prompt="Tap the YubiKey to authenticate"]
```

Mettre en commentaire la ligne suivante (située juste en dessous): 

```bash
#@include common-auth
```

Redémarrer la Raspberry Pi pour tester la fonctionnalité:
```bash
sudo reboot
```

### Dans notre cas précis, l'authentification via Yubikey est activée, ce qui permet de se connecter sans mot de passe et uniquement en touchant la YubiKey. 


[Continuer la configuration](./5_automatic_detection.md)



