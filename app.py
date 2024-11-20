import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
api_key = os.getenv("API_KEY")

# Configuração da API generative AI do Google
genai.configure(api_key=api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message")
    
    try:
        # Inicializa o modelo e envia a mensagem
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Olá"},
                {"role": "model", "parts": "Bom te conhecer. O que você gostaria de saber?"},
            ]
        )
        response = chat.send_message(user_message)
        print(response)

        return jsonify({"message": response.text})
    except Exception as e:
        print("Erro ao se comunicar com a API:", e)
        return jsonify({"error": "Erro ao se comunicar com o modelo."}), 500

if __name__ == "__main__":
    app.run(debug=True)
