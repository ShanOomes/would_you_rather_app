from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)

PROMPTS = {
    "en": "Generate a funny, creative, or strange 'Would You Rather' question. Keep it safe for all audiences. Only return the question itself.",
    "nl": "Genereer een grappige, creatieve of vreemde 'Zou je liever'-vraag. Houd het geschikt voor alle leeftijden. Geef alleen de vraag zelf terug."
}

def generate_would_you_rather(lang):
    prompt = PROMPTS.get(lang, PROMPTS["en"])
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "qwen/qwen3-1.7b:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Error code: {response.status_code} - {response.text}")

    full = response.json()["choices"][0]["message"]["content"].strip()
    return full.split("?")[0].strip() + "?"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    lang = request.args.get("lang", "en")

    print(f"Generating question in {lang}...")  # Add this to see details
    
    try:
        question = generate_would_you_rather(lang)
        return jsonify({"question": question})
    except Exception as e:
        print("❌ Error in /generate:", e)  # Add this to see details
        return jsonify({"error": str(e)}), 500