# Flujo n8n — Orquestación de la Automatización

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Carpeta:** `docs_agente/herramientas_ia/`  
**Fecha:** 2026-11-27

---

## 1. Objetivo

Diseñar los workflows de n8n que orquestan el flujo completo:
1. Ingesta de correo/propuesta.
2. Triaje (clasificación y priorización).
3. Estandarización de email (extracción y validación).
4. Consulta al agente RAG (dictamen de crédito).
5. Generación de respuesta estandarizada.
6. Registro en Staging/Excepciones y notificación.

## 2. Workflows propuestos

### WF-01: Ingesta de Email

**Trigger:** IMAP (monitorea `financiero@taranisblack.com.br`) o Webhook (simulador).

**Nodos:**
1. **IMAP Trigger** — descarga correos no leídos.
2. **Extract Text** — extrae texto del cuerpo y adjuntos PDF (OCR si es necesario).
3. **HTTP Request (RAG)** — envía el texto al agente RAG para clasificación inicial.
4. **IF** — si es propuesta válida → WF-02; si es consulta → respuesta automática; si es spam → archivar.

### WF-02: Triaje y Estandarización

**Trigger:** Llamado desde WF-01.

**Nodos:**
1. **LLM (OpenAI/Anthropic)** — extrae campos JSON de la propuesta (prompt de extracción).
2. **Code (Python/JS)** — valida R1-R9, clasifica prioridad y tipo.
3. **IF (válido?)** — si válido → WF-03; si inválido → WF-04 (excepción).
4. **Set** — prepara el payload para el correo estandarizado.

### WF-03: Consulta RAG y Generación de Respuesta

**Trigger:** Llamado desde WF-02 (si válido).

**Nodos:**
1. **HTTP Request (RAG)** — envía datos del cliente al agente RAG para dictamen.
2. **LLM** — genera el correo estandarizado con el resumen del RAG.
3. **Email (SMTP)** — envía el correo estandarizado al asistente financiero.
4. **HTTP Request (Staging)** — registra la propuesta en Staging (Excel/DB).

### WF-04: Gestión de Excepciones

**Trigger:** Llamado desde WF-02 (si inválido).

**Nodos:**
1. **Set** — prepara el mensaje de excepción con los campos faltantes.
2. **Email (SMTP)** — notifica al vendedor con la lista de campos faltantes.
3. **HTTP Request (Excepciones)** — registra la excepción en la tabla de Excepciones.

## 3. Diagrama de flujo (n8n)

```
[IMAP/Webhook] → [Extract Text] → [LLM: extraer campos] → [Code: validar R1-R9]
                                                              │
                                                              ├─ válido ──▶ [HTTP: RAG] → [LLM: correo estandar.] → [Email] → [HTTP: Staging]
                                                              │
                                                              └─ inválido ──▶ [Email: notificar vendedor] → [HTTP: Exceções]
```

## 4. Configuración de n8n (local)

### Instalación (Docker)

```bash
docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

### Instalación (npm)

```bash
npm install -g n8n
n8n start
```

### Variables de entorno

| Variable | Descripción |
|---|---|
| `OPENAI_API_KEY` | API key de OpenAI (para LLM y embeddings) |
| `ANTHROPIC_API_KEY` | API key de Anthropic (alternativa) |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` | Configuración de email |
| `IMAP_HOST`, `IMAP_PORT`, `IMAP_USER`, `IMAP_PASS` | Configuración de buzón |
| `RAG_ENDPOINT` | URL del servicio RAG |
| `STAGING_WEBHOOK` | URL del webhook de Staging |

## 5. Plantillas de workflows (JSON)

Las plantillas de workflows n8n se encuentran en la subcarpeta `workflows/`:
- `wf_01_ingesta_email.json` — Ingesta de correo/propuesta.
- `wf_02_triaje_estandarizacion.json` — Triaje y estandarización.
- `wf_03_rag_respuesta.json` — Consulta RAG y generación de respuesta.
- `wf_04_excepciones.json` — Gestión de excepciones.

Para importar: en n8n, ir a "Workflows" → "Import from File" → seleccionar el JSON.

## 6. Modo demo (sin n8n)

El simulador en Streamlit (`05_simulador_streamlit.py`) permite probar el flujo completo sin n8n:
- El usuario pega el texto de una propuesta.
- El simulador ejecuta clasificación, extracción y validación localmente (reglas R1-R9).
- Muestra el correo estandarizado generado y las excepciones detectadas.
- Opcionalmente, envía el payload a un webhook de n8n real (modo integrado).

## 7. Implementación sugerida

1. Instalar n8n localmente (Docker o npm).
2. Importar los workflows JSON en n8n.
3. Configurar las variables de entorno (API keys, SMTP, IMAP).
4. Indexar la base de conocimiento en el vector DB.
5. Implementar el servicio RAG (FastAPI + Chroma + OpenAI).
6. Probar con el simulador en modo demo y en modo integrado.
7. Validar con propuestas completas e incompletas.
8. Documentar los resultados y capturas para la tabla de evidencias.
"