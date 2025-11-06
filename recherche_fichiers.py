#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading

# Configuration de l'apparence (similaire à l'app de roulette)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FileSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chercheur de Fichiers")
        self.geometry("800x750")

        # Variables pour la recherche (qui doivent être accessibles par les threads)
        self.zFilter = ""
        self.output_file = None

        # --- Création de l'interface ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="Paramètres de Recherche", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

        # --- 1. Chemin de recherche ---
        ctk.CTkLabel(self.main_frame, text="Dossier de recherche (chemin complet) :").pack(pady=(10, 5))
        
        path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        path_frame.pack(fill="x", padx=20)
        self.path_entry = ctk.CTkEntry(path_frame, width=500)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(path_frame, text="Parcourir...", width=100, command=self.browse_search_path).pack(side="left")

        # --- 2. Filtre (Extension) ---
        ctk.CTkLabel(self.main_frame, text="Extension de fichier (ex: jpg, avi, txt) :").pack(pady=(15, 5))
        self.filter_entry = ctk.CTkEntry(self.main_frame, width=150)
        self.filter_entry.pack(pady=5, padx=20)

        # --- 3. Dossier de sortie ---
        ctk.CTkLabel(self.main_frame, text="Dossier pour le fichier de résultats :").pack(pady=(15, 5))
        
        output_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        output_frame.pack(fill="x", padx=20)
        self.output_path_entry = ctk.CTkEntry(output_frame, width=500)
        self.output_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(output_frame, text="Parcourir...", width=100, command=self.browse_output_path).pack(side="left")

        # --- 4. Nom du fichier de sortie ---
        ctk.CTkLabel(self.main_frame, text="Nom du fichier de résultats (sans .txt) :").pack(pady=(15, 5))
        self.output_name_entry = ctk.CTkEntry(self.main_frame, width=200)
        self.output_name_entry.pack(pady=5, padx=20)

        # --- Bouton d'action ---
        self.run_button = ctk.CTkButton(self.main_frame, text="Lancer la recherche", 
                                        command=self.start_search_thread,
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.run_button.pack(pady=25, ipady=10, ipadx=20)

        # --- Console de Log ---
        ctk.CTkLabel(self.main_frame, text="Logs :").pack(anchor="w", padx=20, pady=(10, 5))
        self.log_textbox = ctk.CTkTextbox(self.main_frame, state="disabled")
        self.log_textbox.pack(pady=(0, 20), padx=20, fill="both", expand=True)

    # --- Fonctions de l'interface ---

    def log(self, message):
        """Ajoute un message à la console de log de l'application."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert(ctk.END, f"{message}\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see(ctk.END) # Auto-scroll

    def browse_search_path(self):
        """Ouvre un dialogue pour choisir le dossier de recherche."""
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, directory)

    def browse_output_path(self):
        """Ouvre un dialogue pour choisir le dossier de sortie."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_path_entry.delete(0, ctk.END)
            self.output_path_entry.insert(0, directory)

    # --- Logique de recherche (corrigée et améliorée) ---

    def start_search_thread(self):
        """Lance la recherche dans un thread séparé pour ne pas geler l'interface."""
        # Désactive le bouton pour éviter les clics multiples
        self.run_button.configure(state="disabled", text="Recherche en cours...")
        
        # Efface les anciens logs
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", ctk.END)
        self.log_textbox.configure(state="disabled")

        # Lance la fonction de recherche dans un thread
        search_thread = threading.Thread(target=self.run_search)
        search_thread.daemon = True # Permet à l'app de se fermer même si le thread tourne
        search_thread.start()

    def run_search(self):
        """Contient la logique de recherche principale."""
        try:
            path = self.path_entry.get()
            zFilter_raw = self.filter_entry.get().lower().replace(".", "")
            fictxt_path = self.output_path_entry.get()
            nomfic = self.output_name_entry.get()

            # --- Validation ---
            if not all([path, zFilter_raw, fictxt_path, nomfic]):
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                self.run_button.configure(state="normal", text="Lancer la recherche")
                return

            # --- Préparation de la recherche ---
            self.zFilter = f".{zFilter_raw}" # On s'assure que le filtre est ".jpg"
            output_file_full_path = os.path.join(fictxt_path, f"{nomfic}.txt")

            self.log(f"Scan démarré pour : {path}")
            self.log(f"Filtre appliqué : *{self.zFilter}")
            self.log(f"Fichier de sortie : {output_file_full_path}\n")
            
            file_count = 0

            # --- Exécution de la recherche ---
            with open(output_file_full_path, "w", encoding="utf-8") as f:
                self.output_file = f # Stocke la référence du fichier pour la fonction de scan
                file_count = self.listdirectory(path)
            
            self.log(f"\n--- RECHERCHE TERMINÉE ---")
            self.log(f"{file_count} fichier(s) trouvé(s).")
            messagebox.showinfo("Succès", f"Recherche terminée !\n{file_count} fichier(s) trouvé(s).\n\nFichier sauvegardé :\n{output_file_full_path}")

        except Exception as e:
            self.log(f"ERREUR: {str(e)}")
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")
        finally:
            # Réactive le bouton
            self.run_button.configure(state="normal", text="Lancer la recherche")
            self.output_file = None # Nettoie la référence du fichier

    def listdirectory(self, path):
        """Parcourt récursivement les dossiers."""
        count = 0
        for dirname, dirnames, filenames in os.walk(path, topdown=True):
            try:
                self.log(f">> Analyse du dossier : {dirname}")
                for filename in filenames:
                    if self.scandirectory(os.path.join(dirname, filename)):
                        count += 1
            except Exception as e:
                self.log(f"Erreur (accès?) dossier {dirname}: {e}")
        return count

    def scandirectory(self, currentFile):
        """Vérifie si un fichier correspond au filtre et l'écrit."""
        try:
            # Logique de filtrage simplifiée et corrigée
            filename, extension = os.path.splitext(currentFile)
            if extension.lower() == self.zFilter:
                if self.output_file:
                    self.output_file.write(currentFile + "\n")
                    return True
        except Exception as e:
            self.log(f"Erreur analyse fichier {currentFile}: {e}")
        return False


if __name__ == "__main__":
    app = FileSearchApp()
    app.mainloop()