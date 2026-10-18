# Jules task — Serveur de visualisation, édition et versionnage SQLite des feuilles Markdown

## Contexte

Le dépôt `tibidibtibo/programme` contient l'ensemble des documents Markdown du programme politique *« Réunir la France »* (Version 3) :
- `programme/00-index.md` (Accueil et index général)
- `programme/programme-v3.md` (Synthèse exécutive officielle)
- `programme/arbitrage.md` (Arbitrage et trajectoire budgétaire)
- `programme/CHANGELOG.md`
- `programme/domaines/01-*.md` à `45-*.md` (Les 45 fiches sectorielles détaillées)
- `programme/annexes/*.md` (Hypothèses macroéconomiques)
- `programme/lots/*.md` (Rapports de lots)

L'objectif est de doter le projet d'une application serveur web légère, autonome et performante qui :
1. Expose et restitue toutes les feuilles Markdown dans une interface web soignée et réactive.
2. Propose un **volet de navigation latéral (sidenav)** à gauche répertoriant l'ensemble des pages avec une recherche/filtrage rapide, et affiche la feuille d'index (`programme/00-index.md` ou `programme/programme-v3.md`) en accueil.
3. Intègre un **Mode Édition** commutable en un clic pour modifier directement le texte Markdown et la mise en page (avec prévisualisation en direct et barre d'outils de formatage).
4. Assure le **versionnage de chaque feuille dans une base SQLite** : chaque modification (via l'interface ou externe sur le disque) génère une nouvelle révision horodatée avec diff/historique.
5. Référence les feuilles en base de données et **suit en temps réel ou à chaque synchronisation les changements de cycle de vie** : création de nouveaux fichiers, modifications de contenu, renommages / déplacements, et suppressions.

---

## Architecture technique recommandée

- **Backend** : Python 3 avec **FastAPI** (ou Flask) + **SQLite** (`sqlite3` standard) + convertisseur Markdown robuste (ex. `markdown` avec extensions tables, fenced_code, toc, attr_list, def_list).
- **Frontend** : Interface moderne, fluide et responsive (HTML5 / CSS / Vanilla JS ou Alpine.js + Tailwind CSS via CDN ou CSS moderne sans étape de build complexe).
- **Emplacement du code** : dossier `server/` (ex. `server/app.py` ou `server/main.py`, `server/db.py`, `server/sync.py`, `server/static/`, `server/templates/`) et fichier `requirements.txt`.
- **Base de données** : fichier SQLite `server/data/programme.db` (avec création automatique du dossier et des tables au premier démarrage).

---

## Spécifications fonctionnelles détaillées

### 1. Volet de navigation (Sidenav) & Accueil
- **Sidenav à gauche** :
  - Arborescence ordonnée et catégorisée :
    - 📌 **Général & Accueil** (`00-index.md`, `programme-v3.md`, `arbitrage.md`, `CHANGELOG.md`)
    - 🏛️ **45 Domaines d'action** (triés par numéro de 01 à 45, affichant le titre extrait du H1 du fichier)
    - 📊 **Annexes & Trajectoire** (`hypotheses-macro.md`, etc.)
    - 📑 **Lots de travail** (`lots/lot-*.md`)
  - **Champ de recherche instantanée** : filtrage en temps réel dans la liste des pages par titre, numéro ou mot-clé.
  - État actif : surbrillance de la page en cours de consultation.
  - Rétractable / responsive pour mobile ou confort de lecture.
- **Page d'accueil** :
  - Par défaut, charge et affiche la synthèse exécutive (`programme/programme-v3.md`) ou l'index (`programme/00-index.md`).

### 2. Moteur de rendu Markdown
- Rendu fidèle du Markdown étendu (GFM) :
  - Tableaux mis en page proprement.
  - Alertes / Callouts GitHub style (`> [!NOTE]`, `> [!IMPORTANT]`, `> [!WARNING]`, etc.).
  - Emojis, listes à puces et cases à cocher.
  - Blocs de code préformatés.
- **Résolution des liens internes relatifs** : un clic sur un lien Markdown (ex. `[Santé](12-sante.md)` ou `[Index](../00-index.md)`) doit naviguer de manière transparente dans l'application sans recharger toute l'arborescence.

### 3. Mode Édition (Toggle "Lecture" / "Édition")
- Bouton clair en haut de page pour basculer entre **Mode Lecture** et **Mode Édition**.
- En Mode Édition :
  - Éditeur de texte avec coloration ou police monospace ergonomique.
  - Prévisualisation en direct (split view ou onglets Vue/Code).
  - Barre d'outils d'assistance à la mise en page (Titres H1/H2/H3, Gras, Italique, Tableau, Liens, Citations, Listes).
  - Bouton **« Sauvegarder »** :
    - Écrit le contenu mis à jour directement dans le fichier `.md` sur le disque.
    - Calcule le nouveau hash SHA-256.
    - Incrémente le numéro de version de la page dans la base SQLite.
    - Crée une nouvelle entrée dans la table d'historique des révisions avec horodatage, auteur/source (`ui_edit`) et résumé des modifications.
  - Bouton **« Annuler »** pour quitter sans modifier le fichier.

### 4. Versionnage SQLite & Historique des révisions
- **Schéma SQLite** :
  - Table `documents` :
    - `id` (INTEGER PRIMARY KEY)
    - `file_path` (TEXT UNIQUE) — chemin relatif depuis la racine du dépôt (ex. `programme/domaines/01-relations-internationales.md`)
    - `title` (TEXT) — titre extrait automatiquement (1er titre `# ...`)
    - `category` (TEXT) — ex. `racine`, `domaines`, `lots`, `annexes`
    - `file_hash` (TEXT) — SHA-256 du contenu
    - `file_size` (INTEGER)
    - `mtime` (REAL) — date de modification fichier
    - `version_count` (INTEGER DEFAULT 1)
    - `is_active` (INTEGER DEFAULT 1) — 0 si le fichier a été supprimé du disque
    - `created_at` (TIMESTAMP)
    - `updated_at` (TIMESTAMP)
  - Table `revisions` :
    - `id` (INTEGER PRIMARY KEY)
    - `document_id` (INTEGER REFERENCES documents(id))
    - `version_number` (INTEGER)
    - `content` (TEXT) — snapshot complet du markdown à cette version
    - `file_hash` (TEXT)
    - `source` (TEXT) — `'initial_scan'`, `'ui_edit'`, `'disk_change'`, `'restore'`
    - `diff_summary` (TEXT NULL)
    - `created_at` (TIMESTAMP)
  - Table `file_events` (optionnelle ou journal d'audit) :
    - `id`, `event_type` (`'created'`, `'modified'`, `'moved'`, `'deleted'`), `file_path`, `details`, `timestamp`.
- **Panneau / Modal d'historique des versions** :
  - Pour la page courante, affiche la liste chronologique des versions (v1, v2, v3...) avec horodatage et origine de la modification.
  - Possibilité de visualiser le contenu d'une version antérieure et de cliquer sur **« Restaurer cette version »** (ce qui réécrit le fichier sur le disque et crée une révision `v(N+1)` marquée `'restore'`).

### 5. Détection des changements de fichiers (Sync & Watcher)
- Module `sync.py` capable de parcourir récursivement les fichiers `.md` :
  - **Au démarrage du serveur** : synchronisation complète automatique.
  - **Détection des nouveaux fichiers** : insertion dans `documents` et création de la révision v1.
  - **Détection des modifications sur disque** (ex. édition via git ou éditeur externe) : comparaison du hash et de la mtime. Si différent, création d'une nouvelle révision `disk_change` et mise à jour de la table `documents`.
  - **Détection des déplacements / renommages** : si un fichier disparaît d'un chemin mais qu'un nouveau fichier apparaît avec le même contenu (hash identique), associer le document existant au nouveau chemin et historiser le déplacement (`moved`).
  - **Détection des suppressions** : si un fichier référencé en base n'existe plus sur le disque, passer `is_active = 0` (le document n'apparaît plus dans le sidenav actif mais son historique de révisions est conservé).
  - Endpoint API `POST /api/sync` pour forcer un re-scan à la demande avec retour JSON des changements détectés.

### 6. API REST exposée
- `GET /api/documents` : liste hiérarchique de tous les documents actifs avec métadonnées (titre, chemin, catégorie, dernière version).
- `GET /api/documents/{id}` ou `GET /api/document?path=...` : détails, métadonnées, contenu brut Markdown et HTML pré-rendu.
- `PUT /api/documents/{id}` : mise à jour du contenu markdown (sauvegarde disque + nouvelle révision SQLite).
- `GET /api/documents/{id}/revisions` : liste des révisions d'un document.
- `GET /api/documents/{id}/revisions/{rev_id}` : contenu d'une révision spécifique.
- `POST /api/documents/{id}/restore/{rev_id}` : restauration d'une révision.
- `POST /api/sync` : déclenchement manuel de la synchronisation filesystem <-> SQLite.

---

## Critères d'acceptation

- [ ] L'application se lance facilement avec une commande documentée (ex. `python -m server.main` ou `uvicorn server.main:app`).
- [ ] Le volet de navigation (sidenav) affiche l'intégralité des fichiers `.md` de `programme/` classés de manière ergonomique (index, 45 domaines avec titres propres, annexes, lots).
- [ ] La recherche dans le sidenav filtre dynamiquement les pages affichées.
- [ ] La page d'accueil affiche une feuille d'index lisible avec un rendu Markdown soigné (tableaux, listes, alertes).
- [ ] Les liens relatifs entre documents Markdown fonctionnent au clic dans l'application.
- [ ] Le mode édition permet de modifier le texte, offre une prévisualisation, et enregistre les modifications directement dans le fichier `.md` sur le disque.
- [ ] Chaque modification enregistrée crée une nouvelle révision dans la base SQLite `programme.db`.
- [ ] L'historique des révisions est consultable et une ancienne version peut être restaurée.
- [ ] Le moteur de synchronisation détecte et gère les ajouts, modifications externes sur disque, renommages et suppressions de fichiers `.md`.
- [ ] Des tests unitaires automatisés (`pytest`) valident le schéma SQLite, le moteur de synchronisation, les opérations CRUD de fichiers et l'API.

---

## Contraintes strictes

- Do not run Playwright, Cypress, or any headless-browser/e2e/UI test runner — they routinely hang or crash this sandbox and kill the session. Verify UI behavior via static/type checks and unit tests only, and describe manual verification steps in the PR description instead.
- Never run destructive git commands (`git reset --hard`, `git checkout -- .` / `git restore .`, `git clean -fd`/`-fdx`, unresolved `git stash`, force-push, history rewrite on pushed commits). Never discard uncommitted changes. Commit work incrementally and frequently so nothing is lost if the session stops early.
- Préserver l'intégralité du contenu existant dans `programme/` (ne pas écraser ni corrompre les 45 fiches de domaines, les synthèses ou les annexes).
- Les dépendances doivent être listées dans un fichier `requirements.txt` léger et standard (ex. `fastapi`, `uvicorn`, `markdown`, `pytest`, `httpx`).

---

## Livrable attendu

Une Pull Request complète comprenant :
1. Le code de l'application serveur dans `server/`.
2. Les modèles et migrations SQLite dans `server/db.py` ou équivalent.
3. Le moteur de synchronisation et détection des changements dans `server/sync.py`.
4. L'interface utilisateur (HTML / CSS / JS) dans `server/templates/` et `server/static/`.
5. La suite de tests unitaires dans `tests/`.
6. Le fichier `requirements.txt` et une section dans `README.md` expliquant l'installation et le lancement de l'application.
