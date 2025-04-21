
# app/classifier.py

import joblib
from app.utils import clean_text, get_embedding

def load_model(path="data/model.pkl"):
    return joblib.load(path)

def predict_category(text, model):
    text_cleaned = clean_text(text)
    embedding = get_embedding(text_cleaned)
    return model.predict([embedding[0]])[0]
