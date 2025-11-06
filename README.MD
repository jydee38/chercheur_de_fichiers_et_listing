# 🔎 Chercheur de Fichiers GUI

Un outil de bureau simple, développé en Python et CustomTkinter, pour rechercher récursivement tous les fichiers d'un type spécifique (par extension) dans un dossier et ses sous-dossiers. Les résultats sont sauvegardés dans un fichier `.txt`.

![Interface du Chercheur de Fichiers]


---

## 🚀 Fonctionnalités

* **Interface Moderne :** Construit avec CustomTkinter pour un look agréable et un mode sombre.
* **Recherche Récursive :** Scanne le dossier de départ et tous ses sous-dossiers (`os.walk`).
* **Filtrage par Extension :** Isolez facilement les fichiers que vous recherchez (ex: `jpg`, `mkv`, `pdf`).
* **Sélection Facile :** Des boutons "Parcourir..." permettent de sélectionner les dossiers sans erreur de saisie.
* **Non-Blocage (Multi-threading) :** La recherche s'exécute dans un thread séparé, ce qui empêche l'application de "geler" pendant les longues analyses de disques durs.
* **Console de Log :** Une fenêtre de log intégrée vous montre les dossiers en cours d'analyse et vous informe de la fin de l'opération.

---

## 🛠️ Installation

Ce projet nécessite Python 3 et la bibliothèque `customtkinter`.

1.  **Clonez le dépôt :**
    ```bash
    git clone [https://github.com/VOTRE_NOM/votre-repo-chercheur-fichiers.git](https://github.com/VOTRE_NOM/votre-repo-chercheur-fichiers.git)
    cd votre-repo-chercheur-fichiers
    ```

2.  **Installez les dépendances :**
    ```bash
    pip install customtkinter
    ```

---

## 🏃 Comment Lancer l'Application

Une fois les dépendances installées, exécutez simplement le script principal :

```bash
python votre_script.py