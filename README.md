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

7. 


