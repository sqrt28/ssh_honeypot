# SSH Honeypot 🎣

Ce projet est un **faux serveur SSH** destiné à piéger et enregistrer les tentatives de connexion malveillantes.  
Chaque commande envoyée par l'attaquant est enregistrée dans un fichier `honeypot.log`.

Le serveur simule un environnement basique type Linux Ubuntu, avec quelques commandes comme `ls`, `pwd`, `whoami`, etc.

---

## Fonctionnalités

- Capture des tentatives de connexion SSH.
- Journalisation (`logging`) des identifiants utilisés et des commandes exécutées.
- Faux shell simulé.
- Dockerisé pour faciliter le déploiement rapide.

---

## Prérequis

- Docker
- Docker Compose

---

## Installation rapide 🚀

Clonez le projet :

```bash
git clone https://github.com/tonuser/ssh_honeypot.git
cd ssh_honeypot
docker compose build