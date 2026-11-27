# Diagnóstico Inicial — Datos y Flujo (Taranis Black, Finanzas)

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Documento:** `docs_agente/01_diagnostico_inicial_datos_y_flujo.md`  
**Fecha:** 2026-11-26  
**Etapa:** Análisis inicial de datos y flujo (AS-IS + observaciones de auditoría).  
**Base tomada:** `docs_challenge/entregables/Auditoria de proceso Taranis.docx` (diagnóstico AS-IS del auditor, v1.0) + kit de datos.  
**Estado:** Borrador inicial (pendiente de revisión del auditor).

---

## 1. Resumen ejecutivo

- El flujo B2B de Taranis Black (aprobación de crédito → facturación → expedición) es **funcional pero estructuralmente frágil**: depende de correos no estandarizados, tres hojas de cálculo locales no sincronizadas y un ERP legado sin integración por API. (Hecho / Evidencia: SIPOC y diagnóstico AS-IS.)
- El flujo representa **~70% de los ingresos** (USD 33,6 M/año) y **180–220 pedidos corporativos/mes**. La meta 2026 exige ciclo total ≤ 24 h útiles; el actual supera **5 días útiles**, con **+5 días de retraso en el cierre contable mensual**. (Hecho / Evidencia: SIPOC p.1; diagnóstico §1.)
- El análisis de `05_Finanzas_Presupuesto_vs_Real.xlsx` muestra que la **renta no se perdió por ventas** (ingresos B2B −1,2% vs presupuesto), sino por **costos de proceso**: EBITDA anual real USD 5,77 M vs presupuestado USD 9,85 M (−41,4%). (Hallazgo verificado / cálculo sobre datos del archivo.)
- Las mayores fugas verificadas son: **fletes y logística +57,1%** sobre presupuesto (USD 3,74 M vs 2,38 M), **cancelaciones/reentregas +245%** (USD 0,73 M vs 0,21 M) y **provisión por inadimplencia +152%** (USD 1,11 M vs 0,44 M). (Hallazgo verificado.)
- El diagnóstico AS-IS existente es de buena calidad cualitativa (etapas, problemas 6M, KPIs con meta), pero sus **baselines son estimaciones no validadas** y varias secciones del documento plantilla quedan con texto marcador ("Escribe aquí tu texto"). (Observación de auditoría.)
- **Palancas de mayor impacto (recomendación de diseño):** Etapa 4 (decisión gerencial, ~40% del ciclo) + Etapa 3 (ausencia de matriz de alzada) + Etapa 1 (entrada no estandarizada, ~20% y fuente de retrabajo). La tecnología/IA es habilitador, no punto de partida.

---

## 2. Base tomada y alcance

### 2.1 Documento base (Hecho / Evidencia en archivo)

- `docs_challenge/entregables/Auditoria de proceso Taranis.docx` — "Diagnóstico AS-IS — Etapas 1 a 5", v1.0, noviembre 2026, autor Gonzalo Costela.
- Contenido reutilizado: descripción AS-IS de 5 etapas, problemas por etapa (P1.x–P5.x), causas raíz 6M, KPIs iniciales (baseline estimado / meta preliminar) y hallazgos transversales.
- **Limitación declarada por el propio documento:** datos cualitativos/documentales; baselines estimados a validar con extracción real; sin series históricas por etapa.

### 2.2 Alcance de este documento

- **Incluye:** estructura y calidad de datos del kit; análisis de impacto financiero/operativo verificado; síntesis del flujo AS-IS; observaciones y brechas del diagnóstico base; flujo de trabajo por etapas para la entrega; alineación a la guía oficial.
- **No incluye:** rediseño TO-BE completo, plan de acción detallado, matriz Esfuerzo×Impacto formal ni políticas de gobernanza (etapas posteriores / Etapa 2 y 3 de la guía).
- **Fuera de alcance declarado (heredado):** inventario/almacén como dependencia externa; decisiones del buró de crédito (Serasa) como externo; plan de acción (segundo informe).

---

## 3. Fuentes y método de inspección

