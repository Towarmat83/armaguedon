#!/bin/bash

# Écriture dans le log pour le suivi
echo "YubiKey retirée à $(date) - Désactivation du port USB" >> /tmp/yubikey-log.txt

# Petit délai pour être sûr que le retrait est bien pris en compte
sleep 2

# Désactiver définitivement le port USB concerné
echo 0 | sudo tee /sys/bus/usb/devices/1-1.3/authorized
