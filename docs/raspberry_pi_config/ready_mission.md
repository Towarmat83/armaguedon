# Mise en place de la mission

## Prérequis

* [Configuration OS](1_configuration_os.md)
* [Configuration basique Yubikey](2_yubikey_basic_configuration.md)
* [Configuration LUKS](3_configuration_luks.md)
* [Configuration du login](4_login_authentication.md)
* [Configuration Service Détection / Cas critique](/docs/raspberry_pi_config/5_automatic_detection.md)


## Étapes de mise en place

### Votre Raspberry Pi est maintenant équipée, voici les étapes à suivre pour configurer correctement les configurations système à votre code métier.

## Create GPG Keys

```bash
gpg --full-generate-key

# Suivre ce lien https://support.yubico.com/hc/en-us/articles/360013790259-Using-Your-YubiKey-with-OpenPGP

gpg --list-keys

# Au moment de import les clés sur la Yubikey (étape 3), lors de la commande:
keytocard

# Insérer la passphrase de la clé en premier puis le code PUK de la Yubi deux fois !! 
# Meme chose pour les prochains commande `keytocard`

# Bien sélectionner no quand on quitte sinon ça va supprimé la clé du PC.
```

## Import to Rasp

```bash
# La clé est privée est stockée sur la Yubikey
# Pour importer la clé publique sur la Rasp et pouvoir l'exploiter avec gpg côté Rasp, il faut:

# Exporter la clé sur le PC
gpg --export --armor <ID_DE_TA_CLÉ> > public_key.asc

# La transférer sur la Rasp
scp public_key.asc pi@<adresse_ip_rasp>:/home/pi/

# Importer la clé publique dans gpg (bien avoir installé scdaemon sur la Rasp avant)
gpg --import public_key.asc

# Vérifier que c'est disponible
gpg --list-keys
```
