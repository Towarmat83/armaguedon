import os
import gnupg
import time

# Résoudre ~ en chemin absolu
gnupghome = os.path.expanduser('~/.gnupg')

# Initialisation de GPG
gpg = gnupg.GPG(gnupghome=gnupghome)

# Charger la clé publique
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, "armaguedon_pub.asc")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

with open(KEY_FILE, "r") as key_file:
    key_data = key_file.read()

import_result = gpg.import_keys(key_data)

# Lister les clés publiques
keys = gpg.list_keys()

# Si des clés sont présentes, récupérer le fingerprint de la première clé
if keys:
    recipient = keys[0]['fingerprint']
else:
    print("Aucune clé trouvée.")

while True:
    # Utilisation du même format de timestamp que le deuxième script
    timestamp = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Log message"
    print(f"🕒 Timestamp généré : {timestamp}")

    encrypted_data = gpg.encrypt(timestamp, recipient, always_trust=True)

    if not encrypted_data.ok:
        print(f"❌ Erreur lors du chiffrement : {encrypted_data.stderr}")
    else:
        with open(LOG_FILE, "a") as f:
            f.write(str(encrypted_data) + "\n")
        print("🔐 Timestamp chiffré et enregistré")

    time.sleep(1)