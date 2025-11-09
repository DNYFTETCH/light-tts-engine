# Light TTS Engine

Lightweight FastAPI-based TTS engine designed to run in Termux or a small Linux server.
Uses `pico2wave` if available, otherwise falls back to `espeak-ng`.

Endpoints:
- `GET /health` — health check
- `GET /voices` — list voices (API key required)
- `POST /synthesize` — generate wav (X-API-KEY required)
