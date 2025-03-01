import time
import os

# Récupérer le dossier où se trouve le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemin du fichier de logs
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")

# Boucle pour écrire des logs toutes les secondes
try:
    while True:
        # Générer un message de log avec un timestamp
        log_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Log message\n"
        
        # Écrire le message dans le fichier de logs
        with open(LOG_FILE, "a") as f:
            f.write(log_message)
        
        print(f"📝 Log écrit : {log_message.strip()}")
        
        # Attendre 1 seconde avant la prochaine itération
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 Script arrêté par l'utilisateur.")