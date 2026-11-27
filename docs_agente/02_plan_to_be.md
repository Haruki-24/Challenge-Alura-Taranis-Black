# Plan TO-BE — Rediseño del Proceso B2B (Taranis Black, Finanzas)

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Documento:** `docs_agente/02_plan_to_be.md`  
**Fecha:** 2026-11-26  
**Etapa:** Diseño del proceso TO-BE (rediseño operativo y de control).  
**Base tomada:** `docs_agente/01_diagnostico_inicial_datos_y_flujo.md` + diagnóstico AS-IS + kit de datos + propuestas de solución con IA (Informe Ruta 4 y Canvas IA).  
**Estado:** Borrador inicial (pendiente de revisión del auditor).

---

## 1. Resumen ejecutivo

- El rediseño **no parte de tecnología**, sino de **orden, estandarización y reglas de decisión**; la IA y la automatización son habilitadores posteriores. (Recomendación de diseño, consistente con el diagnóstico.)
- Objetivo: reducir el ciclo firma → expedición de **>5 días útiles a ≤24 h útiles** (meta 2026) y el cierre contable de **7 días a ≤2 días**, eliminando el retrabajo por datos incompletos y la centralización de aprobaciones.
- El TO-BE se organiza en **5 etapas rediseñadas** con validaciones de entrada, motor de reglas de crédito, matriz de alzada, integración de datos y control de SLA por etapa.
- Se proponen **umbrales iniciales de auto-aprobación** como supuesto de diseño (a validar con datos reales), y se mantiene la supervisión humana (Human-in-the-Loop) en excepciones.

---

## 2. Base y alcance

### 2.1 Fuentes (Hecho / Evidencia)

- `docs_agente/01_diagnostico_inicial_datos_y_flujo.md` (diagnóstico inicial datos + flujo).
- `docs_challenge/entregables/Auditoria de proceso Taranis.docx` (diagnóstico AS-IS, v1.0).
- `docs_challenge/taranis_black/05_Finanzas_Presupuesto_vs_Real.xlsx` (datos presupuesto vs. real).
- `docs_challenge/taranis_black/06_Descripcion_del_proceso_operativo_SIPOC.pdf` (proceso AS-IS, SIPOC, 6M).
- `docs_challenge/Informe_Ruta_4_finanzas_ES.docx` (casos de uso de IA y plantilla de entrega).
- `docs_challenge/entregables/canvas_ai_tarantis_black.pdf` (AI Canvas).

### 2.2 Alcance

- **Incluye:** rediseño del flujo B2B (aprobación de crédito → facturación → expedición), reglas de negocio, roles, SLA/KPIs, soluciones de IA, tecnología y datos, gestión del cambio y gobernanza.
- **No incluye:** rediseño de inventario/almacén ni del buró de crédito (dependencias externas); plan de acción detallado con costos; políticas legales definitivas (se proponen lineamientos).
- **Fuera de alcance declarado (heredado):** inventario/almacén, decisiones del buró, plan de acción (siguiente documento).

---

## 3. Principios de rediseño

1. **Estandarizar la entrada** (poka-yoke): sin datos completos y válidos no se avanza.
2. **Validar temprano:** CNPJ/IE/razón social/dirección y catálogo de productos se verifican en la Etapa 1.
3. **Reglas antes que personas:** matriz de alzada y auto-aprobación para casos de bajo riesgo.
4. **Paralelizar, no serializar:** la consulta de crédito se dispara al recibir la propuesta, no al abrirla.
5. **Fuente única de verdad:** catálogo de productos, tabla de precios y límites de crédito en un repositorio único y sincronizado.
6. **Visibilidad en tiempo real:** SLA por etapa y dashboard de pipeline.
7. **IA como habilitador:** clasificación/extracción (generativa), automatización de flujos (tradicional), agente RAG para políticas y priorización.
8. **Human-in-the-Loop en excepciones:** datos faltantes, correos fuera de formato, discrepancias y consultas al buró.

---

## 4. Proceso TO-BE por etapas

### 4.1 Etapa 1 — Captura estandarizada de la propuesta (rediseño de la entrada)

**Objetivo:** eliminar la entrada libre por correo y garantizar completitud ≥95%.

