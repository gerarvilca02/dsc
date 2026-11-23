# Banco LLM | Copiloto de campañas para Marketing

Proyecto Integrador · Laboratorio 3 · Grupo 1

Banco LLM es el banco ficticio en el que se desarrolla este proyecto. Su equipo de Marketing utiliza un copiloto para preparar correos promocionales personalizados a partir de las campañas del banco y las preferencias de cada cliente.

El flujo comienza cuando una persona de Marketing ingresa el identificador interno de un cliente (`client_id`) y una fecha. El agente consulta el perfil, busca promociones vigentes y prepara tres alternativas de correo. Marketing elige una, revisa el texto y decide si guarda un borrador o aprueba su entrega en una bandeja de prueba. Los clientes, comercios, campañas y documentos del laboratorio son sintéticos.

## Flujo del sistema

### 1. Marketing inicia una solicitud

El operador ingresa el `client_id` y la fecha para la que desea preparar la comunicación. El identificador permite consultar al cliente sin solicitar su DNI. La fecha determina qué catálogo mensual corresponde revisar y qué promociones están vigentes ese día.

El caso incluido en el notebook utiliza `CLI-1001` y el `22 de noviembre de 2026`.

### 2. El agente consulta el perfil del cliente

El agente invoca `consultar_perfil`. La API de perfiles devuelve el segmento, los productos, los permisos de contacto y personalización, y las tres categorías de mayor afinidad del cliente. Cada categoría contiene dos subcategorías que permiten precisar la búsqueda.

Por ejemplo, el perfil de demostración incluye la categoría `Viajes` y las subcategorías `Hoteles` y `Vuelos internacionales`. Esta distinción permite buscar promociones específicas para esos intereses. Antes de preparar el correo, el sistema comprueba que el perfil autorice el contacto por correo y la personalización del texto.

### 3. El agente identifica las campañas elegibles

Con las afinidades recuperadas, el agente invoca `consultar_campanas`. Envía el mes, el año y las categorías con sus subcategorías. La API devuelve las fichas comerciales coincidentes y el sistema comprueba la vigencia, la edad, los productos y el segmento del cliente.

En el caso de demostración, la búsqueda de `Viajes / Hoteles` en noviembre recupera la campaña `LLM-33` de Posada Demo Lumbre. Su ficha aporta el comercio, el beneficio, las fechas y las restricciones que deben aparecer en el correo. Si ninguna campaña cumple las condiciones del encargo, el flujo informa que no hay una promoción elegible.

### 4. El agente consulta el manual y redacta tres correos

Una vez identificadas las campañas, el agente invoca `buscar_directrices` para recuperar las reglas de comunicación de Banco LLM. El RAG consulta el manual institucional y devuelve los fragmentos pertinentes con su identificador y archivo de origen.

El agente prepara tres alternativas de correo. Cada una contiene un asunto, un saludo, una apertura, el beneficio, las condiciones y un llamado a la acción. Las alternativas pueden presentar distintos enfoques para una misma campaña. Los términos comerciales se incorporan desde la ficha seleccionada para conservar los importes, topes y fechas publicados.

### 5. Marketing selecciona una propuesta y se genera el prompt visual

El operador revisa los tres correos, elige una alternativa y puede editar el asunto, la apertura y el llamado a la acción. Después de esa selección, el agente consulta la guía de dirección visual y redacta un prompt de imagen coherente con la campaña y con la versión elegida del correo.

Por ejemplo, para una promoción de alojamiento, el prompt puede describir la llegada al vestíbulo de un hotel. Así, la escena representa el servicio ofrecido. Si el perfil permite personalización visual, el agente puede incorporar los atributos autorizados. En caso contrario, describe el producto o el ambiente. El resultado de esta etapa es el prompt textual.

### 6. Marketing guarda el borrador o aprueba la entrega

La decisión final corresponde al operador. El notebook permite dos resultados:

| Decisión | Resultado |
|---|---|
| `APROBAR_ENVIO = False` | Guarda el correo seleccionado y su prompt visual en `resultados/borradores/<client_id>/`. |
| `APROBAR_ENVIO = True` | Vuelve a consultar los permisos del cliente y, si continúan vigentes, registra el correo en `resultados/bandeja/<client_id>/`. |

