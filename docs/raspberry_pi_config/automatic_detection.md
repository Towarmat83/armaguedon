# Mise en place du système automatique pour la détection

Ajouter les documents dans la partition chiffrée depuis le PC OPS.

Installer ce package python:
```bash
sudo pip3 install RPi.GPIO --break-system-packages
```

Création du script:
```bash
sudo vim /usr/local/bin/start-python-scripts.sh
sudo chmod +x /usr/local/bin/start-python-scripts.sh
```

Création du service:
```bash
sudo vim /etc/systemd/system/python-scripts.service
```

Activation + démarrage du service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable python-scripts.service
sudo systemctl start python-scripts.service
```

# Pour mettre à jour le boot
```bash
sudo update-initramfs -u
```
