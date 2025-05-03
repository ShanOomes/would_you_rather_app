from flask import Flask, render_template, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

PROMPTS = {
    "en": "Generate a funny, creative, or strange 'Would You Rather' question. Keep it safe for all audiences. Only return the question itself.",
    "nl": "Genereer een grappige, creatieve of vreemde 'Zou je liever'-vraag. Houd het geschikt voor alle leeftijden. Geef alleen de vraag zelf terug."
}

def generate_would_you_rather(lang):
    prompt = PROMPTS.get(lang, PROMPTS["en"])
    completion = client.chat.completions.create(
        model="qwen/qwen3-1.7b:free",
        extra_headers={
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Would You Rather Generator"
        },
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    full = completion.choices[0].message.content.strip()
    return full.split("?")[0].strip() + "?"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    lang = request.args.get("lang", "en")
    try:
        question = generate_would_you_rather(lang)
        return jsonify({"question": question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