Ambos resultados se guardan como archivos JSON. La bandeja es local y simula la entrega para el laboratorio.

## Herramientas y fuentes de información

| Herramienta | Fuente | Pregunta que resuelve |
|---|---|---|
| `consultar_perfil` | API local de perfiles, puerto `8001` | ¿Qué intereses tiene este cliente y qué personalización autoriza? |
| `consultar_campanas` | API local de campañas, puerto `8002` | ¿Qué promociones del periodo coinciden con sus afinidades y qué condiciones establece cada ficha? |
| `buscar_directrices` | Manual de comunicación y guía visual indexados en ChromaDB | ¿Cómo debe redactarse el correo o describirse la imagen según las normas de Banco LLM? |

El agente utiliza Microsoft Agent Framework y el deployment `gpt-5.6-luna` de Azure AI Foundry. Para el RAG, el notebook divide el manual por normas y la guía visual por secciones. Genera los embeddings con `text-embedding-3-small` y almacena los vectores, textos y metadatos en ChromaDB. La recuperación utiliza similitud coseno y admite filtros por categoría documental: `comunicacion` o `visual`.

## Archivos del proyecto

| Archivo o carpeta | Contenido |
|---|---|
| `Banco_LLM_LAB3_GRUPO1.ipynb` | Construcción del RAG, configuración del agente, pruebas y flujo completo de Marketing. |
| `api_perfiles.py` | API que consulta un perfil por `client_id`. |
| `api_campanas.py` | API que busca promociones en el catálogo mensual. |
| `datos/perfiles/` | 24 perfiles sintéticos en JSON. |
| `datos/campanas/` | 12 catálogos mensuales de campañas. |
| `conocimiento/` | Manual de comunicación en PDF y guía visual en Markdown. |
| `instrucciones_agente.md` | Rol, alcance, restricciones y formato de respuesta del agente. |
| `requirements.txt` | Dependencias del notebook y de las dos APIs. |

## Ejecución en VS Code

### 1. Crear el entorno e instalar las dependencias

Abre la carpeta del proyecto en VS Code. Desde PowerShell, ejecuta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Configurar Azure AI Foundry

Coloca el archivo `env` o `.env` junto al notebook y configura los valores del recurso:

```dotenv
FOUNDRY_MODEL_ENDPOINT=https://TU-RECURSO.openai.azure.com/openai/v1/
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.6-luna
FOUNDRY_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

Inicia sesión con una cuenta que tenga acceso a ambos deployments:

```powershell
az login
```

### 3. Levantar las dos APIs

Abre dos terminales en la carpeta del proyecto y mantén ambas en ejecución.

Terminal 1, perfiles:

```powershell
.\.venv\Scripts\Activate.ps1
python api_perfiles.py
```

Terminal 2, campañas:

```powershell
.\.venv\Scripts\Activate.ps1
python api_campanas.py
```

### 4. Ejecutar el notebook

Abre `Banco_LLM_LAB3_GRUPO1.ipynb`, selecciona `.venv` como kernel y ejecuta las celdas en orden. En la sección 5 se muestran las herramientas invocadas y los tres correos generados. En la sección 6 puedes modificar `ALTERNATIVA` para elegir el correo y `APROBAR_ENVIO` para decidir su destino.

## Validación del laboratorio

Las pruebas cubren cada herramienta por separado, cada herramienta invocada por el agente y el uso conjunto de las tres en el flujo completo. La evaluación documental incluye una pregunta directa, una reformulada, una sobre otro fragmento, una con filtro y una cuya respuesta está ausente del corpus.

En la ejecución presentada se verificaron las dos APIs, la indexación, la recuperación directa y el flujo completo con el agente. En las cuatro consultas documentales con respuesta disponible se recuperó el fragmento esperado, aunque las respuestas cumplieron parcialmente los criterios de contenido o citación. La prueba aislada del agente con `buscar_directrices` quedó marcada para revisión. Ante la pregunta sin respaldo documental, el agente reconoció que la información era insuficiente.
