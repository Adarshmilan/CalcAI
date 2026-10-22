# CalcAI ✏️🧮

Draw a math problem on a canvas and let AI solve it.

CalcAI takes a hand-drawn image of an expression, equation or diagram, sends it to **Google Gemini 2.5 Flash**, and returns the answer in a structured form that the UI can render with MathJax.

> See [`REPORT.md`](REPORT.md) for the full project report (architecture, workflow and frontend details).

## What it can solve

The Gemini prompt handles five kinds of input:

1. **Simple expressions** – `2 + 3 * 4` (solved with PEMDAS)
2. **Systems of equations** – `x^2 + 2x + 1 = 0`, `3y + 4x = 0`
3. **Variable assignments** – `x = 4` (remembered and reused in later drawings)
4. **Graphical word problems** – Pythagoras, trigonometry, cricket wagon wheels, etc.
5. **Abstract concepts** – drawings that represent ideas like love, war or a famous invention

## How it works

```
Canvas drawing ──(base64 PNG + saved variables)──▶ POST /calculate
                                                     │
                                                     ▼
                                           FastAPI decodes image (Pillow)
                                                     │
                                                     ▼
                                           Gemini 2.5 Flash + prompt
                                                     │
                                                     ▼
                         [{ "expr": "...", "result": "...", "assign": true? }]
```

## Tech stack

| Part | Tools |
|------|-------|
| Backend (`calcai-be`) | Python, FastAPI, Uvicorn, Pydantic, Pillow, `google-generativeai`, `python-dotenv` |
| Frontend (`calcai-fe`) | React 19, TypeScript, Vite, Tailwind CSS, Mantine, MathJax, Axios, react-draggable |

> **Note:** `calcai-fe` is stored as a git submodule pointer, so the frontend source is not included in this repository.

## Project structure

```
calcai-be/
├── main.py                    # FastAPI app, CORS, health route
├── constants.py               # Host, port, GEMINI_API_KEY from .env
├── schema.py                  # ImageData request model
└── apps/calculator/
    ├── route.py               # POST /calculate
    └── utils.py               # Gemini prompt + response parsing
calcai-fe/                     # React frontend (submodule)
```

## Running the backend

```bash
cd calcai-be
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi uvicorn pydantic pillow google-generativeai python-dotenv

echo "GEMINI_API_KEY=your_key_here" > .env
python main.py                  # runs on http://localhost:8000
```

## API

### `GET /`
Health check → `{"message": "Welcome to CalcAI "}`

### `POST /calculate`

```json
{
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "dict_of_vars": { "x": 4 }
}
```

Response:

```json
{
  "message": "Image analyzed successfully",
  "type": "success",
  "data": [{ "expr": "2 + x", "result": 6 }]
}
```
