# Banco LLM | Copiloto de campañas para Marketing

Proyecto Integrador · Laboratorio 3 · Grupo 1

Banco LLM es un asistente que ayuda al equipo de Marketing a preparar correos promocionales personalizados. A partir del identificador interno de un cliente (`client_id`) y una fecha de campaña, el agente consulta sus preferencias, identifica promociones vigentes para las que es elegible y redacta tres alternativas de correo. Marketing elige una propuesta, puede editarla y decide si la guarda como borrador o aprueba su entrega en una bandeja de prueba.

El proyecto utiliza datos sintéticos. La operación se realiza desde un notebook de Jupyter, con dos APIs locales y un agente construido con Microsoft Agent Framework.

## Cómo funciona el sistema

1. **Consulta del perfil.** El agente recibe el `client_id` y consulta la API de perfiles. Recupera los permisos de contacto y personalización, los productos del cliente, su segmento y sus tres categorías principales de afinidad, con dos subcategorías por cada una.
2. **Selección de campañas.** El agente consulta la API de campañas con el mes, el año y las afinidades recuperadas. El sistema comprueba la vigencia de cada promoción y sus requisitos de edad, producto y segmento.
3. **Redacción de propuestas.** El agente consulta el manual de comunicación mediante RAG y redacta tres alternativas. El asunto, la apertura y el llamado a la acción pueden variar. El comercio, el beneficio, la vigencia y las condiciones se incorporan desde la ficha comercial.
4. **Selección y edición.** Marketing revisa las propuestas en el notebook, elige una y puede ajustar el texto. Con la versión elegida, el agente consulta la guía visual y genera un prompt que describe la imagen sugerida para el correo. La salida de esta etapa es una descripción textual.
5. **Borrador o entrega.** Por defecto, el notebook guarda la propuesta seleccionada y su prompt visual como borrador. Si Marketing aprueba la entrega, el sistema vuelve a consultar los permisos del cliente y registra el correo en una bandeja local sintética.

## Herramientas del agente

| Herramienta | Fuente | Función |
|---|---|---|
| `consultar_perfil` | API de perfiles, puerto `8001` | Recupera el perfil comercial autorizado y las afinidades del cliente a partir de su `client_id`. |
| `consultar_campanas` | API de campañas, puerto `8002` | Busca promociones por periodo, categoría y subcategoría. Devuelve las fichas con sus beneficios y condiciones. |
| `buscar_directrices` | ChromaDB local | Recupera fragmentos del manual de comunicación o de la guía visual para sustentar la redacción. |

El agente utiliza `gpt-5.6-luna` en Azure AI Foundry. El RAG divide los documentos por estructura: cada norma del manual y cada sección de la guía visual forman un fragmento. Microsoft Agent Framework genera los embeddings con `text-embedding-3-small`. ChromaDB almacena el texto, el vector y los metadatos de cada fragmento. La búsqueda utiliza distancia coseno y admite filtros por categoría documental (`comunicacion` o `visual`).

## Archivos del proyecto

| Archivo o carpeta | Contenido |
|---|---|
| `Banco_LLM_LAB3_GRUPO1.ipynb` | Construcción del índice, configuración del agente, pruebas y flujo de Marketing. |
| `api_perfiles.py` | API que consulta los perfiles sintéticos por `client_id`. |
| `api_campanas.py` | API que consulta el catálogo mensual de campañas. |
| `datos/perfiles/` | 24 perfiles sintéticos en JSON. |
| `datos/campanas/` | 12 catálogos mensuales de campañas en Markdown. |
| `conocimiento/` | Manual de comunicación en PDF y guía de dirección visual en Markdown. |
| `instrucciones_agente.md` | Rol, alcance, restricciones y formato de respuesta del agente. |
| `requirements.txt` | Dependencias del notebook y de las dos APIs. |

## Ejecución en VS Code

Se requiere Python 3.12, Azure CLI y las extensiones Python y Jupyter de VS Code. Coloca el notebook y `requirements.txt` en la misma carpeta que los dos scripts de las APIs. Ejecuta los comandos desde esa carpeta.

### 1. Crear el entorno e instalar las dependencias

En PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Configurar Azure AI Foundry

Crea un archivo `.env` junto al notebook o utiliza el archivo `env` del laboratorio. Configura el endpoint de tu recurso y los nombres de los deployments:

```dotenv
FOUNDRY_MODEL_ENDPOINT=https://TU-RECURSO.openai.azure.com/openai/v1/
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.6-luna
FOUNDRY_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

Inicia sesión con una cuenta que tenga acceso a ambos deployments. El notebook utiliza `DefaultAzureCredential` para autenticarse.

```powershell
az login
```

### 3. Iniciar las APIs en terminales separadas

Terminal 1, API de perfiles:

```powershell
.\.venv\Scripts\Activate.ps1
python api_perfiles.py
```

Terminal 2, API de campañas:

```powershell
.\.venv\Scripts\Activate.ps1
python api_campanas.py
```

Mantén ambas terminales abiertas mientras utilizas el notebook. Puedes comprobar el servicio de perfiles en `http://127.0.0.1:8001/perfiles/CLI-1001` y probar la API de campañas en `http://127.0.0.1:8002/docs`.

### 4. Ejecutar el notebook

Abre `Banco_LLM_LAB3_GRUPO1.ipynb`, selecciona `.venv` como kernel y ejecuta las celdas en orden. El caso de demostración utiliza el cliente `CLI-1001` y la fecha `2026-11-22`.

En la sección 6, `ALTERNATIVA` permite elegir uno de los tres correos. Con `APROBAR_ENVIO = False`, el resultado se guarda en `resultados/borradores/`. Con `APROBAR_ENVIO = True`, la entrega aprobada queda registrada en `resultados/bandeja/`. Ambos directorios se organizan por cliente.

## Pruebas y resultados

El notebook prueba primero cada herramienta de forma independiente, luego registra una sola herramienta por agente y finalmente ejecuta el flujo con las tres herramientas habilitadas. La evaluación documental incluye cinco casos: pregunta directa, pregunta reformulada, consulta sobre otro fragmento, búsqueda con filtro y pregunta sin respuesta en los documentos.

En la ejecución del laboratorio se verificaron las dos APIs, el índice, la recuperación directa y el flujo completo con las tres herramientas. En los cuatro casos documentales con respuesta disponible, el RAG recuperó el fragmento esperado y la evaluación de la respuesta fue parcial. La prueba aislada del agente con `buscar_directrices` quedó marcada para revisión. En el caso sin información disponible, el agente reconoció la falta de evidencia.

La sección 7 muestra las respuestas, los fragmentos recuperados y la justificación de cada evaluación. La sección 8 presenta la tabla de herramientas y la evaluación de `Agent as a Tool`. La sección 9 reúne los resultados de la ejecución.
