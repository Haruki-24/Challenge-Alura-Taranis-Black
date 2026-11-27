# Historial de Prompts — Proyecto Taranis Black (Finanzas)

**Propósito:** registro acumulativo de interacciones/prompts aplicados durante el challenge, para respaldar la trazabilidad y el uso de un entorno propio (VS Code + OpenCode) frente a una sesión web genérica.  
**Convención de registro:** cada interacción se numera consecutivamente (`#000`, `#001`, …). Se distingue entre (a) Hecho/Evidencia en archivo, (b) Hallazgo/Cálculo verificado y (c) Recomendación o supuesto de diseño.  
**Herramienta base:** VS Code + OpenCode (SST). **Modelo declarado:** Beam Free (`opencode/beam-free`).

---

## Campos del registro

| Campo | Descripción |
|---|---|
| ID | Numeración consecutiva de la interacción |
| Fecha | Fecha y hora local de la interacción |
| Etapa | Fase del trabajo (configuración, análisis, redacción, etc.) |
| Herramienta / Modelo | Entorno y modelo utilizado |
| Prompt (resumen) | Resumen fiel del prompt aplicado |
| Cita clave | Fragmento representativo del prompt (cuando aporte evidencia) |
| Artefactos | Archivos creados/modificados |
| Estado | Completado / En curso / Pendiente |

---

## #000 — Preparación de entorno (pasos previos al primer prompt)

- **Fecha:** 2026-11-26 (entorno creado ~09:02, según metadatos del sistema de archivos).
- **Etapa:** Configuración de entorno.
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** No aplica (pasos previos de preparación del workspace realizados por el usuario antes de la primera interacción con el agente).
- **Hecho / Evidencia en archivo:**
  - Entorno virtual Python `.venv` creado en la raíz del proyecto (Python 3.13.2).
  - Paquetes instalados: `et_xmlfile 2.0.0`, `numpy 2.5.5`, `openpyxl 3.1.5`, `pandas 3.1.1`, `pip 26.3`, `pypdf 7.2.0`, `python-dateutil 4.0.0`, `tzdata 2026.6`.
  - Repositorio Git existente en la raíz, rama `main`, remoto `origin` → `https://github.com/Haruki-24/Challenge-Alura-Taranis-Black.git`, último commit `b30e436` ("Carga de archivos en repositorio principal").
  - Carpeta `docs_agente/` existente y vacía antes de esta interacción.
- **Artefactos:** `.venv/` (no versionado), estructura base del proyecto.
- **Estado:** Completado.

---

## #001 — Configuración de trazabilidad y declaración de entorno

- **Fecha:** 2026-11-26 22:01 (hora local).
- **Etapa:** Configuración de trazabilidad.
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** El usuario solicitó configurar la trazabilidad del proyecto y registrar la declaración de su entorno propio antes de iniciar el rol de Business Analyst consultor. Incluyó: revisar `AGENTS.md` y la estructura del workspace; hacer preguntas concretas si algo no estuviera claro u optimizable; presentar un Plan de Ruta breve para crear `docs_agente/historial_prompts.md` (y, si conveniente, `docs_agente/00_entorno_y_configuracion.md`) con la declaración de herramienta, modelo (`Beam Free`) y configuración, más el registro inicial de este primer prompt y los pasos previos del workspace; esperar aprobación antes de crear/modificar archivos.
- **Cita clave:** "Antes de comenzar a actuar como Business Analyst consultor para Taranis Black, vamos a configurar la trazabilidad del proyecto y dejar registrada la declaración de mi entorno propio."
- **Decisiones registradas (aprobadas por el usuario):**
  - Identificador de modelo asumido: `opencode/beam-free` (declarado, no verificado en archivos).
  - Incluir snapshot de Python (`pip list`) en la declaración de entorno.
  - Repositorio Git ya existente; se mantiene y se versionarán los archivos de `docs_agente/`.
  - Primer prompt registrado como resumen fiel + cita clave.
- **Artefactos:**
  - `docs_agente/00_entorno_y_configuracion.md` (creado).
  - `docs_agente/historial_prompts.md` (creado).
- **Estado:** Completado.

---

