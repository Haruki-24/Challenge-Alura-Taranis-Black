# Matriz de Esfuerzo × Impacto y Métricas de Éxito (Taranis Black, Finanzas)

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Documento:** `docs_agente/03_matriz_esfuerzo_impacto_y_metricas.md`  
**Fecha:** 2026-11-26  
**Etapa:** Priorización y métricas (Ruta 0, Etapa 2).  
**Base tomada:** `docs_agente/01_diagnostico_inicial_datos_y_flujo.md`, `docs_agente/02_plan_to_be.md`, kit de datos y propuestas de IA.  
**Estado:** Borrador inicial (pendiente de revisión del auditor).

---

## 1. Resumen ejecutivo

- Se identifican **10 iniciativas clave** derivadas del TO-BE, priorizadas por Esfuerzo (bajo/medio/alto) e Impacto (bajo/medio/alto).
- **Quick wins (alto impacto / esfuerzo bajo-medio):** estandarización de la entrada (I1), motor de reglas de crédito (I4), detección de anomalías (I9), automatización de facturación (I6).
- **Iniciativas fundacionales (alto impacto / esfuerzo alto):** repositorio único de datos maestros (I2) e integración de consulta de crédito (I3); habilitan el resto.
- Las métricas de éxito se definen por iniciativa (KPI, horas ahorradas, ROI estimado, adopción), marcadas como **supuesto de diseño** por ausencia de costos reales en los archivos.
- Se incluye un plan de gestión del cambio breve y la alineación a la guía oficial (Etapa 2).

---

## 2. Escala de valoración

| Dimensión | Bajo | Medio | Alto |
|---|---|---|---|
| **Esfuerzo** | Cambio acotado, sin integraciones complejas; < 4 semanas | Integración moderada o cambio de proceso; 1–3 meses | Integración compleja con sistemas legados; > 3 meses o alto cambio cultural |
| **Impacto** | Mejora localizada; < 10% de un KPI crítico | Mejora significativa; 10–30% de un KPI crítico | Impacto en el ciclo completo o en EBITDA/margen; > 30% |

> Nota: la valoración es una estimación de consultoría basada en el diagnóstico y el TO-BE; debe validarse con el equipo y los costos reales.

---

## 3. Matriz de Esfuerzo × Impacto

| ID | Iniciativa | Etapa TO-BE | Esfuerzo | Impacto | Prioridad |
|---|---|---|---|---|---|
| I1 | Estandarizar captura de propuesta (formulario + validaciones) | 1 | Medio | Alto | 1 — Quick win |
| I2 | Repositorio único de datos maestros (clientes, catálogo, precios, límites) | Transversal | Alto | Alto | 3 — Fundacional |
| I3 | Integración/automatización de consulta de crédito (ERP + Serasa + límites) | 2 | Medio-Alto | Alto | 4 — Fundacional |
| I4 | Motor de reglas de crédito + matriz de alzada | 3–4 | Medio | Alto | 2 — Quick win |
| I5 | Agente IA (RAG) para clasificación y priorización de solicitudes | 3–4 | Medio | Medio-Alto | 5 |
| I6 | Automatización de facturación (NF) a partir de datos validados | 5 | Medio | Alto | 6 |
| I7 | Integración con CD Joinville (transmisión + validación CIF/FOB) | 5 | Medio-Alto | Medio | 7 |
| I8 | Dashboard de SLA/BI (visibilidad en tiempo real) | Transversal | Medio | Medio-Alto | 8 |
| I9 | Detección de anomalías en datos (IA) | Transversal | Bajo-Medio | Medio | 9 |
| I10 | Capacitación y gestión del cambio | Transversal | Medio | Medio | 10 — Continuo |

### 3.1 Secuencia recomendada de implementación (orden lógico)

1. **I1 + I4** (estandarizar entrada y reglas) — mayor palanca con esfuerzo moderado.  
2. **I9** (anomalías) — rápido, mejora la calidad de datos.  
3. **I2** (repositorio único) — fundacional para I3, I6, I7.  
4. **I3 + I5** (crédito automatizado + agente) — elimina el cuello de botella principal.  
5. **I6 + I7** (facturación y expedición) — reduce errores y fletes.  
6. **I8** (dashboard) — consolida la visibilidad.  
7. **I10** (capacitación/cambio) — continuo a lo largo de todas las fases.

> Nota: no se incluyen plazos ni cronograma detallado (fuera del alcance acordado); solo orden lógico y dependencias.

---

## 4. Métricas de éxito por iniciativa

### 4.1 Tabla consolidada

