import socket
import threading
import paramiko
import logging

logging.basicConfig(
    filename='honeypot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#https://chatgpt.com/c/68000044-ed78-800c-a1c6-778a01742650

HOST_KEY = paramiko.RSAKey.generate(2048)

class SSHHoneypot(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        print(f"[+] Requête de canal : {kind}")
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_auth_password(self, username, password):
        log_msg = f"Tentative de login : {username} / {password}"
        print(f"[!] {log_msg}")
        logging.info(log_msg)

        if password == "toto123":
            logging.info("Connexion acceptée.")
            return paramiko.AUTH_SUCCESSFUL
        else:
            logging.info("Connexion refusée.")
            return paramiko.AUTH_FAILED



def handle_connection(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = SSHHoneypot()
    try:
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel is not None:
            server.event.wait(10)
            if not server.event.is_set():
                print("[!] Pas de requête de shell.")
                return
            # FAUX SHELL ↓↓↓
            channel.send("Bienvenue sur Ubuntu 22.04 LTS\n")
            channel.send("user@ubuntu:~$ ")
            while True:
                command = ''
                while not command.endswith('\n'):
                    command += channel.recv(1024).decode('utf-8')
                logging.info(f"Commande reçue : {command.strip()}")
                print(f"[>] Commande : {command.strip()}")
                if command.strip().lower() in ['exit', 'quit']:
                    channel.send("Déconnexion...\n")
                    break
                cmd = command.strip().lower()

                if cmd == "ls":
                    response = "Documents  Downloads  Music  Pictures  Public  Videos\n"
                elif cmd == "whoami":
                    response = "root\n"
                elif cmd == "pwd":
                    response = "/home/login\n"
                elif cmd.startswith("cat"):
                    response = "Permission denied\n"
                elif cmd == "help":
                    response = "Commandes disponibles : ls, whoami, pwd, cat, exit\n"
                else:
                    response = f"bash: {cmd}: commande introuvable\n"

                channel.send(response)

                channel.send("login@honeypot:~$ ")


    except Exception as e:
        print(f"[!] Erreur : {e}")
    finally:
        transport.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 2222))  # Port SSH "fake"
    server_socket.listen(100)
    print("[*] SSH Honeypot en écoute sur le port 2222...")

    while True:
        client, addr = server_socket.accept()
        print(f"[+] Connexion de {addr}")
        threading.Thread(target=handle_connection, args=(client,)).start()

if __name__ == "__main__":
    main()