| Fuente | Uso | Método |
|---|---|---|
| `docs_challenge/Guia_oficial_informe_ES.pdf` | Estructura de entrega, etapas Ruta 0 y vertical, tabla de evidencias | Extracción de texto (pypdf, `.venv`) |
| `docs_challenge/taranis_black/00_Indice_y_guia_del_kit_de_datos.md` | Índice y descripción del kit | Lectura directa |
| `docs_challenge/taranis_black/05_Finanzas_Presupuesto_vs_Real.xlsx` | Datos presupuesto vs. real, productos, cuellos de botella | Inspección con pandas (`.venv`) |
| `docs_challenge/taranis_black/06_Descripcion_del_proceso_operativo_SIPOC.pdf` | Proceso AS-IS, SIPOC, 6M | Extracción de texto (pypdf, `.venv`) |
| `docs_challenge/entregables/Auditoria de proceso Taranis.docx` | Diagnóstico AS-IS base | Extracción de XML (zipfile, Python estándar) |
| `docs_challenge/taranis_black/01_Catalogo_de_productos_y_precios_Taranis_Black.pdf` | Referencia de líneas de producto (ErgoPro, SmartDesk, Silence) | Referenciado; no inspeccionado en detalle en esta etapa |

**Herramienta de análisis:** Python 3.13.2 (`.venv`), pandas 3.1.1, pypdf 7.2.0.  
**Nota:** las cifras de `05` se toman tal cual del archivo; no se recalcularon fórmulas ni se imputaron valores faltantes.

---

## 4. Estructura y calidad de los datos (`05_Finanzas_Presupuesto_vs_Real.xlsx`)

### 4.1 Hojas y dimensiones (Hecho / Evidencia)

| Hoja | Dimensiones | Contenido |
|---|---|---|
| `Resultados_trimestrales` | 24 filas × 16 cols | Estado de resultados T1–T4: presupuestado vs. real, variación %, totales anuales |
| `Ingresos_por_producto` | 6 filas × 8 cols | Líneas de producto: participación, presupuestado/real anual, variación, margen bruto medio, cuello de botella |
| `Cuellos_de_botella_y_costos` | 6 filas × 6 cols | Métricas operativas: meta/benchmark, situación real, desviación, costo/impacto anual, causa raíz |

### 4.2 Observaciones de calidad de datos (Hallazgo / Recomendación)

- **Encabezados de negocio en fila 1**, datos desde fila 2; filas de sección ("1. INGRESOS BRUTOS…") con valores vacíos (NaN) en columnas numéricas. Requiere limpieza antes de automatizar reportes. (Hallazgo.)
- **Variaciones (%) ya calculadas en el archivo** (col. "Var T1 (%)", etc.); se usaron como evidencia, sin recalcular. (Hecho.)
- **Moneda y contexto:** USD y tributos brasileños (ICMS, PIS, COFINS), consistente con el proceso descrito (CNPJ, Serasa, CD Joinville/SC). (Hecho.)
- **Sin series mensuales ni por pedido:** el archivo es agregado por trimestre; no permite análisis por pedido ni por etapa del flujo. **Dato no disponible / Requiere validación** para medir SLA por etapa. (Limitación.)
- **Sin diccionario de datos ni fecha de corte documentada** en el archivo. (Limitación.)

---

## 5. Análisis de datos: impacto financiero y operativo (verificado)

### 5.1 Bloque de métricas verificadas (selección)

| # | Métrica | Presupuesto | Real | Variación | Fuente |
|---|---|---|---|---|---|
| 1 | Ingresos brutos totales (anual) | USD 48,60 M | USD 48,50 M | −0,2% | `Resultados_trimestrales` |
| 2 | Ingreso canal B2B (70%) | USD 34,00 M | USD 33,60 M | −1,2% | `Resultados_trimestrales` |
| 3 | EBITDA anual | USD 9,85 M | USD 5,77 M | **−41,4%** | `Resultados_trimestrales` |
| 4 | Lucro líquido anual | USD 5,97 M | USD 3,11 M | −47,9% | `Resultados_trimestrales` |
| 5 | Fletes y logística (OPEX) | USD 2,38 M | USD 3,74 M | **+57,1%** | `Resultados_trimestrales` |
| 6 | Cancelaciones/reentregas por retraso logístico | USD 0,21 M | USD 0,73 M | **+245%** | `Resultados_trimestrales` |
| 7 | Provisión por inadimplencia B2B | USD 0,44 M | USD 1,11 M | +152% | `Resultados_trimestrales` |
| 8 | Gastos administrativos y sistemas legados | USD 1,76 M | USD 2,02 M | +14,8% | `Resultados_trimestrales` |

> Nota: los porcentajes se calcularon como (Real − Presupuesto) / Presupuesto. Los valores del archivo coinciden con estos cálculos para las filas citadas.