- **Entrada:** propuesta firmada (PDF) + datos del cliente.
- **Mecanismo:** formulario digital / plantilla obligatoria con campos: cantidad, valor, cliente (CNPJ, IE, razón social, dirección), fecha, condiciones (30/60/90), CIF/FOB, códigos de producto.
- **Validaciones automáticas:** CNPJ/IE (formato), razón social vs. tarjeta CNPJ, dirección actualizada, códigos de producto vs. catálogo 01, disponibilidad de stock (integración con inventario cuando exista).
- **IA (caso de uso 1):** IA generativa para interpretar texto del correo/PDF y estructurar campos; redactar respuesta sobre plantilla.
- **Salida:** propuesta estructurada y validada (o devuelta con lista de campos faltantes).
- **SLA:** triaje ≤ 1 h; completitud de primera entrada ≥ 95%; tasa de rechazo por datos faltantes ≤ 5%.
- **Rol:** vendedor B2B (captura) + asistente financiero (validación).

### 4.2 Etapa 2 — Validación y enriquecimiento de datos (paralelización)

**Objetivo:** reducir el tiempo de análisis de crédito de ~40 min a ≤5 min (automatizado) / ≤20 min (semiautomatizado).

- **Acción:** al recibir la propuesta, se dispara en paralelo: consulta de historial de compras (ERP), consulta al buró (Serasa) y verificación de límite de crédito (repositorio único).
- **Fuente única de verdad:** `Control_Limites_2026.xlsx` migrado a repositorio compartido/sincronizado (o sistema de crédito), junto con tabla de precios y catálogo.
- **IA (caso de uso 2):** automatización de flujos (IA tradicional) para mover/rellenar datos estructurados; IA generativa para resumir texto libre.
- **Salida:** dictamen de crédito preliminar (score, pendencias, historial, límite disponible).
- **SLA:** tiempo medio de análisis ≤ 20 min (meta ≤ 5 min automatizado); throughput ≥ 20 propuestas/analista/día.
- **Rol:** asistente financiero (validación) + sistema (automatización).

### 4.3 Etapa 3 — Evaluación de crédito (motor de reglas)

**Objetivo:** eliminar aprobaciones manuales innecesarias mediante reglas objetivas.

- **Motor de reglas (IA tradicional):** aplica criterios por monto, score Serasa, historial de pago e inadimplencia.
- **Agente (IA generativa + RAG):** consulta políticas de crédito, clasifica y prioriza solicitudes, redacta resumen para el aprobador cuando se requiere alzada.
- **Salida:** auto-aprobación (casos de bajo riesgo) o solicitud de alzada estructurada (casos de riesgo).
- **SLA:** tiempo de solicitud ≤ 5 min (plantilla); % de solicitudes auto-aprobables ≥ 50–60%.
- **Rol:** sistema (reglas) + asistente financiero (revisión de excepciones).

### 4.4 Etapa 4 — Aprobación (matriz de alzada y escalamiento)

**Objetivo:** reducir la espera de 24–48 h a ≤4 h (auto ≤ minutos) mediante delegación y SLA.

- **Matriz de alzada (propuesta inicial — supuesto de diseño):**
  - Auto-aprobación: monto ≤ USD 10.000 **y** score Serasa ≥ 700 **y** sin inadimplencia >90 días **y** cliente con historial de pago ≥ 2 pedidos.
  - Aprobación del Gerente Financiero: monto > USD 10.000 o score < 700 o inadimplencia activa.
  - Escalamiento a Director: monto > USD 50.000 o score < 600.
- **Delegación:** suplente designado cuando el titular no está disponible; escalamiento automático si se supera el SLA.
- **SLA:** tiempo medio de espera ≤ 4 h (auto ≤ minutos); % dentro de SLA ≥ 90%; antigüedad máxima ≤ 8 h.
- **Rol:** Gerente Financiero (alzada), suplente (delegado), Director (escalamiento).

> Nota: los umbrales son **supuesto de diseño** a validar con el histórico real de pedidos y la política de crédito de la empresa.

### 4.5 Etapa 5 — Facturación y expedición (validación y liberación)

**Objetivo:** reducir la tasa de error en NF de ~10–20% a ≥98% FPY y eliminar divergencias CIF/FOB.

