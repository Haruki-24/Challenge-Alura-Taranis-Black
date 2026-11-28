# Dashboard Interactivo — Taranis Black (Finanzas)

Dashboard en Streamlit que consume `Taranis_Black_Modelo_Gerencial.xlsx` (pestañas consolidadas) y presenta KPIs, gráficos y tablas con filtros.

## Ejecución local

```bash
cd docs_agente/dashboard
streamlit run app.py
```

## Fuente de datos

- `docs_challenge/entregables/Taranis_Black_Modelo_Gerencial.xlsx`

## Filtros

- Trimestre (T1–T4)
- Línea de producto
- Canal (B2B / D2C)

## Contenido

- KPIs consolidados (ingresos, EBITDA, lucro líquido, fletes %, inadimplencia %)
- Ingresos presupuesto vs. real por trimestre
- EBITDA por trimestre
- Ingresos y margen por línea de producto
- OPEX por categoría
- Métricas operativas y SLA
- Calidad de datos (DQ) — resumen
"