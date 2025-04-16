import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger
from pdf2image import convert_from_path
from PIL import Image
import docx2pdf
import img2pdf
import tempfile
import time
import threading
from datetime import datetime, timedelta

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['style'] = 'Accent.TButton'

    def on_leave(self, e):
        self['style'] = 'TButton'

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusionneur de PDF")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f6f7')
        
        # Variables
        self.files_to_merge = []
        self.processing = False
        self.start_time = None
        self.output_filename = tk.StringVar(value="fusion_finale.pdf")
        self.output_path = tk.StringVar(value=os.path.expanduser("~/Documents"))
        
        # Style
        self.setup_styles()
        
        # Interface
        self.create_widgets()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f6f7')
        self.style.configure('TButton', padding=10, font=('Helvetica', 10))
        self.style.configure('Accent.TButton', background='#007bff')
        self.style.configure('TLabel', font=('Helvetica', 10), background='#f5f6f7')
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), background='#f5f6f7')
        self.style.configure('TProgressbar', thickness=8, background='#007bff')
        self.style.configure('Card.TFrame', background='white', relief='flat')
        self.style.configure('TEntry', padding=5, font=('Helvetica', 10))
        
        # Configuration des couleurs pour la liste
        self.root.option_add('*TCombobox*Listbox.font', ('Helvetica', 10))
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#007bff')
        
    def create_widgets(self):
        # Frame principal avec padding
        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                              text="Fusionneur de Documents PDF",
                              style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Carte pour les boutons
        button_card = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        button_card.pack(fill=tk.X, pady=(0, 20))
        
        # Boutons avec icônes
        select_files_btn = ModernButton(button_card, 
                                      text="📁 Sélectionner des fichiers",
                                      command=self.select_files)
        select_files_btn.pack(side=tk.LEFT, padx=5)
        
        select_folder_btn = ModernButton(button_card,
                                       text="📂 Sélectionner un dossier",
                                       command=self.select_folder)
        select_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # Carte pour la liste des fichiers
        files_card = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        files_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # En-tête de la liste
        files_header = ttk.Frame(files_card)
        files_header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(files_header, text="Fichiers sélectionnés", 
                 font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        
        # Frame pour la liste et les boutons de gestion
        list_frame = ttk.Frame(files_card)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Liste des fichiers avec style moderne
        self.files_listbox = tk.Listbox(list_frame,
                                      font=('Helvetica', 10),
                                      selectmode=tk.EXTENDED,
                                      bg='white',
                                      fg='#333333',
                                      selectbackground='#007bff',
                                      selectforeground='white',
                                      activestyle='none',
                                      highlightthickness=1,
                                      highlightcolor='#ddd',
                                      relief=tk.FLAT)
        
        # Scrollbar avec style moderne
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Boutons de gestion des fichiers
        file_actions = ttk.Frame(files_card)
        file_actions.pack(fill=tk.X, pady=(10, 0))
        
        remove_btn = ModernButton(file_actions,
                                text="🗑️ Supprimer la sélection",
                                command=self.remove_selected_files)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ModernButton(file_actions,
                               text="🧹 Tout effacer",
                               command=self.clear_files)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Placement de la liste et scrollbar
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Carte pour les options de sortie
        output_card = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        output_card.pack(fill=tk.X, pady=(0, 20))
        
        # Titre de la section
        ttk.Label(output_card, text="Options de sortie", 
                 font=('Helvetica', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Frame pour le nom du fichier
        filename_frame = ttk.Frame(output_card)
        filename_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filename_frame, text="Nom du fichier :").pack(side=tk.LEFT, padx=(0, 10))
        filename_entry = ttk.Entry(filename_frame, textvariable=self.output_filename, width=30)
        filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Frame pour le dossier de sortie
        output_path_frame = ttk.Frame(output_card)
        output_path_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(output_path_frame, text="Dossier de sortie :").pack(side=tk.LEFT, padx=(0, 10))
        path_entry = ttk.Entry(output_path_frame, textvariable=self.output_path, width=30)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ModernButton(output_path_frame,
                                text="📂 Parcourir",
                                command=self.select_output_folder)
        browse_btn.pack(side=tk.LEFT)
        
        # Carte pour la progression
        progress_card = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        progress_card.pack(fill=tk.X, pady=(0, 10))
        
        # Barre de progression avec style moderne
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_card,
                                          variable=self.progress_var,
                                          maximum=100,
                                          style='TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Labels d'information avec style moderne
        self.status_label = ttk.Label(progress_card,
                                    text="",
                                    font=('Helvetica', 10))
        self.status_label.pack(fill=tk.X)
        
        self.time_label = ttk.Label(progress_card,
                                  text="",
                                  font=('Helvetica', 10))
        self.time_label.pack(fill=tk.X)
        
        # Bouton de fusion
        merge_btn = ModernButton(main_frame,
                               text="🔄 Fusionner les documents",
                               command=self.start_merge)
        merge_btn.pack(pady=10)
        
    def select_output_folder(self):
        folder = filedialog.askdirectory(
            title="Sélectionner le dossier de sortie",
            initialdir=self.output_path.get()
        )
        if folder:
            self.output_path.set(folder)
            
    def remove_selected_files(self):
        if self.processing:
            return
            
        selected = self.files_listbox.curselection()
        if not selected:
            return
            
        # Supprimer les fichiers sélectionnés (en commençant par la fin pour éviter les problèmes d'index)
        for index in reversed(selected):
            del self.files_to_merge[index]
            
        self.update_files_list()
        
    def clear_files(self):
        if self.processing:
            return
            
        self.files_to_merge = []
        self.update_files_list()
        
    def select_files(self):
        if self.processing:
            return
            
        files = filedialog.askopenfilenames(
            title="Sélectionner les fichiers",
            filetypes=[
                ("Tous les fichiers supportés", "*.pdf *.jpg *.jpeg *.png *.docx"),
                ("PDF", "*.pdf"),
                ("Images", "*.jpg *.jpeg *.png"),
                ("Word", "*.docx")
            ]
        )
        if files:
            self.files_to_merge.extend(list(files))
            self.update_files_list()
            
    def select_folder(self):
        if self.processing:
            return
            
        folder = filedialog.askdirectory(title="Sélectionner un dossier")
        if folder:
            for file in os.listdir(folder):
                if file.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.docx')):
                    self.files_to_merge.append(os.path.join(folder, file))
            self.update_files_list()
            
    def update_files_list(self):
        self.files_listbox.delete(0, tk.END)
        for file in self.files_to_merge:
            filename = os.path.basename(file)
            icon = "📄 "  # Icône par défaut
            if file.lower().endswith('.pdf'):
                icon = "📕 "
            elif file.lower().endswith(('.jpg', '.jpeg', '.png')):
                icon = "🖼️ "
            elif file.lower().endswith('.docx'):
                icon = "📝 "
            self.files_listbox.insert(tk.END, f"{icon}{filename}")
            
    def update_progress(self, current, total, file_name):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            if current > 0:
                estimated_total = (elapsed / current) * total
                remaining = estimated_total - elapsed
                eta = datetime.now() + timedelta(seconds=int(remaining))
                self.time_label.config(
                    text=f"⏱️ Temps estimé restant : {int(remaining)} secondes"
                )
        
        self.status_label.config(
            text=f"🔄 Traitement de : {file_name}"
        )
        self.root.update_idletasks()
            
    def convert_to_pdf(self, file_path, current, total):
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        
        try:
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                self.update_progress(current, total, f"Conversion de l'image {os.path.basename(file_path)}")
                with open(temp_pdf.name, "wb") as f:
                    f.write(img2pdf.convert(file_path))
            elif file_path.lower().endswith('.docx'):
                self.update_progress(current, total, f"Conversion du document Word {os.path.basename(file_path)}")
                docx2pdf.convert(file_path, temp_pdf.name)
            else:
                return file_path
                
            return temp_pdf.name
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la conversion de {file_path}: {str(e)}")
            return None
            
    def merge_documents(self):
        if not self.files_to_merge:
            messagebox.showwarning("Attention", "Veuillez sélectionner des fichiers à fusionner")
            return
            
        self.processing = True
        self.start_time = time.time()
        merger = PdfMerger()
        temp_files = []
        total_files = len(self.files_to_merge)
        
        try:
            for i, file in enumerate(self.files_to_merge, 1):
                if file.lower().endswith('.pdf'):
                    self.update_progress(i, total_files, f"Fusion du PDF {os.path.basename(file)}")
                    merger.append(file)
                else:
                    converted_pdf = self.convert_to_pdf(file, i, total_files)
                    if converted_pdf:
                        merger.append(converted_pdf)
                        if converted_pdf != file:
                            temp_files.append(converted_pdf)
                            
            self.update_progress(total_files, total_files, "Sauvegarde du PDF final")
            
            # Vérification et création du dossier de sortie si nécessaire
            output_dir = self.output_path.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # Vérification de l'extension .pdf
            output_filename = self.output_filename.get()
            if not output_filename.lower().endswith('.pdf'):
                output_filename += '.pdf'
                
            output_path = os.path.join(output_dir, output_filename)
            merger.write(output_path)
            merger.close()
            
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
            messagebox.showinfo("Succès", f"✅ Fusion terminée !\nLe fichier a été sauvegardé sous :\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Une erreur est survenue lors de la fusion : {str(e)}")
        finally:
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
            self.processing = False
            self.progress_var.set(0)
            self.status_label.config(text="")
            self.time_label.config(text="")
            
    def start_merge(self):
        if not self.processing:
            thread = threading.Thread(target=self.merge_documents)
            thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop() 