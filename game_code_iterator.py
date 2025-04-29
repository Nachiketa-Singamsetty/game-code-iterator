from flask import Flask, render_template, request, jsonify
import os
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_code', methods=['POST'])
def process_code():
    try:
        data = request.json
        original_code = data.get('code', '')
        prompt = data.get('prompt', '')
        
        logger.info(f"Received prompt: {prompt[:50]}...")
        
        full_prompt = f"""You are a game development code assistant. Your task is to improve the following code based on the user's request.

Original Code:

User Request: {prompt}

Please provide:
1. The improved code
2. A clear explanation of the changes made and why they improve the code
3. Any additional suggestions for further improvement

Format your response as follows:
<improved_code>
// Place the improved code here
</improved_code>

<explanation>
// Place your explanation here
</explanation>

<additional_suggestions>
// Place any additional suggestions here
</additional_suggestions>
"""
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        })

        if response.status_code != 200:
            raise Exception(f"Error from Ollama API: {response.text}")
        
        content = response.json().get("response", "")
        improved_code = extract_section(content, "improved_code")
        explanation = extract_section(content, "explanation")
        suggestions = extract_section(content, "additional_suggestions")

        if not improved_code and "```" in content:
            improved_code = content.split("```")[1].strip()
            if improved_code.startswith(("python", "java", "c#", "cpp", "c++", "javascript", "ts")):
                improved_code = improved_code.split("\n", 1)[1]

        if not explanation:
            explanation = extract_fallback(content, "explanation", "additional suggestions")

        if not suggestions:
            suggestions = "None provided."

        return jsonify({
            "improved_code": improved_code,
            "explanation": explanation,
            "additional_suggestions": suggestions,
            "original_code": original_code
        })

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def extract_section(content, section_name):
    start_tag = f"<{section_name}>"
    end_tag = f"</{section_name}>"
    start = content.find(start_tag)
    if start == -1:
        return ""
    end = content.find(end_tag, start)
    return content[start + len(start_tag):end].strip() if end != -1 else content[start + len(start_tag):].strip()

def extract_fallback(content, start_key, end_key):
    lower = content.lower()
    start = lower.find(start_key)
    end = lower.find(end_key)
    if start == -1:
        return ""
    return content[start:end].strip() if end != -1 else content[start:].strip()

def check_ollama_connection():
    try:
        res = requests.get("http://localhost:11434/api/tags")
        if res.status_code == 200:
            models = res.json().get("models", [])
            if models:
                print("✅ Ollama is running with models:")
                for m in models:
                    print(f" - {m['name']}")
                return True
            else:
                print("⚠️ No models installed. Run: ollama pull llama3")
        else:
            print("❌ Ollama not responding.")
    except:
        print("❌ Unable to connect to Ollama.")
    return False

if __name__ == '__main__':
    os.makedirs("templates", exist_ok=True)
    if not os.path.exists("templates/index.html"):
        with open("templates/index.html", "w", encoding="utf-8") as f:
            f.write("<!-- Add your HTML template here -->")
    check_ollama_connection()
    app.run(debug=True)
