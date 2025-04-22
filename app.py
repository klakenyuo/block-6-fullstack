# main.py

import streamlit as st
from predict_category import predict_category
from rag_cv_structurer import generate_structure_from_text
from PyPDF2 import PdfReader
import io

# Configuration de la page
st.set_page_config(
    page_title="Analyseur de CV",
    page_icon="📄",
    layout="wide"
)

# Titre de l'application
st.title("📄 Analyseur de CV")
st.markdown("""
Cette application permet d'analyser un CV et d'en extraire :
- La catégorie professionnelle
- La structure détaillée des informations
""")

# Zone d'upload de fichier
uploaded_file = st.file_uploader("Choisissez un fichier CV (PDF ou TXT)", type=['pdf', 'txt'])

if uploaded_file is not None:
    # Lecture du contenu du fichier
    try:
        if uploaded_file.type == "text/plain":
            content = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            # Lecture du PDF
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text()
        else:
            st.error("Format de fichier non supporté. Veuillez utiliser un fichier PDF ou TXT.")
            st.stop()

        # Affichage du texte extrait
        with st.expander("Voir le texte extrait"):
            st.text_area("Contenu du CV", content, height=200)

        # Affichage des résultats dans deux colonnes
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Catégorie Prédite")
            with st.spinner("Analyse en cours..."):
                predicted_category = predict_category(content)
                st.success(f"Catégorie : {predicted_category}")

        with col2:
            st.subheader("🔍 Structure du CV")
            with st.spinner("Analyse en cours..."):
                structure = generate_structure_from_text(content)
                st.json(structure)

    except Exception as e:
        st.error(f"Une erreur est survenue lors du traitement du fichier : {str(e)}")
        st.stop()
