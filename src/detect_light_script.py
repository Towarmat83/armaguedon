import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess

# Définition du numéro de broche GPIO
LIGHT_SENSOR_PIN = 27  # Adapter selon le câblage

# Configuration de la broche en entrée
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)

# Chemins des fichiers à supprimer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MISSION_PARTITION = "/dev/mmcblk0p3"
LOG_SCRIPT = os.path.join(BASE_DIR, "log_script.py")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")
PUBLIC_KEY_FILE = os.path.join(BASE_DIR, "armaguedon_pub.asc")


def stop_log_script():
    """Arrête le script de logs en cours d'exécution."""
    try:
        print("📋 Recherche des processus log_script.py...")
        processes = os.popen("ps aux | grep log_script.py").read().splitlines()
        for process in processes:
            if "/usr/bin/python3 /mnt/log_script.py" in process:
                pid = int(process.split()[1])
                os.kill(pid, signal.SIGTERM)
                print(f"🛑 Processus log_script.py (PID {pid}) arrêté.")
                time.sleep(1)
                break
        else:
            print("✅ Aucun processus log_script.py trouvé.")
    except Exception as e:
        print(f"❌ Erreur lors de l'arrêt du script de logs : {e}")


def secure_delete(file_path):
    """Utilise shred pour supprimer un fichier de manière sécurisée."""
    if os.path.exists(file_path):
        print(f"🔥 Suppression sécurisée du fichier : {file_path}")
        os.system(f"shred -v -n 5 -z {file_path}")  # 5 passes + écrasement final avec des zéros
        os.remove(file_path)  # Supprime le fichier après écrasement
        print(f"✅ {file_path} supprimé de façon sécurisée.")
    else:
        print(f"⚠️ Fichier {file_path} introuvable.")


def delete_files():
    """Supprime et écrase les fichiers sensibles avant de supprimer la partition."""
    print("🚨 Début de la suppression des fichiers sensibles...")

    # 🔥 Suppression sécurisée des fichiers
    secure_delete(LOG_FILE)
    secure_delete(LOG_SCRIPT)
    secure_delete(PUBLIC_KEY_FILE)

    print("✅ Suppression des fichiers terminée.")


def close_partition():
    """Ferme la partition cryptée (si nécessaire) avant de procéder à sa destruction."""
    print(f"🛑 Fermeture de la partition {MISSION_PARTITION}...")
    # Vérifier si la partition est montée et la démonter
    mount_check = subprocess.run(["lsblk", "-f"], capture_output=True, text=True)
    if MISSION_PARTITION in mount_check.stdout:
        print("⚠️ La partition est montée, démontage en cours...")
        os.system(f"sudo umount {MISSION_PARTITION}")
        print(f"✅ Partition {MISSION_PARTITION} démontée.")
    
    # Fermer la partition si elle est cryptée
    if os.path.exists(f"/dev/mapper/cryptroot"):
        print("⚠️ La partition est cryptée, fermeture en cours...")
        os.system("sudo cryptsetup close cryptroot")
        print("✅ Partition cryptée fermée.")


def destroy_partition():
    """Détruit complètement la partition en écrasant ses données."""
    print(f"🚨 Début de la destruction sécurisée de la partition {MISSION_PARTITION}...")

    # Vérifier si la partition existe
    if not os.path.exists(MISSION_PARTITION):
        print(f"⚠️ La partition {MISSION_PARTITION} n'existe pas.")
        return

    # 🔥 Utilisation de `shred` pour détruire la partition
    print("🛑 Remplacement des données de la partition avec des données aléatoires...")
    os.system(f"sudo shred -v -n 5 -z {MISSION_PARTITION}")  # 5 passes + écrasement final avec des zéros

    print("Destruction des headers LUKS...")
    os.system("sudo cryptsetup luksErase /dev/mapper/cryptroot")

    print("Suppression des fichiers de complémentaires")
    os.system(f"sudo journalctl --rotate")
    os.system(f"sudo journalctl --vacuum-time=1s")
    os.system(f"sudo rm -rf /var/log/journal/*")
    os.system(f"shred -v -n 5 -z ~/.bash_history")
    os.system(f"rm ~/.bash_history")
    os.system(f"history -c")

    print(f"✅ Partition {MISSION_PARTITION} effacée de façon sécurisée.")


def read_light_sensor():
    """Lit l'état du capteur de lumière et agit en conséquence."""
    while True:
        light_detected = GPIO.input(LIGHT_SENSOR_PIN)
        if not light_detected:  # Si de la lumière est détectée
            print("💡 Lumière détectée ! Début de l'effacement...")
            stop_log_script()  # 🛑 Arrêter proprement les logs
            delete_files()     # 🔥 Supprimer tout et éteindre la Raspberry Pi
            close_partition()
            destroy_partition()
            print("Mise hors tension.")
            os.system("sudo poweroff")
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