### 5.2 Lectura de negocio (Hallazgo / Recomendación de diseño)

- **El problema es de margen, no de ventas.** Ingresos B2B prácticamente en meta (−1,2%), pero EBITDA cae 41,4%. La fuga se concentra en costos operativos vinculados al flujo (fletes, cancelaciones, inadimplencia, sistemas legados). (Hallazgo.)
- **Fletes de emergencia** (+57,1%) son el mayor incremento OPEX y se atribuyen en `Cuellos_de_botella_y_costos` a error en la transposición manual de datos de la propuesta a la orden de expedición del CD. (Hecho + Hallazgo.)
- **Cancelaciones/reentregas** (+245%) son el mayor factor de retrabajo y se vinculan a divergencia entre tabla de precios comercial y registro desactualizado en el ERP. (Hecho + Hallazgo.)
- **Inadimplencia B2B** (3,4% real vs meta 1,2%) impacta caja y se atribuye a cobranza no automatizada (recordatorios manuales por correo). (Hecho + Hallazgo.)

### 5.3 Desempeño por línea de producto (Hecho + Observación)

| Línea | Participación | Presup. anual | Real anual | Var. (USD) | Var. (%) | Margen bruto medio | Cuello principal observado |
|---|---|---|---|---|---|---|---|
| ErgoPro (sillas) | 48,5% | 23,50 M | 23,85 M | +0,35 M | +1,5% | 44,2% | Ventas calentadas; margen comprimido por fletes y descartes |
| SmartDesk (mesas) | 27,5% | 13,20 M | 12,65 M | −0,55 M | −4,2% | 38,5% | Retrasos en homologación de crédito traban facturación B2B |
| Silence (cabinas) | 18,0% | 8,60 M | 8,10 M | −0,50 M | −5,8% | 52,0% | Ciclo largo (90 días) y logística con montaje técnico |
| Accesorios/periféricos | 6,0% | 2,70 M | 2,80 M | +0,10 M | +3,7% | 61,0% | Alto volumen/tíquete bajo; conciliación de boletos manuales sobrecarga al equipo |

**Observación de auditoría:** el catálogo 01 (ErgoPro, SmartDesk, Silence, periféricos) es consistente con las líneas del archivo; las especificaciones de producto (NR-17, flete CIF/FOB, garantía 5 años) están en el catálogo y son relevantes para validar códigos en la Etapa 5. (Recomendación: usar el catálogo como referencia de validación de producto.)

### 5.4 Métricas operativas y SLA (Hecho / Evidencia)

| Métrica | Meta / Benchmark | Situación real | Desviación | Costo/impacto anual | Causa raíz (según archivo) |
|---|---|---|---|---|---|
| Tiempo de cierre contábil mensual | 2 días laborables | 7 días laborables | +5 días | USD 180.000 (horas extras/auditorías) | Conciliación manual entre 3 hojas Excel y ERP legado |
| Homologación de crédito B2B | Máx. 4 h | 48 h | +44 h | USD 1.250.000 (pedidos cancelados) | Consulta manual a Serasa (40 min/pedido) + dependencia de correo del gerente |
| Reentregas y fletes expresos | 0,8% de facturación | 2,8% | +2,0 p.p. | USD 960.000 (fletes duplicados) | Transposición manual de datos propuesta → orden de expedición |
| Divergencia en boletos emitidos | <0,5% de NF-e | 6,8% | +6,3 p.p. | USD 390.000 (cancelación/intereses) | Tabla de precios comercial vs. registro desactualizado en ERP |
| Inadimplencia B2B >90 días | 1,2% de la receta | 3,4% | +2,2 p.p. | USD 1.110.000 (PDD) | Cobranza no automatizada; recordatorios manuales |

**Observación:** estas métricas son más creíbles como **línea base** que los baselines estimados del diagnóstico AS-IS (§4.2 de ese documento), porque provienen del archivo de gestión. Recomendación: adoptarlas como baseline oficial y validar las estimaciones restantes.

---

## 6. Flujo operativo AS-IS (síntesis)

### 6.1 Contexto macro (Hecho / Evidencia)

- Pedidos corporativos B2B = 70% de ingresos (USD 33,6 M/año); 180–220 pedidos/mes facturados (ErgoPro, SmartDesk, Silence).
- Meta 2026: ciclo total firma → expedición ≤ 24 h útiles. Actual: > 5 días útiles; cierre contable +5 días.
- Crecimiento 35%/año tensionó sistemas legados y asistentes financieros.

