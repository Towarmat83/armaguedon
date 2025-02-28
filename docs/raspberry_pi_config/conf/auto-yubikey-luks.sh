#!/bin/bash
# Script pour déverrouiller automatiquement une partition LUKS avec Yubikey

echo "Déverrouillage de LUKS avec la YubiKey..." >&2

# Vérifier si la partition est déjà déverrouillée
if [ -e /dev/mapper/cryptroot ]; then
    echo "cryptroot est déjà déverrouillé. Pas besoin de le rouvrir."
    exit 0
fi

# Exécuter la commande correcte directement
echo -n "$(ykchalresp -2 'luks_challenge')" | sudo cryptsetup luksOpen --key-file=- /dev/mmcblk0p3 cryptroot
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "Déverrouillage réussi." >&2
else
    echo "Échec du déverrouillage." >&2
    exit 1
fi

exit 0
