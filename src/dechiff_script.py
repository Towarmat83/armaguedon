import gnupg
import os

# Récupérer le dossier où se trouve le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemins relatifs aux fichiers
PRIVATE_KEY_FILE = os.path.join(BASE_DIR, "armaguedon_private.asc")
ENCRYPTED_FILE = os.path.join(BASE_DIR, "logs.txt")
DECRYPTED_FILE = os.path.join(BASE_DIR, "logs_dechiff.txt")

# Vérifier si les fichiers existent
if not os.path.exists(PRIVATE_KEY_FILE):
    print(f"Erreur : Le fichier de clé privée '{PRIVATE_KEY_FILE}' est introuvable.")
    exit(1)

if not os.path.exists(ENCRYPTED_FILE):
    print(f"Erreur : Le fichier chiffré '{ENCRYPTED_FILE}' est introuvable.")
    exit(1)

# Résoudre ~ en chemin absolu
gnupghome = os.path.expanduser('~/.gnupg')

# Initialisation de GPG
gpg = gnupg.GPG(gnupghome=gnupghome)

print("🔍 Clés disponibles avant import :", gpg.list_keys(secret=True))

# Importer la clé privée
with open(PRIVATE_KEY_FILE, "r") as key_file:
    key_data = key_file.read()
    import_result = gpg.import_keys(key_data)
    
if not import_result.fingerprints:
    print("Erreur : Impossible d'importer la clé privée.")
    exit(1)

print(f"✅ Résultat de l'import : {import_result.results}")
print(f"✅ Clé privée importée avec fingerprint : {import_result.fingerprints[0]}")

# Lire le fichier chiffré
with open(ENCRYPTED_FILE, "r") as f:
    encrypted_data = f.read()

# Séparer les messages chiffrés et les reformater correctement
messages = []
current_message = []
for line in encrypted_data.split('\n'):
    if "-----BEGIN PGP MESSAGE-----" in line:
        if current_message:
            messages.append('\n'.join(current_message))
        current_message = ["-----BEGIN PGP MESSAGE-----"]
    elif "-----END PGP MESSAGE-----" in line:
        current_message.append("-----END PGP MESSAGE-----")
        messages.append('\n'.join(current_message))
        current_message = []
    elif current_message:
        current_message.append(line)

# Déchiffrer chaque message
decrypted_messages = []
for i, msg in enumerate(messages, start=1):
    try:
        decrypted_data = gpg.decrypt(msg, passphrase='Armagued0n2025')  # Remplacez par le mot de passe de la clé privée
        
        if decrypted_data.ok:
            decrypted_messages.append(str(decrypted_data))
            print(f"🔓 Message {i} déchiffré avec succès : {str(decrypted_data)}")
        else:
            print(f"❌ Erreur lors du déchiffrement du message {i}")
            print(f"Status : {decrypted_data.status}")
            print(f"Stderr : {decrypted_data.stderr}")
            
    except Exception as e:
        print(f"❌ Exception lors du déchiffrement du message {i}: {str(e)}")

# Enregistrer les résultats déchiffrés
if decrypted_messages:
    with open(DECRYPTED_FILE, "w") as f:
        for i, msg in enumerate(decrypted_messages, start=1):
            f.write(f"=== Message {i} ===\n")
            f.write(msg + "\n\n")
    print(f"🔓 Messages déchiffrés enregistrés dans {DECRYPTED_FILE}")
else:
    print("❌ Aucun message n'a pu être déchiffré")