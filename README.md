# Projet ARMAGUEDON - ISEN

Ce Github vous permettra de configurer correctement votre Raspberry Pi.

## Étapes de lecture :

1. [Configuration OS](/docs/raspberry_pi_config/1_configuration_os.md)
2. [Configuration basique de votre Yubikey](2_yubikey_basic_configuration.md)
3. [Configuration de votre partition LUKS](3_configuration_luks.md)
4. [Configuration du login lié à votre Yubikey](4_login_authentication.md)
5. [Configuration Service Détection / Cas critique](/docs/raspberry_pi_config/5_automatic_detection.md)

Ces 5 premiers points correspondent à la mise en place de la Raspberry Pi.

6. [Mise en place de la mission](/docs/raspberry_pi_config/6_ready_mission.md)

Ce sixième point vous explique comment configurer correctement votre code métier dans l'environnement que vous venez de mettre en place.

Pour vous l'illustrer, notre code métier correspond à un timestamps s'écrivant toutes les secondes de manière sécurisée dans un fichier situé dans la partition LUKS.

### Arborescence de la partition LUKS
```bash
|-- log_script.py
|-- armaguedon_pub.asc
|-- detect_light_script.py
```

# Utiliser notre solution :

1. Disposer la carte microSD dans la Raspberry Pi.
2. Disposer la Raspberry Pi dans la boite en impression 3D.
3. Disposer la boite en impression 3D sur le drone.
4. Brancher la Yubikey au port USB disponible.
5. Alimenter la Raspberry Pi.
6. Attendre que la Yubikey clignote vert (attendre une trentaine de seconde)
7. Extraire la Yubikey.

La session s'est déverrouillée et le code métier s'exécute.
Vous pouvez utiliser votre drône.

8. Récupérer le drône, débrancher l'alimentation du drone.
9. Extraire la carte microSD de la Raspberry Pi.
10. Analyser les données sur le poste de travail.

# Analyse forensique et récupération de données

En cas de besoin d'analyse ou de récupération de fichiers supprimés, voici quelques outils utiles :

- **Récupération de fichiers supprimés :**
  - `testdisk` : Restauration de partitions et fichiers supprimés.
  - `photorec` : Récupération de fichiers multimédias.
  - `foremost` : Analyse et extraction de fichiers supprimés.

- **Dump et analyse de la mémoire vive :**
  - `LiME` : Extraction de la RAM pour analyse forensique.
  - `Volatility` : Analyse approfondie des processus et données en mémoire.

- **Analyse brute du disque :**
  - `dd` : Création d'une image disque pour inspection.
  - `strings` : Extraction de texte et fragments de données exploitables.

Si rm a été utilisé → Récupération possible avec TestDisk, Foremost, PhotoRec.
Si shred ou wipe ont été utilisés → Très difficile voire impossible sauf s'il y a une copie en RAM ou en cache.