| ID | Iniciativa | KPI principal | Baseline actual | Meta TO-BE | Horas ahorradas (est.) | Adopción (meta) |
|---|---|---|---|---|---|---|
| I1 | Captura estandarizada | Completitud de primera entrada | ~50–60% (est.) | ≥ 95% | 20–40 h/mes (retrabajo evitado) | ≥ 90% de propuestas por formulario |
| I2 | Repositorio único | Divergencia de datos (precio/límite) | No medido | ≤ 2% | 10–20 h/mes (conciliación) | 100% de áreas usando la fuente única |
| I3 | Consulta de crédito automatizada | Tiempo medio de análisis | ~40 min | ≤ 20 min (≤ 5 min autom.) | ~110–130 h/mes* | ≥ 80% de consultas automatizadas |
| I4 | Motor de reglas + alzada | % de solicitudes auto-aprobables | No medido | ≥ 50–60% | 15–30 h/mes (redacción/decisión) | ≥ 90% de solicitudes por el motor |
| I5 | Agente IA (RAG) | Tiempo de solicitud al aprobador | ~15–30 min | ≤ 5 min | 5–15 h/mes | ≥ 70% de solicitudes con resumen automático |
| I6 | Automatización de NF | Tasa de error en NF (FPY) | ~10–20% (est.) | ≥ 98% | 10–25 h/mes (reproceso) | ≥ 95% de NF generadas sin digitación manual |
| I7 | Integración con CD | Divergencia CIF/FOB | No medido | ≤ 2% | 5–15 h/mes (liberación) | 100% de órdenes transmitidas automáticamente |
| I8 | Dashboard SLA/BI | % de aprobaciones dentro de SLA | Bajo | ≥ 90% | 5–10 h/mes (reportes manuales) | ≥ 80% de usuarios activos mensuales |
| I9 | Detección de anomalías | Anomalías detectadas antes del cierre | No medido | ≥ 80% | 5–10 h/mes | Uso continuo en el cierre |
| I10 | Capacitación/cambio | Adopción de nuevas prácticas | — | ≥ 80% de adopción | — | ≥ 80% de los roles capacitados |

\* Estimación: 200 pedidos/mes × (40 − 5) min ≈ 117 h/mes. Supuesto de diseño.

### 4.2 ROI estimado (supuesto de diseño)

No existen costos reales en los archivos; se expresan como **rangos de impacto anualizado** a validar:

| Iniciativa | Impacto anual estimado (USD) | Base del estimado (Hecho/Evidencia) |
|---|---|---|
| I1 + I4 (entrada + reglas) | Reducción de retrabajo y cancelaciones: hasta USD 1,25 M/año | Pedidos cancelados por lentitud (05) |
| I3 (crédito) | Liberación de capacidad: ~110–130 h/mes | 40 min/propuesta (SIPOC) |
| I6 + I7 (facturación/expedición) | Reducción de fletes duplicados: hasta USD 0,96 M/año; cancelaciones/reentregas: hasta USD 0,73 M/año | 05 (fletes +2,8%, cancelaciones +245%) |
| I2 + I8 (datos + visibilidad) | Reducción de PDD/inadimplencia: hasta USD 1,11 M/año | 05 (inadimplencia 3,4% vs 1,2%) |
| I10 (cambio) | Habilitador; sin impacto directo aislado | — |

> Nota: los valores son techos de impacto observados en `05`, no proyecciones de ahorro total; el ahorro real depende del grado de implementación. **Dato no disponible / Requiere validación** para costos de implementación y ROI neto.

### 4.3 Métricas transversales de éxito (alineadas al TO-BE)

| Métrica | Baseline actual | Meta TO-BE |
|---|---|---|
| Lead time total (firma → expedición) | > 5 días útiles | ≤ 24 h |
| Cierre contable mensual | 7 días | ≤ 2 días |
| Fletes (OPEX) | USD 3,74 M (+57,1%) | Reducción progresiva a 0,8% de facturación |
| Inadimplencia B2B >90 días | 3,4% | ≤ 1,2% |
| EBITDA (anual) | USD 5,77 M (−41,4% vs presupuesto) | Recuperación progresiva del margen |

---

## 5. Plan de gestión del cambio (breve)

- **Comunicación:** presentar el impacto en EBITDA/margen y los beneficios por rol; involucrar a vendedores, asistentes, gerencia y CD.
- **Capacitación:** por rol, sobre el formulario, reglas de crédito, uso del dashboard; acompañamiento en los primeros ciclos.
- **Piloto:** iniciar en una línea (ej., SmartDesk, más afectada por crédito) antes de escalar.
- **Resistencia esperada:** centralización de aprobaciones; mitigar con transparencia del motor de reglas y visibilidad.
- **Medición de adopción:** % de propuestas por formulario, % de auto-aprobaciones, uso del dashboard.

---

## 6. Alineación a la guía oficial (Ruta 0, Etapa 2)

- **Matriz Esfuerzo × Impacto:** presentada en §3 con orden de implementación.
- **Métricas de éxito:** ROI estimado, horas ahorradas y metas de adopción por iniciativa (§4).
- **Plan de gestión del cambio:** §5.
- **Tabla de evidencias:** registrar enlaces públicos de prompts, skills, hojas generadas y capturas (Human-in-the-Loop) al final de la etapa.

---

## 7. Riesgos y limitaciones

- Estimaciones de ROI/horas no validadas por ausencia de costos reales en los archivos. (Dato no disponible / Requiere validación.)
- La valoración de esfuerzo/impacto es juicio de consultoría; debe validarse con el equipo.
- Dependencias externas (ERP legado, Serasa, CD) pueden alterar el esfuerzo real.
- No se modificaron archivos del kit ni de `entregables/`.

---

## 8. Próximos pasos (Recomendación)

1. Validar la matriz y las estimaciones con el equipo y los costos reales.
2. Definir el piloto (línea de producto y etapas) y sus criterios de éxito.
3. Avanzar a la política de gobernanza, ética y cumplimiento (Etapa 3 de la guía) si se requiere para la entrega.
4. Preparar la tabla de evidencias y el entregable final en Google Docs (guía oficial).

---

**Responsable de la declaración:** Auditor encargado (usuario).  
**Herramienta:** VS Code + OpenCode (SST). **Modelo:** Beam Free (`opencode/beam-free`, declarado).