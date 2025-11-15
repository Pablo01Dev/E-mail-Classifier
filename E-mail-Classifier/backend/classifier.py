import os
import re
import math
from typing import Dict, Any, List, Tuple

from nlp import normalize, mask_pii
from llm import zero_shot_category, refine_reply


# Regras simples
KEYWORDS_PRODUCTIVE = [
    r"\b(status|atualiza[çc][aã]o|andamento|progresso|prazo)\b",
    r"\b(chamado|ticket|protocolo|ocorr[eê]ncia|case)\b",
    r"\b(senha|acesso|login|bloqueio|reset)\b",
    r"\b(fatura|boleto|cobran[çc]a|pagamento|cart[aã]o|limite|lan[cç]amento)\b",
    r"\b(movimenta[çc][aã]o|transa[çc][aã]o|compra|d[eé]bito|cr[eé]dito|estorno|fraude|contest[aã]o|chargeback)\b",
    r"\b(anexo|em anexo|segue anexo|segue em anexo)\b",
    r"\b(erro|bug|falha|instabilidade|suporte|ajuda)\b",
    r"\b(contrato|cadastro|atualizar|atualiza[rç])\b",
]

KEYWORDS_UNPRODUCTIVE = [
    r"\b(feliz natal|boas festas|feliz ano|parab[eé]ns)\b",
    r"\b(agrade[çc]o|obrigado|obrigada)\b",
    r"\b(sem necessidade de retorno|apenas para informar)\b",
    r"\b(bom dia|boa tarde|boa noite).{0,40}$",
]


def _rule_based_score(text: str) -> Tuple[float, float, List[str]]:
    t = text.lower()
    hits = []
    pos = 0
    neg = 0

    for kw in KEYWORDS_PRODUCTIVE:
        if re.search(kw, t):
            pos += 1
            hits.append(kw)
    for kw in KEYWORDS_UNPRODUCTIVE:
        if re.search(kw, t):
            neg += 1
            hits.append(kw)

    rb_score = (pos - 0.7 * neg)
    prob_prod = 1 / (1 + math.exp(-rb_score))
    return prob_prod, 1 - prob_prod, hits



# AÇÕES
ATTACHMENT_HINTS = re.compile(
    r"\b(anexo|em anexo|segue anexo|segue em anexo)\b",
    re.IGNORECASE
)
TICKET_HINTS = re.compile(
    r"\b(chamado|protocolo|ticket|case|ocorr[eê]ncia)\b",
    re.IGNORECASE
)

FEEDBACK_CSV = os.getenv("FEEDBACK_CSV", "data/labels.csv")


def _detect_actions(text: str) -> Dict[str, Any]:
    actions = []
    if ATTACHMENT_HINTS.search(text):
        actions.append({"type": "check_attachments"})
        if TICKET_HINTS.search(text):
            actions.append({"type": "open_or_update_ticket"})
    return {"actions": actions}