## #002 — Diagnóstico inicial de datos y flujo (etapa inicial de análisis)

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Análisis inicial de datos y flujo (Finanzas).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** El usuario solicitó pasar a la etapa inicial de análisis de datos y flujo para Taranis Black (Finanzas): consultar la guía oficial y el índice del kit; revisar `05_Finanzas_Presupuesto_vs_Real.xlsx` y `06_Descripcion_del_proceso_operativo_SIPOC.pdf`; estructurar contexto y desafíos de datos, control interno y procesos; definir flujo de trabajo por etapas; inspeccionar la estructura real de los archivos con `.venv` antes de conclusiones numéricas; presentar Plan de Ruta para `docs_agente/01_diagnostico_inicial_datos_y_flujo.md`; registrar este prompt; esperar aprobación antes de crear el documento.
- **Cita clave:** "En esta etapa inicial, quiero que: 1. Consultes ... 2. Estructures el contexto ... 3. Definas el flujo de trabajo por etapas ... 4. ... inspecciona la estructura real de los archivos usando el entorno `.venv` antes de sacar conclusiones numéricas".
- **Fuentes inspeccionadas (Hecho / Evidencia en archivo):**
  - `docs_challenge/Guia_oficial_informe_ES.pdf` (2 págs.): entrega oficial, etapas Ruta 0 (obligatorias) y vertical (Ruta 4: Etapa 1 obligatoria, Etapa 2 opcional), tabla de evidencias y permisos.
  - `docs_challenge/taranis_black/00_Indice_y_guia_del_kit_de_datos.md`: descripción de archivos y recomendaciones por ruta.
  - `docs_challenge/taranis_black/06_Descripcion_del_proceso_operativo_SIPOC.pdf` (3 págs.): macroproceso B2B (70% de ingresos, USD 33,6 M/año), 5 pasos AS-IS, SIPOC, causas raíz 6M.
  - `docs_challenge/taranis_black/05_Finanzas_Presupuesto_vs_Real.xlsx`: hojas `Resultados_trimestrales` (24x16), `Ingresos_por_producto` (6x8), `Cuellos_de_botella_y_costos` (6x6).
- **Artefactos:** `docs_agente/01_diagnostico_inicial_datos_y_flujo.md` (creado tras aprobación del Plan de Ruta).
- **Fuentes adicionales incorporadas:** `docs_challenge/entregables/Auditoria de proceso Taranis.docx` (diagnóstico AS-IS base), `05_Finanzas_Presupuesto_vs_Real.xlsx`, `06_Descripcion_del_proceso_operativo_SIPOC.pdf`, `Guia_oficial_informe_ES.pdf`.
- **Estado:** Completado.

---

## #003 — Revisión de documentación de soluciones (Informe Ruta 4 y Canvas IA) y plan TO-BE

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Diseño TO-BE / planificación de rediseño.
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** El usuario solicitó tomar el diagnóstico AS-IS como base para generar el documento de auditoría final; revisar `Informe_Ruta_4_finanzas_ES.docx` y `canvas_ai_tarantis_black.pdf` para evaluar las propuestas de solución con IA; y, tras revisar toda la documentación, presentar el plan TO-BE para comenzar a establecer el plan de ruta.
- **Fuentes revisadas (Hecho / Evidencia):**
  - `docs_challenge/Informe_Ruta_4_finanzas_ES.docx`: plantilla oficial con casos de uso de IA (Etapa 1 Ruta 0) y secciones de Etapa 2/3 y Ruta 4 (mayormente placeholders).
  - `docs_challenge/entregables/canvas_ai_tarantis_black.pdf`: AI Canvas con problema, solución sin/con IA, personas, datos, herramientas e indicadores.
- **Artefactos:** `docs_agente/02_plan_to_be.md` (creado tras aprobación del Plan de Ruta).
- **Estado:** Completado.

---

## #004 — Matriz de Esfuerzo × Impacto y métricas de éxito (Informe Ruta 4)

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Priorización y métricas (Ruta 0, Etapa 2).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** El usuario solicitó avanzar con la matriz de Esfuerzo × Impacto y las métricas de éxito correspondientes al `Informe_Ruta_4_finanzas_ES.docx`, a partir del TO-BE y del diagnóstico previo.
- **Artefactos:** `docs_agente/03_matriz_esfuerzo_impacto_y_metricas.md` (creado tras aprobación del Plan de Ruta).
- **Estado:** Completado.

---

## #005 — Gobernanza, ética y cumplimiento (Informe Ruta 4)

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Gobernanza y ética (Ruta 0, Etapa 3).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** El usuario solicitó avanzar con el documento de gobernanza, ética y cumplimiento correspondiente a la Etapa 3 de la guía oficial, a partir del diagnóstico, TO-BE y matriz de priorización.
- **Artefactos:** `docs_agente/04_gobernanza_etica_cumplimiento.md` (creado tras aprobación del Plan de Ruta).
- **Estado:** Completado.

