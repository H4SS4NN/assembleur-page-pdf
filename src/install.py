import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

def check_python():
    """Vérifie que Python est installé correctement."""
    try:
        subprocess.run(['python3', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Python 3 n'est pas installé ou n'est pas dans le PATH")
        print("Veuillez installer Python 3 via Homebrew :")
        print("1. /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. brew install python")
        return False

def check_brew():
    """Vérifie que Homebrew est installé."""
    try:
        subprocess.run(['brew', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Homebrew n'est pas installé")
        print("Veuillez installer Homebrew en exécutant :")
        print("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        return False

def install_dependencies():
    """Installe les dépendances nécessaires."""
    print("📦 Installation des dépendances...")
    
    # Vérifier et installer Python si nécessaire
    if not check_python():
        if check_brew():
            print("Installation de Python via Homebrew...")
            subprocess.run(['brew', 'install', 'python'], check=True)
        else:
            return False
            
    # Installer les dépendances
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True
    except subprocess.SubprocessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances : {e}")
        return False

def create_default_icon():
    """Crée une icône par défaut pour l'application."""
    print("🎨 Création de l'icône par défaut...")
    
    # Créer une image 1024x1024
    img = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dessiner un fond bleu
    draw.ellipse([100, 100, 924, 924], fill=(0, 123, 255, 255))
    
    # Dessiner un "F" blanc
    draw.rectangle([400, 300, 500, 700], fill=(255, 255, 255, 255))
    draw.rectangle([400, 300, 700, 400], fill=(255, 255, 255, 255))
    draw.rectangle([400, 450, 600, 550], fill=(255, 255, 255, 255))
    
    # Sauvegarder en PNG
    img.save('icon.png')
    
    # Convertir en ICNS pour macOS
    if platform.system() == "Darwin":
        try:
            subprocess.run(['iconutil', '-c', 'icns', 'icon.iconset'], check=True)
            return True
        except subprocess.SubprocessError:
            print("⚠️ Impossible de créer l'icône .icns, utilisation du mode sans icône")
            return False
    return True

def create_executable():
    """Crée l'exécutable selon le système d'exploitation."""
    system = platform.system()
    print(f"🛠️ Création de l'exécutable pour {system}...")
    
    # Créer l'icône par défaut
    if not create_default_icon():
        # Si on ne peut pas créer l'icône, on crée l'exécutable sans icône
        if system == "Windows":
            cmd = [
                "pyinstaller",
                "--name=FusionneurPDF",
                "--onefile",
                "--windowed",
                "--add-data=requirements.txt;.",
                "pdf_merger.py"
            ]
        elif system == "Darwin":  # macOS
            cmd = [
                "pyinstaller",
                "--name=FusionneurPDF",
                "--onefile",
                "--windowed",
                "--add-data=requirements.txt:.",
                "pdf_merger.py"
            ]
    else:
        # Utiliser l'icône créée
        if system == "Windows":
            cmd = [
                "pyinstaller",
                "--name=FusionneurPDF",
                "--onefile",
                "--windowed",
                "--icon=icon.ico",
                "--add-data=requirements.txt;.",
                "pdf_merger.py"
            ]
        elif system == "Darwin":  # macOS
            cmd = [
                "pyinstaller",
                "--name=FusionneurPDF",
                "--onefile",
                "--windowed",
                "--icon=icon.icns",
                "--add-data=requirements.txt:.",
                "pdf_merger.py"
            ]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.SubprocessError as e:
        print(f"❌ Erreur lors de la création de l'exécutable : {e}")
        return False

def create_desktop_shortcut():
    """Crée un raccourci sur le bureau."""
    system = platform.system()
    desktop = Path.home() / "Desktop"
    
    if system == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(desktop / "FusionneurPDF.lnk"))
            shortcut.Targetpath = str(Path.cwd() / "dist" / "FusionneurPDF.exe")
            shortcut.WorkingDirectory = str(Path.cwd() / "dist")
            shortcut.save()
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la création du raccourci Windows : {e}")
            return False
            
    elif system == "Darwin":
        try:
            app_path = Path.cwd() / "dist" / "FusionneurPDF.app"
            if app_path.exists():
                # Créer un alias sur le bureau
                os.system(f'ln -s "{app_path}" "{desktop / "FusionneurPDF.app"}"')
                return True
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la création du raccourci macOS : {e}")
            return False

def create_windows_package():
    """Crée un package de distribution pour Windows."""
    print("📦 Création du package de distribution Windows...")
    
    # Créer le dossier de distribution
    dist_dir = Path("dist")
    package_dir = dist_dir / "FusionneurPDF_Windows"
    package_dir.mkdir(exist_ok=True)
    
    # Copier l'exécutable
    exe_path = dist_dir / "FusionneurPDF.exe"
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir)
        
        # Créer un fichier README
        readme_content = """# FusionneurPDF - Guide d'installation

## Installation
1. Double-cliquez sur `FusionneurPDF.exe`
2. Si Windows Defender affiche un avertissement :
   - Cliquez sur "Plus d'informations"
   - Cliquez sur "Exécuter quand même"

## Utilisation
- Cliquez sur "Sélectionner des fichiers" pour choisir des fichiers individuels
- Ou cliquez sur "Sélectionner un dossier" pour sélectionner tous les fichiers d'un dossier
- Choisissez le nom et l'emplacement du fichier final
- Cliquez sur "Fusionner les documents"

## Formats supportés
- PDF (.pdf)
- Images (.jpg, .jpeg, .png)
- Documents Word (.docx)

## Désinstallation
Pour désinstaller l'application, supprimez simplement le fichier `FusionneurPDF.exe`
"""
        
        with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
            
        print(f"✅ Package créé dans : {package_dir}")
        return True
    else:
        print("❌ L'exécutable n'a pas été trouvé")
        return False

def create_windows_installer():
    """Crée un installateur Windows avec Inno Setup."""
    print("📦 Création de l'installateur Windows...")
    
    # Vérifier si Inno Setup est installé
    try:
        subprocess.run(['iscc', '/?'], check=True, capture_output=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Inno Setup n'est pas installé")
        print("Veuillez installer Inno Setup depuis : https://jrsoftware.org/isdl.php")
        return False
    
    # Créer le script Inno Setup
    iss_content = """#define MyAppName "FusionneurPDF"
#define MyAppVersion "1.0"
#define MyAppPublisher "Votre Nom"
#define MyAppExeName "FusionneurPDF.exe"

[Setup]
AppId={{YOUR-APP-ID}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=FusionneurPDF_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\FusionneurPDF.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{group}\\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
"""
    
    # Sauvegarder le script Inno Setup
    with open("installer.iss", "w", encoding="utf-8") as f:
        f.write(iss_content)
    
    # Créer l'installateur
    try:
        subprocess.run(['iscc', 'installer.iss'], check=True)
        print("✅ Installateur créé avec succès !")
        print("📁 L'installateur se trouve dans le dossier 'dist' sous le nom 'FusionneurPDF_Setup.exe'")
        return True
    except subprocess.SubprocessError as e:
        print(f"❌ Erreur lors de la création de l'installateur : {e}")
        return False

def main():
    print("🚀 Installation de FusionneurPDF...")
    
    # Installation des dépendances
    if not install_dependencies():
        print("❌ L'installation a échoué. Veuillez corriger les erreurs ci-dessus.")
        return
        
    # Création de l'exécutable
    if not create_executable():
        print("❌ La création de l'exécutable a échoué.")
        return
        
    # Création du raccourci
    if not create_desktop_shortcut():
        print("⚠️ La création du raccourci a échoué, mais l'application a été créée.")
    
    # Création de l'installateur Windows si on est sur Windows
    if platform.system() == "Windows":
        create_windows_installer()
    
    print("\n✅ Installation terminée avec succès !")
    print("📁 L'application a été installée dans le dossier 'dist'")
    print("🖥️ Un raccourci a été créé sur votre bureau")
    if platform.system() == "Windows":
        print("📦 Un installateur a été créé dans 'dist/FusionneurPDF_Setup.exe'")
    print("\nPour lancer l'application, double-cliquez sur le raccourci sur votre bureau.")

if __name__ == "__main__":
    main() 