- **Facturación:** generación del espejo de NF a partir de los datos validados (sin digitación manual); validación de códigos de producto e IE contra el catálogo 01 y el ERP.
- **Expedición:** transmisión automática de la orden de expedición al CD (Joinville/SC) con verificación CIF/FOB antes del cierre; liberación del camión condicionada a la validación.
- **SLA:** tiempo medio de emisión de NF ≤ 1 h; divergencia CIF/FOB ≤ 2%; días de almacenamiento por divergencia = 0; FPY de expedición ≥ 95%.
- **Rol:** facturación/contabilidad (emisión) + CD Joinville/transportadoras (expedición).

---

## 5. Roles y responsabilidades (RACI — propuesta)

| Actividad | Vendedor B2B | Asistente financiero | Gerente Financiero | Sistema/IA | CD Joinville |
|---|---|---|---|---|---|
| Captura de propuesta | R/A | C | I | S | I |
| Validación de datos (CNPJ/IE/catálogo) | C | R/A | I | S | I |
| Consulta de crédito (paralela) | I | R | I | A | I |
| Evaluación por reglas | I | C | I | R/A | I |
| Aprobación (alzada) | I | C | R/A | S | I |
| Facturación (NF) | I | R/A | I | S | I |
| Expedición/liberación | I | C | I | S | R/A |

Leyenda: R = Responsable, A = Aprobador, C = Consultado, I = Informado, S = Soporte (IA/sistema).

---

## 6. KPIs TO-BE (metas propuestas)

| Etapa | KPI crítico | Baseline actual | Meta TO-BE |
|---|---|---|---|
| 1. Entrada | Completitud de primera entrada | ~50–60% (est.) | ≥ 95% |
| 1. Entrada | Tasa de rechazo por datos faltantes | ~30–40% (est.) | ≤ 5% |
| 2. Crédito | Tiempo medio de análisis | ~40 min | ≤ 20 min (≤ 5 min autom.) |
| 3. Aprobación | % de solicitudes auto-aprobables | No medido | ≥ 50–60% |
| 4. Decisión | Tiempo medio de espera de aprobación | 24–48 h | ≤ 4 h |
| 4. Decisión | % de aprobaciones dentro de SLA | Bajo | ≥ 90% |
| 5. Facturación | Tasa de error en NF (FPY) | ~10–20% (est.) | ≥ 98% |
| 5. Facturación | Divergencia CIF/FOB | No medido | ≤ 2% |
| Transversal | Lead time total (firma → expedición) | > 5 días útiles | ≤ 24 h |
| Transversal | Cierre contable mensual | 7 días | ≤ 2 días |
| Transversal | Fletes (OPEX) | USD 3,74 M (+57,1%) | Reducción progresiva a meta 0,8% de facturación |
| Transversal | Inadimplencia B2B >90 días | 3,4% | ≤ 1,2% |

---

## 7. Soluciones de IA propuestas (mapeo a casos de uso)

Fuente: `Informe_Ruta_4_finanzas_ES.docx` (Etapa 1, Ruta 0) y `canvas_ai_tarantis_black.pdf`.

| Caso de uso (informe) | Etapa TO-BE | Tipo de IA | Supervisión humana (Human-in-the-Loop) |
|---|---|---|---|
| 1. Estandarizar y clasificar correos para extraer datos clave | Etapa 1 | Generativa (interpretar texto y estructurar campos / redactar respuestas) | Correos fuera de formato o datos faltantes → aclaración humana |
| 2. Automatización del flujo para completar planillas y reducir errores/tiempos | Etapa 2 | Tradicional (automatización de flujos) + Generativa (resumir/redactar) | Discrepancias o datos incompletos en tablas |
| 3. Agente para clasificar, pre-evaluar bajo reglas y priorizar solicitudes para el gerente | Etapas 3–4 | Generativa (RAG para políticas/clasificación/resumen) + Tradicional (reglas de negocio) | Consulta manual al buró; validaciones sobre registros críticos |

**Soluciones complementarias (Canvas IA):** software de conciliación financiera centralizado, BI para reportes en tiempo real, detección de anomalías y validación de datos, planilla maestra en la nube como puente (sin IA), estandarización de documentos/procesos/plazos/responsables.

---

