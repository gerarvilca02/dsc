# Banco LLM | Laboratorio 2. Construcción del agente

El copiloto de Banco LLM ayuda al equipo de Marketing a consultar las 12 campañas del catálogo sintético de 2026 y a redactar correos promocionales respetando los beneficios, las vigencias y las condiciones de cada oferta. El laboratorio utiliza Microsoft Agent Framework para evaluar el alcance del agente, la memoria de corto plazo y la compactación del historial.

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `Banco_LLM_LAB2_GRUPO1.ipynb` | Notebook principal con la construcción del agente, las pruebas, las respuestas a las tres preguntas del laboratorio y el checkpoint final. |
| `instrucciones_agente.md` | System prompt con el rol, el objetivo, el contexto, las restricciones, el formato de salida y los ejemplos. |
| `catalogo_campanas.md` | Catálogo de campañas con comercios, beneficios, vigencias, montos mínimos y topes. |
| `notas_laboratorio.md` | Justificación de las técnicas de prompting, el tamaño de la memoria y la estrategia de compactación. |
| `requirements.txt` | Dependencias para ejecutar el notebook. |
| `env` o `.env` | Configuración del despliegue de Azure AI Foundry. |

## Ejecución en VS Code

Abre la carpeta del proyecto en VS Code. Para ejecutar el laboratorio completo necesitas Python 3.12, las extensiones **Python** y **Jupyter**, Azure CLI y una cuenta con acceso al modelo desplegado.

### 1. Crear y activar el entorno virtual

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS o Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar las dependencias

Con el entorno virtual activo, ejecuta desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
```

### 3. Configurar el acceso a Foundry

Coloca el archivo `env` o `.env` junto al notebook. Debe contener el endpoint del recurso y el nombre exacto del despliegue:

```dotenv
FOUNDRY_MODEL_ENDPOINT=https://<recurso>.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=<nombre-del-despliegue>
```

Inicia sesión con la cuenta que tiene acceso al modelo:

```bash
az login
```

### 4. Ejecutar el notebook

Abre `Banco_LLM_LAB2_GRUPO1.ipynb`, selecciona `.venv` como kernel y pulsa **Ejecutar todo**. La primera celda de código carga `instrucciones_agente.md` y `catalogo_campanas.md`, por lo que ambos archivos deben estar en la misma carpeta que el notebook.

## Pruebas del laboratorio

| Prueba | Comportamiento evaluado |
|---|---|
| Alcance del agente | Recomienda campañas, redacta correos, solicita datos faltantes, rechaza consultas ajenas e identifica las que corresponden a otra especialidad bancaria. |
| Fidelidad al catálogo | Conserva el beneficio autorizado, incluso cuando el usuario le pide anunciar un descuento mayor. |
| Memoria de corto plazo | Recupera el `client_id`, el mes, el canal y el tono indicados en turnos anteriores de una misma sesión. |
| Compactación del historial | Aplica `SlidingWindowStrategy` y comprueba qué datos siguen disponibles al superar el tamaño de la ventana. |

La configuración final conserva **8 interacciones completas**, equivalentes a 16 mensajes entre usuario y agente. La prueba de compactación utiliza una ventana de **2 interacciones** para observar cómo el alias inicial sale del historial mientras el canal y la firma siguen disponibles.
