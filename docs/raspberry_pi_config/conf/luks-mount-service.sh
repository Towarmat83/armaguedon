#!/bin/bash
# Rediriger toutes les sorties vers un fichier de log
exec > /tmp/luks-mount-service.log 2>&1

echo "Service démarré à $(date)"

# Afficher l'état du système
echo "État du système :"
lsblk
echo "Mappages LUKS actifs :"
ls -la /dev/mapper/
echo "État de /mnt :"
ls -la /mnt

# Attendre que le système soit complètement démarré
sleep 10
echo "Après attente de 10 secondes"

# Vérifier si la partition est disponible
if [ -e /dev/mmcblk0p3 ]; then
    echo "Partition mmcblk0p3 disponible"

    # Vérifier si la partition est déjà déverrouillée
    if [ -e /dev/mapper/cryptroot ]; then
        echo "Volume cryptroot déjà déverrouillé."
    else
        echo "Tentative de déverrouillage LUKS..."

        # Utiliser notre script automatique
        /usr/local/bin/auto-yubikey-luks.sh
        RESULT=$?
        echo "Résultat de yubikey-luks-open: $RESULT"

        if [ $RESULT -ne 0 ]; then
            echo "Erreur: Impossible de déverrouiller la partition LUKS !"
            exit 1
        fi

        # Vérifier si le volume est bien ouvert après le déverrouillage
        if [ ! -e /dev/mapper/cryptroot ]; then
            echo "Erreur: cryptroot n'existe toujours pas après le déverrouillage."
            exit 1
        fi
    fi
else
    echo "Erreur: Partition mmcblk0p3 non disponible."
    exit 1
fi

# Vérifier si le montage est nécessaire
if findmnt /mnt > /dev/null 2>&1; then
    echo "/mnt est déjà monté, aucun besoin de le remonter."
else
    echo "Tentative de montage de /dev/mapper/cryptroot sur /mnt..."
    mount /dev/mapper/cryptroot /mnt
    MOUNT_RESULT=$?
    echo "Résultat du montage: $MOUNT_RESULT"

    if [ $MOUNT_RESULT -eq 0 ]; then
        echo "Montage réussi, modification des permissions..."
        chown raspi:raspi /mnt
        ls -la /mnt

        # Vérifier si le montage est bien actif
        if findmnt /mnt > /dev/null 2>&1; then
            echo "Vérification: /mnt est bien monté."
        else
            echo "Erreur: /mnt semble ne pas être monté malgré le succès du `mount`."
            exit 1
        fi
    else
        echo "Échec du montage, vérification du système de fichiers..."
        fsck -n /dev/mapper/cryptroot
        exit 1
    fi
fi

# Forcer l'écriture des modifications
sync

echo "Service terminé à $(date)"