## 8. Tecnología y datos (propuesta de diseño)

- **Repositorio único de datos maestros:** clientes (CNPJ, IE, dirección), catálogo de productos (códigos, CIF/FOB, NR-17), tabla de precios, límites de crédito.
- **Integraciones:** ERP legado (vía API o RPA si no hay API), portal Serasa (consulta automatizada o asistida), CD Joinville (transmisión de orden de expedición).
- **Automatización:** RPA para consultas repetitivas; motor de reglas para crédito; generación automática de NF a partir de datos validados.
- **BI/Analytics:** dashboard de SLA por etapa, pipeline de pedidos, fletes, inadimplencia y cierre contable.
- **Validación:** poka-yoke en la entrada (campos obligatorios, catálogo) para evitar propagación de errores.

> Nota: la viabilidad técnica depende de la capacidad de integración del ERP legado; si no hay API, se propone RPA como puente (supuesto de diseño).

---

## 9. Gestión del cambio

- **Comunicación:** explicar el "por qué" (impacto en EBITDA/margen) y el "qué cambia" por rol; involucrar a vendedores, asistentes, gerencia y CD.
- **Capacitación:** capacitación por rol sobre el nuevo formulario, reglas de crédito y uso del dashboard; acompañamiento en los primeros ciclos.
- **Adopción gradual:** piloto en una línea de producto (ej., SmartDesk, más afectada por crédito) antes de escalar.
- **Resistencia esperada:** centralización de aprobaciones y pérdida de control percibida por la gerencia; mitigar con visibilidad y transparencia del motor de reglas.
- **Medición de adopción:** % de propuestas capturadas por el formulario, % de auto-aprobaciones, uso del dashboard.

---

## 10. Gobernanza, ética y cumplimiento

- **Comité de IA/proceso:** gerente financiero, responsable de datos, representante comercial y de operaciones (CD); reuniones periódicas (ej., mensual) para revisar métricas y excepciones.
- **Política de IA responsable:** qué se permite (clasificación, extracción, RAG sobre políticas internas) y qué se prohíbe (decisiones de crédito sin supervisión humana en casos de riesgo; uso de datos personales sin base legal).
- **Protección de datos:** CNPJ/datos de clientes tratados conforme a la LGPD; minimización de datos; acceso por rol; auditoría de accesos.
- **Riesgos de sesgo:** el motor de reglas puede perpetuar criterios históricos; revisar umbrales periódicamente y auditar decisiones rechazadas.
- **Auditoría:** revisión periódica de logs de decisiones (auto-aprobaciones, alzadas, excepciones) y de la calidad de datos.
- **Trazabilidad:** registrar prompts, decisiones y cambios de reglas (alineado con `docs_agente/historial_prompts.md`).

---

## 11. Riesgos y limitaciones

- **Sin datos históricos por etapa:** las metas son propuestas; requieren validación con time-study real. (Dato no disponible / Requiere validación.)
- **ERP legado sin API:** puede requerir RPA o migración parcial; costo y tiempo no estimados (no hay presupuesto en los archivos).
- **Dependencias externas:** buró (Serasa) y CD (Joinville/SC) no se rediseñan; solo se aíslan con validaciones y flujos paralelos.
- **Cambio cultural:** centralización de aprobaciones y resistencia al cambio.
- **Modelo/proveedor de IA no verificado en archivos** (declarado: `opencode/beam-free`).
- **No se modificaron** archivos del kit ni de `entregables/`.

---

## 12. Próximos pasos (Recomendación)

1. Validar los umbrales de la matriz de alzada con el histórico real de pedidos.
2. Definir el time-study por etapa para establecer baselines reales.
3. Elaborar la matriz Esfuerzo × Impacto formal (Etapa 2 de la guía) para priorizar iniciativas.
4. Diseñar el formulario/plantilla de entrada y el repositorio único de datos maestros.
5. Definir la política de IA responsable y el comité de gobernanza.
6. Preparar el plan de acción y el entregable final alineado a la guía oficial (tabla de evidencias, enlace público).

---

**Responsable de la declaración:** Auditor encargado (usuario).  
**Herramienta:** VS Code + OpenCode (SST). **Modelo:** Beam Free (`opencode/beam-free`, declarado).