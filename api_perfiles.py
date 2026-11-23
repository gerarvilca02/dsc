import json
import re
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException

BASE = Path(__file__).resolve().parent

app = FastAPI(title="Banco LLM | Perfiles")


@app.get("/perfiles/{client_id}")
def perfil_http(client_id: str):
    if not re.fullmatch(r"CLI-\d{4}", client_id):
        raise HTTPException(422, "Formato esperado: CLI-1001.")
    archivo = BASE / "datos/perfiles" / f"{client_id}.json"
    if not archivo.exists():
        raise HTTPException(404, "Perfil sintético no encontrado.")
    return json.loads(archivo.read_text(encoding="utf-8"))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
