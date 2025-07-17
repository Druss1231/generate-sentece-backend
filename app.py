from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

# Configure Gemini API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from any frontend

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    word = data.get('word')
    if not word:
        return jsonify({"error": "No word provided"}), 400

    prompt = f"""Generate a TOEIC-like English sentence using the word '{word}'.
Return the output in **real TSV format** (tab-separated, not comma-separated) with no headers.
Only output one line in this format:

[example sentence] \t [Japanese meaning]"""

    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content(prompt)

    return jsonify({"result": response.text.strip()})

if __name__ == '__main__':
    app.run(debug=False)