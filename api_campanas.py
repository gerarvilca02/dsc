import re
import unicodedata
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

BASE = Path(__file__).resolve().parent


def clave(valor):
    return "".join(
        c
        for c in unicodedata.normalize("NFKD", valor.strip().casefold())
        if not unicodedata.combining(c)
    )


class Afinidad(BaseModel):
    categoria: str
    subcategorias: list[str] = Field(min_length=1, max_length=8)


class ConsultaCampanas(BaseModel):
    mes: int = Field(ge=1, le=12)
    anio: int = Field(ge=2000, le=2100)
    afinidades: list[Afinidad] = Field(min_length=1, max_length=12)


app = FastAPI(title="Banco LLM | Campañas")


@app.post("/campanas")
def campanas_http(consulta: ConsultaCampanas):
    archivo = BASE / "datos/campanas" / f"{consulta.anio:04}-{consulta.mes:02}.md"
    if not archivo.exists():
        return []
    pares = {(clave(a.categoria), clave(s)) for a in consulta.afinidades for s in a.subcategorias}
    fichas = []
    for cuerpo in re.split(r"^## ", archivo.read_text(encoding="utf-8"), flags=re.M)[1:]:
        cabecera, *lineas = cuerpo.splitlines()
        ident, nombre = cabecera.split(" | ", 1)
        campos = dict(linea[2:].split(": ", 1) for linea in lineas if linea.startswith("- "))
        if (clave(campos["Categoría"]), clave(campos["Subcategoría"])) in pares:
            fichas.append({"id": ident, "nombre": nombre, "fuente": archivo.name, **campos})
    return fichas


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