### 6.2 Cinco pasos AS-IS (Hecho / Evidencia: SIPOC y diagnóstico)

| Paso | Descripción | Tiempo / cuello |
|---|---|---|
| 1. Envío de propuesta por el vendedor | Correo manual a `financiero@...` con PDF; sin validación previa de stock, crédito ni CNPJ; >40 correos en pico sin prioridad | Origen del retrabajo |
| 2. Revisión manual y consulta al buró | Triple ventana (ERP + Serasa + Excel local `Control_Limites_2026.xlsx`); 40 min/propuesta; loops de aclaración | ~14% del ciclo |
| 3. Solicitud de aprobación por correo | Redacción manual al Gerente Financiero; sin motor de reglas; todo pedido requiere aprobación | Alimenta el cuello |
| 4. Espera de decisión gerencial | 24–48 h hábiles; centralización en una persona; sin SLA/escalamiento | **~40% del ciclo** (principal) |
| 5. Facturación manual y envío al CD (Joinville/SC) | Digitación manual del espejo de NF; errores de código/IE; tercer correo manual; divergencia CIF/FOB | ~14% del ciclo |

### 6.3 SIPOC (resumen)

- **Proveedores:** consultores B2B/SDRs, asistentes financieros, Gerente Financiero, buró (Serasa), facturación/contabilidad, CD Joinville/transportadoras.
- **Entradas:** propuesta firmada (PDF), datos catastrales (CNPJ, IE, dirección), buró (score/protestas), autorización por correo, tabla de fletes/rutas.
- **Proceso:** 5 pasos anteriores.
- **Salidas:** orden de venta registrada, dictamen de crédito, autorización formal, DANFE/XML y boletos 30/60/90, picking list y minuta de embarque.
- **Clientes:** clientes corporativos (compradores B2B), CD Joinville y transportadoras.

### 6.4 Causas raíz (6M) — síntesis (Hecho / Evidencia: SIPOC)

1. **Método:** sin POP documentado; flujo por correo informal; sin matriz de alzada; reglas CIF/FOB no verificadas antes del cierre.
2. **Máquina:** ERP legado sin API; sin OCR/IA para PDF; 3 hojas locales no sincronizadas.
3. **Mano de obra:** equipo sobrecargado con digitación; burnout en cierres; centralización de aprobaciones.
4. **Material:** propuestas con campos incompletos; divergencia de códigos; falta de comprobante de dirección actualizado.
5. **Medición:** sin SLA por etapa en tiempo real; visibilidad solo al cierre de mes; sin pipeline de pedidos embalsados.
6. **Medio ambiente:** distancia/fricción SP–Joinville/SC; cultura reactiva de "apagar incendios".

---

## 7. Observaciones y brechas del diagnóstico AS-IS existente (Auditoría)

### 7.1 Fortalezas (a mantener)

- Descomposición clara en 5 etapas con problemas, evidencia y causa raíz 6M.
- KPIs con definición/fórmula, unidad, baseline estimado, meta preliminar y fuente.
- Vista consolidada de KPIs y hallazgos transversales bien articulados.
- Conclusión acertada: la mayor palanca es organizacional/proceso; tecnología e IA son habilitadores.

### 7.2 Brechas y oportunidades de mejora (Hallazgo / Recomendación)

