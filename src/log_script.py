import os
import sys
import time
import gnupg
import fcntl

# Lock dans le home utilisateur (propre & sans conflit)
# Permet de s'assurer qu'une seule instance du script est en cours (car udev en lance plusieurs)
lock_file_path = os.path.expanduser("~/.log_script.lock")
lock_file = open(lock_file_path, "w")

try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print("🚫 Script déjà en cours. Fin.")
    sys.exit(0)

# Résoudre ~ en chemin absolu
gnupghome = os.path.expanduser('~/.gnupg')

# Vérifier si le dossier existe, sinon le créer
if not os.path.exists(gnupghome):
    os.makedirs(gnupghome, mode=0o700)

# Initialisation de GPG
gpg = gnupg.GPG(gnupghome=gnupghome)

# Charger la clé publique
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, "armaguedon_pub.asc")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

try:
    with open(KEY_FILE, "r") as key_file:
        key_data = key_file.read()
except Exception as e:
    print(f"❌ Erreur ouverture de la clé publique : {e}")
    sys.exit(1)

import_result = gpg.import_keys(key_data)

# Lister les clés publiques
keys = gpg.list_keys()

# Si des clés sont présentes, récupérer le fingerprint de la première clé
if keys:
    recipient = keys[0]['fingerprint']
    print(f"✅ Clé importée. Fingerprint : {recipient}")
else:
    print("⚠️ Aucune clé trouvée. Le script ne peut pas continuer.")
    sys.exit(1)

# Boucle de génération + chiffrement de timestamp
while True:
    timestamp = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Log message"
    print(f"🕒 Timestamp généré : {timestamp}")

    encrypted_data = gpg.encrypt(timestamp, recipient, always_trust=True)

    if not encrypted_data.ok:
        print(f"❌ Erreur lors du chiffrement : {encrypted_data.stderr}")
    else:
        try:
            with open(LOG_FILE, "a") as f:
                f.write(str(encrypted_data) + "\n")
            print("🔐 Timestamp chiffré et enregistré")
        except Exception as e:
            print(f"❌ Erreur écriture fichier log : {e}")

    time.sleep(1)
