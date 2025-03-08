# Configuration LUKS + Yubikey

## Prérequis

* [Configuration OS](1_configuration_os.md)
* [Configuration basique Yubikey](2_yubikey_basic_configuration.md)

(Optionnel pour l'accès SSH)
* Clavier filaire
* Souris filaire
* Cable microHDMI -> HDMI
* Yubikey

## Étapes de mise en place

### Création de la partition LUKS

1. Allouer du stockage à rootfs.

**Conseil :** Utiliser l'interface graphique pour le faire.

2. Créer une partition LUKS

Pour l'utilisation demandée dans le cadre de notre BE, une partition chiffrée de 20Mo suffit.

**Attention :** Bien conserver le mot de passe de la partition lors de sa création.

### Mise sous tension de la Raspberry Pi

3. Extraire la microSD du PC et démarrer la Raspberry Pi avec.

Le premier démarrage peut durer quelques minutes.

4. Brancher souris, clavier et microHDMI pour contrôler l'interface graphique.

5. Renseigner le WIFI pour communiquer en SSH avec la Raspberry Pi.

### Lier la partition à la Yubikey.

[Tutoriel utile](https://quentin.demouliere.eu/sysadmin/2024/12/04/luks-yubi.html)

**Conseil :** Cette partie sera beaucoup plus agréable à réaliser en SSH pour pouvoir copier/coller depuis ce Github.

1. Installer les dépendances nécessaires au projet
```bash
sudo apt update && sudo apt upgrade
```

```bash
sudo apt -y install yubikey-luks yubikey-personalization pcscd yubikey-manager vim libpam-u2f wget gnupg2 gnupg-agent dirmngr cryptsetup scdaemon
```

2. Remplacer le [ykluks-keyscript](../raspberry_pi_config/conf/ykluks-keyscript) dans `/usr/share/yubikey-luks/ykluks-keyscript`

Le fichier `/usr/share/yubikey-luks/ykluks-keyscript` généré par le paquet `yubikey-luks` dysfonctionne et ne permet pas de pré-enregister le mot de passe utilisé lors du challenge Yubikey - LUKS dans le fichier de configuration `/etc/ykluks.cfg`.


```bash
# Transférer un fichier depuis votre PC vers la Raspberry Pi
scp ./docs/raspberry_pi_config/ykluks-keyscript raspi@IP:~/

# Renomage du fichier déprécié
sudo mv /usr/share/yubikey-luks/ykluks-keyscript /usr/share/yubikey-luks/ykluks-keyscript.old

# Mise en place du nouveau fichier
sudo mv ~/ykluks-keyscript /usr/share/yubikey-luks/
```

3. Allouer un slot de la Yubikey à un challenge-response `ykpersonalize -2 -ochal-resp -ochal-hmac -ohmac-lt64 -oserial-api-visible`

Lister les disques `lsblk`

Avoir des infos sur le disque chiffré `sudo cryptsetup luksDump /dev/mmcblk0p3`

Enroller le Slot Luks et le Slot Yubi `sudo yubikey-luks-enroll -d /dev/mmcblk0p3 -s 1`

Pour monter la partition manuellement:
```bash
sudo cryptsetup open /dev/mmcblk0p3 cryptroot
sudo mount /dev/mapper/cryptroot /mnt
```

Pour démonter la partition manuellement:
```bash
sudo umount /dev/mapper/cryptroot 
sudo cryptsetup close cryptroot
```

Pour ouvrir la partition grace à la Yubikey:
```bash
echo -n "$(ykchalresp -2 'luks_challenge')" | sudo cryptsetup luksOpen --key-file=- /dev/mmcblk0p3 cryptroot
```

Pour faire disparaitre cryptroot de `lsblk`:
```bash
sudo dmsetup remove cryptroot
``` 

# Configurer les fichiers suivants:

```bash
sudo vim /etc/systemd/system/luks-mount.service
sudo vim /usr/local/bin/luks-mount-service.sh

sudo chmod +x /usr/local/bin/luks-mount-service.sh
# Activer le service
sudo ln -s /etc/systemd/system/luks-mount.service /etc/systemd/system/multi-user.target.wants/

sudo vim /usr/local/bin/auto-yubikey-luks.sh
sudo chmod +x /usr/local/bin/auto-yubikey-luks.sh

sudo vim /etc/systemd/system/yubikey-luks-cryptroot.service
sudo systemctl enable yubikey-luks-cryptroot.service

# Pour mettre à jour le boot
sudo update-initramfs -u

# Logs
cat /tmp/luks-mount-service.log
```
