# Guide d'installation de FusionneurPDF

## Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation automatique (recommandée)

1. Téléchargez le dossier contenant tous les fichiers du projet
2. Ouvrez un terminal/command prompt dans le dossier du projet
3. Exécutez la commande suivante :
   ```bash
   python install.py
   ```

L'installation automatique va :
- Installer toutes les dépendances nécessaires
- Créer un exécutable pour votre système d'exploitation
- Créer un raccourci sur votre bureau

## Installation manuelle

### Windows

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Créez l'exécutable :
   ```bash
   pyinstaller --name=FusionneurPDF --onefile --windowed --icon=icon.ico --add-data=requirements.txt;. pdf_merger.py
   ```

3. L'exécutable sera créé dans le dossier `dist`

### macOS

1. Installez les dépendances :
   ```bash
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   ```

2. Créez l'application :
   ```bash
   pyinstaller --name=FusionneurPDF --onefile --windowed --icon=icon.icns --add-data=requirements.txt:. pdf_merger.py
   ```

3. L'application sera créée dans le dossier `dist`

## Distribution

Pour distribuer l'application, vous pouvez simplement partager le dossier `dist` qui contient l'exécutable.

### Windows
- Le fichier `FusionneurPDF.exe` dans le dossier `dist`
- Les utilisateurs peuvent simplement double-cliquer sur l'exécutable

### macOS
- Le fichier `FusionneurPDF.app` dans le dossier `dist`
- Les utilisateurs peuvent simplement double-cliquer sur l'application

## Notes importantes

- Sur macOS, la première fois que l'application est lancée, il faudra peut-être autoriser son exécution dans les préférences de sécurité
- Sur Windows, l'antivirus peut bloquer l'exécution la première fois. Il faudra autoriser l'application
- L'application nécessite les droits d'administrateur pour certaines opérations

## Désinstallation

Pour désinstaller l'application :
1. Supprimez le raccourci sur le bureau
2. Supprimez le dossier `dist` contenant l'exécutable
3. (Optionnel) Supprimez les dépendances Python avec :
   ```bash
   pip uninstall -r requirements.txt
   ``` 