1. **Baselines estimados, no verificados.** Varios KPIs usan "~50–60%", "estimado", "no medido". El archivo `05` ofrece métricas reales (7 días de cierre, 48 h de crédito, 2,8% fletes, 6,8% divergencia de boletos, 3,4% inadimplencia) que deberían adoptarse como baseline oficial. (Recomendación.)
2. **Porcentajes de atribución del ciclo sin trazabilidad.** "~40% (Etapa 4)", "~20% (Etapa 1)", "~14% (Etapas 2 y 5)" se presentan como estimaciones sin cálculo visible ni fuente. Recomendación: definir método de medición (time-study por etapa) antes de comprometer metas. (Dato no disponible / Requiere validación.)
3. **Inconsistencia en la suma de atribuciones.** 40 + 20 + 14 + 14 = 88%; el 12% restante (aprox. Etapa 3) no se explica. Aclarar si la Etapa 3 se incluye en el 40% de la Etapa 4. (Observación.)
4. **Documento plantilla incompleto.** Secciones como "Resumen ejecutivo", "Visión general", "Objetivos", "Especificaciones", "Hitos" contienen texto marcador ("Escribe aquí tu texto"). Esto afecta la calidad del entregable final. (Hecho / Evidencia en archivo.)
5. **Sin dueño de proceso ni RACI.** No se asigna responsabilidad por etapa ni contrato de servicio entre áreas. (Recomendación.)
6. **Sin matriz de priorización (Esfuerzo × Impacto).** La guía oficial menciona la Etapa 2 (opcional) de la vertical; el diagnóstico afirma que las Etapas 1, 3 y 4 tienen mayor palanca, pero sin matriz formal que lo respalde. (Recomendación.)
7. **Dependencias externas bien identificadas** (inventario, buró, CD) pero sin plan de aislamiento (poka-yoke/flujos paralelos) detallado. (Recomendación.)
8. **Sin análisis de datos financieros vinculado.** El diagnóstico AS-IS no cruza los KPIs operativos con el impacto en EBITDA/margen (05), lo que limita la priorización por valor. Este documento inicia ese cruce (§5). (Observación.)

---

## 8. Riesgos, limitaciones y datos no disponibles

- **Baselines no validados:** la mayoría de los KPIs del diagnóstico AS-IS son estimaciones; solo las métricas de `05` son verificadas. (Dato no disponible / Requiere validación.)
- **Sin series por pedido/etapa:** no es posible calcular SLA real por etapa ni lead time total por pedido. (Dato no disponible.)
- **Extracción de PDF con pypdf:** posible pérdida de formato/tablas; el texto se verificó manualmente, pero se recomienda contrastar con el DOCX original si hay dudas.
- **Contexto Brasil (CNPJ, Serasa, ICMS, CD Joinville/SC)** con cifras en USD; no se validó conversión ni vigencia de los valores.
- **Modelo/proveedor de IA no verificado en archivos** (declarado por el usuario: `opencode/beam-free`).
- **No se modificaron** archivos del kit ni de `entregables/`.

---

## 9. Flujo de trabajo por etapas (recepción → entrega)

| Etapa | Actividad | Salida |
|---|---|---|
| 1. Recepción | Recibir y registrar fuentes (kit, diagnóstico base, guía) | Inventario de fuentes |
| 2. Inspección | Inspeccionar estructura real de archivos (`.venv`) | Mapa de datos y calidad |
| 3. Análisis | Cruzar flujo AS-IS con datos (05) y causas 6M | Hallazgos verificados |
| 4. Hallazgos | Consolidar brechas, riesgos y limitaciones | Lista priorizada |
| 5. Recomendaciones | Recomendaciones ejecutivas y próximos pasos | Plan de acción (siguiente documento) |
| 6. Entrega | Alinear a guía oficial y tabla de evidencias | Informe final (Ruta 4) |

---

## 10. Alineación a la guía oficial (Ruta 4)

- **Etapa 1 (obligatoria) — vertical Finanzas/Operaciones:** diagnóstico AS-IS + análisis de datos + hallazgos (este documento).
- **Etapa 2 (opcional, recomendada para portafolio):** matriz Esfuerzo × Impacto y gestión del cambio; plan de acción; políticas de gobernanza/ética/LGPD (Etapa 3 de la Ruta 0).
- **Tabla de evidencias:** registrar enlaces públicos de prompts, skills, hojas generadas y capturas (Human-in-the-Loop) al final de cada etapa.
- **Entrega:** copia en Google Docs con acceso "Cualquier persona con el enlace" (Lector) y envío en la plataforma Alura.

---

## 11. Siguientes pasos (Recomendación)

1. Validar los baselines estimados contra datos reales (time-study por etapa) y adoptar las métricas de `05` como baseline oficial.
2. Construir matriz Esfuerzo × Impacto para las etapas 1, 3 y 4 (priorización formal).
3. Definir matriz de alzada (umbrales por monto, score, historial) y reglas de auto-aprobación.
4. Estandarizar la entrada (formulario/campos obligatorios) y validar contra catálogo 01 (CIF/FOB, códigos).
5. Diseñar tablero de SLA por etapa y cierre contable.
6. Preparar el plan de acción y la política de gobernanza (Etapa 2/3) para el entregable final.

---

**Responsable de la declaración:** Auditor encargado (usuario).  
**Herramienta:** VS Code + OpenCode (SST). **Modelo:** Beam Free (`opencode/beam-free`, declarado).