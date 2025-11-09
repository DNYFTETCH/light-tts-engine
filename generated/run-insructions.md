# Run instructions (Termux / Linux)

1. Install OS packages (Termux):
   - `pkg update && pkg upgrade -y`
   - `pkg install -y python ffmpeg sox espeak-ng` 
   - (If pico2wave available: `pkg install -y libttspico-utils`)

2. Install Python deps:
   - `pip install -r requirements.txt`

3. Copy example env:
   - `cp .env.example .env`
   - `export API_KEY=debug-key`

4. Run:
   - `uvicorn app:app --host 0.0.0.0 --port 8000`

5. Test:
   - `curl -X POST "http://127.0.0.1:8000/synthesize" -H "Content-Type: application/json" -H "X-API-KEY: debug-key" -d '{"text":"Hello, how are you?"}' --output test.wav`
