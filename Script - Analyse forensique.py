import re
from collections import defaultdict

def analyze_web_logs(logfile):
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(GET|POST) (.*?) HTTP/1.1" (\d+) (\d+)')
    attack_patterns = defaultdict(int)

    with open(logfile, "r") as file:
        for line in file:
            match = pattern.match(line)
            if match:
                ip = match.group(1)
                request = match.group(4)
                status = match.group(5)
                if status == "404":
                    attack_patterns[ip] += 1

    for ip, count in attack_patterns.items():
        if count > 10:  # Threshold for suspicious activity
            print(f"Potential attack from {ip}: {count} 404 errors")

if __name__ == "__main__":
    logfile = "/var/log/apache2/access.log"  # Remplacez par le chemin vers le fichier de journal du serveur web
    analyze_web_logs(logfile)