import streamlit as st
import fitz
import requests
import json
import os

# === Extraction PDF ===
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)

# === Création du prompt ===
def build_prompt(text):
    return f"""
You are a recruitment assistant. Extract the following information from the text below in strict JSON format:
- Full Name
- Email Address
- Phone Number
- Level of Education
- Educational Institution

Example output:
{{
  "Full Name": "",
  "Email Address": "",
  "Phone Number": "",
  "Level of Education": "",
  "Educational Institution": ""
}}

Text:
{text}
Réponds uniquement en JSON :
"""

# === Envoi à Mistral ===
def query_mistral(prompt):
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    result = response.json()["response"]
    try:
        return json.loads(result)
    except:
        return result

# === Interface Streamlit ===
st.set_page_config(page_title="Batch Extraction CV", layout="wide")
st.title("Extraction en lot de CV PDF")

uploaded_files = st.file_uploader("Téléverser plusieurs CV", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    results = []

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_path = os.path.join("temp", file_name)

        # Enregistrer le fichier
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Traitement
        text = extract_text_from_pdf(file_path)
        prompt = build_prompt(text)
        json_result = query_mistral(prompt)

        # Stocker le résultat
        results.append((file_name, json_result))

    # Affichage
    for name, data in results:
        st.subheader(f"CV : {name}")
        st.json(data)

        # Convertir en bytes
        json_bytes = json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8")

        # Bouton de téléchargement
        st.download_button(
            label=f"Télécharger JSON - {name}",
            data=json_bytes,
            file_name=f"{name.replace('.pdf', '')}_extrait.json",
            mime="application/json"
        )

    