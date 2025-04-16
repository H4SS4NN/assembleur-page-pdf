# Guide Développeur - FusionneurPDF

## Architecture du Projet

### Structure des Dossiers

```
FusionneurPDF/
├── src/                    # Code source
│   ├── pdf_merger.py      # Application principale
│   └── install.py         # Script d'installation
├── docs/                   # Documentation
│   ├── user_guide.md      # Guide utilisateur
│   └── dev_guide.md       # Ce guide
├── tests/                  # Tests unitaires
├── dist/                   # Fichiers de distribution
├── requirements.txt        # Dépendances
└── README.md              # Documentation principale
```

### Composants Principaux

1. **Interface Utilisateur** (`pdf_merger.py`)
   - Classe `ModernButton` : Boutons personnalisés
   - Classe `PDFMergerApp` : Application principale
   - Gestion des événements et callbacks

2. **Installation** (`install.py`)
   - Création d'exécutable
   - Génération d'icônes
   - Création d'installateur

3. **Traitement des Documents**
   - Fusion de PDF avec PyPDF2
   - Conversion d'images avec pdf2image
   - Conversion de Word avec docx2pdf

## Environnement de Développement

### Prérequis

- Python 3.8+
- pip
- virtualenv (recommandé)
- Git

### Configuration

1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
cd FusionneurPDF
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Développement

### Conventions de Code

- PEP 8 pour le style Python
- Docstrings pour la documentation
- Commentaires en français
- Noms de variables en anglais

### Ajout de Fonctionnalités

1. Créez une branche :
```bash
git checkout -b feature/nouvelle-fonctionnalite
```

2. Développez la fonctionnalité
3. Testez localement
4. Soumettez une Pull Request

### Tests

Les tests sont dans le dossier `tests/`. Pour les exécuter :
```bash
python -m pytest tests/
```

## Distribution

### Création d'Exécutable

1. Windows :
```bash
python src/install.py
```

2. macOS :
```bash
python3 src/install.py
```

### Création d'Installateur

1. Windows :
- Inno Setup doit être installé
- Le script génère automatiquement l'installateur

2. macOS :
- Le script crée un fichier .app
- Utilisez create-dmg pour créer un .dmg

## Maintenance

### Mise à Jour des Dépendances

1. Mettez à jour les dépendances :
```bash
pip install --upgrade -r requirements.txt
```

2. Testez l'application
3. Mettez à jour le fichier requirements.txt si nécessaire

### Correction de Bugs

1. Reproduisez le bug
2. Créez une branche de correction
3. Corrigez le bug
4. Ajoutez un test pour éviter la régression
5. Soumettez une Pull Request

## Bonnes Pratiques

### Sécurité

- Ne stockez pas de données sensibles
- Validez les entrées utilisateur
- Gérez les erreurs proprement
- Utilisez des chemins relatifs

### Performance

- Utilisez des threads pour les opérations longues
- Nettoyez les fichiers temporaires
- Optimisez la mémoire
- Utilisez des progress bars

### Internationalisation

- Utilisez des variables pour les textes
- Préparez le code pour la traduction
- Supportez différents formats de date

## Contribution

1. Fork le projet
2. Créez une branche
3. Committez vos changements
4. Push vers la branche
5. Ouvrez une Pull Request

## Ressources

- [Documentation Python](https://docs.python.org/)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/) 