# FusionneurPDF

Une application moderne pour fusionner des documents PDF, images et documents Word en un seul PDF.

## Fonctionnalités

- Fusion de fichiers PDF
- Conversion et fusion d'images (JPG, JPEG, PNG)
- Conversion et fusion de documents Word (DOCX)
- Interface utilisateur moderne et intuitive
- Barre de progression en temps réel
- Estimation du temps restant
- Support multilingue (Français)

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Poppler (pour la conversion PDF vers image)
  - Windows : Téléchargez depuis [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/) et ajoutez le dossier bin au PATH
  - Linux : `sudo apt-get install poppler-utils`
  - macOS : `brew install poppler`

## Installation

### Option 1 : Installation via l'exécutable (Recommandé)

1. Téléchargez la dernière version depuis la section [Releases](https://github.com/votre_username/FusionneurPDF/releases)
2. Exécutez le fichier `FusionneurPDF-Setup.exe`
3. Suivez les instructions de l'installateur
4. L'application sera disponible dans le menu Démarrer et sur le bureau

### Option 2 : Installation depuis les sources

1. Clonez le dépôt :

```bash
git clone https://github.com/votre_username/FusionneurPDF.git
cd FusionneurPDF
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancez l'application :

```bash
python src/pdf_merger.py
```

## Utilisation

1. Lancez l'application
2. Cliquez sur "Ajouter des fichiers" pour sélectionner les documents à fusionner
3. Utilisez les boutons de la barre d'outils pour :
   - Réorganiser les fichiers (glisser-déposer)
   - Supprimer des fichiers
   - Vider la liste
4. Cliquez sur "Fusionner" pour créer le PDF final
5. Choisissez l'emplacement de sauvegarde du fichier final

## Structure du Projet

```
FusionneurPDF/
├── src/                    # Code source
│   ├── pdf_merger.py      # Application principale
│   └── install.py         # Script d'installation
├── docs/                   # Documentation
│   ├── user_guide.md      # Guide utilisateur
│   └── dev_guide.md       # Guide développeur
├── tests/                  # Tests unitaires
├── dist/                   # Fichiers de distribution
├── requirements.txt        # Dépendances
└── README.md              # Ce fichier
```

## Développement

### Architecture

L'application est construite avec :

- Python 3.8+
- Tkinter pour l'interface graphique
- PyPDF2 pour la manipulation des PDF
- pdf2image pour la conversion d'images
- docx2pdf pour la conversion de Word

### Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Tests

Pour exécuter les tests :

```bash
python -m pytest tests/
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter)

Lien du Projet: [https://github.com/votre_username/FusionneurPDF](https://github.com/votre_username/FusionneurPDF)
