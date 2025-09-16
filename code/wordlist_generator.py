

# Configuration d'exemple pour déploiement
DEPLOYMENT_CONFIG = {
    'production': {
        'debug': False,
        'max_passwords_default': 100000,
        'api_rate_limit': '1000/hour',
        'enable_caching': True,
        'log_level': 'INFO'
    },
    'development': {
        'debug': True,
        'max_passwords_default': 10000,
        'api_rate_limit': '100/minute',
        'enable_caching': False,
        'log_level': 'DEBUG'
    },
    'testing': {
        'debug': True,
        'max_passwords_default': 1000,
        'api_rate_limit': '50/minute',
        'enable_caching': False,
        'log_level': 'DEBUG'
    }
}

# Documentation des API endpoints
API_DOCUMENTATION = {
    'endpoints': {
        '/': {
            'method': 'GET',
            'description': 'Information sur l\'API',
            'response': 'JSON avec métadonnées'
        },
        '/generate': {
            'method': 'POST',
            'description': 'Génère une wordlist personnalisée',
            'parameters': {
                'name': 'string (requis)',
                'surname': 'string (requis)',
                'company': 'string (optionnel)',
                'options': {
                    'max_passwords': 'int (défaut: 10000)',
                    'include_ai': 'bool (défaut: true)',
                    'include_osint': 'bool (défaut: true)',
                    'target_url': 'string (optionnel)'
                }
            },
            'response': 'JSON avec wordlist et statistiques'
        },
        '/profile': {
            'method': 'POST',
            'description': 'Sauvegarde un profil cible',
            'response': 'JSON avec ID du profil'
        },
        '/profile/<id>': {
            'method': 'GET',
            'description': 'Récupère un profil sauvegardé',
            'response': 'JSON avec données du profil'
        },
        '/analyze': {
            'method': 'POST',
            'description': 'Analyse une wordlist existante',
            'parameters': {
                'wordlist': 'array de strings (requis)'
            },
            'response': 'JSON avec analytics et recommandations'
        },
        '/status': {
            'method': 'GET',
            'description': 'Statut du service',
            'response': 'JSON avec état opérationnel'
        }
    },
    'authentication': 'API Key optionnelle (header: X-API-Key)',
    'rate_limiting': 'Basé sur IP, voir configuration',
    'response_format': 'JSON avec structure standardisée'
}

# Scripts d'installation automatique
INSTALL_SCRIPT = """
#!/bin/bash
# Installation automatique - Professional Wordlist Generator

echo "🔐 Installation Professional Wordlist Generator v2.0"
echo "=================================================="

# Vérification Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 requis"
    exit 1
fi

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

# Création des dossiers
mkdir -p output logs config

# Configuration par défaut
if [ ! -f config.ini ]; then
    echo "⚙️ Création configuration par défaut..."
    cat > config.ini << EOF
[ai]
provider = gemini
api_key = 

[scraping]
depth = 2
timeout = 10
user_agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36

[generation]
max_length = 25
min_length = 4
max_passwords = 50000

[security]
encrypt_profiles = true
log_level = INFO
EOF
fi

echo "✅ Installation terminée!"
echo "Usage: python3 wordlist_generator.py --help"
"""




