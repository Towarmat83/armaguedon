import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess

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
        print("liste des processus")
        # Lister tous les processus et filtrer ceux qui exécutent `log_script.py`
        processes = os.popen("ps aux | grep log_script.py").read().splitlines()
        print(processes)
        for process in processes:
            if "/usr/bin/python3 /mnt/log_script.py" in process:
                # Extraire le PID (Process ID)
                pid = int(process.split()[1])
                # Envoyer un signal d'arrêt (SIGTERM)
                os.kill(pid, signal.SIGTERM)
                print(f"🛑 Processus du script de logs (PID {pid}) arrêté.")
                time.sleep(1)  # Attendre que le processus s'arrête
                break
            else:
                print("Aucun processus log_script.py en cours.")
    except Exception as e:
        print(f"❌ Erreur lors de l'arrêt du script de logs : {e}")

def secure_delete(file_path):
    """Utilise shred pour supprimer un fichier de manière sécurisée."""
    if os.path.exists(file_path):
        print(f"🛑 Suppression sécurisée du fichier : {file_path}")
        os.system(f"shred -v -n 5 -z {file_path}")  # 5 passes + écrasement final avec des zéros
        os.remove(file_path)  # Supprimer l'entrée du fichier après l'écrasement
        print(f"✅ {file_path} supprimé de façon sécurisée.")
    else:
        print(f"⚠️ Fichier {file_path} introuvable.")

def delete_files():
    """Supprime et écrase les fichiers sensibles avant d'effacer la Raspberry Pi, puis éteint le système."""
    
    print("🚨 Début de la procédure d'effacement total...")

    # 🔥 Suppression sécurisée des fichiers sensibles
    secure_delete(LOG_FILE)
    secure_delete(LOG_SCRIPT)
    secure_delete(PUBLIC_KEY_FILE)

    # # 🔄 Écrasement du disque avec des données aléatoires
    # print("🔄 Écrasement du disque avec des données aléatoires...")
    # os.system("dd if=/dev/random of=/dev/mmcblk0 bs=1M status=progress")
    # print("✅ Écrasement avec /dev/random terminé.")

    # # 🔄 Écrasement du disque avec des zéros
    # print("🔄 Écrasement du disque avec des zéros...")
    # os.system("dd if=/dev/zero of=/dev/mmcblk0 bs=1M status=progress")
    # print("✅ Écrasement avec /dev/zero terminé.")

    # # 🛑 Suppression définitive avec `shred`
    # print("🛑 Suppression définitive avec `shred`...")
    # os.system("shred -v -n 5 /dev/mmcblk0")
    # print("✅ `shred` terminé, disque irrécupérable.")

    print("Done.")

    # # ⚡ Éteindre la Raspberry Pi définitivement
    # print("⚡ Arrêt de la Raspberry Pi...")
    # os.system("sudo poweroff")
    # os.system("sudo shutdown now")


def read_light_sensor():
    """Lit l'état du capteur de lumière et agit en conséquence."""
    while True:
        light_detected = GPIO.input(LIGHT_SENSOR_PIN)
        if not light_detected:  # Si de la lumière est détectée
            print("💡 Lumière détectée ! Début de l'effacement...")
            stop_log_script()  # 🛑 Arrêter proprement les logs
            delete_files()     # 🔥 Supprimer tout et éteindre la Raspberry Pi
            break  # Sortir de la boucle après avoir agi
        else:
            print("🌑 Obscurité ou faible lumière")
        time.sleep(1)  # Pause d'une seconde avant la prochaine lecture

try:
    read_light_sensor()
except KeyboardInterrupt:
    print("\nArrêt du programme.")
finally:
    GPIO.cleanup()  # Réinitialisation des GPIO
