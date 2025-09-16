#!/usr/bin/env python3
"""
Générateur de Wordlists Personnalisées pour Cybersécurité Offensive - VERSION CORRIGÉE
Auteur: Outil de test de pénétration
Usage: Uniquement pour des tests autorisés et audits de sécurité légaux
"""

import itertools
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Set
import argparse
import random


class PersonalizedWordlistGenerator:
    def __init__(self):
        self.base_info = {}
        self.generated_passwords = set()
        
        # Patterns de transformation communs - VERSION CORRIGÉE
        self.transformations = {
            'leet': {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'},
            'caps': ['upper', 'lower', 'title', 'capitalize'],
            'numbers': ['123', '12', '1', '01', '2023', '2024', '2025'],
            'symbols': ['!', '@', '#', '$', '%', '&', '*'],
            'common_suffixes': ['123', '!', '01', '2024', '2025', '!123'],
            'complex_symbols': ['@123', '#123', '@123!', '#123*', '*123#', '@123*#!', '#*!', '@#!']
        }
        
        # Mots de passe patterns courants
        self.common_patterns = [
            '{name}{year}',
            '{name}{birth_year}',
            '{initials}{year}',
            '{initials}@{year}',
            '{initials}{birth_year}',
            '{pet}{year}',
            '{company}{number}',
            '{hobby}{birth_year}',
            '{city}{year}',
            '{name}{month}{day}',
            '{company}@{year}'
        ]

    def load_personal_info(self, info_dict: Dict):
        """Charge les informations personnelles de la cible"""
        self.base_info = info_dict
        print(f"[+] Informations chargées pour: {info_dict.get('name', 'Anonyme')}")
        
    def extract_dates(self) -> List[str]:
        """Extrait et génère des dates importantes"""
        dates = []
        
        if 'birth_date' in self.base_info:
            birth = self.base_info['birth_date']
            dates.extend([birth, birth[-4:], birth[-2:]])
            
        if 'important_dates' in self.base_info:
            for date in self.base_info['important_dates']:
                dates.extend([date, date[-4:], date[-2:]])
                
        # Années courantes et récentes
        current_year = datetime.now().year
        for i in range(5):
            dates.append(str(current_year - i))
            
        return list(set(dates))

    def generate_base_words(self) -> Set[str]:
        """Génère la liste des mots de base à partir des infos personnelles"""
        base_words = set()
        
        # Informations personnelles de base
        for key in ['name', 'surname', 'nickname', 'username']:
            if key in self.base_info and self.base_info[key]:
                base_words.add(self.base_info[key].lower())
                
        # Génération des initiales - CORRECTION
        initials = ""
        if 'name' in self.base_info and self.base_info['name']:
            initials += self.base_info['name'][0].lower()
        if 'surname' in self.base_info and self.base_info['surname']:
            initials += self.base_info['surname'][0].lower()
        if len(initials) >= 2:
            base_words.add(initials)
            
        # Initiales avec nom du milieu si disponible
        if 'middle_name' in self.base_info and self.base_info['middle_name']:
            full_initials = initials[0] + self.base_info['middle_name'][0].lower() + initials[-1]
            base_words.add(full_initials)
                
        # Informations professionnelles
        for key in ['company', 'job_title', 'department']:
            if key in self.base_info and self.base_info[key]:
                words = re.split(r'[^\w]', self.base_info[key].lower())
                base_words.update([w for w in words if len(w) > 2])
                
        # Informations personnelles
        for key in ['pet_name', 'favorite_team', 'hobby', 'city', 'street']:
            if key in self.base_info and self.base_info[key]:
                base_words.add(self.base_info[key].lower())
                
        # Mots-clés spécifiques
        if 'keywords' in self.base_info:
            base_words.update([kw.lower() for kw in self.base_info['keywords']])
            
        return base_words

    def apply_leet_speak(self, word: str) -> List[str]:
        """Applique les transformations leet speak"""
        variations = [word]
        
        # Transformation leet complète
        leet_word = word
        for char, replacement in self.transformations['leet'].items():
            leet_word = leet_word.replace(char, replacement)
        if leet_word != word:
            variations.append(leet_word)
            
        # Transformations partielles
        for char, replacement in self.transformations['leet'].items():
            if char in word:
                partial = word.replace(char, replacement)
                variations.append(partial)
                
        return variations

    def apply_case_variations(self, word: str) -> List[str]:
        """Applique les variations de casse"""
        return [
            word.lower(),
            word.upper(),
            word.capitalize(),
            word.title()
        ]

    def generate_combinations(self) -> Set[str]:
        """Génère des combinaisons intelligentes - VERSION CORRIGÉE"""
        combinations = set()
        base_words = list(self.generate_base_words())
        dates = self.extract_dates()
        
        print(f"[DEBUG] Mots de base trouvés: {base_words[:5]}...")  # Debug
        
        # Combinaisons simples
        for word in base_words:
            if not word:  # Skip empty words
                continue
                
            # Mot seul avec variations
            for variation in self.apply_case_variations(word):
                combinations.add(variation)
                for leet in self.apply_leet_speak(variation):
                    combinations.add(leet)
                    
            # Mot + dates
            for date in dates:
                combinations.add(f"{word}{date}")
                combinations.add(f"{word.capitalize()}{date}")
                
            # Mot + nombres communs
            for num in self.transformations['numbers']:
                combinations.add(f"{word}{num}")
                combinations.add(f"{word.capitalize()}{num}")
                
            # Mot + symboles simples
            for symbol in self.transformations['symbols']:
                combinations.add(f"{word}{symbol}")
                combinations.add(f"{symbol}{word}")
                
            # Mot + combinaisons complexes de symboles - CORRECTION
            if 'complex_symbols' in self.transformations:
                for complex_suffix in self.transformations['complex_symbols']:
                    combinations.add(f"{word}{complex_suffix}")
                    combinations.add(f"{word.capitalize()}{complex_suffix}")
                    combinations.add(f"{word.upper()}{complex_suffix}")
                
        # Combinaisons de deux mots
        valid_words = [w for w in base_words if w and len(w) > 1]
        for word1, word2 in itertools.combinations(valid_words[:5], 2):
            combinations.add(f"{word1}{word2}")
            combinations.add(f"{word1.capitalize()}{word2}")
            combinations.add(f"{word1}{word2.capitalize()}")
            
            # Avec suffixes complexes
            if 'complex_symbols' in self.transformations:
                for suffix in self.transformations['complex_symbols'][:3]:  # Limiter
                    combinations.add(f"{word1}{word2}{suffix}")
                
        return combinations

    def generate_pattern_based(self) -> Set[str]:
        """Génère des mots de passe basés sur des patterns courants"""
        pattern_passwords = set()
        
        # Extraction des valeurs pour les patterns
        values = {
            'name': self.base_info.get('name', '').lower(),
            'surname': self.base_info.get('surname', '').lower(),
            'company': self.base_info.get('company', '').lower().replace(' ', ''),
            'pet': self.base_info.get('pet_name', '').lower(),
            'hobby': self.base_info.get('hobby', '').lower(),
            'city': self.base_info.get('city', '').lower(),
            'year': str(datetime.now().year),
            'birth_year': self.base_info.get('birth_date', '')[-4:] if self.base_info.get('birth_date') else '',
            'month': str(datetime.now().month).zfill(2),
            'day': str(datetime.now().day).zfill(2),
            'number': '123'
        }
        
        # Génération des initiales pour les patterns
        initials = ""
        if values['name']:
            initials += values['name'][0]
        if values['surname']:
            initials += values['surname'][0]
        values['initials'] = initials
        
        # Application des patterns
        for pattern in self.common_patterns:
            try:
                password = pattern.format(**values)
                if password and len(password) >= 4:
                    pattern_passwords.add(password)
                    pattern_passwords.add(password.capitalize())
                    
                    # Avec suffixes communs
                    for suffix in self.transformations['common_suffixes']:
                        pattern_passwords.add(f"{password}{suffix}")
                        
            except KeyError as e:
                print(f"[DEBUG] Pattern ignoré: {pattern} (clé manquante: {e})")
                continue
                
        return pattern_passwords

    def generate_ai_inspired_passwords(self) -> Set[str]:
        """Génère des mots de passe inspirés par l'IA (patterns réalistes)"""
        ai_passwords = set()
        base_words = list(self.generate_base_words())
        
        if not base_words:
            return ai_passwords
            
        # Patterns réalistes observés
        realistic_patterns = [
            # Nom + année + caractère spécial
            lambda w: f"{w.capitalize()}{random.choice(range(2020, 2026))}{random.choice(['!', '@', '#'])}",
            # Mot à l'envers + chiffres
            lambda w: f"{w[::-1]}{random.choice(['123', '456', '789'])}",
            # Première lettre majuscule + reste + nombre
            lambda w: f"{w[0].upper()}{w[1:]}{random.choice(range(10, 100))}",
            # Répétition de pattern
            lambda w: f"{w}{w[:3]}{random.choice(range(1, 10))}",
        ]
        
        for word in base_words[:3]:  # Limiter pour éviter trop de génération
            if not word:
                continue
            for pattern_func in realistic_patterns:
                try:
                    password = pattern_func(word)
                    if 6 <= len(password) <= 20:
                        ai_passwords.add(password)
                except Exception as e:
                    print(f"[DEBUG] Erreur pattern IA pour '{word}': {e}")
                    continue
                    
        return ai_passwords

    def generate_wordlist(self, max_length: int = None, min_length: int = 4) -> List[str]:
        """Génère la wordlist complète"""
        print("[+] Génération des mots de base...")
        all_passwords = set()
        
        try:
            # Combinaisons de base
            combinations = self.generate_combinations()
            all_passwords.update(combinations)
            print(f"[DEBUG] {len(combinations)} combinaisons générées")
            
            # Patterns courants
            print("[+] Application des patterns courants...")
            patterns = self.generate_pattern_based()
            all_passwords.update(patterns)
            print(f"[DEBUG] {len(patterns)} patterns générés")
            
            # Génération IA
            print("[+] Génération de mots de passe réalistes...")
            ai_passwords = self.generate_ai_inspired_passwords()
            all_passwords.update(ai_passwords)
            print(f"[DEBUG] {len(ai_passwords)} mots de passe IA générés")
            
        except Exception as e:
            print(f"[-] Erreur lors de la génération: {e}")
            return []
        
        # Filtrage par longueur
        filtered = [pwd for pwd in all_passwords 
                   if len(pwd) >= min_length and (not max_length or len(pwd) <= max_length)]
        
        # Tri par longueur puis alphabétique
        filtered.sort(key=lambda x: (len(x), x))
        
        return filtered

    def save_wordlist(self, wordlist: List[str], filename: str = None):
        """Sauvegarde la wordlist dans un fichier"""
        if not filename:
            target_name = self.base_info.get('name', 'target')
            filename = f"{target_name}_wordlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
        with open(filename, 'w', encoding='utf-8') as f:
            for password in wordlist:
                f.write(f"{password}\n")
                
        print(f"[+] Wordlist sauvegardée: {filename} ({len(wordlist)} mots de passe)")

    def display_stats(self, wordlist: List[str]):
        """Affiche les statistiques de la wordlist"""
        if not wordlist:
            print("[-] Aucun mot de passe généré!")
            return
            
        print(f"\n[+] Statistiques de la wordlist:")
        print(f"    Total: {len(wordlist)} mots de passe")
        
        lengths = [len(pwd) for pwd in wordlist]
        print(f"    Longueur min: {min(lengths)}")
        print(f"    Longueur max: {max(lengths)}")
        print(f"    Longueur moyenne: {sum(lengths)/len(lengths):.1f}")
        
        # Distribution par longueur
        length_dist = {}
        for length in lengths:
            length_dist[length] = length_dist.get(length, 0) + 1
            
        print(f"    Distribution par longueur:")
        for length in sorted(length_dist.keys()):
            print(f"      {length} caractères: {length_dist[length]} mots de passe")


def main():
    parser = argparse.ArgumentParser(
        description="Générateur de wordlists personnalisées pour tests de pénétration",
        epilog="Usage éthique uniquement - Tests autorisés seulement"
    )
    
    parser.add_argument('-i', '--input', help='Fichier JSON avec les informations personnelles')
    parser.add_argument('-o', '--output', help='Nom du fichier de sortie')
    parser.add_argument('--min-length', type=int, default=4, help='Longueur minimale des mots de passe')
    parser.add_argument('--max-length', type=int, help='Longueur maximale des mots de passe')
    parser.add_argument('--interactive', action='store_true', help='Mode interactif pour saisir les informations')
    parser.add_argument('--debug', action='store_true', help='Mode debug pour plus d\'informations')
    
    args = parser.parse_args()
    
    generator = PersonalizedWordlistGenerator()
    
    if args.interactive:
        # Mode interactif
        print("=== Générateur de Wordlists Personnalisées ===")
        print("Veuillez saisir les informations disponibles sur la cible:\n")
        
        personal_info = {}
        
        # Informations de base
        personal_info['name'] = input("Prénom: ").strip()
        personal_info['surname'] = input("Nom de famille: ").strip()
        personal_info['nickname'] = input("Surnom/Pseudo: ").strip()
        personal_info['birth_date'] = input("Date de naissance (DDMMYYYY): ").strip()
        
        # Informations professionnelles
        personal_info['company'] = input("Entreprise: ").strip()
        personal_info['job_title'] = input("Poste: ").strip()
        
        # Informations personnelles
        personal_info['pet_name'] = input("Nom d'animal de compagnie: ").strip()
        personal_info['hobby'] = input("Hobby/Passion: ").strip()
        personal_info['city'] = input("Ville: ").strip()
        personal_info['favorite_team'] = input("Équipe favorite: ").strip()
        
        # Mots-clés additionnels
        keywords = input("Mots-clés supplémentaires (séparés par des virgules): ").strip()
        if keywords:
            personal_info['keywords'] = [kw.strip() for kw in keywords.split(',')]
            
        # Nettoyage des champs vides
        personal_info = {k: v for k, v in personal_info.items() if v}
        
    elif args.input:
        # Chargement depuis fichier JSON
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                personal_info = json.load(f)
        except Exception as e:
            print(f"[-] Erreur lors du chargement du fichier: {e}")
            return
    else:
        # Exemple de démonstration
        personal_info = {
            "name": "Souley",
            "surname": "Diallo",
            "nickname": "sdiallo",
            "birth_date": "15031990",
            "company": "TechSenegal",
            "job_title": "administrateur",
            "pet_name": "rex",
            "hobby": "football",
            "city": "dakar",
            "favorite_team": "terangalions",
            "keywords": ["admin", "tech", "linux"]
        }
        print("[i] Utilisation des données d'exemple. Utilisez -i ou --interactive pour vos données.")
    
    # Génération de la wordlist
    try:
        generator.load_personal_info(personal_info)
        wordlist = generator.generate_wordlist(
            max_length=args.max_length,
            min_length=args.min_length
        )
        
        if not wordlist:
            print("[-] Aucun mot de passe généré. Vérifiez vos données d'entrée.")
            return
        
        # Affichage des statistiques
        generator.display_stats(wordlist)
        
        # Sauvegarde
        generator.save_wordlist(wordlist, args.output)
        
        # Aperçu des premiers résultats
        print(f"\n[+] Aperçu des 10 premiers mots de passe:")
        for i, pwd in enumerate(wordlist[:10], 1):
            print(f"    {i:2d}. {pwd}")
            
        if len(wordlist) > 10:
            print(f"    ... et {len(wordlist) - 10} autres")
            
        # Recherche du mot de passe spécifique pour Souley Diallo
        if personal_info.get('name', '').lower() == 'souley' and personal_info.get('surname', '').lower() == 'diallo':
            target_password = 'sld@123*#!'
            if target_password in wordlist:
                position = wordlist.index(target_password) + 1
                print(f"\n🎯 [SUCCESS] Le mot de passe '{target_password}' a été trouvé à la position {position}!")
            else:
                print(f"\n❌ [INFO] Le mot de passe '{target_password}' n'a pas été généré.")
                print("    Mots de passe similaires trouvés:")
                similar = [pwd for pwd in wordlist if 'sld' in pwd.lower()]
                for sim in similar[:5]:
                    print(f"      - {sim}")
        
    except Exception as e:
        print(f"[-] Erreur fatale: {e}")