print("🎉 Script Professional Wordlist Generator v2.0 - Prêt à l'emploi!")
print("📖 Consultez --help pour toutes les options disponibles.")
print("🌟 Fonctionnalités complètes: IA, OSINT, GUI, API, Analytics")#!/usr/bin/env python3
"""
Professional Wordlist Generator - Version Complète
Fonctionnalités professionnelles avancées pour cybersécurité offensive
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
import sqlite3
import hashlib
import base64
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional, Tuple, Any
import argparse
import random
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
import asyncio
import aiohttp
from cryptography.fernet import Fernet
import configparser
import pickle
from collections import Counter, defaultdict
import nltk
from nltk.corpus import words
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import plotly.graph_objs as go
import plotly.offline as pyo
from flask import Flask, request, jsonify, render_template
import phonenumbers
from phonenumbers import carrier, geocoder
import yara


# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wordlist_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class TargetProfile:
    """Structure de données pour profil cible"""
    name: str = ""
    surname: str = ""
    middle_name: str = ""
    nickname: str = ""
    username: str = ""
    birth_date: str = ""
    age: int = 0
    company: str = ""
    job_title: str = ""
    department: str = ""
    email: str = ""
    phone: str = ""
    city: str = ""
    country: str = "Sénégal"
    street: str = ""
    postal_code: str = ""
    school: str = ""
    university: str = ""
    pet_name: str = ""
    hobby: str = ""
    favorite_team: str = ""
    keywords: List[str] = None
    social_media: Dict[str, str] = None
    languages: List[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.social_media is None:
            self.social_media = {}
        if self.languages is None:
            self.languages = ["français", "wolof", "english"]
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class DatabaseManager:
    """Gestionnaire de base de données pour profils et métriques"""
    
    def __init__(self, db_path: str = "wordlist_generator.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des profils
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                profile_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des générations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER,
                wordlist_count INTEGER,
                generation_time REAL,
                success_rate REAL DEFAULT 0,
                config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles (id)
            )
        ''')
        
        # Table des mots scrapés (cache)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                words TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des métriques
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_value TEXT,
                success_count INTEGER DEFAULT 0,
                total_attempts INTEGER DEFAULT 0,
                last_success TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_profile(self, profile: TargetProfile) -> int:
        """Sauvegarde un profil en base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        profile_json = json.dumps(asdict(profile), ensure_ascii=False)
        
        cursor.execute('''
            INSERT INTO profiles (name, profile_data)
            VALUES (?, ?)
        ''', (f"{profile.name} {profile.surname}", profile_json))
        
        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Profil sauvegardé avec ID: {profile_id}")
        return profile_id
    
    def load_profile(self, profile_id: int) -> Optional[TargetProfile]:
        """Charge un profil depuis la base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT profile_data FROM profiles WHERE id = ?', (profile_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            profile_data = json.loads(result[0])
            return TargetProfile(**profile_data)
        return None
    
    def get_scraped_cache(self, url: str) -> Optional[Set[str]]:
        """Récupère le cache de scraping pour une URL"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT words FROM scraped_cache 
            WHERE url = ? AND scraped_at > datetime('now', '-7 days')
        ''', (url,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return set(json.loads(result[0]))
        return None
    
    def save_scraped_cache(self, url: str, words: Set[str]):
        """Sauvegarde le cache de scraping"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        words_json = json.dumps(list(words))
        
        cursor.execute('''
            INSERT OR REPLACE INTO scraped_cache (url, words)
            VALUES (?, ?)
        ''', (url, words_json))
        
        conn.commit()
        conn.close()


class CulturalPatterns:
    """Générateur de patterns culturels sénégalais/ouest-africains"""
    
    def __init__(self):
        # Noms wolof/sérère courants
        self.wolof_names = [
            'amadou', 'fatou', 'moussa', 'awa', 'mamadou', 'aissatou',
            'ibrahim', 'marieme', 'ousmane', 'ndeye', 'cheikh', 'rama',
            'modou', 'khady', 'babacar', 'coumba', 'alioune', 'bineta'
        ]
        
        # Dates importantes sénégalaises
        self.important_dates = {
            '04041960': 'Indépendance du Sénégal',
            '20081959': 'Fête de l\'Indépendance Mali',
            '01011960': 'Nouvelle année',
            '14021960': 'Saint Valentin populaire'
        }
        
        # Expressions/mots courants en wolof
        self.wolof_expressions = [
            'teraanga', 'yallah', 'inchallah', 'baraka', 'alhamdoulillah',
            'assalamaleikum', 'barakallah', 'mashallah', 'bismillah'
        ]
        
        # Équipes sportives populaires
        self.teams = [
            'teranga', 'lions', 'jeanne', 'casa', 'niary', 'tally',
            'diaraf', 'gfc', 'linguere', 'pikine'
        ]
        
        # Lieux emblématiques
        self.places = [
            'dakar', 'thies', 'saint-louis', 'kaolack', 'ziguinchor',
            'diourbel', 'louga', 'fatick', 'kolda', 'sedhiou',
            'almadies', 'plateau', 'medina', 'parcelles', 'pikine',
            'guediawaye', 'rufisque', 'bargny'
        ]
        
        # Numérotation téléphonique sénégalaise
        self.phone_patterns = ['77', '78', '76', '70', '75', '33']
        
        # Années importantes récentes
        self.important_years = ['2000', '2012', '2024', '1960', '2019', '2021']
    
    def generate_cultural_variations(self, base_info: Dict) -> Set[str]:
        """Génère des variations culturelles"""
        variations = set()
        
        # Ajout des noms wolof si pas présents
        if base_info.get('name', '').lower() in self.wolof_names:
            variations.update(self.wolof_names)
        
        # Expressions wolof avec années
        for expr in self.wolof_expressions:
            for year in self.important_years:
                variations.add(f"{expr}{year}")
                variations.add(f"{expr}{year[-2:]}")
        
        # Équipes avec numéros
        for team in self.teams:
            for num in ['1', '12', '123', '01', '2024']:
                variations.add(f"{team}{num}")
        
        # Lieux avec codes postaux/années
        for place in self.places:
            variations.add(place)
            variations.add(place.capitalize())
            for year in self.important_years[-3:]:  # Années récentes
                variations.add(f"{place}{year}")
        
        # Patterns téléphoniques
        name = base_info.get('name', '').lower()
        if name:
            for prefix in self.phone_patterns:
                variations.add(f"{name}{prefix}")
                variations.add(f"{prefix}{name}")
        
        return variations
    
    def generate_religious_dates(self) -> Set[str]:
        """Génère des dates religieuses importantes"""
        dates = set()
        
        # Dates islamiques approximatives (variables chaque année)
        ramadan_dates = ['24032024', '13032025', '01032026']  # Début Ramadan
        eid_dates = ['24042024', '13042025', '01042026']      # Eid al-Fitr
        
        dates.update(ramadan_dates + eid_dates)
        
        # Format court
        for date in list(dates):
            if len(date) == 8:
                dates.add(date[2:])  # DDMMYY
                dates.add(date[4:])  # YYYY
                dates.add(date[:4])  # DDMM
        
        return dates


class AIWordlistGenerator:
    """Générateur utilisant l'IA (Gemini/OpenAI)"""
    
    def __init__(self, api_key: str = None, provider: str = "gemini"):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.provider = provider
        self.session = requests.Session()
        
        if not self.api_key:
            logger.warning("Aucune clé API fournie - Fonctionnalités IA désactivées")
    
    def generate_contextual_passwords(self, profile: TargetProfile, count: int = 50) -> Set[str]:
        """Génère des mots de passe contextuels avec IA"""
        if not self.api_key:
            return set()
        
        try:
            context = self._build_context_prompt(profile)
            
            if self.provider == "gemini":
                return self._call_gemini_api(context, count)
            elif self.provider == "openai":
                return self._call_openai_api(context, count)
        except Exception as e:
            logger.error(f"Erreur génération IA: {e}")
            return set()
    
    def _build_context_prompt(self, profile: TargetProfile) -> str:
        """Construit le prompt contextualisé"""
        prompt = f"""
Génère des mots de passe probables pour un profil sénégalais:

INFORMATIONS PERSONNELLES:
- Nom: {profile.name} {profile.surname}
- Surnom: {profile.nickname}
- Âge: {profile.age}
- Ville: {profile.city}
- Entreprise: {profile.company}
- Poste: {profile.job_title}

CONTEXTE CULTUREL:
- Pays: Sénégal (culture wolof/français)
- Langues: {', '.join(profile.languages)}
- Religion probable: Islam
- Contexte: Afrique de l'Ouest

CONSIGNES:
1. Considère les patterns culturels sénégalais
2. Utilise des mots wolof courants (teranga, yallah, etc.)
3. Inclus des dates importantes (indépendance 1960)
4. Mélange français/wolof/anglais
5. Ajoute des numéros de téléphone locaux (77, 78, 76)
6. Utilise des lieux de Dakar (Almadies, Plateau, etc.)
7. Longueur: 6-16 caractères
8. Variété de complexité

Réponds uniquement par une liste de mots de passe, un par ligne.
"""
        return prompt
    
    def _call_gemini_api(self, prompt: str, count: int) -> Set[str]:
        """Appel API Gemini"""
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}"
        
        data = {
            "contents": [{
                "parts": [{"text": f"{prompt}\n\nNombre souhaité: {count}"}]
            }],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 1000
            }
        }
        
        response = self.session.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Extraction des mots de passe
            passwords = set()
            for line in text.split('\n'):
                line = line.strip()
                if line and not line.startswith(('#', '-', '*', '/')):
                    # Nettoie les numéros de liste
                    clean_line = re.sub(r'^\d+\.?\s*', '', line)
                    if 6 <= len(clean_line) <= 20:
                        passwords.add(clean_line)
            
            logger.info(f"IA Gemini: {len(passwords)} mots de passe générés")
            return passwords
        else:
            logger.error(f"Erreur API Gemini: {response.status_code}")
            return set()
    
    def _call_openai_api(self, prompt: str, count: int) -> Set[str]:
        """Appel API OpenAI (GPT)"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Tu es un expert en génération de mots de passe contextuels."},
                {"role": "user", "content": f"{prompt}\n\nNombre souhaité: {count}"}
            ],
            "temperature": 0.8,
            "max_tokens": 1000
        }
        
        response = self.session.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['message']['content']
            
            passwords = set()
            for line in text.split('\n'):
                line = line.strip()
                if line and 6 <= len(line) <= 20:
                    passwords.add(line)
            
            logger.info(f"IA OpenAI: {len(passwords)} mots de passe générés")
            return passwords
        else:
            logger.error(f"Erreur API OpenAI: {response.status_code}")
            return set()


class AdvancedOSINT:
    """Module OSINT avancé pour collecte d'informations"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def search_social_media(self, profile: TargetProfile) -> Dict[str, Any]:
        """Recherche sur réseaux sociaux (version éthique)"""
        social_data = {}
        
        # Recherche publique only - pas d'intrusion
        search_terms = [
            f"{profile.name} {profile.surname}",
            f"{profile.nickname}",
            f"{profile.company}"
        ]
        
        # Simulation de recherche publique
        for term in search_terms:
            # En production, intégrer avec APIs publiques
            social_data[term] = await self._simulate_social_search(term)
        
        return social_data
    
    async def _simulate_social_search(self, term: str) -> Dict:
        """Simule une recherche sociale publique"""
        # Placeholder - en production, utiliser APIs légitimes
        await asyncio.sleep(0.1)  # Simulation
        return {
            'found': random.choice([True, False]),
            'keywords': ['tech', 'senegal', 'dakar'] if random.random() > 0.5 else []
        }
    
    def check_haveibeenpwned(self, email: str) -> Set[str]:
        """Vérifie les fuites de données"""
        if not email:
            return set()
        
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {'hibp-api-key': os.getenv('HIBP_API_KEY', '')}
            
            if not headers['hibp-api-key']:
                logger.warning("Clé API Have I Been Pwned manquante")
                return set()
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                breach_names = {breach['Name'].lower() for breach in breaches}
                logger.info(f"HIBP: {len(breach_names)} fuites trouvées pour {email}")
                return breach_names
            elif response.status_code == 404:
                logger.info(f"HIBP: Aucune fuite trouvée pour {email}")
                return set()
                
        except Exception as e:
            logger.error(f"Erreur HIBP: {e}")
        
        return set()
    
    def analyze_phone_number(self, phone: str) -> Dict[str, str]:
        """Analyse un numéro de téléphone"""
        if not phone:
            return {}
        
        try:
            parsed = phonenumbers.parse(phone, "SN")  # Sénégal par défaut
            
            if phonenumbers.is_valid_number(parsed):
                carrier_name = carrier.name_for_number(parsed, "fr")
                location = geocoder.description_for_number(parsed, "fr")
                
                return {
                    'carrier': carrier_name or '',
                    'location': location or '',
                    'country': phonenumbers.region_code_for_number(parsed) or '',
                    'type': 'mobile' if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else 'unknown'
                }
        except Exception as e:
            logger.error(f"Erreur analyse téléphone: {e}")
        
        return {}


class ProfessionalWordlistGenerator:
    """Générateur principal avec toutes les fonctionnalités avancées"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config = self._load_config(config_file)
        self.db = DatabaseManager()
        self.cultural = CulturalPatterns()
        self.ai_generator = AIWordlistGenerator(
            self.config.get('ai', {}).get('api_key'),
            self.config.get('ai', {}).get('provider', 'gemini')
        )
        self.osint = AdvancedOSINT()
        
        # Données de génération
        self.base_info = {}
        self.profile = None
        self.generated_passwords = set()
        self.scraped_words = set()
        self.social_media_data = {}
        self.generation_stats = defaultdict(int)
        
        # Règles de transformation avancées
        self.transformation_rules = {
            'leet_basic': {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'g': '9', 'l': '1'},
            'leet_advanced': {'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$', 't': '+', 'g': '6', 'c': '(', 'h': '#'},
            'leet_extreme': {'a': '4', 'e': '€', 'i': '!', 'o': '°', 's': '$', 't': '†', 'g': '6', 'l': '|', 'z': '2'},
            'substitutions': {'and': '&', 'at': '@', 'to': '2', 'for': '4', 'you': 'u', 'be': 'b'},
            'caps_patterns': ['upper', 'lower', 'title', 'capitalize', 'alternate', 'random'],
            'number_patterns': ['123', '12', '1', '01', '007', '21', '69', '99', '2023', '2024', '2025', '77', '78'],
            'symbol_patterns': ['!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '?', '~', '€', '§'],
            'date_formats': ['DDMM', 'MMDD', 'DDMMYY', 'MMDDYY', 'DDMMYYYY', 'MMDDYYYY', 'YYYY', 'YY'],
            'keyboard_walks': ['qwerty', '123456', 'asdf', 'zxcvbn', '987654321', 'qazwsx', 'azerty', '147258']
        }
        
        # Chargement des dictionnaires
        self._load_dictionaries()
        
        logger.info("Générateur initialisé avec succès")
    
    def _load_config(self, config_file: str) -> Dict:
        """Charge la configuration"""
        config = configparser.ConfigParser()
        
        if os.path.exists(config_file):
            config.read(config_file)
            return {section: dict(config[section]) for section in config.sections()}
        else:
            # Configuration par défaut
            default_config = {
                'ai': {'provider': 'gemini', 'api_key': ''},
                'scraping': {'depth': '2', 'timeout': '10', 'user_agent': 'Mozilla/5.0'},
                'generation': {'max_length': '20', 'min_length': '4', 'max_passwords': '100000'},
                'security': {'encrypt_profiles': 'true', 'log_level': 'INFO'}
            }
            
            # Créer le fichier de config
            with open(config_file, 'w') as f:
                config_obj = configparser.ConfigParser()
                for section, values in default_config.items():
                    config_obj[section] = values
                config_obj.write(f)
            
            return default_config
    
    def _load_dictionaries(self):
        """Charge les dictionnaires de mots"""
        try:
            # Téléchargement NLTK si nécessaire
            import nltk
            nltk.download('words', quiet=True)
            from nltk.corpus import words
            self.english_words = set(words.words())
        except:
            self.english_words = set()
        
        # Dictionnaire français basique
        self.french_words = {
            'bonjour', 'salut', 'merci', 'oui', 'non', 'peut', 'être',
            'avoir', 'faire', 'dire', 'aller', 'voir', 'savoir', 'pouvoir',
            'mot', 'passe', 'sécurité', 'ordinateur', 'internet', 'email'
        }
    
    def load_profile(self, profile_data: Dict) -> TargetProfile:
        """Charge un profil cible"""
        if isinstance(profile_data, dict):
            self.profile = TargetProfile(**profile_data)
        else:
            self.profile = profile_data
        
        self.base_info = asdict(self.profile)
        self._enhance_profile_info()
        
        logger.info(f"Profil chargé: {self.profile.name} {self.profile.surname}")
        return self.profile
    
    def _enhance_profile_info(self):
        """Enrichit automatiquement les informations du profil"""
        # Calcul de l'âge si date de naissance
        if self.profile.birth_date and len(self.profile.birth_date) >= 4:
            try:
                birth_year = int(self.profile.birth_date[-4:])
                self.profile.age = datetime.now().year - birth_year
            except:
                pass
        
        # Extraction d'informations du téléphone
        if self.profile.phone:
            phone_info = self.osint.analyze_phone_number(self.profile.phone)
            if phone_info:
                self.base_info['phone_info'] = phone_info
        
        # Génération des combinaisons de noms
        self._generate_name_combinations()
        
        # Extraction de mots-clés depuis les champs texte
        self._extract_keywords_from_fields()
    
    def _generate_name_combinations(self):
        """Génère toutes les combinaisons possibles de noms"""
        combinations = set()
        
        name = self.profile.name.lower() if self.profile.name else ''
        surname = self.profile.surname.lower() if self.profile.surname else ''
        nickname = self.profile.nickname.lower() if self.profile.nickname else ''
        middle = self.profile.middle_name.lower() if self.profile.middle_name else ''
        
        if name and surname:
            # Combinaisons basiques
            combinations.update([
                name, surname, nickname,
                f"{name}{surname}", f"{surname}{name}",
                f"{name[0]}{surname}", f"{surname[0]}{name}",
                f"{name}{surname[0]}", f"{surname}{name[0]}",
                f"{name[0]}{surname[0]}", f"{surname[0]}{name[0]}"
            ])
            
            # Avec nom du milieu
            if middle:
                combinations.update([
                    f"{name[0]}{middle[0]}{surname[0]}",
                    f"{name}{middle[0]}", f"{middle[0]}{surname}",
                    f"{name}{middle}", f"{middle}{surname}"
                ])
        
        # Variations avec underscores et points
        base_combinations = list(combinations)
        for combo in base_combinations:
            if len(combo) > 3:
                combinations.add(combo.replace(' ', '_'))
                combinations.add(combo.replace(' ', '.'))
                combinations.add(combo.replace(' ', '-'))
        
        self.base_info['name_combinations'] = list(combinations)
    
    def _extract_keywords_from_fields(self):
        """Extrait des mots-clés depuis tous les champs texte"""
        keywords = set(self.profile.keywords or [])
        
        text_fields = ['company', 'job_title', 'department', 'street', 'school', 'university', 'hobby']
        
        for field in text_fields:
            field_value = getattr(self.profile, field, '')
            if field_value:
                # Extraction de mots significatifs
                words = re.findall(r'\b[a-zA-Z]{3,}\b', field_value.lower())
                keywords.update(words)
        
        self.profile.keywords = list(keywords)
        self.base_info['keywords'] = list(keywords)
    
    async def advanced_scraping(self, url: str, depth: int = 2) -> Set[str]:
        """Scraping avancé avec cache et analyse sémantique"""
        logger.info(f"Scraping avancé: {url} (profondeur: {depth})")
        
        # Vérification cache
        cached_words = self.db.get_scraped_cache(url)
        if cached_words:
            logger.info(f"Cache utilisé: {len(cached_words)} mots")
            return cached_words
        
        scraped_words = set()
        visited_urls = set()
        
        async def scrape_page(session, page_url: str, current_depth: int):
            if current_depth > depth or page_url in visited_urls:
                return
                
            visited_urls.add(page_url)
            
            try:
                async with session.get(page_url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extraction du texte visible
                        for script in soup(["script", "style"]):
                            script.extract()
                        
                        text = soup.get_text()
                        
                        # Extraction de mots avec analyse de fréquence
                        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
                        word_freq = Counter(words)
                        
                        # Garder les mots les plus fréquents (potentiellement importants)
                        for word, freq in word_freq.most_common(200):
                            if freq >= 2 and len(word) <= 20:
                                scraped_words.add(word)
                        
                        # Extraction spécialisée
                        # Emails et noms d'utilisateur
                        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
                        for email in emails:
                            username = email.split('@')[0]
                            scraped_words.add(username.lower())
                        
                        # Numéros de téléphone sénégalais
                        phone_numbers = re.findall(r'\b(77|78|76|70|75|33)\d{7}\b', content)
                        for phone in phone_numbers:
                            scraped_words.add(phone)
                        
                        # Métadonnées et attributs
                        for meta in soup.find_all('meta'):
                            content_attr = meta.get('content', '')
                            if content_attr:
                                meta_words = re.findall(r'\b[a-zA-Z]{4,}\b', content_attr.lower())
                                scraped_words.update(meta_words[:10])
                        
                        # Navigation récursive
                        if current_depth < depth:
                            links = soup.find_all('a', href=True)[:20]
                            for link in links:
                                next_url = urljoin(page_url, link['href'])
                                if urlparse(next_url).netloc == urlparse(url).netloc:
                                    await scrape_page(session, next_url, current_depth + 1)
                                    
            except Exception as e:
                logger.error(f"Erreur scraping {page_url}: {e}")
        
        # Scraping asynchrone
        async with aiohttp.ClientSession() as session:
            await scrape_page(session, url, 0)
        
        # Sauvegarde en cache
        if scraped_words:
            self.db.save_scraped_cache(url, scraped_words)
        
        logger.info(f"Scraping terminé: {len(scraped_words)} mots extraits")
        return scraped_words
    
    async def comprehensive_osint(self) -> Dict[str, Any]:
        """OSINT complet et éthique"""
        osint_data = {}
        
        if not self.profile:
            return osint_data
        
        logger.info("Démarrage OSINT complet...")
        
        # 1. Recherche sociale publique
        social_data = await self.osint.search_social_media(self.profile)
        osint_data['social'] = social_data
        
        # 2. Vérification fuites de données
        if self.profile.email:
            breaches = self.osint.check_haveibeenpwned(self.profile.email)
            osint_data['breaches'] = list(breaches)
        
        # 3. Analyse géolocalisation
        if self.profile.city:
            geo_keywords = self._generate_geo_keywords(self.profile.city, self.profile.country)
            osint_data['geo_keywords'] = geo_keywords
        
        # 4. Génération de mots-clés contextuels
        context_keywords = self._generate_context_keywords()
        osint_data['context_keywords'] = context_keywords
        
        logger.info(f"OSINT terminé: {sum(len(v) if isinstance(v, list) else 1 for v in osint_data.values())} éléments")
        return osint_data
    
    def _generate_geo_keywords(self, city: str, country: str) -> List[str]:
        """Génère des mots-clés géographiques"""
        keywords = []
        
        if city:
            city_lower = city.lower()
            keywords.extend([
                city_lower,
                city_lower[:4] if len(city_lower) > 4 else city_lower,
                city_lower.replace(' ', ''),
                city_lower.replace('-', '')
            ])
        
        if country and country.lower() == 'sénégal':
            keywords.extend(['senegal', 'sn', 'dakar', 'afrique'])
        
        return keywords
    
    def _generate_context_keywords(self) -> List[str]:
        """Génère des mots-clés contextuels avancés"""
        keywords = []
        
        # Secteur d'activité
        if self.profile.company:
            company = self.profile.company.lower()
            # Extraction de mots significatifs
            company_words = re.findall(r'\b[a-zA-Z]{3,}\b', company)
            keywords.extend(company_words)
            
            # Acronymes
            if ' ' in company:
                acronym = ''.join([word[0] for word in company.split()])
                keywords.append(acronym)
        
        # Domaine professionnel
        if self.profile.job_title:
            job_words = re.findall(r'\b[a-zA-Z]{3,}\b', self.profile.job_title.lower())
            keywords.extend(job_words)
        
        # Années importantes déduites
        current_year = datetime.now().year
        birth_year = None
        
        if self.profile.birth_date and len(self.profile.birth_date) >= 4:
            try:
                birth_year = int(self.profile.birth_date[-4:])
                # Années de remise de diplôme probables
                keywords.extend([
                    str(birth_year + 18),  # Bac
                    str(birth_year + 22),  # Licence
                    str(birth_year + 24)   # Master
                ])
            except:
                pass
        
        return list(set(keywords))
    
    def generate_advanced_patterns(self) -> Set[str]:
        """Génère des patterns avancés multi-culturels"""
        patterns = set()
        
        if not self.profile:
            return patterns
        
        # 1. Patterns culturels sénégalais
        cultural_variations = self.cultural.generate_cultural_variations(self.base_info)
        patterns.update(cultural_variations)
        
        # 2. Patterns religieux
        religious_dates = self.cultural.generate_religious_dates()
        patterns.update(religious_dates)
        
        # 3. Patterns professionnels
        if self.profile.company:
            company = self.profile.company.lower().replace(' ', '')
            patterns.update([
                f"{company}123",
                f"{company}2024",
                f"{company}!",
                company[:6] + "123" if len(company) > 6 else company + "123"
            ])
        
        # 4. Patterns familiaux
        if self.profile.name and self.profile.surname:
            name_combos = self.base_info.get('name_combinations', [])
            for combo in name_combos[:10]:  # Limiter
                patterns.update([
                    f"{combo}123",
                    f"{combo}123!",
                    f"{combo}2024",
                    f"{combo}@123",
                    combo.capitalize() + "123"
                ])
        
        # 5. Patterns spécifiques Sénégal
        if self.profile.phone:
            # Extraction préfixe téléphonique
            phone_prefix = re.findall(r'^(77|78|76|70|75|33)', self.profile.phone)
            if phone_prefix:
                prefix = phone_prefix[0]
                name = self.profile.name.lower() if self.profile.name else 'user'
                patterns.update([
                    f"{name}{prefix}",
                    f"{prefix}{name}",
                    f"{name}{prefix}123"
                ])
        
        return patterns
    
    async def generate_ai_enhanced_wordlist(self) -> Set[str]:
        """Génère une wordlist améliorée par IA"""
        ai_passwords = set()
        
        if not self.ai_generator.api_key:
            logger.warning("IA désactivée - clé API manquante")
            return ai_passwords
        
        logger.info("Génération IA en cours...")
        
        try:
            # Génération contextuelle principale
            main_passwords = self.ai_generator.generate_contextual_passwords(self.profile, 100)
            ai_passwords.update(main_passwords)
            
            # Génération spécialisée par domaine
            domains = ['professionnel', 'personnel', 'culturel']
            for domain in domains:
                specialized_profile = self._create_specialized_profile(domain)
                specialized_passwords = self.ai_generator.generate_contextual_passwords(specialized_profile, 30)
                ai_passwords.update(specialized_passwords)
            
            logger.info(f"IA: {len(ai_passwords)} mots de passe générés")
            
        except Exception as e:
            logger.error(f"Erreur génération IA: {e}")
        
        return ai_passwords
    
    def _create_specialized_profile(self, domain: str) -> TargetProfile:
        """Crée un profil spécialisé pour un domaine"""
        specialized = TargetProfile(**asdict(self.profile))
        
        if domain == 'professionnel':
            # Accent sur l'aspect professionnel
            specialized.keywords.extend(['work', 'job', 'office', 'admin', 'manager'])
        elif domain == 'personnel':
            # Accent sur l'aspect personnel
            specialized.keywords.extend(['family', 'home', 'personal', 'private'])
        elif domain == 'culturel':
            # Accent sur l'aspect culturel sénégalais
            specialized.keywords.extend(['teranga', 'senegal', 'wolof', 'dakar'])
        
        return specialized
    
    def apply_advanced_transformations(self, base_words: Set[str], max_variations: int = 1000) -> Set[str]:
        """Applique des transformations avancées avec limitation intelligente"""
        transformed = set()
        word_priority = self._prioritize_words(base_words)
        
        for word, priority in word_priority[:50]:  # Top 50 mots par priorité
            # Transformations de base
            variations = self._apply_basic_transformations(word)
            transformed.update(variations)
            
            # Transformations leet avancées
            for leet_type in ['leet_basic', 'leet_advanced', 'leet_extreme']:
                leet_word = self._apply_leet_speak(word, leet_type)
                transformed.add(leet_word)
                
                # Combinaisons avec années et symboles
                for year in ['2024', '2023', '2025', '24', '23', '25']:
                    transformed.add(f"{leet_word}{year}")
                    transformed.add(f"{year}{leet_word}")
                
                for symbol in ['!', '@', '#', '
        , '*']:
                    transformed.add(f"{leet_word}{symbol}")
            
            # Transformations positionnelles
            if len(word) > 4:
                transformed.update([
                    word[::-1],  # Reverse
                    word[1:] + word[0],  # Rotation
                    word[:-1] + word[-1].upper(),  # Dernière lettre maj
                    word[0].upper() + word[1:],  # Première lettre maj
                ])
            
            # Limitation pour éviter explosion
            if len(transformed) > max_variations:
                break
        
        logger.info(f"Transformations: {len(transformed)} variations générées")
        return transformed
    
    def _prioritize_words(self, words: Set[str]) -> List[Tuple[str, float]]:
        """Priorise les mots par probabilité d'utilisation"""
        word_scores = []
        
        for word in words:
            score = 0.0
            
            # Bonus pour noms/prénoms
            if word.lower() in [self.profile.name.lower(), self.profile.surname.lower()]:
                score += 10.0
            
            # Bonus pour mots courts (plus probables)
            if 4 <= len(word) <= 8:
                score += 5.0
            elif len(word) <= 12:
                score += 2.0
            
            # Bonus pour mots alphabétiques simples
            if word.isalpha():
                score += 3.0
            
            # Bonus pour mots culturels
            if word.lower() in self.cultural.wolof_expressions:
                score += 8.0
            
            # Malus pour mots trop longs ou complexes
            if len(word) > 15:
                score -= 5.0
            
            word_scores.append((word, score))
        
        # Tri par score décroissant
        return sorted(word_scores, key=lambda x: x[1], reverse=True)
    
    def _apply_basic_transformations(self, word: str) -> Set[str]:
        """Applique les transformations de base"""
        variations = set()
        
        variations.update([
            word.lower(),
            word.upper(),
            word.capitalize(),
            word.title()
        ])
        
        # Transformations avec chiffres courants
        for num in ['1', '12', '123', '01', '2024', '77', '78']:
            variations.update([
                f"{word}{num}",
                f"{num}{word}",
                f"{word.capitalize()}{num}"
            ])
        
        # Transformations avec symboles
        for symbol in ['!', '@', '#', '
        , '*', '+']:
            variations.update([
                f"{word}{symbol}",
                f"{symbol}{word}"
            ])
        
        return variations
    
    def _apply_leet_speak(self, word: str, leet_type: str = 'leet_basic') -> str:
        """Applique une transformation leet speak"""
        if leet_type not in self.transformation_rules:
            leet_type = 'leet_basic'
        
        result = word.lower()
        leet_dict = self.transformation_rules[leet_type]
        
        for original, replacement in leet_dict.items():
            result = result.replace(original, replacement)
        
        return result
    
    def apply_mask_generation(self, base_words: Set[str]) -> Set[str]:
        """Génération par masques avec optimisation"""
        masked_passwords = set()
        
        # Sélection des meilleurs mots de base
        priority_words = [word for word, _ in self._prioritize_words(base_words)[:10]]
        
        # Masques optimisés pour le Sénégal
        senegal_masks = [
            '?w?d?d',           # mot + 2 chiffres
            '?w?d?d?d',         # mot + 3 chiffres
            '?w?s',             # mot + symbole
            '?w?d?d?s',         # mot + 2 chiffres + symbole
            '?w77?d',           # mot + préfixe téléphone sénégalais
            '?w78?d?d',         # mot + préfixe téléphone + chiffres
            '?d?d?w',           # 2 chiffres + mot
            '?u?l?l?w?d?d',     # Maj + 2 min + mot + 2 chiffres
        ]
        
        for mask in senegal_masks:
            for word in priority_words:
                patterns = self._generate_mask_patterns(mask, word)
                masked_passwords.update(patterns)
                
                if len(masked_passwords) > 500:  # Limitation
                    break
            
            if len(masked_passwords) > 500:
                break
        
        logger.info(f"Masques: {len(masked_passwords)} mots de passe générés")
        return masked_passwords
    
    def _generate_mask_patterns(self, mask: str, base_word: str) -> Set[str]:
        """Génère des patterns depuis un masque"""
        patterns = set()
        
        # Remplacements de base
        charset_map = {
            '?l': 'abcdefghijklmnopqrstuvwxyz',
            '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '?d': '0123456789',
            '?s': '!@#$%^&*()+=-_',
            '?w': [base_word]
        }
        
        # Version simplifiée pour éviter explosion combinatoire
        try:
            # Remplacement des masques
            pattern = mask
            pattern = pattern.replace('?w', base_word)
            
            # Génération limitée pour les autres masques
            parts = []
            i = 0
            while i < len(pattern):
                if i < len(pattern) - 1 and pattern[i:i+2] in charset_map:
                    charset = charset_map[pattern[i:i+2]]
                    if isinstance(charset, str):
                        # Limitation à 3 caractères par charset pour éviter explosion
                        parts.append(list(charset)[:3])
                    else:
                        parts.append(charset)
                    i += 2
                else:
                    parts.append([pattern[i]])
                    i += 1
            
            # Génération avec limitation stricte
            count = 0
            for combination in itertools.product(*parts):
                if count >= 20:  # Limite stricte
                    break
                password = ''.join(combination)
                if 4 <= len(password) <= 20:
                    patterns.add(password)
                count += 1
                    
        except Exception as e:
            logger.debug(f"Erreur génération masque {mask}: {e}")
        
        return patterns
    
    async def generate_comprehensive_wordlist(self, 
                                           max_passwords: int = 50000,
                                           include_ai: bool = True,
                                           include_osint: bool = True,
                                           target_url: str = None) -> List[str]:
        """Génère une wordlist complète et optimisée"""
        logger.info("=== GÉNÉRATION WORDLIST COMPLÈTE ===")
        all_passwords = set()
        
        if not self.profile:
            raise ValueError("Aucun profil chargé")
        
        # 1. Mots de base depuis le profil
        logger.info("Extraction mots de base...")
        base_words = self._extract_comprehensive_base_words()
        all_passwords.update(base_words)
        self.generation_stats['base_words'] = len(base_words)
        
        # 2. Patterns culturels avancés
        logger.info("Génération patterns culturels...")
        cultural_patterns = self.generate_advanced_patterns()
        all_passwords.update(cultural_patterns)
        self.generation_stats['cultural_patterns'] = len(cultural_patterns)
        
        # 3. Scraping web si URL fournie
        if target_url:
            logger.info(f"Scraping avancé: {target_url}")
            scraped_words = await self.advanced_scraping(target_url, depth=2)
            base_words.update(scraped_words)
            self.generation_stats['scraped_words'] = len(scraped_words)
        
        # 4. OSINT complet
        if include_osint:
            logger.info("OSINT complet...")
            osint_data = await self.comprehensive_osint()
            
            # Intégration des données OSINT
            osint_keywords = []
            for key, value in osint_data.items():
                if isinstance(value, list):
                    osint_keywords.extend(value)
            
            base_words.update(osint_keywords)
            all_passwords.update(osint_keywords)
            self.generation_stats['osint_keywords'] = len(osint_keywords)
        
        # 5. Génération par IA
        if include_ai:
            logger.info("Génération IA...")
            ai_passwords = await self.generate_ai_enhanced_wordlist()
            all_passwords.update(ai_passwords)
            self.generation_stats['ai_passwords'] = len(ai_passwords)
        
        # 6. Transformations avancées
        logger.info("Transformations avancées...")
        transformed = self.apply_advanced_transformations(base_words, max_variations=max_passwords//4)
        all_passwords.update(transformed)
        self.generation_stats['transformed'] = len(transformed)
        
        # 7. Génération par masques
        logger.info("Génération par masques...")
        masked = self.apply_mask_generation(base_words)
        all_passwords.update(masked)
        self.generation_stats['masked'] = len(masked)
        
        # 8. Patterns spécialisés
        logger.info("Patterns spécialisés...")
        specialized = self._generate_specialized_patterns()
        all_passwords.update(specialized)
        self.generation_stats['specialized'] = len(specialized)
        
        # Filtrage et optimisation finale
        logger.info("Filtrage et optimisation...")
        filtered_passwords = self._filter_and_optimize_passwords(all_passwords, max_passwords)
        
        logger.info(f"GÉNÉRATION TERMINÉE: {len(filtered_passwords)} mots de passe")
        return filtered_passwords
    
    def _extract_comprehensive_base_words(self) -> Set[str]:
        """Extraction complète de tous les mots de base possibles"""
        words = set()
        
        # Champs personnels
        personal_fields = [
            'name', 'surname', 'middle_name', 'nickname', 'username'
        ]
        
        for field in personal_fields:
            value = getattr(self.profile, field, '')
            if value:
                words.add(value.lower())
                # Variations
                words.add(value.capitalize())
                if len(value) > 3:
                    words.add(value[:4])  # Préfixe
                    words.add(value[-4:])  # Suffixe
        
        # Combinaisons de noms
        name_combinations = self.base_info.get('name_combinations', [])
        words.update(name_combinations)
        
        # Informations géographiques
        geo_fields = ['city', 'country', 'street']
        for field in geo_fields:
            value = getattr(self.profile, field, '')
            if value:
                geo_words = re.findall(r'\b[a-zA-Z]{3,}\b', value.lower())
                words.update(geo_words)
        
        # Informations professionnelles
        if self.profile.company:
            company_words = re.findall(r'\b[a-zA-Z]{3,}\b', self.profile.company.lower())
            words.update(company_words)
            
            # Acronymes d'entreprise
            company_parts = self.profile.company.split()
            if len(company_parts) > 1:
                acronym = ''.join([part[0].lower() for part in company_parts])
                words.add(acronym)
        
        # Dates importantes
        if self.profile.birth_date:
            birth = self.profile.birth_date
            words.update([
                birth, birth[-4:], birth[-2:], birth[:4], birth[2:6],
                birth[:2], birth[2:4]  # Jour et mois
            ])
        
        # Mots-clés utilisateur
        words.update(self.profile.keywords or [])
        
        # Nettoyage
        cleaned_words = {word for word in words if word and 2 <= len(word) <= 20}
        
        return cleaned_words
    
    def _generate_specialized_patterns(self) -> Set[str]:
        """Génère des patterns spécialisés par domaine"""
        patterns = set()
        
        # Patterns administrateurs système
        if 'admin' in self.profile.job_title.lower() if self.profile.job_title else False:
            admin_patterns = [
                'admin123', 'root123', 'password123', 'administrator',
                'system123', 'server123', 'linux123', 'windows123'
            ]
            patterns.update(admin_patterns)
        
        # Patterns développeur
        if any(tech in (self.profile.job_title + ' ' + ' '.join(self.profile.keywords)).lower() 
               for tech in ['dev', 'program', 'code', 'tech']):
            dev_patterns = [
                'code123', 'dev123', 'python123', 'java123', 'github123',
                'api123', 'database123', 'frontend123', 'backend123'
            ]
            patterns.update(dev_patterns)
        
        # Patterns par industrie (Sénégal)
        if self.profile.company:
            company_lower = self.profile.company.lower()
            if any(word in company_lower for word in ['bank', 'banque', 'finance']):
                patterns.update(['bank123', 'finance123', 'money123', 'credit123'])
            elif any(word in company_lower for word in ['telecom', 'orange', 'free', 'expresso']):
                patterns.update(['telecom123', 'orange123', 'mobile123', 'phone123'])
            elif any(word in company_lower for word in ['tech', 'digital', 'it']):
                patterns.update(['tech123', 'digital123', 'innovation123'])
        
        return patterns
    
    def _filter_and_optimize_passwords(self, passwords: Set[str], max_count: int) -> List[str]:
        """Filtre et optimise la liste finale de mots de passe"""
        # Filtrage de base
        filtered = []
        for pwd in passwords:
            # Critères de base
            if not (4 <= len(pwd) <= 25):
                continue
            if pwd.isspace() or not pwd.strip():
                continue
            # Éviter les doublons de casse
            if pwd.lower() not in [p.lower() for p in filtered]:
                filtered.append(pwd)
        
        # Score et tri par probabilité
        scored_passwords = []
        for pwd in filtered:
            score = self._calculate_password_probability(pwd)
            scored_passwords.append((pwd, score))
        
        # Tri par score décroissant
        scored_passwords.sort(key=lambda x: x[1], reverse=True)
        
        # Limitation et retour
        final_passwords = [pwd for pwd, _ in scored_passwords[:max_count]]
        
        logger.info(f"Filtrage: {len(passwords)} -> {len(final_passwords)} mots de passe")
        return final_passwords
    
    def _calculate_password_probability(self, password: str) -> float:
        """Calcule la probabilité d'utilisation d'un mot de passe"""
        score = 0.0
        
        # Bonus pour longueur optimale (6-12 caractères)
        if 6 <= len(password) <= 12:
            score += 10.0
        elif 4 <= len(password) <= 16:
            score += 5.0
        
        # Bonus pour éléments personnels
        if self.profile:
            name_lower = self.profile.name.lower() if self.profile.name else ''
            surname_lower = self.profile.surname.lower() if self.profile.surname else ''
            
            if name_lower in password.lower():
                score += 15.0
            if surname_lower in password.lower():
                score += 12.0
            if self.profile.nickname and self.profile.nickname.lower() in password.lower():
                score += 10.0
        
        # Bonus pour patterns courants
        if re.search(r'\d{2,4}
        , password):  # Chiffres à la fin
            score += 8.0
        if password.endswith('123'):
            score += 12.0
        if password.endswith('!'):
            score += 6.0
        if password.endswith(('2024', '2023', '2025')):
            score += 8.0
        
        # Bonus pour complexité modérée
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password) 
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in '!@#$%^&*()_+-=' for c in password)
        
        complexity = sum([has_upper, has_lower, has_digit, has_symbol])
        if complexity == 2:  # Complexité modérée, plus probable
            score += 5.0
        elif complexity == 3:
            score += 3.0
        
        # Bonus pour patterns culturels
        cultural_words = ['teranga', 'senegal', 'dakar', 'wolof', 'yallah']
        for word in cultural_words:
            if word in password.lower():
                score += 7.0
                break
        
        # Malus pour complexité excessive (moins probable)
        if len(password) > 16:
            score -= 5.0
        if complexity >= 4:  # Trop complexe
            score -= 3.0
        
        return score
    
    def save_comprehensive_wordlist(self, wordlist: List[str], 
                                  output_dir: str = "output",
                                  save_analytics: bool = True) -> Dict[str, str]:
        """Sauvegarde complète avec analytics et formats multiples"""
        # Création du dossier de sortie
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        target_name = f"{self.profile.name}_{self.profile.surname}" if self.profile else "target"
        base_name = f"{target_name}_comprehensive_{timestamp}"
        
        files_created = {}
        
        # 1. Wordlist principale
        wordlist_file = f"{output_dir}/{base_name}.txt"
        with open(wordlist_file, 'w', encoding='utf-8') as f:
            f.write(f"# Professional Wordlist Generator - Version Complète\n")
            f.write(f"# Target: {target_name}\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Total passwords: {len(wordlist)}\n")
            f.write("#" + "="*70 + "\n\n")
            
            for password in wordlist:
                f.write(f"{password}\n")
        
        files_created['wordlist'] = wordlist_file
        
        # 2. Format JSON avec métadonnées
        json_file = f"{output_dir}/{base_name}.json"
        json_data = {
            'metadata': {
                'target': target_name,
                'generated_at': datetime.now().isoformat(),
                'total_passwords': len(wordlist),
                'profile': asdict(self.profile) if self.profile else {},
                'generation_stats': dict(self.generation_stats)
            },
            'passwords': wordlist
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        files_created['json'] = json_file
        
        # 3. Règles Hashcat avancées
        hashcat_file = f"{output_dir}/{base_name}_hashcat.rule"
        hashcat_rules = self._generate_advanced_hashcat_rules()
        with open(hashcat_file, 'w', encoding='utf-8') as f:
            f.write("# Advanced Hashcat Rules - Professional Generator\n")
            for rule in hashcat_rules:
                f.write(f"{rule}\n")
        
        files_created['hashcat_rules'] = hashcat_file
        
        # 4. Règles John the Ripper
        john_file = f"{output_dir}/{base_name}_john.rule"
        john_rules = self._generate_advanced_john_rules()
        with open(john_file, 'w', encoding='utf-8') as f:
            f.write("# Advanced John the Ripper Rules\n")
            for rule in john_rules:
                f.write(f"{rule}\n")
        
        files_created['john_rules'] = john_file
        
        # 5. Analytics et statistiques
        if save_analytics:
            analytics_file = f"{output_dir}/{base_name}_analytics.html"
            self._generate_analytics_report(wordlist, analytics_file)
            files_created['analytics'] = analytics_file
        
        # 6. Top passwords pour tests rapides
        top_file = f"{output_dir}/{base_name}_top100.txt"
        with open(top_file, 'w', encoding='utf-8') as f:
            f.write("# Top 100 Most Probable Passwords\n")
            for password in wordlist[:100]:
                f.write(f"{password}\n")
        
        files_created['top100'] = top_file
        
        # 7. Configuration pour réutilisation
        config_file = f"{output_dir}/{base_name}_config.json"
        config_data = {
            'profile': asdict(self.profile) if self.profile else {},
            'generation_stats': dict(self.generation_stats),
            'timestamp': timestamp,
            'files_created': files_created
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        files_created['config'] = config_file
        
        logger.info(f"Sauvegarde complète: {len(files_created)} fichiers créés")
        return files_created
    
    def _generate_advanced_hashcat_rules(self) -> List[str]:
        """Génère des règles Hashcat avancées"""
        rules = [
            # Règles de base
            ':',          # Aucune modification
            'l',          # Tout en minuscules
            'u',          # Tout en majuscules
            'c',          # Première lettre en majuscule
            'C',          # Première lettre en minuscule, reste majuscule
            't',          # Toggle case (inverse)
            'TN',         # Toggle case position N
            
            # Ajouts de caractères
            '$1', '$2', '$3', '$!', '$@', '$#',
            '$1$2', '$1$2$3', '$!$@', '$2$0$2$4',
            '$7$7', '$7$8',  # Préfixes téléphoniques sénégalais
            
            # Préfixes
            '^1', '^2', '^@', '^!',
            '^1^2', '^2^0^2^4',
            
            # Substitutions leet speak
            'sa4', 'se3', 'si1', 'so0', 'ss5', 'st7', 'sg9',
            'sa@ se3 si! so0 ss$ st+',  # Leet avancé
            
            # Règles combinées populaires
            'l $1 $2 $3',     # Minuscule + 123
            'c $! $@ $#',     # Capitalize + !@#
            'l sa4 se3 $1 $2 $3',  # Leet + 123
            'c $2 $0 $2 $4',  # Capitalize + 2024
            
            # Spécial Sénégal
            'l $7 $7',        # + 77
            'l $7 $8',        # + 78
            'c $7 $7 $1 $2 $3',  # Capitalize + 77123
            
            # Transformations avancées
            'l r',            # Lowercase + reverse
            'c r',            # Capitalize + reverse
            'l d',            # Lowercase + duplicate
            'c d',            # Capitalize + duplicate
            
            # Insertions
            'i1@', 'i2!', 'i3#',  # Insert @ position 1, ! position 2, etc.
            'i4
        , 'i5%',
            
            # Suppressions et remplacements
            '[', ']',         # Supprime premier/dernier caractère
            'D1', 'D2',       # Supprime caractère position 1, 2
            
            # Règles de longueur
            '>', '<',         # Rejette si longueur > ou <
            
            # Règles spécialisées
            'l sa4 se3 si1 so0 ss5 $!',  # Leet complet + !
            'c $M $a $r $c $h',          # Ajout du mois
        ]
        
        return rules
    
    def _generate_advanced_john_rules(self) -> List[str]:
        """Génère des règles John the Ripper avancées"""
        rules = [
            # Format John the Ripper
            '[List.Rules:Professional]',
            '',
            
            # Règles de base
            ':',      # Aucun changement
            '-c',     # Capitalize
            '-l',     # Lowercase
            '-u',     # Uppercase
            '-C',     # Complement (inverse case first)
            'r',      # Reverse
            'd',      # Duplicate
            'f',      # Reflect (mot + reverse)
            
            # Ajouts
            '$1', '$2', '$3', '$!', '$@', '$#', '$*',
            '$1$2$3', '$!$@$#', '$2$0$2$4',
            '$7$7', '$7$8', '$7$6',  # Sénégal
            
            # Substitutions
            'sa4', 'se3', 'si1', 'so0', 'ss5', 'st7',
            'sa@', 'se3', 'si!', 'so0', 'ss
        , 'st+',
            
            # Combinaisons populaires
            'l$1$2$3',        # lowercase + 123
            'c$!$@$#',        # capitalize + !@#
            'lsa4se3$1$2$3',  # leet + 123
            'c$2$0$2$4',      # capitalize + 2024
            
            # Insertions
            '^1', '^2', '^@', '^!',
            
            # Suppressions
            '[', ']',
            
            # Règles complexes
            'lr',     # lowercase + reverse
            'cr',     # capitalize + reverse
            'ld',     # lowercase + duplicate
            'cd',     # capitalize + duplicate
            
            # Spécial téléphone sénégalais
            'l$7$7$1$2$3',
            'c$7$8$!',
            
            # Multi-règles
            'lsa4se3si1so0$!',
            'csa@se3si!so0$',
        ]
        
        return rules
    
    def _generate_analytics_report(self, wordlist: List[str], output_file: str):
        """Génère un rapport d'analytics HTML interactif"""
        # Analyse des données
        analytics = self._analyze_wordlist_patterns(wordlist)
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Analytics - Wordlist Professional</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .metric {{ display: inline-block; background: #ecf0f1; padding: 15px; margin: 10px; border-radius: 5px; text-align: center; min-width: 120px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                .metric-label {{ color: #7f8c8d; }}
                .chart {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #bdc3c7; padding: 10px; text-align: left; }}
                th {{ background: #3498db; color: white; }}
                .password-example {{ font-family: monospace; background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Rapport d'Analytics - Wordlist Professional</h1>
                
                <div class="metrics-section">
                    <div class="metric">
                        <div class="metric-value">{len(wordlist):,}</div>
                        <div class="metric-label">Total Passwords</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{analytics['avg_length']:.1f}</div>
                        <div class="metric-label">Longueur Moyenne</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{analytics['complexity_score']:.1f}/10</div>
                        <div class="metric-label">Score Complexité</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{analytics['unique_patterns']}</div>
                        <div class="metric-label">Patterns Uniques</div>
                    </div>
                </div>
                
                <h2>📈 Distribution par Longueur</h2>
                <div id="lengthChart" class="chart"></div>
                
                <h2>🎯 Analyse de Complexité</h2>
                <div id="complexityChart" class="chart"></div>
                
                <h2>🔥 Top 20 Patterns les Plus Probables</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Rang</th>
                            <th>Password</th>
                            <th>Longueur</th>
                            <th>Score Probabilité</th>
                            <th>Complexité</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Top 20 passwords avec scores
        for i, password in enumerate(wordlist[:20], 1):
            score = self._calculate_password_probability(password)
            complexity = self._get_complexity_level(password)
            html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td class="password-example">{password}</td>
                            <td>{len(password)}</td>
                            <td>{score:.1f}</td>
                            <td>{complexity}</td>
                        </tr>
            """
        
        html_content += f"""
                    </tbody>
                </table>
                
                <h2>📋 Statistiques de Génération</h2>
                <table>
                    <thead>
                        <tr><th>Source</th><th>Nombre</th><th>Pourcentage</th></tr>
                    </thead>
                    <tbody>
        """
        
        total_stats = sum(self.generation_stats.values())
        for source, count in self.generation_stats.items():
            percentage = (count / total_stats * 100) if total_stats > 0 else 0
            html_content += f"""
                        <tr>
                            <td>{source.replace('_', ' ').title()}</td>
                            <td>{count:,}</td>
                            <td>{percentage:.1f}%</td>
                        </tr>
            """
        
        html_content += f"""
                    </tbody>
                </table>
                
                <h2>💡 Recommandations d'Utilisation</h2>
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107;">
                    <h3>🎯 Pour Tests Rapides:</h3>
                    <p>Utilisez le fichier <code>{Path(output_file).stem}_top100.txt</code> qui contient les 100 mots de passe les plus probables.</p>
                    
                    <h3>⚡ Optimisation Hashcat:</h3>
                    <p><code>hashcat -m 0 -a 0 hashes.txt wordlist.txt -r rules.rule --force</code></p>
                    
                    <h3>🔧 Configuration John:</h3>
                    <p><code>john --wordlist=wordlist.txt --rules=Professional hashes.txt</code></p>
                </div>
                
                <div style="margin-top: 30px; padding: 15px; background: #d4edda; border-radius: 5px; border-left: 5px solid #28a745;">
                    <p><strong>⚖️ Rappel Légal:</strong> Cette wordlist est destinée uniquement aux tests de pénétration autorisés et aux audits de sécurité légaux.</p>
                </div>
            </div>
            
            <script>
                // Graphique distribution longueur
                var lengthData = {analytics['length_distribution']};
                var lengthTrace = {{
                    x: Object.keys(lengthData),
                    y: Object.values(lengthData),
                    type: 'bar',
                    marker: {{color: '#3498db'}}
                }};
                Plotly.newPlot('lengthChart', [lengthTrace], {{
                    title: 'Distribution des Longueurs',
                    xaxis: {{title: 'Longueur'}},
                    yaxis: {{title: 'Nombre de Passwords'}}
                }});
                
                // Graphique complexité
                var complexityData = {analytics['complexity_distribution']};
                var complexityTrace = {{
                    labels: Object.keys(complexityData),
                    values: Object.values(complexityData),
                    type: 'pie',
                    marker: {{colors: ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']}}
                }};
                Plotly.newPlot('complexityChart', [complexityTrace], {{
                    title: 'Répartition par Complexité'
                }});
            </script>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Rapport analytics généré: {output_file}")
    
    def _analyze_wordlist_patterns(self, wordlist: List[str]) -> Dict[str, Any]:
        """Analyse les patterns de la wordlist"""
        if not wordlist:
            return {}
        
        # Distribution par longueur
        length_dist = Counter(len(pwd) for pwd in wordlist)
        
        # Distribution par complexité
        complexity_dist = Counter(self._get_complexity_level(pwd) for pwd in wordlist)
        
        # Longueur moyenne
        avg_length = sum(len(pwd) for pwd in wordlist) / len(wordlist)
        
        # Score de complexité global
        complexity_scores = [self._get_complexity_score(pwd) for pwd in wordlist]
        avg_complexity = sum(complexity_scores) / len(complexity_scores)
        
        # Patterns uniques
        unique_patterns = len(set(self._extract_pattern(pwd) for pwd in wordlist))
        
        return {
            'length_distribution': dict(length_dist),
            'complexity_distribution': dict(complexity_dist),
            'avg_length': avg_length,
            'complexity_score': avg_complexity,
            'unique_patterns': unique_patterns
        }
    
    def _get_complexity_level(self, password: str) -> str:
        """Détermine le niveau de complexité d'un mot de passe"""
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        complexity = sum([has_lower, has_upper, has_digit, has_symbol])
        
        if complexity == 1:
            return "Faible"
        elif complexity == 2:
            return "Modérée"
        elif complexity == 3:
            return "Bonne"
        else:
            return "Élevée"
    
    def _get_complexity_score(self, password: str) -> float:
        """Calcule un score de complexité (0-10)"""
        score = 0.0
        
        # Longueur
        if len(password) >= 8:
            score += 2.0
        if len(password) >= 12:
            score += 1.0
        
        # Types de caractères
        if any(c.islower() for c in password):
            score += 1.0
        if any(c.isupper() for c in password):
            score += 1.0
        if any(c.isdigit() for c in password):
            score += 1.0
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            score += 2.0
        
        # Patterns variés
        if not password.isalnum():  # Contient des symboles
            score += 1.0
        if not password.islower():  # Pas tout en minuscules
            score += 1.0
        
        return min(score, 10.0)
    
    def _extract_pattern(self, password: str) -> str:
        """Extrait le pattern d'un mot de passe"""
        pattern = ""
        for char in password:
            if char.islower():
                pattern += "l"
            elif char.isupper():
                pattern += "u"
            elif char.isdigit():
                pattern += "d"
            else:
                pattern += "s"
        return pattern


# class WordlistGUI:
#     """Interface graphique pour le générateur"""
    
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Professional Wordlist Generator")
#         self.root.geometry("800x600")
#         self.root.configure(bg='#f0f0f0')
        
#         self.generator = ProfessionalWordlistGenerator()
#         self.setup_ui()
    
#     def setup_ui(self):
#         """Configure l'interface utilisateur"""
#         # Titre
#         title_label = tk.Label(
#             self.root,
#             text="🔐 Professional Wordlist Generator",
#             font=("Arial", 16, "bold"),
#             bg='#f0f0f0',
#             fg='#2c3e50'
#         )
#         title_label.pack(pady=10)
        
#         # Notebook pour les onglets
#         self.notebook = ttk.Notebook(self.root)
#         self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
#         # Onglet Profil
#         self.profile_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.profile_frame, text="👤 Profil Cible")
#         self.setup_profile_tab()
        
#         # Onglet Options
#         self.options_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.options_frame, text="⚙️ Options")
#         self.setup_options_tab()
        
#         # Onglet Résultats
#         self.results_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.results_frame, text="📊 Résultats")
#         self.setup_results_tab()
        
#         # Boutons d'action
#         self.setup_action_buttons()
    
#     def setup_profile_tab(self):
#         """Configure l'onglet profil"""
#         # Champs du profil
#         self.profile_fields = {}
        
#         fields = [
#             ("Prénom:", "name"),
#             ("Nom:", "surname"),
#             ("Surnom:", "nickname"),
#             ("Date naissance:", "birth_date"),
#             ("Entreprise:", "company"),
#             ("Poste:", "job_title"),
#             ("Email:", "email"),
#             ("Téléphone:", "phone"),
#             ("Ville:", "city"),
#             ("Animal:", "pet_name"),
#             ("Hobby:", "hobby")
#         ]
        
#         for i, (label, field) in enumerate(fields):
#             row = i // 2
#             col = (i % 2) * 2
            
#             tk.Label(self.profile_frame, text=label, font=("Arial", 10)).grid(
#                 row=row, column=col, sticky='e', padx=5, pady=5
#             )
            
#             entry = tk.Entry(self.profile_frame, width=20, font=("Arial", 10))
#             entry.grid(row=row, column=col+1, sticky='w', padx=5, pady=5)
#             self.profile_fields[field] = entry
        
#         # Zone mots-clés
#         tk.Label(self.profile_frame, text="Mots-clés:", font=("Arial", 10)).grid(
#             row=len(fields)//2 + 1, column=0, sticky='ne', padx=5, pady=5
#         )
        
#         self.keywords_text = tk.Text(self.profile_frame, height=3, width=40, font=("Arial", 10))
#         self.keywords_text.grid(
#             row=len(fields)//2 + 1, column=1, columnspan=3, sticky='ew', padx=5, pady=5
#         )
    
#     def setup_options_tab(self):
#         """Configure l'onglet options"""
#         # Options de génération
#         options_frame = ttk.LabelFrame(self.options_frame, text="Options de Génération")
#         options_frame.pack(fill='x', padx=10, pady=10)
        
#         # Nombre maximum de mots de passe
#         tk.Label(options_frame, text="Nombre max:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
#         self.max_passwords = tk.IntVar(value=10000)
#         tk.Spinbox(options_frame, from_=1000, to=100000, textvariable=self.max_passwords, width=10).grid(
#             row=0, column=1, sticky='w', padx=5, pady=5
#         )
        
#         # Longueurs
#         tk.Label(options_frame, text="Longueur min:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
#         self.min_length = tk.IntVar(value=4)
#         tk.Spinbox(options_frame, from_=1, to=20, textvariable=self.min_length, width=10).grid(
#             row=1, column=1, sticky='w', padx=5, pady=5
#         )
        
#         tk.Label(options_frame, text="Longueur max:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
#         self.max_length = tk.IntVar(value=20)
#         tk.Spinbox(options_frame, from_=1, to=50, textvariable=self.max_length, width=10).grid(
#             row=2, column=1, sticky='w', padx=5, pady=5
#         )
        
#         # Checkboxes pour les options
#         self.use_ai = tk.BooleanVar(value=True)
#         tk.Checkbutton(options_frame, text="Utiliser l'IA", variable=self.use_ai).grid(
#             row=3, column=0, columnspan=2, sticky='w', padx=5, pady=5
#         )
        
#         self.use_osint = tk.BooleanVar(value=True)
#         tk.Checkbutton(options_frame, text="OSINT automatique", variable=self.use_osint).grid(
#             row=4, column=0, columnspan=2, sticky='w', padx=5, pady=5
#         )
        
#         # URL pour scraping
#         tk.Label(options_frame, text="URL à scraper:").grid(row=5, column=0, sticky='w', padx=5, pady=5)
#         self.target_url = tk.Entry(options_frame, width=40)
#         self.target_url.grid(row=5, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
    
#     def setup_results_tab(self):
#         """Configure l'onglet résultats"""
#         # Zone de texte pour les résultats
#         self.results_text = tk.Text(self.results_frame, font=("Consolas", 10))
        
#         # Scrollbar
#         scrollbar = tk.Scrollbar(self.results_frame)
#         scrollbar.pack(side='right', fill='y')
        
#         self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
#         self.results_text.config(yscrollcommand=scrollbar.set)
#         scrollbar.config(command=self.results_text.yview)
        
#         # Barre de progression
#         self.progress_var = tk.StringVar(value="Prêt")
#         self.progress_label = tk.Label(self.results_frame, textvariable=self.progress_var)
#         self.progress_label.pack(pady=5)
        
#         self.progress_bar = ttk.Progressbar(self.results_frame, mode='indeterminate')
#         self.progress_bar.pack(fill='x', padx=10, pady=5)
    
#     def setup_action_buttons(self):
#         """Configure les boutons d'action"""
#         button_frame = tk.Frame(self.root, bg='#f0f0f0')
#         button_frame.pack(fill='x', padx=10, pady=10)
        
#         # Bouton Générer
#         generate_btn = tk.Button(
#             button_frame,
#             text="🚀 Générer Wordlist",
#             command=self.generate_wordlist,
#             bg='#3498db',
#             fg='white',
#             font=("Arial", 12, "bold"),
#             relief='flat',
#             padx=20
#         )
#         generate_btn.pack(side='left', padx=5)
        
#         # Bouton Sauvegarder
#         save_btn = tk.Button(
#             button_frame,
#             text="💾 Sauvegarder",
#             command=self.save_wordlist,
#             bg='#2ecc71',
#             fg='white',
#             font=("Arial", 12, "bold"),
#             relief='flat',
#             padx=20
#         )
#         save_btn.pack(side='left', padx=5)
        
#         # Bouton Charger Profil
#         load_btn = tk.Button(
#             button_frame,
#             text="📂 Charger Profil",
#             command=self.load_profile,
#             bg='#f39c12',
#             fg='white',
#             font=("Arial", 12, "bold"),
#             relief='flat',
#             padx=20
#         )
#         load_btn.pack(side='left', padx=5)
    
#     def generate_wordlist(self):
#         """Génère la wordlist"""
#         try:
#             # Collecte des données du profil
#             profile_data = {}
#             for field, entry in self.profile_fields.items():
#                 value = entry.get().strip()
#                 if value:
#                     profile_data[field] = value
            
#             # Mots-clés
#             keywords_text = self.keywords_text.get("1.0