# Professional Wordlist Generator v2.0

🔐 Générateur de wordlists professionnel avec IA, OSINT et analytics avancés.
Optimisé pour les tests de pénétration en Afrique de l'Ouest / Sénégal.

## 🚀 Fonctionnalités

### ⚡ Génération Avancée
- **IA Contextuelle**: Intégration Gemini/OpenAI pour génération intelligente
- **OSINT Automatique**: Collecte d'informations publiques éthique
- **Patterns Culturels**: Optimisé pour le Sénégal et l'Afrique de l'Ouest
- **Transformations Avancées**: Leet speak, masques, règles Hashcat/John

### 🎯 Interfaces Multiples
- **Interface Graphique**: GUI intuitive avec Tkinter
- **API REST**: Endpoints pour intégration
- **Ligne de Commande**: Scripts automatisés
- **Mode Interactif**: Collecte guidée d'informations

### 📊 Analytics Professionnels
- **Rapports HTML**: Visualisations interactives
- **Métriques Détaillées**: Statistiques de génération
- **Recommendations**: Conseils d'optimisation
- **Benchmark**: Tests d'efficacité

## 📦 Installation

```bash
# Clonage du repository
git clone https://github.com/your-repo/professional-wordlist-generator.git
cd professional-wordlist-generator

# Installation des dépendances
pip install -r requirements.txt

# Configuration
cp config.ini.example config.ini
# Éditer config.ini avec vos clés API
```

## 🔧 Utilisation

### Interface Graphique
```bash
python wordlist_generator.py --gui
```

### Ligne de Commande - Exemple Simple
```bash
python wordlist_generator.py --example
```

### Profil Personnalisé
```bash
python wordlist_generator.py -i profil.json -o wordlists/
```

### Mode Interactif
```bash
python wordlist_generator.py --interactive
```

### API REST
```bash
python wordlist_generator.py --api --port 5000
```

### Avec IA et OSINT
```bash
python wordlist_generator.py --example --api-key YOUR_GEMINI_KEY -u https://target-website.com
```

## 📄 Format du Profil JSON

```json
{
  "name": "Amadou",
  "surname": "Diallo",
  "nickname": "adiallo",
  "birth_date": "15031990",
  "company": "TechAfrique SARL",
  "job_title": "Ingénieur Système",
  "email": "amadou@techafrique.sn",
  "phone": "771234567",
  "city": "Dakar",
  "country": "Sénégal",
  "keywords": ["linux", "python", "admin"],
  "languages": ["français", "wolof", "english"]
}
```

## 🌐 API REST

### Génération de Wordlist
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Amadou",
    "surname": "Diallo",
    "company": "TechAfrique",
    "options": {
      "max_passwords": 10000,
      "include_ai": true
    }
  }'
```

### Analyse de Wordlist
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"wordlist": ["password123", "admin123"]}'
```

## ⚡ Commandes Rapides

### Hashcat
```bash
# Mode basique
hashcat -m 0 -a 0 hashes.txt wordlist.txt --force

# Avec règles avancées
hashcat -m 0 -a 0 hashes.txt wordlist.txt -r rules.rule --force
```

### John the Ripper
```bash
john --wordlist=wordlist.txt --rules=Professional hashes.txt
```

### Hydra
```bash
# SSH
hydra -l username -P wordlist.txt ssh://target.com

# HTTP Form
hydra -l username -P wordlist.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"
```

## 🇸🇳 Spécificités Sénégal/Afrique de l'Ouest

- **Patterns Téléphoniques**: 77, 78, 76, 70, 75, 33
- **Expressions Wolof**: teranga, yallah, inchallah, etc.
- **Dates Importantes**: Indépendance 1960, fêtes religieuses
- **Lieux Emblématiques**: Dakar, Almadies, Plateau, etc.
- **Multi-linguisme**: Français, Wolof, Anglais

## ⚖️ Aspects Légaux et Éthiques

### ✅ Utilisation Autorisée
- Tests de pénétration avec contrat signé
- Audits de sécurité internes
- Recherche académique autorisée
- Formation en cybersécurité

### ❌ Utilisation Interdite
- Attaques non autorisées
- Systèmes tiers sans permission
- Usage malveillant
- Violation de la vie privée

## 🔒 Sécurité

- **Chiffrement**: Profils sensibles chiffrés
- **Logging**: Traçabilité complète
- **Rate Limiting**: Protection API
- **Validation**: Contrôles d'entrée stricts

## 🤝 Contribution

Les contributions sont bienvenues! Voir CONTRIBUTING.md

## 📄 Licence

MIT License - Voir LICENSE pour détails

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: Wiki du projet
- **Contact**: security@yourcompany.com

---

**⚠️ Rappel**: Cet outil est destiné aux professionnels de la cybersécurité pour des usages légitimes uniquement.