# Feedback
def save_feedback(email_text: str, predicted: str, corrected: str | None = None, improved_reply: str | None = None):
    import csv
    import datetime

    os.makedirs(os.path.dirname(FEEDBACK_CSV), exist_ok=True)
    headers = ["timestamp", "predicted", "corrected", "improved_reply", "chars"]

    row = [
        datetime.datetime.utcnow().isoformat(),
        predicted,
        corrected or "",
        improved_reply or "",
        len(email_text or "")
    ]

    exists = os.path.exists(FEEDBACK_CSV)
    with open(FEEDBACK_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(headers)
        w.writerow(row)


def retrain_from_feedback():
    return False



# Templates
TEMPLATES = {
    "status": ("Produtivo", """Assunto: Atualização de status do seu caso

Olá, {{nome}}.

Recebemos sua solicitação sobre o status do caso {{id_caso}}. Já encaminhamos ao time responsável e a previsão de retorno é {{prazo}}.
Se houver novos documentos, você pode responder a este e-mail anexando-os.

Ficamos à disposição.
Atenciosamente,
{{assinatura}}"""),

    "anexo": ("Produtivo", """Assunto: Arquivo recebido

Olá, {{nome}}.

Confirmamos o recebimento do(s) arquivo(s) referente(s) ao caso {{id_caso}}. Iniciaremos a validação e retornamos até {{prazo}}.

Atenciosamente,
{{assinatura}}"""),

    "suporte": ("Produtivo", """Assunto: Suporte ao acesso

Olá, {{nome}}.

Entendemos a dificuldade de acesso. Reiniciamos o procedimento de reset de senha. Você receberá um e-mail em até {{prazo_curto}} com instruções.

Atenciosamente,
{{assinatura}}"""),

    "financeiro": ("Produtivo", """Assunto: Análise de movimentação / cobrança

Olá, {{nome}}.

Registramos sua solicitação sobre a movimentação ou cobrança em sua conta/cartão. Encaminharemos o caso para análise e retornaremos com os próximos passos até {{prazo}}.
Se desejar, você pode responder a este e-mail anexando comprovantes ou prints para apoiar a análise.

Atenciosamente,
{{assinatura}}"""),

    "cortesia": ("Improdutivo", """Assunto: Agradecimento

Olá, {{nome}}.

Agradecemos a mensagem! Registramos seus votos. Permanecemos à disposição sempre que precisar.

Atenciosamente,
{{assinatura}}"""),

    "generic_prod": ("Produtivo", """Assunto: Recebemos sua solicitação

Olá, {{nome}}.

Sua solicitação foi recebida e aberta sob o protocolo {{id_caso}}. Nossa equipe analisará e retornará até {{prazo}}.

Atenciosamente,
{{assinatura}}"""),

    "generic_improd": ("Improdutivo", """Assunto: Mensagem recebida

Olá, {{nome}}.

Recebemos sua mensagem. Não há ação necessária no momento. Permanecemos à disposição.

Atenciosamente,
{{assinatura}}""")
}


def _pick_template(text: str, category: str) -> str:
    t = text.lower()

    if category == "Produtivo":
        if re.search(r"\b(fatura|boleto|cobran[çc]a|pagamento|cart[aã]o|limite|lan[cç]amento|movimenta[çc][aã]o|transa[çc][aã]o|compra|d[eé]bito|cr[eé]dito|estorno|fraude|contest[aã]o|chargeback)\b", t):
            return TEMPLATES["financeiro"][1]
        if re.search(r"\b(status|andamento|prazo|protocolo|ticket|chamado)\b", t):
            return TEMPLATES["status"][1]
        if re.search(r"\b(senha|acesso|login|bloqueio|reset)\b", t):
            return TEMPLATES["suporte"][1]
        if re.search(r"\b(anexo|em anexo|segue anexo|segue em anexo)\b", t):
            return TEMPLATES["anexo"][1]
        return TEMPLATES["generic_prod"][1]

    else:
        if re.search(r"\b(feliz natal|boas festas|parab[eé]ns|obrigad[oa])\b", t):
            return TEMPLATES["cortesia"][1]
        return TEMPLATES["generic_improd"][1]



# CLASSIFY EMAIL — versão corrigida
def classify_email(text: str) -> Dict[str, Any]:
    raw = normalize(text)

    if not raw:
        return {
            "category": "Improdutivo",
            "confidence": 0.5,
            "signals": ["texto_vazio"],
            **_detect_actions(raw)
        }

    # 🔹 LLM FIRST — bloco recolocado dentro da função
    llm_cat = zero_shot_category(mask_pii(raw))

    if llm_cat and llm_cat.get("category") in ("Produtivo", "Improdutivo"):
        out = {
            "category": llm_cat["category"],
            "confidence": float(llm_cat.get("confidence", 0.88)),
            "signals": llm_cat.get("signals", []) + ["llm_zero_shot_first"],
        }
        if llm_cat.get("rationale") and len(out["signals"]) == 1:
            out["signals"].append(llm_cat["rationale"])

        out.update(_detect_actions(raw))
        return out

    # 🔹 FALLBACK RULES
    p_prod, _, hits = _rule_based_score(raw)
    final_label = "Produtivo" if p_prod >= 0.5 else "Improdutivo"
    final_conf = p_prod if final_label == "Produtivo" else 1 - p_prod

    out = {
        "category": final_label,
        "confidence": round(float(final_conf), 3),
        "signals": hits + ["fallback_rules"],
    }
    out.update(_detect_actions(raw))
    return out


# REPLY – template + refino com LLM
def generate_reply(text: str, result: Dict[str, Any]) -> str:
    category = result["category"]
    tpl = _pick_template(text, category)

    placeholders = {
        "{{nome}}": "Cliente",
        "{{id_caso}}": "#0000",
        "{{prazo}}": "2 dias úteis",
        "{{prazo_curto}}": "1 hora",
        "{{competencia}}": "MM/AAAA",
        "{{assinatura}}": "Equipe Atendimento",
    }

    for k, v in placeholders.items():
        tpl = tpl.replace(k, v)

    refined = refine_reply(mask_pii(text), tpl)
    return refined or tpl
