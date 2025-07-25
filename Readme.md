# 🧠 Clash Royale Deck Analyzer – Projet IA Locale (sans Ollama)

Ce projet analyse les decks de Clash Royale à partir de **replays** en extrayant des **statistiques avancées** (taux de présence, support, position moyenne, coût moyen, etc.) et en générant des conseils personnalisés via des algorithmes internes **sans aucun modèle IA externe comme Ollama**.

---

## 📁 Structure du projet

```
.
├── backend/             # API principale + scraping MongoDB
│   ├── scraping/        # Scripts de scraping et d'analyse
│   ├── controllers/     # Contrôleurs de scraping/API
│   ├── main.py          # Serveur FastAPI (port 8000)
│   └── ...
├── ia_api/              # API IA (algos internes sans modèle externe)
│   └── main.py          # Serveur FastAPI (port 8001)
├── frontend/            # Interface web (Next.js / Vite)
├── .env                 # Clé API et configuration
└── README.md
```

---

## ⚙️ Prérequis

* Python 3.10+
* Node.js 18+
* MongoDB en local

---

## 🔐 Fichier `.env` à créer à la racine

```env
ROYALEAPI_COOKIE=""
```

> Remplace `""` par ton cookie d’authentification RoyaleAPI si nécessaire.

---

## 🚀 Lancement du backend (API principale + Scraping)

### 1. Aller dans le dossier backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Lancer l'API FastAPI (port 8000)

```bash
uvicorn main:app --reload
```

Accède à la documentation Swagger :
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Clique sur `POST /update-data` pour lancer l'update des données.

---

### 3. Lancer les scripts de scraping dans **deux autres terminaux avec le même venv**

Lance la route `/update-data` via Swagger pour démarrer la mise à jour des données :
👉 [http://127.0.0.1:8000/docs#/default/update_data_update_data_post](http://127.0.0.1:8000/docs#/default/update_data_update_data_post)

#### a. scraper

```bash
cd backend
venv\Scripts\activate
python controllers/controllerGamedata.py
```

#### b. Scraper les parties détailler Clash Royale

```bash
cd backend
venv\Scripts\activate
python scraping/gameScrap.py
```

#### c. Analyser les replays collectés

```bash
cd backend
venv\Scripts\activate
python scraping/gameAnalyst.py
```

---

### 4. Scraper toutes les parties d'un joueur (par son tag)

Dans Swagger ([http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)), utilise la route :

```http
POST /fetch-player-matches
```

Cela appelle la fonction du fichier :
`backend/controllers/controllerGamedata.py`

---

## 🧠 Lancement de l'API d'analyse (algos internes)

### 1. Aller dans le dossier `ia_api`

```bash
cd ia_api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Lancer l'API (port 8001)

```bash
uvicorn main:app --reload --port 8001
```

Documentation Swagger de l’IA :
👉 [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 💻 Lancement du frontend

```bash
cd frontend
npm install
npm run dev
```

Interface disponible sur :
👉 [http://localhost:5173](http://localhost:5173)

---

## 📌 Résumé rapide

| Tâche                      | Commande                                                              |
| -------------------------- | --------------------------------------------------------------------- |
| API principale             | `uvicorn main:app --reload` (dans `/backend`)                         |
| Scraper les parties        | `python scraping/gameScrap.py`                                        |
| Analyser les parties       | `python scraping/gameAnalyst.py`                                      |
| Scraper les parties joueur | `POST /fetch-player-matches` via `/controllers/controllerGamedata.py` |
| API IA interne             | `uvicorn main:app --reload --port 8001` (dans `/ia_api`)              |
| Frontend                   | `npm install && npm run dev` (dans `/frontend`)                       |

---

## 🔪 Exemple de requête à l’IA (algos internes)

**POST** `http://localhost:8001/api/analyze-deck`

```json
{
  "deck": [
    "Zap",
    "Bats",
    "Goblin Curse",
    "Ice Wizard",
    "Goblin Gang",
    "Miner",
    "Golden Knight",
    "Goblin Hut"
  ]
}
```

---

## 🙌 Contribuer

Ce projet est un outil pédagogique open-source.
Toute contribution est bienvenue : amélioration des algorithmes, interface utilisateur, ajout de nouvelles statistiques...

---

## 📄 Licence

MIT – Utilisation libre à but non commercial.
