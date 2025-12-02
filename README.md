# 📧 AutoMail Classifier — Classificação Inteligente de E-mails com IA
---

Esta é uma aplicação web desenvolvida com **FastAPI (backend)** e **React + Vite (frontend)**, projetada para automatizar a triagem de e-mails em ambientes de alto volume, classificando e sugerindo respostas automáticas.

---

## ✨ Funcionalidades Principais

* **Classificação Automática**
  Categoriza e-mails em **Produtivo** ou **Improdutivo** usando um modelo híbrido (Regras + TF-IDF/LogReg).

* **Sugestão Automática de Resposta**
  Gera uma resposta adequada ao contexto e à categoria detectada.

---

# 🚀 Como Rodar Localmente

## 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/automail-classifier.git
cd automail-classifier
```

A estrutura geral agora é:

```
backend/
frontend/
```

---

# 🖥️ Backend (FastAPI)

## 2. Criar ambiente virtual e instalar dependências

```bash
cd backend

python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

## 3. Configurar a chave API

1. Copie o arquivo `.env.example` para `.env`
2. Substitua `YOUR_API_KEY_HERE` pela sua chave real

⚠️ Não faça commit do arquivo `.env`.

## 4. Rodar o backend

```bash
uvicorn app:app --reload --port 8000
```

Backend estará em:
➡️ [http://localhost:8000](http://localhost:8000)

---

# 🎨 Frontend (React + Vite)

## 1. Instalar dependências

```bash
cd ../frontend
npm install
```

## 2. Executar o servidor de desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em:
➡️ [http://localhost:5173](http://localhost:5173)

E já estará configurado para se comunicar com o backend em `http://localhost:8000`.

---

# ☁️ Deploy (Render)

### Backend (FastAPI)

1. Faça **fork** do repositório
2. No Render: *New +* → *Web Service*
3. Configure:

   * **Runtime**: Python 3.11
   * **Build command**:

     ```
     pip install -r backend/requirements.txt
     ```
   * **Start command**:

     ```
     uvicorn app:app --host 0.0.0.0 --port $PORT
     ```
4. Adicione as variáveis de ambiente (ex: `OPENAI_API_KEY`)

### Frontend (React + Vite)

1. Criar novo **Static Site** no Render
2. Configurar:

   * **Build Command**:

     ```
     npm install && npm run build
     ```
   * **Publish Directory**:

     ```
     dist
     ```
3. Se necessário, configurar proxy em `vite.config.js` para o backend

---

# 📂 Estrutura do Projeto

```
backend/
├── app.py                 # Ponto de entrada da API
├── classifier.py          # Classificador híbrido + respostas automáticas
├── nlp.py                 # Pré-processamento e leitura de arquivos
├── requirements.txt
└── .env.example

frontend/
├── index.html
├── src/
│   ├── App.jsx
│   ├── services/api.js
├── package.json
└── vite.config.js
```

---

# 🧠 Como Funciona o Classificador

* **Regras determinísticas**
  Palavras-chave como “protocolo”, “status”, “feliz natal”, etc.

* **Modelo TF-IDF + Logistic Regression**
  Treinado em um *seed set* inicial.

* **Combinação Híbrida**
  A probabilidade final é a média ponderada entre regras e modelo ML.

* **Geração de Resposta**
  Seleção automática via templates específicos para cada intenção.

---

# 🛠️ Próximas Melhorias

* Migrar para zero-shot (ex.: `bart-mnli`) ou LLMs (OpenAI / HuggingFace)
* Loop de feedback com *retreinamento*
* Detecção e tratamento avançado de anexos
* Sanitização de PII para maior segurança

---

# 🏆 Tecnologias Utilizadas

### Backend

* Python
* FastAPI
* scikit-learn
* Uvicorn

### Frontend

* React
* Vite
* CSS
---

# 🌐 Demonstração

> [E-mail Classifier](https://e-mail-classifier.vercel.app/)

---

# 🙋🏻‍♂️ Autor

**Pablo Guimarães**

---

# 📄 Licença

Este projeto está sob a licença **MIT**.

---

Se quiser, posso:

✅ gerar uma versão *super profissional* estilo open-source
✅ incluir badges (build passing, license, tech stack)
✅ adicionar GIF da interface
✅ montar um README multilíngue (PT/EN)

Só pedir!
