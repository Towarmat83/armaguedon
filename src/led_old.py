import RPi.GPIO as GPIO
import time
import os
import signal

# Définition du numéro de broche GPIO
LIGHT_SENSOR_PIN = 17  # Adapter selon le câblage

# Configuration de la broche en entrée
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)

# Chemins des fichiers à supprimer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_SCRIPT = os.path.join(BASE_DIR, "log_script.py")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")
PUBLIC_KEY_FILE = os.path.join(BASE_DIR, "armaguedon_pub.asc")

def stop_log_script():
    """Arrête le script de logs en cours d'exécution."""
    try:
        # Lister tous les processus et filtrer ceux qui exécutent `log_script.py`
        processes = os.popen("ps aux | grep log_script.py").read().splitlines()
        for process in processes:
            if "python3" in process and "log_script.py" in process:
                # Extraire le PID (Process ID)
                pid = int(process.split()[1])
                # Envoyer un signal d'arrêt (SIGTERM)
                os.kill(pid, signal.SIGTERM)
                print(f"🛑 Processus du script de logs (PID {pid}) arrêté.")
                time.sleep(1)  # Attendre que le processus s'arrête
                break
    except Exception as e:
        print(f"❌ Erreur lors de l'arrêt du script de logs : {e}")

def delete_files():
    """Supprime le script de logs et le fichier de logs."""
    # Supprimer le fichier de logs
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(f"🗑️ Fichier de logs '{LOG_FILE}' supprimé.")
    else:
        print(f"⚠️ Fichier de logs '{LOG_FILE}' introuvable.")

    # Supprimer le script de logs
    if os.path.exists(LOG_SCRIPT):
        os.remove(LOG_SCRIPT)
        print(f"🗑️ Script de logs '{LOG_SCRIPT}' supprimé.")
    else:
        print(f"⚠️ Script de logs '{LOG_SCRIPT}' introuvable.")
    
    # Supprimer la clé publique
    if os.path.exists(PUBLIC_KEY_FILE):
        os.remove(PUBLIC_KEY_FILE)
        print(f"🗑️ Clé publique '{PUBLIC_KEY_FILE}' supprimée.")
    else:
        print(f"⚠️ Clé publique '{PUBLIC_KEY_FILE}' introuvable.")


def read_light_sensor():
    """Lit l'état du capteur de lumière et agit en conséquence."""
    while True:
        light_detected = GPIO.input(LIGHT_SENSOR_PIN)
        if not light_detected:  # Si de la lumière est détectée
            print("Lumière détectée !")
            stop_log_script()  # Arrêter le script de logs
            delete_files()     # Supprimer les fichiers
            break  # Sortir de la boucle après avoir agi
        else:
            print("Obscurité ou faible lumière")
        time.sleep(1)  # Pause d'une seconde avant la prochaine lecture

try:
    read_light_sensor()
except KeyboardInterrupt:
    print("\nArrêt du programme.")
finally:
    GPIO.cleanup()  # Réinitialisation des GPIO