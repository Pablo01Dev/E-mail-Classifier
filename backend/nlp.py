import re, io
from typing import List
try:
    import pdfminer.high_level as pdfminer_high_level
except Exception:
    pdfminer_high_level = None

PT_STOPWORDS = set("""a o os as um uma de do da das dos e ou mas porém contudo então como para por com sem sob sobre após até entre desde lhe lhes me te se nos vos nós vocês eu tu ele ela eles elas isto isso aquilo que qual quais cujo cuja cujoas onde quando porque porquê para quê quê está estão foi eram será seriam fui sou somos seja sejam""".split())

def normalize(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def tokenize(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"[a-zà-ú0-9@._\-]+", text, flags=re.IGNORECASE)
    return [t for t in tokens if t not in PT_STOPWORDS]

def read_text_from_upload(filename: str, content: bytes) -> str:
    name = (filename or "").lower()
    if name.endswith(".txt"):
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1", errors="ignore")
    if name.endswith(".pdf"):
        if pdfminer_high_level is None:
            raise RuntimeError("Leitura de PDF requer 'pdfminer.six' em requirements.txt")
        fp = io.BytesIO(content)
        text = pdfminer_high_level.extract_text(fp)
        return text or ""
    # fallback attempt
    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return str(content)


# --- PII masking ---

PII_PATTERNS = [
    (re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "<CPF>"),
    (re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}-?\d\b"), "<RG>"),
    (re.compile(r"\b(?:\+?55)?\s?(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}\b"), "<PHONE>"),
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b"), "<CARD>"),
    (re.compile(r"\b\d{5}-?\d{3}\b"), "<CEP>"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<EMAIL>"),
]

def mask_pii(text: str) -> str:
    t = text
    for rx, token in PII_PATTERNS:
        t = rx.sub(token, t)
    return t
