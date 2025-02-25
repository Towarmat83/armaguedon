# Login Authentication for Raspberry Pi 4 Model B 

### Seul l'accès via micro-HDMI est activé sur la Raspberry Pi, ce document vous permet de configurer correctement l'accès au terminal.

1. Retirer l'interface graphique et les différents TTY (TeleTYpewriter)

```bash
sudo systemctl disable lightdm
sudo systemctl stop lightdm

sudo systemctl disable getty@tty2
sudo systemctl disable getty@tty3
sudo systemctl disable getty@tty4
sudo systemctl disable getty@tty5
sudo systemctl disable getty@tty6

sudo systemctl stop getty@tty2
sudo systemctl stop getty@tty3
sudo systemctl stop getty@tty4
sudo systemctl stop getty@tty5
sudo systemctl stop getty@tty6


# Vérifier que la Raspberry Pi démarre bien en mode console (CLI)
sudo systemctl set-default multi-user.target

# Redémarre la Raspberry Pi
sudo reboot
```

Le tty2 à 7 devrait être indisponible.

2. Configurer l'interface tty1 en mode CLI uniquement

Cela permet d'avoir une seule et unique console, sans interface graphique, rendant donc plus simple à protéger et à contrôler.

```bash
# Vérifier que aucun fichier n'existe dans /etc/systemd/system/getty@tty1.service.d/
ls /etc/systemd/system/getty@tty1.service.d/

# Créer le fichier 'autologin.conf' si aucun fichier n'existe sinon override le ficher existant
sudo nano /etc/systemd/system/getty@tty1.service.d/autologin.conf
```

Remplir ce fichier avec le contenu suivant:
```bash
[Service]
ExecStart=
ExecStart=-/sbin/agetty -o '-p -- username' --noclear --skip-login -  %I $TERM

# Remplacer le nom de l'utilisateur par celui que vous souhaitez
```

Ce fichier permet de configurer l'interface tty1 en mode CLI uniquement

```bash
# Recharger la configuration et rédemarrer la Raspberry Pi
sudo systemctl daemon-reload
sudo reboot
```

### Dans cette configuration, dès la mise sous tension de la Raspberry Pi, l'interface tty1 sera automatiquement configurée en mode CLI et demandant le mot de passe de l'utilisateur 'username' pour acceder au terminal.

### Dans notre cas précis, l'authentification via Yubikey est activée, ce qui permet de se connecter sans mot de passe et uniquement en touchant la YubiKey. 









