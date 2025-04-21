import os
import re
import requests
import json
from dotenv import load_dotenv
import tiktoken


# === 1. Charger token API ===
load_dotenv()
API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
# API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# === 2. Prompt structuré ===
STRUCTURE_PROMPT = """
Tu es un assistant intelligent spécialisé dans l’analyse de CVs en français.

Ta mission est d'extraire toutes les informations utiles d’un CV brut et de les structurer en JSON.

Ne laisse **aucun champ vide** si des informations peuvent être inférées. 
Si une information n’est pas disponible, mets la valeur `null`.

Le JSON doit contenir exactement les clés suivantes :

"name", "phoneNumbers", "emails", "addresses", "summary", 
"education", "workExperience", "skills", "certifications"

Voici maintenant le contenu du CV :

<<<CV>>>

Renvoie uniquement le JSON sans texte autour.
"""

def count_tokens(text: str, model_name="gpt-3.5-turbo"):
    try:
        enc = tiktoken.encoding_for_model(model_name)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))



def extract_json_from_text(text: str) -> str:
    start = text.find("{")
    if start == -1:
        return ""

    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                return text[start:i+1]
    return ""


def generate_structure_from_text(cv_text: str) -> dict:

    print("🔢 Découpage du texte...")
    # Découpe si le texte est trop long
    cv_trimmed = cv_text
    prompt_base = STRUCTURE_PROMPT.replace("<<<CV>>>", "")

    max_tokens_allowed = 8192  # max pour Mixtral-8x7B
    tokens_prompt = count_tokens(prompt_base)

    # Limite le texte brut pour que le total reste dans les limites
    while count_tokens(prompt_base + cv_trimmed) > (max_tokens_allowed - 100):
        cv_trimmed = cv_trimmed[:-500]

    prompt = STRUCTURE_PROMPT.replace("<<<CV>>>", cv_trimmed)

    print(prompt)

    print(f"📏 Longueur du texte : {len(cv_text)} caractères")
    print(f"🔢 Tokens envoyés : {count_tokens(prompt)}")

    try:
        print("🔢 Appel API...")
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        print("📝 Réponse brute :")
        print(response.text[:1000])
        response.raise_for_status()

        output = response.json()
        generated = output[0]["generated_text"] if isinstance(output, list) else output.get("generated_text", "")

        json_block = extract_json_from_text(generated)
        if json_block:
            print("🔢 Extraction JSON...")
            try:
                print("🔢 Parsing JSON...")
                return json.loads(json_block)
            except json.JSONDecodeError as je:
                print("⚠️ JSON extrait, mais erreur de parsing :", je)
                print("Contenu partiel :\n", json_block[:500])
                return {}
        else:
            print("❌ Aucun JSON valide trouvé dans la réponse.")
            print("Texte reçu :\n", generated[:500])
            return {}

    except Exception as e:
        print("❌ Erreur d'appel API :", e)
        return {}

# === 4. Exécution ===
if __name__ == "__main__":
    with open("data/example_resume.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()

    structure = generate_structure_from_text(cv_text)
    print("🔢 Structure générée :")
    print(json.dumps(structure, indent=2, ensure_ascii=False))
