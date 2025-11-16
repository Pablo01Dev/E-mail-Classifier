from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, os

from dotenv import load_dotenv
load_dotenv()

from classifier import classify_email, generate_reply, save_feedback, retrain_from_feedback
from nlp import read_text_from_upload

app = FastAPI(title="AutoMail Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/process")
async def process_email(
    file: UploadFile | None = File(default=None),
    text: str = Form(default="")
):
    try:
        if file is None and not text.strip():
            return JSONResponse(
                {"error": "Envie um arquivo .txt/.pdf ou cole o texto."},
                status_code=400
            )

        content = text
        if file is not None:
            content_bytes = await file.read()
            content = read_text_from_upload(file.filename, content_bytes)

        result = classify_email(content)
        reply = generate_reply(content, result)

        return {
            "category": result["category"],
            "confidence": result["confidence"],
            "signals": result.get("signals", []),
            "actions": result.get("actions", []),
            "suggested_reply": reply,
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/feedback")
async def feedback(
    original_text: str = Form(...),
    predicted: str = Form(...),
    corrected: str | None = Form(default=None),
    improved_reply: str | None = Form(default=None),
):
    try:
        save_feedback(original_text, predicted, corrected, improved_reply)
        return {"ok": True}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/retrain")
async def retrain():
    ok = retrain_from_feedback()
    return {"retrained": bool(ok)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
