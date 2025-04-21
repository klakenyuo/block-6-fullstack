import joblib
import re
import string
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# === 1. Nettoyage du texte ===
def clean_text(text):
    french_stopwords = {
        "et", "le", "la", "les", "un", "une", "de", "des", "du", "en", "au", "aux",
        "ce", "ces", "cette", "dans", "pour", "par", "sur", "avec", "sans", "se",
        "son", "sa", "ses", "leurs", "est", "sont", "été", "être", "à", "il", "elle",
        "ils", "elles", "qui", "que", "quoi", "dont", "où", "mais", "ou", "donc", "or", "ni", "car"
    }
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    stop_words = ENGLISH_STOP_WORDS.union(french_stopwords)

    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# === 2. Chargement du texte brut ===
with open("data/example_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()


# === 3. Chargement du dataset nettoyé pour retrouver le TF-IDF vectorizer ===
df_train = pd.read_csv("data/cv_dataset_cleaned.csv")
corpus = df_train["cleaned_resume"].astype(str).tolist()


def predict_category(resume_text):
    # === 5. Charger le modèle de classification ===
    model = joblib.load("models/category_classifier.pkl")
    cleaned_resume = clean_text(resume_text)
    vectorizer = TfidfVectorizer(max_features=300)
    vectorizer.fit(corpus)
    vector = vectorizer.transform([cleaned_resume])
    prediction = model.predict(vector)
    return prediction[0]


# === 6. Prédiction ===
prediction = predict_category(resume_text)
print(f"✅ Catégorie prédite pour ce CV : {prediction}")
