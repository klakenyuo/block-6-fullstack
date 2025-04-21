# app/utils.py

import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()  # charge les variables d'environnement

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(mailto:)?[\w\.-]+@[\w\.-]+', '', text)
    text = re.sub(r'\+?\d[\d\s\-\(\)]{7,}', '', text)
    return text.strip()

def get_embedding(text):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})
    response.raise_for_status()
    return response.json()

def extract_emails(text):
    return re.findall(r'[\w\.-]+@[\w\.-]+', text)

def extract_phones(text):
    return re.findall(r'\+?\d[\d\s\-\(\)]{7,}', text)
