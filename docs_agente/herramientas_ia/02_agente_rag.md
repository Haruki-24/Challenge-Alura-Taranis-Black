# Agente RAG — Consulta de Políticas y Estandarización de Respuestas

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Carpeta:** `docs_agente/herramientas_ia/`  
**Fecha:** 2026-11-27

---

## 1. Objetivo

Implementar un agente de IA basado en RAG (Retrieval-Augmented Generation) que:
- Consulte políticas internas de crédito, catálogo de productos y procedimientos operativos.
- Clasifique y priorice solicitudes de crédito.
- Genere respuestas estandarizadas sobre plantilla para el aprobador (Gerente Financiero).
- Reduzca el tiempo de análisis de ~40 min a ≤5 min (automatizado).

## 2. Base de conocimiento (documentos a indexar)

| Documento | Contenido | Uso en RAG |
|---|---|---|
| `06_Descripcion_del_proceso_operativo_SIPOC.pdf` | Proceso AS-IS, SIPOC, causas 6M | Consulta de procedimientos y reglas de flete CIF/FOB |
| `01_Catalogo_de_productos_y_precios_Taranis_Black.pdf` | Líneas de producto, precios, NR-17, garantía, flete | Validación de códigos de producto y condiciones comerciales |
| `05_Finanzas_Presupuesto_vs_Real.xlsx` (texto) | Métricas operativas, cuellos de botella | Consulta de SLA y costos de impacto |
| Matriz de alzada (TO-BE) | Umbrales de auto-aprobación | Reglas de decisión de crédito |
| Políticas de gobernanza (04) | Política de IA, LFPDPPP/LGPD | Guardrails y cumplimiento |
| Reglas R1–R9 (05) | Validaciones de carga | Validación de datos de entrada |

## 3. Arquitectura del agente RAG

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Consulta    │     │  Retriever   │     │  LLM (cloud)     │
│  (pregunta / │────▶│  (vector DB) │────▶│  (GPT-4o-mini /  │
│   contexto)  │     │  top-k docs  │     │   Claude Haiku)  │
└──────────────┘     └──────────────┘     └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  Respuesta       │
                                          │  estructurada    │
                                          │  (JSON/plantilla)│
                                          └──────────────────┘
```

### Flujo

1. **Ingesta:** los documentos se dividen en chunks (500-1000 tokens) y se generan embeddings (OpenAI `text-embedding-3-small`).
2. **Almacenamiento:** los embeddings se guardan en el vector DB (Chroma local o Pinecone cloud).
3. **Consulta:** el usuario (o n8n) envía una pregunta/contexto.
4. **Retrieval:** se recuperan los top-5 documentos más relevantes.
5. **Generación:** el LLM genera una respuesta estructurada usando el contexto recuperado y el prompt del sistema.
6. **Salida:** JSON con dictamen, resumen, prioridad y campos validados.

## 4. Prompt del sistema (plantilla)

```
Eres un asistente de crédito de Taranis Black. Tu tarea es analizar una solicitud de crédito B2B
y generar un dictamen estructurado.

Contexto recuperado (políticas, catálogo, procedimientos):
{contexto}

Solicitud del cliente:
{datos_cliente}

Instrucciones:
1. Clasifica la solicitud: auto-aprobable, requiere alzada, o requiere escalamiento.
2. Aplica la matriz de alzada: auto si monto <= USD 10.000, score >= 700, sin inadimplencia, historial >= 2 pedidos.
3. Genera un resumen para el aprobador con: empresa, monto, condición, score, historial, recomendación.
4. Si hay datos faltantes o inconsistencias, indica cuáles y solicita aclaración.
5. Responde SOLO en JSON con los campos: clasificacion, recomendacion, resumen, campos_faltantes, prioridad.
```

## 5. Guardrails (seguridad y cumplimiento)

- **No tomar decisiones de crédito de alto riesgo sin supervisión humana.**
- **No usar datos personales fuera de la finalidad declarada (LFPDPPP/LGPD).**
- **Siempre indicar cuando la información proviene de documentos indexados vs. datos de la solicitud.**
- **Registrar todas las consultas y respuestas para auditoría.**
- **Limitar el tamaño del contexto para evitar costos excesivos.**

## 6. Integración con n8n

El agente RAG se expone como un **servicio HTTP** (FastAPI o Flask) que n8n llama mediante un nodo HTTP Request:

- **Endpoint:** `POST /rag/consultar`
- **Input:** `{ "consulta": "...", "datos_cliente": {...} }`
- **Output:** `{ "clasificacion": "...", "recomendacion": "...", "resumen": "...", "campos_faltantes": [...], "prioridad": "..." }`

n8n orquesta el flujo: recibe el correo → extrae campos → llama al RAG → genera respuesta estandarizada → envía al aprobador.

## 7. Métricas de éxito

| Métrica | Baseline | Meta |
|---|---|---|
| Tiempo de análisis de crédito | ~40 min | ≤ 5 min (automatizado) |
| % de solicitudes auto-clasificadas | 0% | ≥ 70% |
| Precisión de clasificación | No medido | ≥ 90% |
| % de respuestas con campos faltantes detectados | No medido | ≥ 95% |

## 8. Implementación sugerida

1. **Indexar** los documentos del kit (01, 05, 06) + políticas (04) + reglas R1-R9 + matriz de alzada.
2. **Crear el servicio** RAG con FastAPI + Chroma + OpenAI embeddings.
3. **Exponer el endpoint** y probar con el simulador de Streamlit.
4. **Integrar con n8n** mediante webhook.
5. **Validar** con casos de prueba (propuestas completas e incompletas).
"