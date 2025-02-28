# Flasher la carte micro SD pour avoir un OS Rasp

# Allouer de la place à rootfs
Le faire avec l'interface graphique

# Créer la partition depuis le pc ops (20Mo) en utilisant LUKS. Se souvenir du mdp de la partition.
Le faire avec l'interface graphique

# Brancher la Rasp

# Se connecter en Wifi via l'interface graphique de la Rasp (le premier démarrage est un peu long) Bien penser à avoir un clavier + souris

# Lier la partition à la Yubikey.

https://quentin.demouliere.eu/sysadmin/2024/12/04/luks-yubi.html

```bash
sudo apt install yubikey-luks yubikey-personalization pcscd yubikey-manager vim
```

Remplacer le ykluks-keyscript dans `/usr/share/yubikey-luks/ykluks-keyscript`


```bash
scp ./docs/raspberry_pi_config/ykluks-keyscript raspi@IP:~/
sudo mv /usr/share/yubikey-luks/ykluks-keyscript /usr/share/yubikey-luks/ykluks-keyscript.old
sudo mv ~/ykluks-keyscript /usr/share/yubikey-luks/
```

Allouer un slot de la Yubikey à un challenge-response `ykpersonalize -2 -ochal-resp -ochal-hmac -ohmac-lt64 -oserial-api-visible`

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

# Configurer les fichiers suivants avec:

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

