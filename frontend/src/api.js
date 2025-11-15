// api.js

const API_URL = "http://localhost:8000"; // Endereço do seu backend Python

/**
 * Processa o email (classifica e gera resposta).
 * @param {string} body - O corpo do email em texto.
 * @param {File} [file=null] - O arquivo (txt, pdf, etc.) do email.
 * @returns {Promise<object>} Os dados de resposta do servidor (categoria, reply, etc.).
 */
export async function classifyEmail(body, file = null) {
  const formData = new FormData();

  const text = body.trim();
  if (!text && !file) {
    throw new Error("Por favor, cole o texto do e-mail ou envie um arquivo.");
  }
  
  if (text) {
      formData.append("text", text);
  }

  if (file) {
    formData.append("file", file);
  }

  const response = await fetch(`${API_URL}/api/process`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status} ao processar e-mail.`);
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(data.error);
  }
  
  return data;
}

/**
 * Envia o feedback de classificação e/ou resposta.
 *
 * @param {string} originalText - O texto original do e-mail.
 * @param {string} predictedCategory - A categoria predita originalmente.
 * @param {string} [correctedCategory] - A categoria correta (se corrigida).
 * @param {string} [improvedReply] - A resposta sugerida (se editada/melhorada).
 * @returns {Promise<object>} O status da operação.
 */
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
    throw new Error(data.error || "Erro desconhecido ao enviar feedback");
  }
  
  return data;
}

/**
 * Solicita o re-treino do modelo.
 * @returns {Promise<object>} O status da operação de re-treino.
 */
export async function retrainAPI() {
  const response = await fetch(`${API_URL}/api/retrain`, {
    method: "POST",
  });
  
  const data = await response.json();
  
  if (data.error) {
     throw new Error(data.error);
  }
  if (!data.retrained) {
     throw new Error("Nada para treinar. Modelo não foi re-treinado.");
  }
  
  return data;
}