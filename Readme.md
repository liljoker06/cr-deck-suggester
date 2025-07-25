# 🧠 Clash Royale Deck Analyzer – Projet IA Locale

Ce projet analyse les decks de Clash Royale à partir de replays, en extrayant des statistiques avancées et en générant des conseils personnalisés grâce à une IA **locale** (Ollama).

---

## 📁 Structure du projet

```
.
├── backend/             # API principale + scraping MongoDB
│   ├── scraping/        # Scripts de scraping et d'analyse
│   ├── main.py          # Serveur FastAPI (port 8000)
│   └── ...
├── ia_api/              # API dédiée à l'IA locale (Ollama)
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
* [Ollama](https://ollama.com/) (pour lancer le modèle IA localement)

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

#### a. Scraper les parties Clash Royale

```bash
cd backend
venv\Scripts\activate
python scraping/gameScrap.py
```

#### b. Analyser les replays collectés

```bash
cd backend
venv\Scripts\activate
python scraping/gameAnalyst.py
```

---

## 🧠 Lancement de l'IA (analyse des decks via Ollama)

### 1. Démarrer Ollama (dans un terminal séparé)

```bash
ollama run mistral
```

### 2. Aller dans le dossier `ia_api`

```bash
cd ia_api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Lancer l'API de l’IA (port 8001)

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
👉 [http://localhost:5173](http://localhost:5173) (ou autre port indiqué)

---

## 📌 Résumé rapide

| Tâche                 | Commande                                                 |
| --------------------- | -------------------------------------------------------- |
| API principale        | `uvicorn main:app --reload` (dans `/backend`)            |
| Scraper les parties   | `python scraping/gameScrap.py`                           |
| Analyser les parties  | `python scraping/gameAnalyst.py`                         |
| Lancer IA avec Ollama | `ollama run mistral`                                     |
| API IA locale         | `uvicorn main:app --reload --port 8001` (dans `/ia_api`) |
| Frontend              | `npm install && npm run dev` (dans `/frontend`)          |

---

## 🔪 Exemple de requête à l’IA

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
Toute contribution est bienvenue : amélioration des modèles, interface utilisateur, ajout de nouvelles statistiques...

---

## 📄 Licence

MIT – Utilisation libre à but non commercial.
