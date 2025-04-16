# Fusionneur de Documents en PDF

Une application simple pour fusionner différents types de documents (PDF, images, Word) en un seul fichier PDF.

## Fonctionnalités

- Fusion de plusieurs fichiers PDF
- Conversion automatique des images (JPG, PNG) en PDF
- Conversion automatique des documents Word (.docx) en PDF
- Interface graphique simple et intuitive
- Possibilité de sélectionner des fichiers individuels ou un dossier entier
- Gestion des erreurs et des fichiers temporaires

## Installation

1. Assurez-vous d'avoir Python 3.7 ou supérieur installé sur votre système
2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez l'application :
   ```bash
   python pdf_merger.py
   ```

2. Dans l'interface graphique :
   - Cliquez sur "Sélectionner des fichiers" pour choisir des fichiers individuels
   - Ou cliquez sur "Sélectionner un dossier" pour sélectionner tous les fichiers d'un dossier
   - Cliquez sur "Fusionner les documents" pour créer le PDF final

3. Le fichier final sera sauvegardé sous le nom `fusion_finale.pdf` dans le même dossier que le premier fichier sélectionné.

## Formats supportés

- PDF (.pdf)
- Images (.jpg, .jpeg, .png)
- Documents Word (.docx)

## Notes

- L'application crée des fichiers temporaires pendant la conversion, qui sont automatiquement supprimés après la fusion
- En cas d'erreur, un message d'erreur explicite sera affiché
- Le fichier final est toujours nommé `fusion_finale.pdf` 