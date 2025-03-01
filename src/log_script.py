import gnupg
import time
import os

# Récupérer le dossier où se trouve le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemins relatifs aux fichiers
KEY_FILE = os.path.join(BASE_DIR, "armaguedon_pub.asc")
OUTPUT_FILE = os.path.join(BASE_DIR, "logs.txt")

# Vérifier si la clé publique existe
if not os.path.exists(KEY_FILE):
    print(f"Erreur : Le fichier de clé publique '{KEY_FILE}' est introuvable.")
    exit(1)

# Initialisation de GPG
gpg = gnupg.GPG()

# Lire la clé publique depuis le fichier
with open(KEY_FILE, "r") as key_file:
    key_data = key_file.read()

# Extraire l'identifiant de la clé (UID) pour l'utiliser comme destinataire
# On suppose que l'UID est "BE-Armaguedon"
recipient = "BE-Armaguedon"

# Boucle pour générer un timestamp toutes les 5 secondes et le chiffrer
while True:
    timestamp = str(int(time.time()))  # Génère un timestamp Unix
    print(f"🕒 Timestamp généré : {timestamp}")

    # Chiffrement avec la clé publique
    encrypted_data = gpg.encrypt(timestamp, recipients=[recipient], always_trust=True)

    if not encrypted_data.ok:
        print(f"❌ Erreur lors du chiffrement : {encrypted_data.stderr}")
    else:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(str(encrypted_data) + "\n")  # Utiliser str() pour convertir en chaîne
        print(f"🔐 Timestamp chiffré et enregistré dans {OUTPUT_FILE}")

    time.sleep(5)  # Attente de 5 secondes avant la prochaine itération