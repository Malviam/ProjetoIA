let history = []; // Histórico de mensagens

document.getElementById("send-btn").addEventListener("click", async () => {
  const userInput = document.getElementById("user-input");
  const userMessage = userInput.value.trim();
  userInput.value = "";

  if (userMessage === "") return;

  // Adiciona a mensagem do usuário à interface
  appendMessage("user", userMessage);

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage, history }),
    });

    const data = await response.json();

    if (data.message) {
      // Adiciona a resposta do bot à interface
      appendMessage("bot", data.message);
      history = data.history; // Atualiza o histórico
    } else {
      appendMessage("bot", "Erro: " + data.error);
    }
  } catch (error) {
    appendMessage("bot", "Erro de conexão: Não foi possível se comunicar com o servidor.");
  }

  // Rolagem automática para a última mensagem
  const chatBox = document.getElementById("chat-box");
  chatBox.scrollTop = chatBox.scrollHeight;
});

function appendMessage(role, message) {
  const chatBox = document.getElementById("chat-box");
  const messageElement = document.createElement("p");

  messageElement.textContent = message;
  messageElement.classList.add(role === "user" ? "user-message" : "bot-message");

  chatBox.appendChild(messageElement);
}
