import re

def detect_suspicious_logins(logfile):
    with open(logfile, "r") as file:
        for line in file:
            if "Failed password" in line:
                print(f"Suspicious login attempt: {line.strip()}")

if __name__ == "__main__":
    logfile = "/var/log/auth.log"  # Remplacez par le chemin vers le fichier de journal des connexions
    detect_suspicious_logins(logfile)