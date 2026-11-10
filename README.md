# Laboratorio Banco LLM

Entrega breve: un notebook, catálogo de campañas de 2 páginas, factura ficticia de 1 página y JSON de 20 clientes. Toda la data es sintética, incluidos comercios y productos.

## Ejecutar en VS Code

1. Abre esta carpeta. Instala las extensiones Python y Jupyter, Python 3.11/3.12 y Azure CLI.
2. En la terminal:

```bash
python -m venv .venv
```

3. Activa el entorno:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Instala las dependencias y autentícate:

```bash
python -m pip install -r requirements.txt
az login
```

5. Copia `.env.example` a `.env` y completa `DOCUMENT_INTELLIGENCE_ENDPOINT`, `CONTENT_SAFETY_ENDPOINT` y un `BLOCKLIST_NAME` exclusivo de tu equipo. No se utilizan API keys ni secretos. La identidad de Azure CLI debe tener permisos de datos en ambos recursos y permisos para administrar blocklists. Usa subdominios personalizados compatibles con Entra ID; ante 403, revisa RBAC y el tenant.
6. Abre `Banco_LLM_Document_Intelligence_Content_Safety.ipynb`, selecciona `.venv` como kernel y ejecuta las celdas en orden.
7. Si los términos recién registrados no coinciden todavía, espera hasta cinco minutos, repite C.5 y el checkpoint. Revisa los resultados y guarda el notebook con las salidas.

## Resultado

El notebook guarda en `resultados/<ejecucion>/` las respuestas originales de Azure, las pruebas de moderación, la blocklist, el JSON `campanas_para_ai_search.json`, el checkpoint y una reflexión basada en esa ejecución. El catálogo se transforma en dos documentos, uno por página; aún no se sube a AI Search.

Las celdas cloud se entregan sin ejecutar. No se incluyen evidencias simuladas como si provinieran de Azure. Se comprobó localmente la estructura del notebook, la sintaxis del código y los documentos sintéticos.

Para la entrega académica, conserva los datos y resultados de tu ejecución, guarda el notebook y presenta tu propio PR. La aprobación del instructor debe corresponder al SHA actual; no sustituye la evidencia de ejecución.
