# Herramientas IA — Arquitectura y Factibilidad (Taranis Black, Finanzas)

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Carpeta:** `docs_agente/herramientas_ia/`  
**Fecha:** 2026-11-27  
**Estado:** Borrador inicial.

---

## 1. Objetivo

Diseñar e implementar (o simular) un conjunto de herramientas de IA para automatizar el flujo B2B de Taranis Black:
- **Agente RAG** para consultar políticas de crédito y estandarizar respuestas.
- **Triaje** de correos/propuestas (clasificación y priorización).
- **Estandarización de email** (extracción de campos, validación R1–R9, respuesta sobre plantilla).

Estas herramientas se integran con **n8n** como orquestador y con el modelo de datos y reglas definidos en los documentos previos.

## 2. Arquitectura propuesta

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────────┐
│  Fuente de      │     │  n8n         │     │  Servicios IA       │
│  entrada        │────▶│  (webhook/   │────▶│  (LLM cloud API)    │
│  (correo /      │     │   IMAP)      │     │  + RAG (vector DB)  │
│  formulario /   │     │              │     │  + validaciones     │
│  simulador)     │     │              │     │                     │
└─────────────────┘     └──────┬───────┘     └──────────┬──────────┘
                               │                        │
                               ▼                        ▼
                        ┌──────────────┐     ┌─────────────────────┐
                        │  Staging /   │     │  Salida             │
                        │  Excepciones │     │  (correo estandar., │
                        │  (Excel/DB)  │     │   dictamen, NF)     │
                        └──────────────┘     └─────────────────────┘
```

### Componentes

| Componente | Rol | Tecnología |
|---|---|---|
| Orquestador | Flujos, webhooks, IMAP, llamadas a APIs | n8n (self-hosted o cloud) |
| LLM | Clasificación, extracción, RAG, redacción | API cloud (OpenAI / Anthropic) |
| Base de conocimiento | Políticas de crédito, catálogo, procedimientos | Vector DB (Pinecone / Qdrant / Chroma) |
| Validaciones | R1–R9 (CNPJ, IE, códigos, completitud) | n8n Code node / Python |
| Almacenamiento | Staging, excepciones, DQ | Excel (modelo) o base de datos |
| Presentación | Dashboard y simulador | Streamlit |

## 3. Factibilidad local vs. cloud

### 3.1 n8n (orquestador)

- **Local:** posible via Docker (`docker run -it --rm -p 5678:5678 n8nio/n8n`) o npm (`npx n8n`). Requiere Node.js.
- **Cloud:** n8n Cloud (plan gratuito limitado) o instancia en Render/Railway.
- **Recomendación:** local para desarrollo y pruebas; cloud para demo compartible (enlace público para la tabla de evidencias).

### 3.2 LLM (APIs cloud)

- **OpenAI (GPT-4o-mini)** o **Anthropic (Claude Haiku)**: bajo costo, buena calidad para clasificación/extracción.
- **Autenticación:** API key en variables de entorno de n8n (nunca hardcodeada).
- **Costo estimado:** < USD 5/mes para el volumen del challenge (180-220 pedidos/mes).

### 3.3 Base de conocimiento (RAG)

- **Opción local:** Chroma (Python) o Qdrant (Docker) con embeddings de OpenAI.
- **Opción cloud:** Pinecone (plan gratuito) o Supabase (pgvector).
- **Contenido a indexar:** políticas de crédito, catálogo de productos (01), procedimientos (06), reglas R1-R9, matriz de alzada.

### 3.4 Simulación de entrada de correo

Como el proyecto es ficticio y no tenemos acceso a un buzón real, se propone:
- **Simulador en Streamlit** que recibe texto de correo/propuesta y envía un webhook a n8n (o procesa localmente con Python).
- **Modo demo:** el simulador ejecuta triaje + estandarización + RAG localmente (sin n8n) para mostrar el flujo completo.
- **Modo integrado:** el simulador envía el payload a un webhook de n8n real, que orquesta el flujo completo.

## 4. Viabilidad de implementación local

| Componente | Viabilidad local | Requisitos | Notas |
|---|---|---|---|
| n8n | Alta | Docker o Node.js 18+ | Fácil de instalar |
| LLM (APIs cloud) | Alta (requiere internet) | API key | Costo bajo |
| LLM (Ollama local) | Media | GPU/RAM suficiente (8GB+ VRAM) | Opcional; no recomendado para este challenge |
| Vector DB (Chroma) | Alta | Python + pip | Fácil, embebido |
| Vector DB (Qdrant) | Media | Docker | Más robusto |
| Simulador Streamlit | Alta | Python + Streamlit | Ya instalado |
| Email real (IMAP) | Baja (ficticio) | Credenciales de buzón | Se simula con el simulador |

**Conclusión:** La implementación local es viable para desarrollo y demo. Para una demo compartible (tabla de evidencias), se recomienda desplegar n8n y el simulador en la nube (Streamlit Cloud + n8n Cloud o Render).

## 5. Seguridad y gobernanza

- **API keys:** almacenadas en variables de entorno de n8n, nunca en el código.
- **Datos personales:** minimización (CNPJ, IE, dirección); acceso por rol; logs auditables.
- **Human-in-the-Loop:** correos fuera de formato, discrepancias y consultas al buró requieren intervención humana.
- **Trazabilidad:** registro de prompts, reglas y decisiones (alineado con `historial_prompts.md`).

## 6. Próximos pasos

1. Instalar n8n localmente (Docker) y crear los workflows (ver `04_flujo_n8n.md`).
2. Indexar la base de conocimiento (políticas, catálogo, procedimientos) en el vector DB.
3. Implementar el simulador en Streamlit (`05_simulador_streamlit.py`).
4. Probar el flujo end-to-end en modo demo (sin n8n) y en modo integrado (con n8n).
5. Documentar los resultados y capturas para la tabla de evidencias.
"