#!/usr/bin/env python3
"""
Discord Bulk Message Deleter
Supprime automatiquement tous vos messages sur les serveurs/MPs sélectionnés

📌 COMMENT RÉCUPÉRER VOTRE TOKEN DISCORD:

=== MÉTHODE 1: NAVIGATEUR WEB (discord.com) ===
1. Ouvrez Discord dans votre navigateur (https://discord.com/app)
2. Appuyez sur F12 pour ouvrir les outils développeur
3. Allez dans l'onglet "Console"
4. Collez ce code et appuyez sur Entrée:

(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()

5. Votre token s'affiche entre guillemets
6. Copiez-le (sans les guillemets) dans le fichier token.txt

=== MÉTHODE 2: APPLICATION DESKTOP ===
1. Ouvrez Discord Desktop
2. Appuyez sur Ctrl+Shift+I (Windows/Linux) ou Cmd+Option+I (Mac)
3. Allez dans l'onglet "Console"
4. Collez le même code que ci-dessus
5. Copiez le token dans token.txt

⚠️  ATTENTION: Ne partagez JAMAIS votre token! C'est comme votre mot de passe.
   Si quelqu'un a votre token, il peut contrôler totalement votre compte.

📁 Le token doit être dans un fichier nommé "token.txt" dans le même dossier que ce script.
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional
from datetime import datetime
import requests

# ========= CONFIGURATION =========
TOKEN_FILE = "tokens.txt"  # Fichier contenant le token Discord
DELAY_BETWEEN_DELETIONS = 1.5  # Secondes entre chaque suppression
DELAY_BETWEEN_REQUESTS = 2.0   # Secondes entre les requêtes API
REQ_TIMEOUT = 10
MAX_RETRIES = 3
# =================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text: str):
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def load_token() -> Optional[str]:
    """Charge le token depuis le fichier token.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_dir, TOKEN_FILE)
    
    if not os.path.exists(token_path):
        print_error(f"Fichier '{TOKEN_FILE}' introuvable!")
        print_info(f"Créez un fichier '{TOKEN_FILE}' dans le même dossier que ce script")
        print_info("Collez votre token Discord dedans (voir instructions en haut du script)")
        
        # Proposer de créer le fichier
        create = input(f"\n{Colors.CYAN}Voulez-vous créer le fichier maintenant? (o/n): {Colors.END}").strip().lower()
        if create == 'o':
            token = input(f"{Colors.CYAN}Collez votre token Discord: {Colors.END}").strip()
            try:
                with open(token_path, 'w', encoding='utf-8') as f:
                    f.write(token)
                print_success(f"Fichier '{TOKEN_FILE}' créé avec succès!")
                return token
            except Exception as e:
                print_error(f"Erreur lors de la création du fichier: {e}")
                return None
        return None
    
    try:
        with open(token_path, 'r', encoding='utf-8') as f:
            token = f.read().strip()
        
        if not token:
            print_error(f"Le fichier '{TOKEN_FILE}' est vide!")
            return None
        
        # Vérifier que ça ressemble à un token Discord
        if len(token) < 50:
            print_warning("Le token semble trop court. Vérifiez que vous avez copié le token complet.")
        
        print_success(f"Token chargé depuis '{TOKEN_FILE}'")
        return token
        
    except Exception as e:
        print_error(f"Erreur lors de la lecture du fichier: {e}")
        return None

