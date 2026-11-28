# Herramientas IA — Automatización de Flujo (Taranis Black)

Carpeta con la documentación y herramientas propuestas para automatizar el flujo B2B de Taranis Black con n8n, RAG, triaje y estandarización de email.

## Archivos

- `01_arquitectura_y_factibilidad.md` — Arquitectura y factibilidad local vs. cloud.
- `02_agente_rag.md` — Agente RAG (base de conocimiento, prompt, guardrails, integración n8n).
- `03_triaje_y_estandarizacion_email.md` — Triaje (clasificación/priorización) y estandarización de email (campos, validaciones R1–R9, plantilla de salida).
- `04_flujo_n8n.md` — Workflows n8n (ingesta, triaje, RAG, excepciones) y configuración local.
- `05_simulador_streamlit.py` — Simulador en Streamlit que ejecuta triaje y estandarización localmente.
- `workflows/` — Plantillas JSON de workflows n8n exportables.

## Ejecución del simulador

```bash
cd docs_agente/herramientas_ia
streamlit run 05_simulador_streamlit.py
```

## Workflows n8n

Importar los JSON de `workflows/` en n8n (Workflows → Import from File).

## Fuente de datos

- `docs_challenge/entregables/Taranis_Black_Modelo_Gerencial.xlsx`
- `docs_challenge/taranis_black/05_Finanzas_Presupuesto_vs_Real.xlsx`
- `docs_challenge/taranis_black/06_Descripcion_del_proceso_operativo_SIPOC.pdf`
- `docs_challenge/taranis_black/01_Catalogo_de_productos_y_precios_Taranis_Black.pdf`
"