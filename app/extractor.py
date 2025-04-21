# app/extractor.py

from app.utils import extract_emails, extract_phones

def extract_cv_structure(text):
    structure = {
        "name": "",  # À détecter si possible
        "phoneNumbers": extract_phones(text),
        "websites": [],  # TODO: via regex
        "emails": extract_emails(text),
        "dateOfBirth": "",
        "addresses": [],  # TODO: détection plus complexe
        "summary": "",
        "education": [],  # TODO: NLP ou RAG
        "workExperience": [],  # TODO: NLP ou heuristiques
        "skills": [],  # TODO: regex ou modèles
        "certifications": []  # TODO: regex ou modèles
    }
    return structure
