const API_URL = "https://e-mail-classifier-backend.onrender.com";

// Envia um e-mail (texto ou arquivo) para classificação
export async function classifyEmail(body, file = null) {
  const formData = new FormData();

  const text = body.trim();
  if (!text && !file) {
    throw new Error("Cole o texto do e-mail ou envie um arquivo.");
  }

  if (text) formData.append("text", text);
  if (file) formData.append("file", file);

  const response = await fetch(`${API_URL}/api/process`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Erro ao processar o e-mail (HTTP ${response.status}).`);
  }

  const data = await response.json();
  if (data.error) throw new Error(data.error);

  return data;
}

// Envia feedback de categoria e/ou resposta gerada
export async function sendFeedbackAPI(
  originalText,
  predictedCategory,
  correctedCategory,
  improvedReply
) {
  const formData = new FormData();
  formData.append("original_text", originalText);
  formData.append("predicted", predictedCategory);

  if (correctedCategory) formData.append("corrected", correctedCategory);
  if (improvedReply) formData.append("improved_reply", improvedReply);

  const response = await fetch(`${API_URL}/api/feedback`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  if (!data.ok) {
    throw new Error(data.error || "Erro ao enviar feedback.");
  }

  return data;
}

// Solicita re-treino do modelo
export async function retrainAPI() {
  const response = await fetch(`${API_URL}/api/retrain`, {
    method: "POST",
  });

  const data = await response.json();

  if (data.error) throw new Error(data.error);
  if (!data.retrained) {
    throw new Error("Nada novo para treinar.");
  }

  return data;
}
