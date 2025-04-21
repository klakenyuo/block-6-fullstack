# Analyseur de CV

Ce projet est une application d'analyse de CV qui permet de :
1. Prédire la catégorie professionnelle d'un CV
2. Extraire et structurer les informations clés d'un CV

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Interface Streamlit](#interface-streamlit)
  - [API FastAPI](#api-fastapi)
- [Structure du projet](#structure-du-projet)
- [Développement](#développement)
- [Licence](#licence)

## Fonctionnalités

- **Prédiction de catégorie** : Analyse le contenu d'un CV et prédit sa catégorie professionnelle
- **Extraction de structure** : Transforme un CV en texte brut en une structure JSON organisée
- **Interface utilisateur** : Application Streamlit pour une utilisation facile
- **API REST** : Endpoints pour l'intégration dans d'autres applications

## Architecture

Le projet est composé de plusieurs composants :

- **Modèle de classification** : Utilise un modèle entraîné pour prédire la catégorie d'un CV
- **Extracteur de structure** : Utilise un modèle RAG (Retrieval-Augmented Generation) pour extraire les informations structurées
- **Interface Streamlit** : Interface utilisateur pour l'upload et l'analyse de CVs
- **API FastAPI** : API REST pour l'intégration dans d'autres applications

## Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Accès à Internet (pour les appels API)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone <url-du-depot>
   cd <nom-du-depot>
   ```

2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement :
   Créez un fichier `.env` à la racine du projet avec :
   ```
   HF_API_TOKEN=votre_token_huggingface
   ```

## Utilisation

### Interface Streamlit

Pour lancer l'interface utilisateur :

```bash
streamlit run main.py
```

L'interface sera accessible à l'adresse : http://localhost:8501

### API FastAPI

Pour lancer l'API :

```bash
uvicorn api.api:app --reload
```

L'API sera accessible à :
- Documentation Swagger UI : http://localhost:8000/docs
- Documentation ReDoc : http://localhost:8000/redoc
- API Root : http://localhost:8000/

#### Endpoints disponibles

1. **Prédiction de catégorie** :
   ```
   POST /predict-category
   Content-Type: application/json
   
   {
     "content": "Texte du CV..."
   }
   ```

2. **Génération de structure** :
   ```
   POST /generate-structured
   Content-Type: application/json
   
   {
     "content": "Texte du CV..."
   }
   ```

## Structure du projet

```
.
├── api/                  # API FastAPI
│   └── api.py            # Définition des endpoints
├── app/                  # Modules principaux
│   ├── classifier.py     # Classification de CV
│   ├── extractor.py      # Extraction de structure
│   └── utils.py          # Utilitaires
├── data/                 # Données
│   ├── cv_dataset.csv    # Dataset d'entraînement
│   └── example_resume.txt # CV exemple
├── models/               # Modèles entraînés
│   └── category_classifier.pkl # Modèle de classification
├── notebooks/            # Notebooks Jupyter
│   └── exploration.ipynb # Exploration des données
├── .env                  # Variables d'environnement
├── main.py               # Application Streamlit
├── predict_category.py   # Script de prédiction
├── rag_cv_structurer.py  # Script d'extraction de structure
└── requirements.txt      # Dépendances
```

## Développement

### Création du dataset

Pour créer un nouveau dataset à partir de CVs :

```bash
python create_dataset.py
```

### Entraînement du modèle

Pour entraîner un nouveau modèle de classification :

1. Ouvrez le notebook `models/train.ipynb`
2. Exécutez toutes les cellules
3. Le modèle entraîné sera sauvegardé dans `models/category_classifier.pkl`

