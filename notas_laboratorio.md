# Banco LLM | Notas del Laboratorio 2

## Archivos y entorno

| Archivo | Uso |
|---|---|
| `Banco_LLM_LAB2_GRUPO1.ipynb` | Construcción del agente y ejecución de pruebas |
| `instrucciones_agente.md` | Rol, objetivo, restricciones, formato y ejemplos del agente |
| `catalogo_campanas.md` | Doce promociones sintéticas de 2026 y sus condiciones comunes |
| `env` o `.env` | Configuración del despliegue de Foundry |
| `notas_laboratorio.md` | Documento de consulta para la presentación |

Los dos documentos que lee el agente y el archivo de entorno van en la misma carpeta que el notebook. El archivo de entorno contiene `FOUNDRY_MODEL_ENDPOINT` y `FOUNDRY_MODEL_DEPLOYMENT`. Azure CLI aporta la identidad mediante `az login`.

Con Python 3.11 o 3.12 y Jupyter, instala las dependencias en el kernel seleccionado.

```python
%pip install agent-framework-core==1.22.0 agent-framework-openai==1.17.0 azure-identity python-dotenv pandas
```

## Decisiones del equipo

### ¿Qué técnicas de prompting utiliza el agente y por qué?

El rol define la especialidad de Marketing. Los ejemplos *few-shot* muestran cuándo pedir aclaraciones, rechazar un tema ajeno o indicar qué área bancaria debe atender la consulta. El agente toma los beneficios, las fechas y los topes del catálogo. La etiqueta de la primera línea permite comprobar la decisión de alcance independientemente de la redacción del correo.

### ¿Cuántas interacciones conserva la memoria de corto plazo?

Ocho interacciones completas, equivalentes a dieciséis mensajes de usuario y asistente. Cuatro turnos cubren un encargo típico, desde identificar al cliente y definir el mes y la categoría hasta seleccionar la campaña y redactar el correo. Los cuatro siguientes permiten revisar el asunto, el tono, las condiciones y la versión final.

### ¿Qué estrategia de compactación utiliza y por qué?

Al cerrar cada turno, `SlidingWindowStrategy` conserva los dieciséis mensajes más recientes. Las últimas revisiones mantienen su redacción exacta, incluidos los códigos de campaña y los topes. Si un dato del encargo sale de la ventana, el agente lo solicita de nuevo. El catálogo y las reglas siguen disponibles porque forman parte de las instrucciones.

## Evidencia para la presentación

Las consultas de alcance usan sesiones independientes. La prueba de memoria usa una misma sesión para recuperar el identificador de cliente, el mes, el canal y el tono. La prueba local de compactación utiliza una ventana de dos interacciones y un cliente con respuesta fija para inspeccionar los mensajes que llegan al cuarto turno. Las pruebas con Foundry muestran la respuesta del modelo y su evaluación en el checkpoint final.
