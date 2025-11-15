git a## 📧 AutoMail Classifier: Classificação e Resposta de E-mails com IA

Esta é uma aplicação web simples (construída com **FastAPI** e **HTML/Tailwind**) desenhada para automatizar a triagem de e-mails em ambientes de alto volume.

### Funcionalidades Principais

* **Classificação Automática**: Categoriza e-mails em **Produtivo** (requer ação) ou **Improdutivo** (agradecimentos, felicitações, etc.) usando um modelo híbrido (regras + TF-IDF/LogReg).
* **Geração de Resposta Sugerida**: Apresenta uma resposta automática adequada ao contexto e à categoria identificada.

---

## 🚀 Como Rodar Localmente

Siga estes passos para configurar e executar a aplicação em sua máquina:

### 1. Configuração do Ambiente e Dependências

```bash
# Crie e ative o ambiente virtual
python -m venv .venv 
. .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
````

### 2\. Configuração da Chave API (Obrigatório)

Se o seu classificador ou gerador de respostas utiliza um serviço externo (como OpenAI, Hugging Face, etc.), você **deve configurar a chave API**.

  * Crie um arquivo chamado **`.env`** na raiz do projeto (o mesmo local de `app.py`).
  * Copie o conteúdo de **`.env.example`** para o novo arquivo.
  * Substitua o valor de `YOUR_API_KEY_HERE` pela sua chave real.

> ⚠️ **Atenção**: O arquivo `.env` não deve ser commitado publicamente por questões de segurança. O `.env.example` é fornecido para referência.

### 3\. Execução da Aplicação

Inicie o servidor local:

```bash
python app.py
```

  * **Acesse a Interface**: Abra seu navegador e acesse a URL: **http://localhost:8000**

-----

## ☁️ Instruções de Deploy (Exemplo: Render)

Para colocar a aplicação online de forma rápida:

1.  Faça **fork** deste repositório para sua conta no GitHub.
2.  No painel do **Render**, clique em *New +* \> *Web Service* e conecte seu GitHub.
3.  Configure os parâmetros do serviço:
      * **Runtime**: Python 3.11
      * **Build command**: `pip install -r requirements.txt`
      * **Start command**: `python app.py` (ou `uvicorn app:app --host 0.0.0.0 --port $PORT` se estiver usando Uvicorn/FastAPI)
4.  **Variáveis de Ambiente**: Na seção *Environment*, adicione a variável com sua chave API (ex.: `OPENAI_API_KEY` ou `HF_TOKEN`) para corresponder ao que está configurado em seu `.env.example`.
5.  Acesse a URL gerada pelo Render.

-----

## 📂 Estrutura do Projeto

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `app.py` | Ponto de entrada. Contém a inicialização do **FastAPI** e as rotas da API. |
| `classifier.py` | Implementa o **Classificador Híbrido** e a lógica de **Geração de Respostas** (baseado em templates). |
| `nlp.py` | Funções de **Pré-processamento de Linguagem Natural** (normalização, tokenização) e rotinas para leitura de arquivos (.pdf/.txt). |
| `static/index.html` | **Interface de Usuário** (UI). Utiliza **Tailwind CSS** via CDN para estilização. |
| `requirements.txt` | Lista de bibliotecas Python necessárias para rodar a aplicação. |
| `.env.example` | Template para variáveis de ambiente (API Keys). |

-----

## 🧠 Detalhes do Modelo de Classificação

O sistema utiliza uma abordagem de classificação **híbrida** para otimizar a precisão e a velocidade:

  * **Regras Determinísticas**: Palavras-chave de alta relevância (`status`, `protocolo`, `anexo`, `feliz natal`, etc.) geram uma probabilidade *prior* inicial.
  * **Modelo de Aprendizado de Máquina**: Uma representação do texto via **TF-IDF** é passada para um modelo de **Regressão Logística** treinado em um conjunto de dados inicial (*seed set*).
  * **Combinação**: A classificação final é determinada pela **média das probabilidades** preditas pelo modelo e a probabilidade *prior* das regras.
  * **Respostas Sugeridas**: A resposta é selecionada e customizada a partir de **templates** específicos para diferentes intenções (suporte, financeiro, solicitação de status, etc.).

-----

## 💡 Próximas Melhorias Sugeridas

O projeto pode ser expandido com as seguintes funcionalidades avançadas:

  * **Troca de Classificador**: Migração para modelos de *zero-shot* (ex.: `bart-large-mnli`) ou uso de **LLMs** (OpenAI/Hugging Face) com *few-shot learning* para maior precisão sem treinamento extensivo.
  * **Aprendizado Contínuo**: Implementar um loop de *feedback* onde o operador pode corrigir rótulos (rótulos de ouro), salvando-os para um **retreinamento** (online learning) periódico.
  * **Análise de Anexos**: Adicionar detecção e processamento de *attachments* para rotear tarefas (ex.: abrir ticket, mover arquivo para pasta específica).
  * **Segurança e Privacidade**: Implementar rotinas de **PII Sanitization** e mascaramento de dados sensíveis antes do envio a APIs de LLMs externos.

-----

## 🏆 Objetivo e Tecnologias-Chave

O principal objetivo deste projeto foi aplicar conhecimentos de **Integração de Sistemas** e **Processamento de Linguagem Natural (NLP)**. As tecnologias centrais utilizadas incluem:

  * **Backend**: Python, **FastAPI** (para alta performance).
  * **Classificação**: Modelo Híbrido (Regras + TF-IDF/LogReg).
  * **Frontend**: HTML, JavaScript e **Tailwind CSS** (via CDN) para uma interface responsiva e moderna.

-----

## 💻 Demonstração Online

Você pode acessar o resultado final da aplicação de classificação de e-mails, hospedada na nuvem, no link abaixo:

  * **Acessar a Aplicação** (Substitua este link pela sua URL de deploy real, ex: Render/Vercel)

-----

## 🙋🏻‍♂️ Autor

Pablo Guimarães

-----

## 📄 Licença

Este projeto está sob a licença **MIT**.

```