class DiscordAPI:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        self.base_url = "https://discord.com/api/v9"
    
    def handle_rate_limit(self, resp: requests.Response) -> bool:
        """Gère le rate limit. Retourne True si retry nécessaire."""
        if resp.status_code != 429:
            return False
        retry_after = float(resp.headers.get("Retry-After", "10"))
        sleep_s = retry_after + 1
        print_warning(f"Rate limit atteint → pause de {sleep_s:.1f}s")
        time.sleep(sleep_s)
        return True
    
    def safe_request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Effectue une requête avec gestion du rate limit et retry."""
        for attempt in range(MAX_RETRIES):
            try:
                kwargs['timeout'] = REQ_TIMEOUT
                kwargs['headers'] = self.headers
                
                if method.upper() == "GET":
                    r = requests.get(url, **kwargs)
                elif method.upper() == "DELETE":
                    r = requests.delete(url, **kwargs)
                else:
                    return None
                
                if self.handle_rate_limit(r):
                    continue
                return r
                
            except requests.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    print_warning(f"Erreur réseau (tentative {attempt + 1}/{MAX_RETRIES}): {e}")
                    time.sleep(3)
                else:
                    print_error(f"Échec après {MAX_RETRIES} tentatives")
                    return None
        return None
    
    def get_user_info(self) -> Optional[Dict]:
        """Récupère les infos de l'utilisateur connecté."""
        r = self.safe_request("GET", f"{self.base_url}/users/@me")
        return r.json() if r and r.status_code == 200 else None
    
    def get_guilds(self) -> List[Dict]:
        """Récupère tous les serveurs de l'utilisateur."""
        r = self.safe_request("GET", f"{self.base_url}/users/@me/guilds")
        return r.json() if r and r.status_code == 200 else []
    
    def get_dms(self) -> List[Dict]:
        """Récupère tous les DMs/MPs de l'utilisateur."""
        r = self.safe_request("GET", f"{self.base_url}/users/@me/channels")
        return r.json() if r and r.status_code == 200 else []
    
    def search_messages(self, location_id: str, author_id: str, is_dm: bool = False) -> List[Dict]:
        """Recherche tous les messages d'un auteur dans un serveur ou DM."""
        messages = []
        offset = 0
        
        if is_dm:
            url = f"{self.base_url}/channels/{location_id}/messages/search"
        else:
            url = f"{self.base_url}/guilds/{location_id}/messages/search"
        
        while True:
            params = {
                "author_id": author_id,
                "offset": offset
            }
            
            r = self.safe_request("GET", url, params=params)
            if not r or r.status_code != 200:
                break
            
            data = r.json()
            pages = data.get("messages", [])
            
            if not pages:
                break
            
            for page in pages:
                for msg in page:
                    if msg.get("id"):
                        messages.append(msg)
            
            if data.get("total_results", 0) <= offset + 25:
                break
            
            offset += 25
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        return messages
    
    def delete_message(self, channel_id: str, message_id: str) -> bool:
        """Supprime un message."""
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        r = self.safe_request("DELETE", url)
        return r is not None and r.status_code == 204

