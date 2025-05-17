# Extraction de données depuis des CV PDF avec Mistral (LLM local) et Streamlit

Ce projet extrait automatiquement les informations clés (nom, email, téléphone, expériences, etc.) depuis des CV au format PDF, en utilisant un modèle LLM local (Mistral via Ollama) et une interface Streamlit.

## Fonctionnalités

- Lecture de fichiers PDF avec `PyMuPDF`
- Extraction des données avec le modèle **Mistral** via **Ollama**
- Interface utilisateur avec **Streamlit**
- Traitement de plusieurs CV en batch
- Téléchargement des résultats en JSON

## Dépendances

- Python 3.9+
- `fitz` (PyMuPDF)
- `requests`
- `streamlit`
- Ollama installé localement avec le modèle `mistral`


