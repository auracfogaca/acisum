from fastapi import FastAPI, Request, UploadFile, File
from app.audio_processing import process_audio
import requests
import os

app = FastAPI()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")  # id do phone no Meta Developers

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    # extrair URL do áudio enviado pelo usuário via webhook do WhatsApp Cloud API
    # ex: data["entry"][0]["changes"][0]["value"]["messages"][0]["audio"]["id"]
    audio_url = "https://graph.facebook.com/v17.0/<media_id>"
    # baixar arquivo de áudio temporário
    # (em produção, use o endpoint de mídia da API do WhatsApp)
    
    # processar áudio
    analysis = process_audio("arquivo.wav")
    
    # enviar resultado de volta
    send_text_to_whatsapp(analysis)
    return {"status": "processed"}

def send_text_to_whatsapp(text):
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": "<user_phone_number>",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)
