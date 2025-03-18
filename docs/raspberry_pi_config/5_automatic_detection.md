# Mise en place du système automatique pour la détection

## Prérequis

* [Configuration OS](1_configuration_os.md)
* [Configuration basique Yubikey](2_yubikey_basic_configuration.md)
* [Configuration LUKS](3_configuration_luks.md)
* [Configuration du login](4_login_authentication.md)

## Étapes de mise en place

1. Ajouter [led.py](../../src/led.py) dans la partition chiffrée depuis le PC OPS.

Installer ces packages python sur la Raspberry Pi:
```bash
sudo pip3 install RPi.GPIO --break-system-packages
sudo pip3 install python-gnupg --break-system-packages
```

Création du script:
```bash
sudo vim /usr/local/bin/start-python-scripts.sh
sudo chmod +x /usr/local/bin/start-python-scripts.sh
```

Création du service:
```bash
sudo vim /etc/systemd/system/python-scripts.service
# Modifier le <USER>
```

Activation + démarrage du service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable python-scripts.service
sudo systemctl start python-scripts.service
```

2. Pour mettre à jour le boot
```bash
sudo update-initramfs -u
```

3. [Mise en place physique du système de détection](../raspberry_pi_config/conf/Technical_documentation_detection.pdf)


### Vous venez de mettre en place le service qui va activer dès la mise sous tension de la Raspberry Pi le système de détection de lumière.

## Votre Raspberry Pi est désormais prête pour la mise en mission


[Continuer la configuration](./6_ready_mission.md)