class MessageDeleter:
    def __init__(self, token: str):
        self.api = DiscordAPI(token)
        self.user_info = None
        self.stats = {
            "total_scraped": 0,
            "total_deleted": 0,
            "failed_deletions": 0,
            "servers_processed": 0,
            "dms_processed": 0
        }
    
    def authenticate(self) -> bool:
        """Vérifie le token et récupère les infos utilisateur."""
        print_info("Authentification en cours...")
        self.user_info = self.api.get_user_info()
        
        if not self.user_info:
            print_error("Token invalide ou expiré")
            print_info("Vérifiez que vous avez copié le bon token dans token.txt")
            print_info("Pour récupérer votre token, consultez les instructions en haut du script")
            return False
        
        username = self.user_info.get('username', 'Inconnu')
        user_id = self.user_info.get('id', 'Inconnu')
        print_success(f"Connecté en tant que: {username} (ID: {user_id})")
        return True
    
    def list_guilds(self) -> List[Dict]:
        """Liste tous les serveurs."""
        print_info("Récupération de la liste des serveurs...")
        guilds = self.api.get_guilds()
        
        if not guilds:
            print_warning("Aucun serveur trouvé")
            return []
        
        print_success(f"{len(guilds)} serveur(s) trouvé(s):\n")
        for i, guild in enumerate(guilds, 1):
            print(f"  [{i}] {guild.get('name', 'Inconnu')} (ID: {guild.get('id')})")
        
        return guilds
    
    def list_dms(self) -> List[Dict]:
        """Liste tous les DMs/MPs."""
        print_info("Récupération de la liste des MPs...")
        dms = self.api.get_dms()
        
        if not dms:
            print_warning("Aucun MP trouvé")
            return []
        
        # Filtrer pour ne garder que les DMs (type 1) et group DMs (type 3)
        dms = [dm for dm in dms if dm.get('type') in [1, 3]]
        
        print_success(f"{len(dms)} conversation(s) trouvée(s):\n")
        for i, dm in enumerate(dms, 1):
            if dm.get('type') == 1:  # DM privé
                recipients = dm.get('recipients', [])
                name = recipients[0].get('username', 'Inconnu') if recipients else 'Inconnu'
                print(f"  [{i}] DM avec {name} (ID: {dm.get('id')})")
            elif dm.get('type') == 3:  # Group DM
                name = dm.get('name') or ', '.join([r.get('username', 'Inconnu') for r in dm.get('recipients', [])])
                print(f"  [{i}] Groupe: {name} (ID: {dm.get('id')})")
        
        return dms
    
    def save_messages_to_json(self, messages: List[Dict], filename: str):
        """Sauvegarde les messages dans un fichier JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        print_success(f"Messages sauvegardés dans {filename}")
    
    def delete_messages_batch(self, messages: List[Dict], location_name: str, auto_mode: bool) -> Dict:
        """Supprime les messages en mode batch ou avec vérification."""
        stats = {"deleted": 0, "failed": 0, "skipped": 0}
        
        if not auto_mode:
            print_info(f"\n{len(messages)} message(s) trouvé(s) dans '{location_name}'")
            
            # Afficher un aperçu des premiers messages
            preview_count = min(5, len(messages))
            print("\n📝 Aperçu des messages:")
            for i, msg in enumerate(messages[:preview_count], 1):
                content = msg.get('content', '')[:50]
                timestamp = msg.get('timestamp', 'Unknown')
                print(f"  {i}. [{timestamp}] {content}...")
            
            if len(messages) > preview_count:
                print(f"  ... et {len(messages) - preview_count} autre(s) message(s)")
            
            confirm = input(f"\n{Colors.YELLOW}Supprimer tous ces messages? (OUI/skip): {Colors.END}").strip().upper()
            
            if confirm != "OUI":
                print_warning("Suppression annulée pour cette location")
                stats["skipped"] = len(messages)
                return stats
        
        print_info(f"Suppression en cours...")
        
        for i, msg in enumerate(messages, 1):
            channel_id = msg.get('channel_id')
            message_id = msg.get('id')
            
            if not channel_id or not message_id:
                stats["failed"] += 1
                continue
            
            success = self.api.delete_message(channel_id, message_id)
            
            if success:
                stats["deleted"] += 1
                content = msg.get('content', '')[:30]
                print(f"  [{i}/{len(messages)}] ✓ Supprimé: {content}...")
            else:
                stats["failed"] += 1
                print_error(f"  [{i}/{len(messages)}] Échec de suppression")
            
            time.sleep(DELAY_BETWEEN_DELETIONS)
        
        return stats
    
    def process_location(self, location_id: str, location_name: str, is_dm: bool, auto_mode: bool, save_backup: bool):
        """Traite une location (serveur ou DM)."""
        print_header(f"Traitement: {location_name}")
        
        # Scraping des messages
        print_info("Recherche des messages...")
        messages = self.api.search_messages(location_id, self.user_info['id'], is_dm)
        
        if not messages:
            print_warning("Aucun message trouvé")
            return
        
        self.stats["total_scraped"] += len(messages)
        print_success(f"{len(messages)} message(s) trouvé(s)")
        
        # Sauvegarde JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Nettoyer le nom de location pour les caractères invalides
        safe_location_name = location_name.replace(' ', '_')
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            safe_location_name = safe_location_name.replace(char, '_')
        
        filename = f"messages_{safe_location_name}_{timestamp}.json"
        self.save_messages_to_json(messages, filename)
        
        # Suppression
        result = self.delete_messages_batch(messages, location_name, auto_mode)
        
        self.stats["total_deleted"] += result["deleted"]
        self.stats["failed_deletions"] += result["failed"]
        
        if is_dm:
            self.stats["dms_processed"] += 1
        else:
            self.stats["servers_processed"] += 1
        
        # Gestion de la sauvegarde
        if not save_backup and result["deleted"] > 0:
            try:
                os.remove(filename)
                print_info(f"Fichier JSON supprimé: {filename}")
            except:
                pass
        
        print_success(f"Résumé: {result['deleted']} supprimés, {result['failed']} échecs")
    
    def print_final_stats(self):
        """Affiche les statistiques finales."""
        print_header("RÉSUMÉ FINAL")
        
        print(f"{Colors.CYAN}📊 Statistiques globales:{Colors.END}\n")
        print(f"  • Serveurs traités: {self.stats['servers_processed']}")
        print(f"  • MPs traités: {self.stats['dms_processed']}")
        print(f"  • Total messages scrapés: {self.stats['total_scraped']}")
        print(f"  • {Colors.GREEN}Total messages supprimés: {self.stats['total_deleted']}{Colors.END}")
        print(f"  • {Colors.RED}Échecs de suppression: {self.stats['failed_deletions']}{Colors.END}")
        
        success_rate = (self.stats['total_deleted'] / self.stats['total_scraped'] * 100) if self.stats['total_scraped'] > 0 else 0
        print(f"\n  • Taux de réussite: {success_rate:.1f}%")

def print_token_instructions():
    """Affiche les instructions détaillées pour récupérer le token."""
    print_header("📖 GUIDE: COMMENT RÉCUPÉRER VOTRE TOKEN DISCORD")
    
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗")
    print(f"║  MÉTHODE 1: NAVIGATEUR WEB (discord.com)                ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print("1. Ouvrez Discord dans votre navigateur:")
    print("   https://discord.com/app\n")
    
    print("2. Appuyez sur F12 pour ouvrir les outils développeur\n")
    
    print("3. Allez dans l'onglet 'Console'\n")
    
    print("4. Copiez et collez ce code, puis appuyez sur Entrée:\n")
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    token_code = "(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()"
    print(f"{Colors.YELLOW}{token_code}{Colors.END}")
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}\n")
    
    print("5. Votre token s'affiche entre guillemets\n")
    
    print("6. Copiez-le (SANS les guillemets) et collez-le dans token.txt\n")
    
    print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗")
    print(f"║  MÉTHODE 2: APPLICATION DESKTOP                          ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print("1. Ouvrez Discord Desktop\n")
    
    print("2. Ouvrez la console développeur:")
    print("   • Windows/Linux: Ctrl + Shift + I")
    print("   • Mac: Cmd + Option + I\n")
    
    print("3. Suivez les étapes 3 à 6 de la méthode navigateur\n")
    
    print(f"{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║  ⚠️  AVERTISSEMENT SÉCURITÉ                              ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print(f"{Colors.RED}• Ne partagez JAMAIS votre token avec qui que ce soit!")
    print(f"• Votre token = accès TOTAL à votre compte Discord")
    print(f"• Si vous pensez que votre token a été compromis,")
    print(f"  changez immédiatement votre mot de passe Discord{Colors.END}\n")

def main():
    print_header("🗑️  DISCORD BULK MESSAGE DELETER")
    
    # Charger le token
    token = load_token()
    
    if not token:
        print("\n" + "="*60)
        show_help = input(f"{Colors.CYAN}Afficher le guide pour récupérer votre token? (o/n): {Colors.END}").strip().lower()
        if show_help == 'o':
            print_token_instructions()
        return
    
    deleter = MessageDeleter(token)
    
    if not deleter.authenticate():
        return
    
    # Choix: Serveurs ou MPs
    print("\n" + "="*60)
    print("1. Serveurs")
    print("2. Messages privés (MPs)")
    print("3. Les deux")
    choice = input(f"\n{Colors.CYAN}Choix (1/2/3): {Colors.END}").strip()
    
    process_guilds = choice in ["1", "3"]
    process_dms = choice in ["2", "3"]
    
    # Mode de suppression
    print("\n" + "="*60)
    print("Mode de suppression:")
    print("1. Automatique (batch) - Tout supprimer sans confirmation")
    print("2. Vérification - Aperçu et confirmation pour chaque location")
    mode_choice = input(f"\n{Colors.CYAN}Choix (1/2): {Colors.END}").strip()
    auto_mode = mode_choice == "1"
    
    # Sauvegarde
    backup_choice = input(f"\n{Colors.CYAN}💾 Sauvegarder les fichiers JSON? (o/n): {Colors.END}").strip().lower()
    save_backup = backup_choice == "o"
    
    # Traitement des serveurs
    if process_guilds:
        guilds = deleter.list_guilds()
        
        if guilds:
            selected = input(f"\n{Colors.CYAN}Numéros des serveurs à traiter (ex: 1,3,5 ou 'all'): {Colors.END}").strip()
            
            if selected.lower() == "all":
                selected_guilds = guilds
            else:
                indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
                selected_guilds = [guilds[i] for i in indices if 0 <= i < len(guilds)]
            
            for guild in selected_guilds:
                deleter.process_location(
                    guild['id'],
                    guild.get('name', 'Inconnu'),
                    is_dm=False,
                    auto_mode=auto_mode,
                    save_backup=save_backup
                )
    
    # Traitement des MPs
    if process_dms:
        dms = deleter.list_dms()
        
        if dms:
            selected = input(f"\n{Colors.CYAN}Numéros des MPs à traiter (ex: 1,2,4 ou 'all'): {Colors.END}").strip()
            
            if selected.lower() == "all":
                selected_dms = dms
            else:
                indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
                selected_dms = [dms[i] for i in indices if 0 <= i < len(dms)]
            
            for dm in selected_dms:
                if dm.get('type') == 1:
                    recipients = dm.get('recipients', [])
                    name = f"DM_{recipients[0].get('username', 'Inconnu')}" if recipients else 'Inconnu'
                else:
                    name = dm.get('name') or 'Group_DM'
                
                deleter.process_location(
                    dm['id'],
                    name,
                    is_dm=True,
                    auto_mode=auto_mode,
                    save_backup=save_backup
                )
    
    # Statistiques finales
    deleter.print_final_stats()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Opération terminée!{Colors.END}\n")

if __name__ == "__main__":
    main()
