# Consignes pour l'Agent IA (Gemini)

Ce document définit les règles et conventions à suivre pour interagir avec ce projet.

### 🚀 Vision & Architecture Globale

- **Point de Départ** : Toujours se référer à `general/VISION.md` et `general/PLANIFICATION.md` pour la vision et la feuille de route globales.
- **Schéma d'Architecture** : L'architecture de référence est définie dans `general/ARCHITECTURE.md`. Toute modification d'interaction entre les services doit y être reflétée.

### 🧱 Structure des Sous-Projets & Code

- **Modularité** : Le projet est divisé en microservices (`mcp_*`) et agents (`agent_*`) indépendants. Chaque dossier est un sous-projet autonome.
- **Documentation Locale** : Chaque sous-projet contient son propre dossier `docs/`. Les consulter pour obtenir le contexte d'un sous-projet.
- **Taille des Fichiers** : Ne jamais créer un fichier de plus de 500 lignes. Si un fichier approche cette limite, proposer un refactoring en plusieurs modules.
- **Imports** : Utiliser des imports clairs et cohérents (préférer les imports relatifs au sein d'un même sous-projet).

### 🤝 Code Partagé & Contrats

- **Contrat de Données** : Le schéma `MCPPayload` défini dans `shared/schemas/mcp_payload.py` est le contrat de données **strict** entre les MCPs.
- **Schéma de Base de Données** : La structure des BDD est définie dans `shared/database_schemas/`. Se référer à ces fichiers comme source de vérité.

### 💻 Conventions de Développement & Style

- **Langage** : Python 3.11+.
- **Style** : Suivre `PEP8` et formater le code avec `black`.
- **Typage** : Utiliser les "type hints" partout.
- **Frameworks** : Utiliser `FastAPI` pour les APIs, `Pydantic` pour la validation de données, et `CrewAI` pour les agents.
- **Variables d'Environnement** : Toujours utiliser `python-dotenv` et `os.getenv()` pour gérer les secrets. Ne jamais les écrire en dur.
- **Docstrings** : Écrire des docstrings pour chaque fonction en utilisant le style Google.
- **Commentaires** : Ajouter des commentaires avec parcimonie. Se concentrer sur le *pourquoi* d'une logique complexe, pas sur le *quoi*.

### 🧪 Tests & Fiabilité

- **Tests Unitaires** : Toujours créer des tests `Pytest` pour les nouvelles fonctionnalités (fonctions, classes, endpoints).
- **Mise à Jour des Tests** : Après avoir modifié une logique, vérifier si les tests existants doivent être mis à jour et le faire.
- **Emplacement des Tests** : Les tests doivent se trouver dans un dossier `/tests` à la racine de chaque sous-projet, en miroir de la structure du code source.

### ✅ Complétion des Tâches

- **Confirmation** : Me demander de confirmer avant de marquer une tâche comme terminée dans un fichier `PLANIFICATION.md`.
- **Validation des Modifications** : Me montrer la ligne de code spécifique (avec `diff` ou en citant le code) que vous prévoyez de modifier avant d'appliquer un changement.

### 🧠 Mon Comportement (Règles IA)

- **Pas de Suppositions** : Ne jamais supposer le contenu d'un fichier ou la disponibilité d'une librairie. Toujours vérifier avec les outils (`read_file`, `glob`, `run_shell_command`).
- **Confirmation des Chemins** : Toujours valider l'existence des fichiers et des dossiers avant de tenter de les lire ou de les modifier.
- **Sécurité** : Ne jamais écrire de secrets (clés API, mots de passe) en dur dans le code.
- **Suivre le Lead** : Adhérer au workflow et aux priorités définies par l'utilisateur.
- **Ne pas supprimer de code** : Ne jamais supprimer ou écraser du code existant sans instruction explicite ou si cela fait partie d'une tâche de refactoring validée.
