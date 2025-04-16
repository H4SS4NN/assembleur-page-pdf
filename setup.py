from setuptools import setup
import sys

# Liste des dépendances
install_requires = [
    'PyPDF2>=3.0.0',
    'pdf2image>=1.16.0',
    'Pillow>=9.0.0',
    'docx2pdf>=0.1.8',
    'img2pdf>=0.4.4',
]

# Configuration pour PyInstaller
if sys.platform == 'win32':
    # Configuration spécifique pour Windows
    import PyInstaller.__main__
    PyInstaller.__main__.run([
        'pdf_merger.py',
        '--name=FusionneurPDF',
        '--onefile',
        '--windowed',
        '--icon=icon.ico',  # Vous devrez créer une icône
        '--add-data=requirements.txt;.',
    ])
elif sys.platform == 'darwin':
    # Configuration spécifique pour macOS
    import PyInstaller.__main__
    PyInstaller.__main__.run([
        'pdf_merger.py',
        '--name=FusionneurPDF',
        '--onefile',
        '--windowed',
        '--icon=icon.icns',  # Vous devrez créer une icône
        '--add-data=requirements.txt:.',
    ])

setup(
    name='FusionneurPDF',
    version='1.0.0',
    description='Application de fusion de documents en PDF',
    author='Votre Nom',
    author_email='votre.email@example.com',
    packages=[],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'fusionneur-pdf=pdf_merger:main',
        ],
    },
) 