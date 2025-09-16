#!/usr/bin/env python3
"""
Professional Wordlist Generator - Niveau CUPP/Mentalist/Wister
Fonctionnalités professionnelles complètes pour cybersécurité offensive
Auteur: Outil de test de pénétration professionnel
Usage: Uniquement pour des tests autorisés et audits de sécurité légaux
"""

import itertools
import re
import json
import requests
import time
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional, Tuple
import argparse
import random
import hashlib
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess


class ProfessionalWordlistGenerator:
    def __init__(self, gemini_api_key: Optional[str] = None):
        self.base_info = {}
        self.generated_passwords = set()
        # self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        self.gemini_api_key = 'AIzaSyAM4Y-IRcsUdQCxhYx3COtg8TQTPHlLb7o'
        self.scraped_words = set()
        self.social_media_data = {}
        
        # Règles de transformation professionnelles (style CUPP)
        self.transformation_rules = {
            'leet_basic': {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'g': '9', 'l': '1'},
            'leet_advanced': {'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$', 't': '+', 'g': '6'},
            'substitutions': {'and': '&', 'at': '@', 'to': '2', 'for': '4'},
            'caps_patterns': ['upper', 'lower', 'title', 'capitalize', 'alternate', 'random'],
            'number_patterns': ['123', '12', '1', '01', '007', '21', '69', '99', '2023', '2024', '2025'],
            'symbol_patterns': ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '?', '~'],
            'date_formats': ['DDMM', 'MMDD', 'DDMMYY', 'MMDDYY', 'DDMMYYYY', 'MMDDYYYY', 'YYYY', 'YY'],
            'keyboard_walks': ['qwerty', '123456', 'asdf', 'zxcvbn', '987654321', 'qazwsx']
        }
        
        # Masques de génération (style Crunch)
        self.mask_patterns = [
            '?l?l?l?d?d',        # 3 lettres + 2 chiffres
            '?u?l?l?l?d?d?d',    # Maj + 3 min + 3 chiffres  
            '?l?l?l?l?d?d?s',    # 4 lettres + 2 chiffres + symbole
            '?u?l?l?l?l?d?d?d?s', # Maj + 4 min + 3 chiffres + symbole
            '?w?d?d',            # Mot + 2 chiffres
            '?w?d?d?d?d',        # Mot + 4 chiffres
            '?w?s?d?d?d',        # Mot + symbole + 3 chiffres
        ]
        
        # Règles Hashcat/John compatibles
        self.hashcat_rules = []
        self.john_rules = []

    def load_personal_info(self, info_dict: Dict):
        """Charge les informations personnelles avec validation avancée"""
        self.base_info = info_dict
        self._validate_and_enhance_info()
        print(f"[+] Profil chargé: {info_dict.get('name', 'Anonyme')} ({len(self.base_info)} champs)")

    def _validate_and_enhance_info(self):
        """Valide et enrichit automatiquement les informations"""
        # Extraction automatique d'infos supplémentaires
        if 'birth_date' in self.base_info:
            birth = self.base_info['birth_date']
            if len(birth) == 8:  # DDMMYYYY
                self.base_info['birth_day'] = birth[:2]
                self.base_info['birth_month'] = birth[2:4]
                self.base_info['birth_year'] = birth[4:]
                self.base_info['birth_year_short'] = birth[6:]
                
                # Calcul âge et génération
                current_year = datetime.now().year
                age = current_year - int(birth[4:])
                self.base_info['age'] = str(age)
                
        # Génération des initiales et combinaisons
        self._generate_name_combinations()
        
        # Extraction des mots-clés depuis les champs texte
        self._extract_keywords_from_fields()

    def _generate_name_combinations(self):
        """Génère toutes les combinaisons possibles de noms"""
        combinations = set()
        
        name = self.base_info.get('name', '')
        surname = self.base_info.get('surname', '')
        nickname = self.base_info.get('nickname', '')
        middle_name = self.base_info.get('middle_name', '')
        
        if name and surname:
            # Initiales
            combinations.add(name[0].lower() + surname[0].lower())
            combinations.add(surname[0].lower() + name[0].lower())
            
            # Combinaisons nom/prénom
            combinations.add(name.lower() + surname.lower())
            combinations.add(surname.lower() + name.lower())
            combinations.add(name.lower() + surname[0].lower())
            combinations.add(surname.lower() + name[0].lower())
            
            # Avec nom du milieu
            if middle_name:
                combinations.add(name[0].lower() + middle_name[0].lower() + surname[0].lower())
                combinations.add(name.lower() + middle_name[0].lower())
        
        self.base_info['name_combinations'] = list(combinations)

    def _extract_keywords_from_fields(self):
        """Extrait des mots-clés depuis tous les champs texte"""
        keywords = set()
        
        text_fields = ['company', 'job_title', 'department', 'street', 'school', 'university']
        
        for field in text_fields:
            if field in self.base_info and self.base_info[field]:
                text = self.base_info[field]
                # Extraction de mots significatifs
                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                keywords.update(words)
        
        if keywords:
            existing_keywords = self.base_info.get('keywords', [])
            self.base_info['keywords'] = list(set(existing_keywords + list(keywords)))

    def scrape_target_website(self, url: str, depth: int = 2, min_word_length: int = 4) -> Set[str]:
        """Scrape un site web pour extraire des mots (style CeWL)"""
        print(f"[+] Scraping de {url} (profondeur: {depth})...")
        scraped_words = set()
        visited_urls = set()
        
        def scrape_page(page_url: str, current_depth: int):
            if current_depth > depth or page_url in visited_urls:
                return
                
            visited_urls.add(page_url)
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(page_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extraction du texte
                    text = soup.get_text()
                    words = re.findall(r'\b[a-zA-Z]{' + str(min_word_length) + ',}\b', text.lower())
                    scraped_words.update(words)
                    
                    # Mots spéciaux (emails, noms de domaine, etc.)
                    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
                    for email in emails:
                        username = email.split('@')[0]
                        scraped_words.add(username.lower())
                    
                    # Extraction de liens pour navigation
                    if current_depth < depth:
                        links = soup.find_all('a', href=True)
                        for link in links[:20]:  # Limiter le nombre de liens
                            next_url = urljoin(page_url, link['href'])
                            if urlparse(next_url).netloc == urlparse(url).netloc:
                                scrape_page(next_url, current_depth + 1)
                                
            except Exception as e:
                print(f"[-] Erreur scraping {page_url}: {e}")
        
        scrape_page(url, 0)
        
        # Filtrage des mots pertinents
        filtered_words = {word for word in scraped_words 
                         if len(word) >= min_word_length and len(word) <= 20}
        
        print(f"[+] {len(filtered_words)} mots extraits du site web")
        self.scraped_words.update(filtered_words)
        return filtered_words

    def generate_osint_keywords(self, target_name: str = None) -> Set[str]:
        """Génère des mots-clés basés sur OSINT automatique"""
        keywords = set()
        
        if not target_name:
            target_name = f"{self.base_info.get('name', '')} {self.base_info.get('surname', '')}"
        
        print(f"[+] Recherche OSINT pour: {target_name}")
        
        # Simule une recherche OSINT (à adapter selon vos besoins)
        # En pratique, vous pourriez intégrer avec des APIs comme:
        # - Shodan, Censys pour l'infrastructure
        # - Have I Been Pwned pour les fuites
        # - Social media APIs
        
        # Mots-clés contextuels basiques
        if self.base_info.get('company'):
            company = self.base_info['company'].lower()
            keywords.update([company, company.replace(' ', ''), company[:5]])
        
        if self.base_info.get('city'):
            city = self.base_info['city'].lower()
            keywords.update([city, city[:4]])
        
        # Années importantes potentielles
        current_year = datetime.now().year
        for year in range(current_year - 10, current_year + 1):
            keywords.add(str(year))
        
        return keywords

    def generate_rules_hashcat(self) -> List[str]:
        """Génère des règles compatibles Hashcat"""
        rules = []
        
        # Règles basiques Hashcat
        rules.extend([
            ':',          # Aucune modification
            'l',          # Tout en minuscules
            'u',          # Tout en majuscules
            'c',          # Première lettre en majuscule
            'C',          # Première lettre en minuscule
            't',          # Toggle case
            '$1',         # Ajoute '1' à la fin
            '$!',         # Ajoute '!' à la fin
            '$2 $0',      # Ajoute '20' à la fin
            '^1',         # Ajoute '1' au début
            'l $1 $2 $3', # Minuscule + '123' à la fin
            'c $!',       # Capitalize + '!' à la fin
            'l $@ $1 $2 $3', # Minuscule + '@123' à la fin
        ])
        
        # Règles de substitution leet
        leet_rules = []
        for original, replacement in self.transformation_rules['leet_basic'].items():
            leet_rules.append(f's{original}{replacement}')  # Substitution
        rules.extend(leet_rules)
        
        # Règles combinées
        rules.extend([
            'l sa4 se3 si1 so0',  # Leet speak complet
            'c $1 $2 $3 $!',      # Capitalize + '123!'
            'l $@ $1 $2 $3 $*',   # Minuscule + '@123*'
        ])
        
        self.hashcat_rules = rules
        return rules

    def generate_rules_john(self) -> List[str]:
        """Génère des règles compatibles John the Ripper"""
        rules = []
        
        # Règles John format
        rules.extend([
            '-c',     # Capitalize
            '-l',     # Lowercase
            '-u',     # Uppercase
            '$1',     # Append '1'
            '$!',     # Append '!'
            '^1',     # Prepend '1'
            'l$1$2$3', # Lowercase + append '123'
        ])
        
        self.john_rules = rules
        return rules

    def apply_mask_patterns(self, base_words: Set[str]) -> Set[str]:
        """Applique des masques de génération (style Crunch)"""
        masked_passwords = set()
        
        mask_mapping = {
            '?l': 'abcdefghijklmnopqrstuvwxyz',
            '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 
            '?d': '0123456789',
            '?s': '!@#$%^&*()',
            '?w': list(base_words)[:10]  # Limité pour éviter explosion
        }
        
        for mask in self.mask_patterns[:5]:  # Limiter les masques
            if '?w' in mask:
                # Masques avec mots
                for word in list(base_words)[:5]:
                    pattern = mask.replace('?w', word)
                    passwords = self._generate_from_simple_mask(pattern, mask_mapping)
                    masked_passwords.update(passwords)
            else:
                # Masques purs
                passwords = self._generate_from_simple_mask(mask, mask_mapping)
                masked_passwords.update(passwords)
        
        return masked_passwords

    def _generate_from_simple_mask(self, mask: str, mapping: dict) -> Set[str]:
        """Génère des mots de passe depuis un masque simple"""
        passwords = set()
        
        # Version simplifiée - en production, utiliser un générateur plus sophistiqué
        parts = []
        i = 0
        while i < len(mask):
            if i < len(mask) - 1 and mask[i:i+2] in mapping:
                charset = mapping[mask[i:i+2]]
                if isinstance(charset, list):
                    parts.append(charset[:3])  # Limiter
                else:
                    parts.append(list(charset)[:5])  # Limiter
                i += 2
            else:
                parts.append([mask[i]])
                i += 1
        
        # Génération avec limitation
        try:
            for combination in itertools.product(*parts):
                password = ''.join(combination)
                if 6 <= len(password) <= 20:
                    passwords.add(password)
                if len(passwords) > 100:  # Limite pour éviter explosion
                    break
        except:
            pass
            
        return passwords

    def generate_advanced_transformations(self, base_words: Set[str]) -> Set[str]:
        """Applique des transformations avancées (style Mentalist)"""
        transformed = set()
        
        for word in list(base_words)[:10]:  # Limiter pour éviter explosion
            # Transformations de casse avancées
            variations = [
                word.lower(),
                word.upper(), 
                word.capitalize(),
                word.title(),
                self._alternate_case(word),
                self._random_case(word)
            ]
            
            for variation in variations:
                transformed.add(variation)
                
                # Substitutions leet avancées
                leet_basic = self._apply_leet_speak(variation, 'leet_basic')
                leet_advanced = self._apply_leet_speak(variation, 'leet_advanced')
                transformed.update([leet_basic, leet_advanced])
                
                # Insertions et préfixes/suffixes
                for num in self.transformation_rules['number_patterns'][:5]:
                    transformed.add(f"{variation}{num}")
                    transformed.add(f"{num}{variation}")
                    
                for symbol in self.transformation_rules['symbol_patterns'][:5]:
                    transformed.add(f"{variation}{symbol}")
                    transformed.add(f"{symbol}{variation}")
                    
                # Transformations de position
                if len(variation) > 3:
                    transformed.add(variation[::-1])  # Reverse
                    transformed.add(variation[1:] + variation[0])  # Rotate
                    
        return transformed

    def _alternate_case(self, word: str) -> str:
        """Alterne majuscules/minuscules"""
        result = []
        for i, char in enumerate(word):
            result.append(char.upper() if i % 2 == 0 else char.lower())
        return ''.join(result)

    def _random_case(self, word: str) -> str:
        """Casse aléatoire contrôlée"""
        result = []
        for char in word:
            result.append(char.upper() if random.random() > 0.5 else char.lower())
        return ''.join(result)

    def _apply_leet_speak(self, word: str, leet_type: str) -> str:
        """Applique une transformation leet speak"""
        result = word.lower()
        leet_dict = self.transformation_rules[leet_type]
        
        for original, replacement in leet_dict.items():
            result = result.replace(original, replacement)
            
        return result

    def generate_keyboard_walks(self) -> Set[str]:
        """Génère des "keyboard walks" et séquences"""
        walks = set()
        
        # Séquences de clavier courantes
        keyboard_patterns = [
            'qwerty', 'qwertyuiop', 'asdfgh', 'asdfghjkl', 'zxcvbn', 'zxcvbnm',
            '123456', '1234567890', '987654321', 'abcdef', 'fedcba'
        ]
        
        for pattern in keyboard_patterns:
            walks.add(pattern)
            walks.add(pattern.upper())
            walks.add(pattern.capitalize())
            
            # Avec suffixes
            for suffix in ['!', '123', '01', '2024']:
                walks.add(f"{pattern}{suffix}")
        
        return walks

    def generate_wordlist_professional(self, 
                                     max_length: int = None, 
                                     min_length: int = 4,
                                     include_scraped: bool = False,
                                     include_osint: bool = False,
                                     target_url: str = None) -> List[str]:
        """Génère une wordlist professionnelle complète"""
        print("[+] === GÉNÉRATION WORDLIST PROFESSIONNELLE ===")
        all_passwords = set()
        
        # 1. Mots de base depuis le profil
        print("[+] Extraction des mots de base...")
        base_words = self._extract_all_base_words()
        all_passwords.update(base_words)
        print(f"    → {len(base_words)} mots de base")
        
        # 2. Scraping web si demandé
        if include_scraped and target_url:
            scraped = self.scrape_target_website(target_url)
            base_words.update(scraped)
            print(f"    → {len(scraped)} mots scrapés")
        
        # 3. OSINT keywords
        if include_osint:
            osint_keywords = self.generate_osint_keywords()
            base_words.update(osint_keywords)
            print(f"    → {len(osint_keywords)} mots-clés OSINT")
        
        # 4. Transformations avancées
        print("[+] Application des transformations avancées...")
        advanced = self.generate_advanced_transformations(base_words)
        all_passwords.update(advanced)
        print(f"    → {len(advanced)} variations avancées")
        
        # 5. Application des masques
        print("[+] Application des masques de génération...")
        masked = self.apply_mask_patterns(base_words)
        all_passwords.update(masked)
        print(f"    → {len(masked)} mots de passe par masques")
        
        # 6. Keyboard walks
        print("[+] Génération des keyboard walks...")
        walks = self.generate_keyboard_walks()
        all_passwords.update(walks)
        print(f"    → {len(walks)} keyboard walks")
        
        # 7. Génération des règles
        print("[+] Génération des règles Hashcat/John...")
        hashcat_rules = self.generate_rules_hashcat()
        john_rules = self.generate_rules_john()
        print(f"    → {len(hashcat_rules)} règles Hashcat, {len(john_rules)} règles John")
        
        # Filtrage final
        filtered = [pwd for pwd in all_passwords 
                   if len(pwd) >= min_length and (not max_length or len(pwd) <= max_length)]
        
        # Tri par probabilité (mots courts et simples d'abord)
        filtered.sort(key=lambda x: (len(x), x.lower()))
        
        print(f"[+] TOTAL: {len(filtered)} mots de passe générés")
        return filtered

    def _extract_all_base_words(self) -> Set[str]:
        """Extrait TOUS les mots de base possibles"""
        words = set()
        
        # Champs texte simples
        simple_fields = ['name', 'surname', 'nickname', 'username', 'pet_name', 
                        'hobby', 'city', 'street', 'favorite_team', 'school']
        
        for field in simple_fields:
            if field in self.base_info and self.base_info[field]:
                words.add(self.base_info[field].lower())
        
        # Combinaisons de noms
        if 'name_combinations' in self.base_info:
            words.update(self.base_info['name_combinations'])
        
        # Mots-clés
        if 'keywords' in self.base_info:
            words.update([kw.lower() for kw in self.base_info['keywords']])
        
        # Dates sous différents formats
        if 'birth_date' in self.base_info:
            birth = self.base_info['birth_date']
            words.update([birth, birth[-4:], birth[-2:], birth[:4], birth[2:6]])
        
        return words

    def save_wordlist_professional(self, wordlist: List[str], filename: str = None, 
                                 save_rules: bool = True):
        """Sauvegarde professionnelle avec règles séparées"""
        if not filename:
            target_name = self.base_info.get('name', 'target')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{target_name}_professional_{timestamp}.txt"
        
        # Sauvegarde de la wordlist principale
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Professional Wordlist - Generated {datetime.now()}\n")
            f.write(f"# Target: {self.base_info.get('name', 'Unknown')}\n")
            f.write(f"# Total passwords: {len(wordlist)}\n")
            f.write("#" + "="*60 + "\n\n")
            
            for password in wordlist:
                f.write(f"{password}\n")
        
        print(f"[+] Wordlist sauvegardée: {filename}")
        
        # Sauvegarde des règles si demandé
        if save_rules:
            base_name = filename.rsplit('.', 1)[0]
            
            # Règles Hashcat
            hashcat_file = f"{base_name}_hashcat.rule"
            with open(hashcat_file, 'w') as f:
                f.write("# Hashcat rules generated by Professional Wordlist Generator\n")
                for rule in self.hashcat_rules:
                    f.write(f"{rule}\n")
            print(f"[+] Règles Hashcat: {hashcat_file}")
            
            # Règles John
            john_file = f"{base_name}_john.rule"
            with open(john_file, 'w') as f:
                f.write("# John the Ripper rules\n")
                for rule in self.john_rules:
                    f.write(f"{rule}\n")
            print(f"[+] Règles John: {john_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Professional Wordlist Generator - Niveau CUPP/Mentalist/Wister",
        epilog="Usage professionnel pour tests de pénétration autorisés"
    )
    
    parser.add_argument('-i', '--input', help='Fichier JSON avec informations cible')
    parser.add_argument('-o', '--output', help='Fichier de sortie')
    parser.add_argument('-u', '--url', help='URL à scraper (style CeWL)')
    parser.add_argument('-k', '--api-key', help='Clé API Gemini pour génération IA')
    parser.add_argument('--min-length', type=int, default=4, help='Longueur minimale')
    parser.add_argument('--max-length', type=int, help='Longueur maximale')
    parser.add_argument('--include-scraped', action='store_true', help='Inclure mots scrapés')
    parser.add_argument('--include-osint', action='store_true', help='Inclure OSINT automatique')
    parser.add_argument('--save-rules', action='store_true', help='Sauvegarder règles Hashcat/John')
    parser.add_argument('--interactive', action='store_true', help='Mode interactif')
    parser.add_argument('--debug', action='store_true', help='Mode debug')
    
    args = parser.parse_args()
    
    # Initialisation
    generator = ProfessionalWordlistGenerator(args.api_key)
    
    if args.interactive:
        print("=== GÉNÉRATEUR WORDLIST PROFESSIONNEL ===")
        personal_info = {}
        
        # Collecte d'informations étendue
        print("Informations de base:")
        personal_info['name'] = input("Prénom: ").strip()
        personal_info['surname'] = input("Nom: ").strip() 
        personal_info['middle_name'] = input("Deuxième prénom: ").strip()
        personal_info['nickname'] = input("Surnom: ").strip()
        personal_info['birth_date'] = input("Date naissance (DDMMYYYY): ").strip()
        
        print("\nInformations professionnelles:")
        personal_info['company'] = input("Entreprise: ").strip()
        personal_info['job_title'] = input("Poste: ").strip()
        personal_info['department'] = input("Département: ").strip()
        
        print("\nInformations personnelles:")
        personal_info['pet_name'] = input("Animal domestique: ").strip()
        personal_info['hobby'] = input("Hobby/Passion: ").strip()
        personal_info['city'] = input("Ville: ").strip()
        personal_info['street'] = input("Rue/Adresse: ").strip()
        personal_info['favorite_team'] = input("Équipe favorite: ").strip()
        personal_info['school'] = input("École/Université: ").strip()
        
        keywords = input("\nMots-clés supplémentaires (séparés par virgules): ").strip()
        if keywords:
            personal_info['keywords'] = [kw.strip() for kw in keywords.split(',')]
        
        # Options avancées
        print("\nOptions avancées:")
        target_url = input("URL à scraper (optionnel): ").strip()
        if target_url:
            args.url = target_url
            args.include_scraped = True
            
        use_osint = input("Utiliser OSINT automatique? (y/N): ").strip().lower()
        if use_osint in ['y', 'yes', 'oui']:
            args.include_osint = True
            
        # Nettoyage
        personal_info = {k: v for k, v in personal_info.items() if v}
        
    elif args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                personal_info = json.load(f)
        except Exception as e:
            print(f"[-] Erreur chargement fichier: {e}")
            return
    else:
        # Données d'exemple étendues
        personal_info = {
            "name": "Souley",
            "surname": "Diallo",
            "middle_name": "Amadou", 
            "nickname": "sdiallo",
            "birth_date": "15031990",
            "company": "TechSenegal SARL",
            "job_title": "Administrateur Système",
            "department": "IT Security",
            "pet_name": "rex",
            "hobby": "football cybersécurité",
            "city": "Dakar",
            "street": "Almadies",
            "favorite_team": "Terangalions ASC",
            "school": "Université Cheikh Anta Diop",
            "keywords": ["admin", "tech", "linux", "server", "security"]
        }
        print("[i] Utilisation des données d'exemple étendues.")
    
    try:
        # Génération professionnelle
        generator.load_personal_info(personal_info)
        
        wordlist = generator.generate_wordlist_professional(
            max_length=args.max_length,
            min_length=args.min_length,
            include_scraped=args.include_scraped,
            include_osint=args.include_osint,
            target_url=args.url
        )
        
        if not wordlist:
            print("[-] Aucun mot de passe généré!")
            return
        
        # Statistiques détaillées
        display_professional_stats(wordlist, generator)
        
        # Sauvegarde
        generator.save_wordlist_professional(
            wordlist, 
            args.output, 
            save_rules=args.save_rules
        )
        
        # Aperçu des résultats
        print(f"\n[+] TOP 20 mots de passe les plus probables:")
        for i, pwd in enumerate(wordlist[:20], 1):
            print(f"    {i:2d}. {pwd}")
        
        # Test spécifique pour patterns connus
        test_common_patterns(wordlist, personal_info)
        
        # Conseils d'utilisation
        print_usage_recommendations(generator, args.output or "wordlist.txt")
        
    except KeyboardInterrupt:
        print("\n[-] Génération interrompue par l'utilisateur")
    except Exception as e:
        print(f"[-] Erreur fatale: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()


def display_professional_stats(wordlist: List[str], generator):
    """Affiche des statistiques professionnelles détaillées"""
    if not wordlist:
        return
        
    print(f"\n{'='*60}")
    print(f"STATISTIQUES PROFESSIONNELLES")
    print(f"{'='*60}")
    
    # Stats de base
    lengths = [len(pwd) for pwd in wordlist]
    print(f"Total mots de passe    : {len(wordlist):,}")
    print(f"Longueur minimale      : {min(lengths)}")
    print(f"Longueur maximale      : {max(lengths)}")
    print(f"Longueur moyenne       : {sum(lengths)/len(lengths):.1f}")
    
    # Analyse de complexité
    categories = {
        'Alphabétique seul': 0,
        'Alphanumérique': 0, 
        'Avec symboles': 0,
        'Casse mixte': 0,
        'Tout majuscules': 0,
        'Tout minuscules': 0
    }
    
    for pwd in wordlist:
        if pwd.isalpha():
            categories['Alphabétique seul'] += 1
        elif any(c.isdigit() for c in pwd) and any(c.isalpha() for c in pwd):
            categories['Alphanumérique'] += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in pwd):
            categories['Avec symboles'] += 1
        if any(c.isupper() for c in pwd) and any(c.islower() for c in pwd):
            categories['Casse mixte'] += 1
        if pwd.isupper():
            categories['Tout majuscules'] += 1
        elif pwd.islower():
            categories['Tout minuscules'] += 1
    
    print(f"\nAnalyse de complexité:")
    for category, count in categories.items():
        percentage = (count / len(wordlist)) * 100
        print(f"  {category:<20} : {count:>6} ({percentage:5.1f}%)")
    
    # Distribution par longueur
    length_dist = {}
    for length in lengths:
        length_dist[length] = length_dist.get(length, 0) + 1
    
    print(f"\nDistribution par longueur:")
    for length in sorted(length_dist.keys()):
        count = length_dist[length]
        percentage = (count / len(wordlist)) * 100
        bar = '█' * min(int(percentage / 2), 30)
        print(f"  {length:2d} chars: {count:>6} ({percentage:5.1f}%) {bar}")


def test_common_patterns(wordlist: List[str], personal_info: Dict):
    """Teste des patterns de mots de passe courants"""
    print(f"\n[+] TEST DE PATTERNS COURANTS:")
    
    # Patterns à tester basés sur les infos
    name = personal_info.get('name', '').lower()
    surname = personal_info.get('surname', '').lower()
    
    test_patterns = []
    
    if name and surname:
        initials = name[0] + surname[0]
        test_patterns.extend([
            f"{name}123",
            f"{name}123!",
            f"{name}2024",
            f"{surname}123",
            f"{initials}@123*#!",  # Pattern spécifique Souley Diallo
            f"{initials}123",
            f"{name.capitalize()}123!",
            f"{name}{surname}123"
        ])
    
    # Test des patterns
    found_patterns = []
    for pattern in test_patterns:
        if pattern in wordlist:
            position = wordlist.index(pattern) + 1
            found_patterns.append((pattern, position))
    
    if found_patterns:
        print(f"  ✅ {len(found_patterns)} patterns trouvés:")
        for pattern, pos in found_patterns:
            print(f"     • '{pattern}' à la position {pos}")
    else:
        print(f"  ❌ Aucun pattern de test trouvé")
        print(f"     Patterns similaires dans le top 50:")
        similar = []
        for pwd in wordlist[:50]:
            if name in pwd.lower() or (surname and surname in pwd.lower()):
                similar.append(pwd)
        
        for sim in similar[:5]:
            print(f"       - {sim}")


def print_usage_recommendations(generator, output_file: str):
    """Affiche des recommandations d'utilisation"""
    print(f"\n{'='*60}")
    print(f"RECOMMANDATIONS D'UTILISATION")
    print(f"{'='*60}")
    
    base_name = output_file.rsplit('.', 1)[0]
    
    print(f"📁 Fichiers générés:")
    print(f"  • {output_file} - Wordlist principale")
    if generator.hashcat_rules:
        print(f"  • {base_name}_hashcat.rule - Règles Hashcat")
        print(f"  • {base_name}_john.rule - Règles John the Ripper")
    
    print(f"\n🔧 Commandes d'utilisation:")
    print(f"  Hashcat (MD5):")
    print(f"    hashcat -m 0 -a 0 hashes.txt {output_file}")
    if generator.hashcat_rules:
        print(f"    hashcat -m 0 -a 0 hashes.txt {output_file} -r {base_name}_hashcat.rule")
    
    print(f"\n  John the Ripper:")
    print(f"    john --wordlist={output_file} hashes.txt")
    if generator.john_rules:
        print(f"    john --wordlist={output_file} --rules={base_name}_john.rule hashes.txt")
    
    print(f"\n  Hydra (SSH):")
    print(f"    hydra -l username -P {output_file} ssh://target.com")
    
    print(f"\n  Hydra (HTTP Form):")
    print(f"    hydra -l username -P {output_file} target.com http-post-form \"/login:user=^USER^&pass=^PASS^:Invalid\"")
    
    print(f"\n⚡ Conseils d'optimisation:")
    print(f"  • Triez la wordlist par probabilité avant utilisation")
    print(f"  • Utilisez les règles pour multiplier l'efficacité") 
    print(f"  • Combinez avec des dictionnaires standards (rockyou.txt)")
    print(f"  • Adaptez les timeouts selon la cible")
    
    print(f"\n⚖️  Rappel légal:")
    print(f"  • Utilisation autorisée uniquement")
    print(f"  • Tests de pénétration avec contrat")
    print(f"  • Audits de sécurité internes")


if __name__ == "__main__":
    print("=" * 70)
    print("GÉNÉRATEUR WORDLIST PROFESSIONNEL")
    print("Niveau CUPP/Mentalist/Wister - Fonctionnalités avancées")
    print("Usage: Tests de pénétration et audits autorisés UNIQUEMENT")
    print("=" * 70)
    main()