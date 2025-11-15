import { useState } from "react";
import { classifyEmail, sendFeedbackAPI, retrainAPI } from "./api";

function getBadgeClasses(category) {
  if (category === "Produtivo") {
    return "badge-productive";
  } else if (category === "Improdutivo") {
    return "badge-unproductive";
  }
  return "badge-default";
}

export default function App() {
  const [body, setBody] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [feedbackStatus, setFeedbackStatus] = useState("");
  const [correctedCategory, setCorrectedCategory] = useState("");
  const [improvedReply, setImprovedReply] = useState("");

  const [lastOriginalText, setLastOriginalText] = useState("");

  function handleFileChange(e) {
    const uploaded = e.target.files[0];
    setFile(uploaded);
    if (uploaded) setBody("");
  }

  function resetFeedback() {
    setFeedbackStatus("");
    setCorrectedCategory("");
    setImprovedReply("");
  }

  function handleReset() {
    setBody("");
    setFile(null);
    setResult(null);
    setError(null);
    setFeedbackStatus("");
    setCorrectedCategory("");
    setImprovedReply("");
    setLastOriginalText("");
  }

  async function handleClassify() {
    setLoading(true);
    setResult(null);
    setError(null);
    resetFeedback();

    try {
      const res = await classifyEmail(body, file);

      setResult(res);
      setLastOriginalText(body.trim());
      setImprovedReply(res.suggested_reply || "");

    } catch (err) {
      console.error(err);
      setError(err.message || "Erro desconhecido ao classificar.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSendFeedback() {
    if (!result || !lastOriginalText) {
      setFeedbackStatus("Erro: Classifique um e-mail antes de enviar feedback.");
      return;
    }
    setFeedbackStatus("Enviando...");

    try {
      await sendFeedbackAPI(
        lastOriginalText,
        result.category,
        correctedCategory,
        improvedReply
      );
      setFeedbackStatus("Feedback salvo com sucesso!");
    } catch (err) {
      console.error(err);
      setFeedbackStatus(`Erro: ${err.message}`);
    }
  }

  async function handleRetrain() {
    setFeedbackStatus("Re-treinando modelo...");
    try {
      await retrainAPI();
      setFeedbackStatus("Modelo re-treinado com sucesso!");
    } catch (err) {
      console.error(err);
      setFeedbackStatus(err.message);
    }
  }

  return (
    <div className="container">
      <header>
        <h1>Classificador de E-mails Automático</h1>
        <p className="subtitle">Classifique emails via texto ou upload</p>
      </header>

      {/* Upload Box (RESTAURADO) */}
      <section className="input-section">
        <div className="upload-box">
          <div className="arquivos">
            <p>Envie um arquivo</p>
            <ul className="file-types">
              <li id="txt">.txt</li>
              <li id="pdf">.pdf</li>
              <li id="eml">.eml</li>
            </ul>
          </div>

          <label className="file-button">
            Escolher arquivo
            <input
              type="file"
              accept=".txt,.pdf"
              onChange={handleFileChange}
            />
          </label>
          {file && <p className="file-name">📎 {file.name}</p>}
        </div>

        {/* Texto manual */}
        <label className="label-text">Ou cole o texto do e-mail:</label>
        <textarea
          value={body}
          onChange={(e) => {
            setBody(e.target.value);
            if (file) setFile(null); // Limpa o arquivo ao digitar
          }}
          rows="6"
          placeholder="Digite ou cole o conteúdo..."
        />

        {/* GRUPO DE BOTÕES DE AÇÃO */}
        <div className="action-buttons-group">
          <button
            className="btn process-btn"
            onClick={handleClassify}
            disabled={loading || (!body.trim() && !file)}
          >
            {loading ? "Analisando..." : "Classificar e-mail"}
          </button>
        </div>
        {error && <p className="error-message">🚨 {error}</p>}
      </section>

      {/* Resultado (Completo com detalhes e Feedback) */}
      {result && (
        <section className="result-card">
          <div className="result-header">
            <h3>Resultado</h3>
            <span className={`badge ${getBadgeClasses(result.category)}`}>
              {result.category}
            </span>
          </div>

          <div className="result-details">
            <p><strong>Confiança:</strong> {(result.confidence * 100).toFixed(1) || "-"}%</p>
            <p><strong>Sinais:</strong> {(result.signals || []).join(", ") || "-"}</p>
            <p><strong>Ações:</strong> {(result.actions || []).map(a => a.type).join(", ") || "-"}</p>
          </div>

          <div className="reply-section">
            <label className="label-text">Resposta sugerida</label>
            <pre className="reply-box">{result.suggested_reply || "Nenhuma resposta sugerida."}</pre>
          </div>

          {/* Seção de Feedback */}
          <div className="feedback-section">
            <h4 className="feedback-title">Feedback (aprendizado contínuo)</h4>
            <p className="feedback-note">Ajuste a categoria ou edite a resposta sugerida e envie.</p>

            <div className="feedback-controls">
              <label>Categoria correta:</label>
              <select
                value={correctedCategory}
                onChange={(e) => setCorrectedCategory(e.target.value)}
              >
                <option value="">(manter)</option>
                <option>Produtivo</option>
                <option>Improdutivo</option>
              </select>
            </div>

            <textarea
              value={improvedReply}
              onChange={(e) => setImprovedReply(e.target.value)}
              rows="4"
              placeholder="Edite a resposta sugerida, se desejar..."
            />

            <div className="feedback-actions">
              <button
                className="btn send-feedback-btn"
                onClick={handleSendFeedback}
              >
                Enviar feedback
              </button>
              <button
                className="btn retrain-btn"
                onClick={handleRetrain}
              >
                Re-treinar
              </button>
              <span className="feedback-status">{feedbackStatus}</span>
              <button
                className="btn reset-btn"
                onClick={handleReset}
                disabled={loading}
              >
                Recomeçar
              </button>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}