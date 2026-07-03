import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Route to serve your frontend index.html page
@app.route('/')
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return render_template_string(html_content)

# Secure Backend Pipeline Node to process requests
@app.route('/api/search', methods=['POST'])
def search_and_explain():
    data = request.get_json() or {}
    target_object = data.get("query", "").strip()
    
    if not target_object:
        return jsonify({"error": "Empty search query"}), 400

    try:
        # 1. Fetch dynamic space image URL using Unsplash architecture
        image_url = f"https://unsplash.com" # High-quality generic fallback
        
        # 2. Query the open live AI engine node for text explanation
        ai_response = requests.post(
            "https://openrouter.ai",
            headers={"Content-Type": "application/json"},
            json={
                "model": "meta-llama/llama-3.2-1b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a friendly, sci-fi space exploration AI tutor for AstroMindAI. Answer the question accurately but keep it conversational, simple, and under 4 sentences."
                    },
                    {
                        "role": "user",
                        "content": f"Explain what a high-resolution telescope photograph shows when looking at: {target_object}"
                    }
                ]
            },
            timeout=10
        )
        
        ai_data = ai_response.json()
        processed_answer = ai_data["choices"][0]["message"]["content"]
        
        # Try to customize the image search dynamically using public keyword endpoints
        dynamic_image = f"https://unsplash.com,{target_object}"

        return jsonify({
            "image_url": dynamic_image,
            "explanation": processed_answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render binds automatically to the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
                       
