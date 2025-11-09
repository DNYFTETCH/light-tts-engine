# app.py
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import subprocess
import uuid
from pathlib import Path
from typing import Optional
import shutil

app = FastAPI(title="Light TTS Engine", version="0.1")

GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)

API_KEY = os.getenv("API_KEY", "debug-key")

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "default"
    format: Optional[str] = "wav"

def synthesize_tts(text: str, out_path: str):
    """
    Uses pico2wave if available; otherwise uses espeak-ng.
    """
    if shutil.which("pico2wave"):
        cmd = ["pico2wave", "-w", out_path, text]
    elif shutil.which("espeak-ng"):
        cmd = ["espeak-ng", "-w", out_path, text]
    else:
        raise RuntimeError("No TTS engine found (pico2wave or espeak-ng). Install one.")

    subprocess.run(cmd, check=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/voices")
def voices(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"voices": [{"id": "default", "name": "Default Voice"}]}

@app.post("/synthesize")
def synthesize(payload: TTSRequest, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    fname = f"{uuid.uuid4().hex}.{payload.format}"
    out_path = GENERATED_DIR / fname

    try:
        synthesize_tts(payload.text, str(out_path))
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"TTS process failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")

    return FileResponse(out_path, media_type="audio/wav", filename=fname)
