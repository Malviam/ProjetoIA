import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder="public", template_folder="templates")
api_key = os.getenv("API_KEY")

# Configuração da API generative AI do Google
genai.configure(api_key=api_key)


@app.route("/")
def chatbot():
    return render_template("chatbot.html")  # Tela 1 - Chatbot interativo


@app.route("/generator")
def generator():
    return render_template("index.html")  # Tela 2 - Gerador de atividades


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()  # Interpreta o corpo da requisição como JSON
        if not data:
            return jsonify({"error": "Requisição inválida. Envie um JSON válido."}), 400

        user_message = data.get("message")
        history = data.get("history", [])

        if not user_message:
            return jsonify({"error": "A mensagem do usuário é obrigatória."}), 400

        # Inicializa o modelo generative AI para o chatbot
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=history)

        # Envia a mensagem do usuário para o modelo
        response = chat.send_message(user_message)

        # Obtém a resposta do modelo e atualiza o histórico
        model_message = response.text
        new_history = history + [
            {"role": "user", "parts": user_message},
            {"role": "model", "parts": model_message},
        ]

        return jsonify({"message": model_message, "history": new_history})
    except Exception as e:
        print("Erro ao se comunicar com a API:", e)
        return jsonify({"error": "Erro ao se comunicar com o modelo."}), 500


@app.route("/generate_activity", methods=["POST"])
def generate_activity():
    data = request.get_json()
    theme = data.get("theme")
    grade_level = data.get("grade_level")

    if not theme or not grade_level:
        return jsonify({"error": "Por favor, forneça um tema e um nível de ensino."}), 400

    try:
        # Inicializa o modelo generative AI para gerar atividades educacionais
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Prompt personalizado para geração de atividades
        prompt = f"Crie 5 atividades educacionais sobre o tema '{theme}' para o nível de ensino '{grade_level}'."
        
        # Gera o conteúdo usando o modelo
        response = model.generate_content(prompt)

        # Processa a resposta
        activities = response.text.split("\n")  # Divide a resposta em linhas
        activities = [activity.strip() for activity in activities if activity.strip()]  # Remove espaços extras

        return jsonify({"activities": activities[:5]})  # Limita a 5 atividades
    except Exception as e:
        print("Erro ao se comunicar com a API:", e)
        return jsonify({"error": "Erro ao gerar atividades."}), 500


if __name__ == "__main__":
    app.run(debug=True)
