from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ZERO-SHOT CLASSIFICATION
def zero_shot_category(text: str):
    try:
        prompt = f"""
        Classifique o email abaixo apenas como "Produtivo" ou "Improdutivo".
        Também diga sinais que te levaram à decisão e um nível de confiança (0 a 1).

        Email:
        {text}

        Responda em JSON com exatamente:
        {{
            "category": "...",
            "confidence": ...,
            "signals": ["...", "..."]
        }}
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",   # << --- MODELO FREE
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        import json
        output = completion.choices[0].message.content.strip()
        return json.loads(output)

    except Exception as e:
        print("ERRO ZERO-SHOT:", e)
        return None


# REFINE REPLY 
def refine_reply(email_text: str, template: str):
    try:
        prompt = f"""
        Você é um assistente que melhora textos de resposta a emails.
        Melhore a clareza, formalidade e mantenha o sentido original.

        Email original:
        {email_text}

        Resposta sugerida:
        {template}

        Retorne apenas o texto final, sem explicações.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("ERRO REFINE:", e)
        return template