---

## #006 — Optimización de carga de datos y presentación de la información (Finanzas)

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Diseño de carga de datos y presentación ejecutiva (BI/visualización).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado).
- **Prompt (resumen):** El usuario solicitó avanzar desde el diagnóstico hacia el diseño de una solución para optimizar la carga/preparación de datos y estructurar la presentación de la información en Taranis Black (Finanzas), proponiendo la mejor organización (secciones, vistas, indicadores, tablas, controles de calidad y apoyos visuales) sin imponer una estructura cerrada ni inventar datos faltantes.
- **Fuentes revisadas:** guía oficial, documentos de `docs_agente/` (00–04), `05_Finanzas_Presupuesto_vs_Real.xlsx`, `06_SIPOC.pdf`, `01_Catalogo...`, entregables previos.
- **Artefactos:** `docs_agente/05_optimizacion_carga_y_presentacion.md` (creado tras aprobación del Plan de Ruta).
- **Estado:** Completado.

---

## #007 — Construcción de plantilla Excel gerencial/financiera/operativa (Taranis Black)

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Implementación de plantilla Excel auditada (BI/finanzas).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado); Python 3.13.2 (`.venv`) con openpyxl.
- **Prompt (resumen):** El usuario solicitó construir el archivo Excel propuesto a partir de `05_optimizacion_carga_y_presentacion.md` y los archivos oficiales, con datos reales (05 y catálogo 01), estructura operativa sin datos falsos, cero valores hardcodeados en cálculos (solo fórmulas), presentación profesional y pestaña final de Premisas/Reglas/Auditoría.
- **Artefactos:** `docs_agente/Taranis_Black_Modelo_Gerencial.xlsx` (consolidado em 7 abas: Resumen_Ejecutivo, Finanzas_P&L, Productos_y_Catalogo, Carga_y_Exceções, Control_Calidad_DQ, Base_Dados_Finanzas, Premisas_y_Auditoria; fórmulas dinâmicas, gráficos, validações e formatação condicional).
- **Estado:** Completado.

---

## #008 — Revisão e correção de fórmulas da plantilla Excel

- **Fecha:** 2026-11-26 (interacción en curso).
- **Etapa:** Revisão de integridade de fórmulas (Excel).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado); Python 3.13.2 (`.venv`).
- **Prompt (resumen):** El usuario solicitó revisar el archivo Excel y corregir enlaces de fórmulas y consultas dañadas. Se detectó que las fórmulas de `Control_Calidad_DQ` referenciaban el nombre de pestaña con acentos (`Carga_y_Exceções`) distinto al nombre real (`Carga_y_Excepciones`), además de ajustar la fórmula de inadimplencia (usar ingresos B2B) y la etiqueta del KPI de fletes.
- **Artefactos:** `docs_agente/Taranis_Black_Modelo_Gerencial.xlsx` (corregido).
- **Estado:** Completado.

---

## #009 — Primeiro informe em PDF: análise de dados e problemas de negócio (Taranis Black)

- **Fecha:** 2026-11-27 (interacción en curso).
- **Etapa:** Informe de análise de dados e problemas de negócio (consultoria/auditoria).
- **Herramienta / Modelo:** VS Code + OpenCode (SST) / Beam Free (`opencode/beam-free`, declarado); Python 3.13.2 (`.venv`).
- **Prompt (resumen):** El usuario solicitó preparar el primer informe en PDF posterior al documento de carga y presentación: análisis de datos y problemas de negocio detectados en Taranis Black, con enfoque de consultoría de auditoría, basado en el kit y en lo trabajado en `docs_agente/`.
- **Artefactos:** `docs_agente/06_informe_analise_dados_problemas_negocio.pdf` (6 páginas; gerado com reportlab a partir de dados verificados).
- **Estado:** Completado.

---

## Notas para registros futuros

- Antes de generar cualquier documento nuevo en `docs_agente/`, presentar primero un Plan de Ruta y esperar aprobación (regla de `AGENTS.md`).
- No modificar ni sobrescribir archivos del kit (`docs_challenge/`) ni de `docs_challenge/entregables/` sin instrucción explícita.
- Marcar explícitamente los datos no disponibles como *Dato no disponible / Requiere validación*.
- Si el modelo/proveedor activo cambia, actualizar `00_entorno_y_configuracion.md` y registrar el cambio aquí.