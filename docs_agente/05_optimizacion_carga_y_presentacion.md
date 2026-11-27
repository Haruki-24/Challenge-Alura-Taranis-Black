# Optimización de Carga de Datos y Presentación de la Información (Taranis Black, Finanzas)

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Documento:** `docs_agente/05_optimizacion_carga_y_presentacion.md`  
**Fecha:** 2026-11-26  
**Etapa:** Diseño de carga de datos y presentación ejecutiva (BI).  
**Base tomada:** diagnóstico inicial, plan TO-BE, matriz de priorización, gobernanza, kit de datos y catálogo.  
**Estado:** Borrador inicial (pendiente de revisión del auditor).

---

## 1. Resumen ejecutivo

- Se propone un **modelo de datos ligero** (entidades y relaciones) que integra Finanzas (05) y el catálogo de productos (01), para validar códigos y analizar por línea.
- Se define una **optimización de carga/preparación** con reglas de validación (poka-yoke), separación entre datos conciliados y no conciliados (staging → validado → conciliado) y manejo de excepciones.
- Se establecen **controles de calidad de datos (DQ)** con umbrales medibles (completitud, unicidad, consistencia, oportunidad, validez).
- Se estructura la **presentación ejecutiva** en vistas/pestañas con mockups textuales: Ejecutiva, Financiera, Operativa, Calidad de Datos, Auditoría/Trazabilidad (y Producto).
- Se incluye un **diccionario de indicadores** (fórmula, fuente, frecuencia, responsable) y apoyos visuales recomendados.

---

## 2. Base y alcance

### 2.1 Fuentes (Hecho / Evidencia)

- `docs_agente/00_entorno_y_configuracion.md`, `01_diagnostico_inicial_datos_y_flujo.md`, `02_plan_to_be.md`, `03_matriz_esfuerzo_impacto_y_metricas.md`, `04_gobernanza_etica_cumplimiento.md`.
- `docs_challenge/taranis_black/05_Finanzas_Presupuesto_vs_Real.xlsx` (3 hojas).
- `docs_challenge/taranis_black/06_Descripcion_del_proceso_operativo_SIPOC.pdf` (proceso, SIPOC, 6M).
- `docs_challenge/taranis_black/01_Catalogo_de_productos_y_precios_Taranis_Black.pdf` (líneas ErgoPro, SmartDesk, Silence, periféricos; CIF/FOB, NR-17, garantía).
- `docs_challenge/Guia_oficial_informe_ES.pdf` (estructura de entrega y evidencias).

### 2.2 Alcance

- **Incluye:** modelo de datos, carga/preparación, calidad de datos, presentación (vistas), diccionario de indicadores, gobernanza de datos.
- **No incluye:** implementación técnica (código, ETL), costos, cronograma detallado.
- **Fuera de alcance:** inventario/almacén como dependencia; buró de crédito (externo).

---

## 3. Diagnóstico de datos (fuentes, calidad, brechas)

### 3.1 Fuentes de datos (Hecho / Evidencia)

| Fuente | Tipo | Uso | Limitación |
|---|---|---|---|
| `05_Finanzas_Presupuesto_vs_Real.xlsx` | Hoja de cálculo (3 hojas) | Resultados, productos, cuellos de botella | Agregado por trimestre; sin series por pedido |
| `06_SIPOC.pdf` | Documento | Proceso AS-IS, SIPOC, 6M | Texto; sin datos transaccionales |
| `01_Catalogo...pdf` | Documento | Dimensiones de producto (códigos, CIF/FOB, NR-17) | No integrado al flujo actual |
| `Control_Limites_2026.xlsx` (citado) | Hoja local | Límites de crédito | No sincronizada; múltiples fuentes de verdad |
| ERP legado | Sistema | Histórico de compras, facturación | Sin API; digitación manual |
| Serasa Experian | Portal externo | Score, protestas, deudas | Consulta manual |
| Correo electrónico | Comunicación | Entrada de propuestas | Sin formato estándar |

### 3.2 Brechas de calidad observadas (Hallazgo)

- **Completitud:** propuestas con campos faltantes (cantidad, valor, cliente, fecha, condiciones, CIF/FOB, IE); tasa de rechazo estimada 30–40%.
- **Consistencia:** divergencia entre códigos de producto de la propuesta y el registro en el ERP; tabla de precios comercial vs. ERP desactualizado.
- **Unicidad:** riesgo de duplicidad de clientes (CNPJ/IE) por digitación manual.
- **Oportunidad:** datos disponibles solo al cierre de mes; sin SLA por etapa.
- **Validez:** CNPJ/IE/razón social/dirección no validados en la entrada.

### 3.3 Consecuencias (Hecho / Evidencia)

- Cancelaciones/reentregas +245% (USD 0,73 M vs 0,21 M).
- Fletes duplicados +57,1% (USD 3,74 M vs 2,38 M).
- Divergencia en boletos 6,8% vs <0,5%.
- Inadimplencia 3,4% vs 1,2%.

---

## 4. Modelo de datos propuesto (ER ligero)

### 4.1 Entidades y relaciones

```
DimTiempo (1) ──< FactVentas (N)
DimProducto (1) ──< FactVentas (N)
DimCliente (1) ──< FactVentas (N)
DimCanal (1) ──< FactVentas (N)

DimCliente (1) ──< FactCredito (N)
FactCredito (1) ──< FactExpedicion (N)   [por pedido]

FactVentas (1) ──< FactExpedicion (N)     [por pedido]
```

### 4.2 Tablas y campos clave

**DimTiempo**
- `id_tiempo` (PK), `fecha`, `anio`, `trimestre`, `mes`, `dia`, `dia_semana`, `es_pico_fin_mes`.

**DimProducto**
- `id_producto` (PK), `codigo_erp`, `nombre`, `linea` (ErgoPro/SmartDesk/Silence/Periféricos), `familia`, `nr17` (sí/no), `condicion_flete` (CIF/FOB), `garantia_anios`, `activo`.

**DimCliente**
- `id_cliente` (PK), `cnpj`, `razon_social`, `ie`, `direccion`, `ciudad`, `uf`, `score_serasa`, `limite_credito`, `inadimplencia_90d`, `segmento`.

**DimCanal**
- `id_canal` (PK), `canal` (B2B/D2C), `descripcion`.

**FactVentas**
- `id_venta` (PK), `id_tiempo`, `id_producto`, `id_cliente`, `id_canal`, `cantidad`, `valor_bruto`, `descuentos`, `impuestos`, `valor_neto`, `margen_bruto`, `presupuestado` (sí/no), `fuente` (real/presupuesto).

**FactCredito**
- `id_credito` (PK), `id_cliente`, `id_tiempo`, `monto_solicitado`, `condicion` (30/60/90), `score_serasa`, `pendencias`, `historial_compras`, `dictamen` (aprobado/rechazado/pendiente), `aprobador`, `tiempo_espera_h`, `auto_aprobado` (sí/no).

**FactExpedicion**
- `id_expedicion` (PK), `id_venta`, `id_credito`, `fecha_autorizacion`, `fecha_nf`, `codigo_nf`, `divergencia_cif_fob` (sí/no), `error_nf` (sí/no), `dias_almacenamiento`, `fecha_liberacion_cd`, `fpv_expedicion`.

**FactOperativo (SLA)**
- `id_evento` (PK), `id_pedido`, `etapa` (1–5), `fecha_inicio`, `fecha_fin`, `duracion_h`, `sla_meta_h`, `cumple_sla` (sí/no), `responsable`.

**FactCalidadDatos (DQ)**
- `id_dq` (PK), `id_fuente`, `fecha_carga`, `completitud_pct`, `unicidad_pct`, `consistencia_pct`, `oportunidad_h`, `validez_pct`, `errores`.

### 4.3 Notas de diseño

- `DimProducto` se alimenta del catálogo 01 para validar códigos y condiciones CIF/FOB.
- `FactVentas` distingue presupuesto vs. real (`fuente`) para análisis de variación.
- `FactOperativo` permite medir SLA por etapa (base para el dashboard).

---

## 5. Optimización de carga y preparación de datos

### 5.1 Reglas de validación en la carga (poka-yoke)

| Regla | Campo | Validación | Acción si falla |
|---|---|---|---|
| R1 | CNPJ | Formato y dígito verificador | Rechazar y solicitar corrección |
| R2 | IE | Formato por UF | Rechazar y solicitar corrección |
| R3 | Razón social | Coincidencia con tarjeta CNPJ | Devolver para aclaración |
| R4 | Dirección | Comprobante actualizado | Devolver para aclaración |
| R5 | Códigos de producto | Existencia en `DimProducto` (catálogo) | Bloquear y alertar |
| R6 | Cantidad / valor | > 0 y dentro de límites | Rechazar |
| R7 | Condiciones de pago | Valores permitidos (30/60/90) | Rechazar |
| R8 | CIF/FOB | Coherencia con catálogo y propuesta | Alertar y validar |
| R9 | Completitud | Todos los campos obligatorios | Devolver lista de faltantes |

### 5.2 Separación: datos conciliados vs. no conciliados

| Capa | Nombre | Contenido | Uso |
|---|---|---|---|
| Staging | `stg_*` | Datos crudos tal cual se reciben (correo/PDF/ERP) | Auditoría de origen |
| Validado | `val_*` | Datos que pasaron las reglas R1–R9 | Análisis de calidad |
| Conciliado | `conc_*` / modelo final | Datos conciliados con fuentes de verdad (catálogo, ERP, Serasa) | Reportes y dashboard |
| Excepciones | `exc_*` | Registros rechazados o con discrepancias | Gestión de excepciones y retrabajo |

- **Flujo:** Staging → Validación (R1–R9) → Conciliado (si OK) o Excepciones (si falla).
- **Principio:** ningún dato llega al dashboard sin pasar por la capa conciliada.

### 5.3 Deduplicación y normalización

- Deduplicación de clientes por CNPJ (clave natural) + razón social normalizada.
- Normalización de códigos de producto (trim, mayúsculas, mapeo a `DimProducto`).
- Estandarización de fechas (ISO 8601) y moneda (USD).
- Tabla de mapeo `map_producto` para códigos legacy → código estándar.

### 5.4 Frecuencia y orquestación (propuesta)

| Proceso | Frecuencia | Justificación |
|---|---|---|
| Carga de propuestas (formulario) | Tiempo real (evento) | Elimina cola de correos |
| Consulta de crédito (ERP + Serasa) | Al recibir propuesta (paralelo) | Reduce 40 min → ≤20 min |
| Conciliación de ventas (FactVentas) | Diaria (batch nocturno) | Balance oportunidad/costo |
| Actualización de catálogo (DimProducto) | Semanal o ante cambio | Estabilidad de dimensiones |
| Cálculo de DQ (FactCalidadDatos) | Diario | Monitoreo continuo |
| Dashboard ejecutivo | Near-real-time (cada 1–4 h) | Visibilidad oportuna |

### 5.5 Manejo de errores y excepciones

- Registro de cada rechazo en `exc_*` con motivo (regla fallida) y responsable.
- Notificación automática al responsable (asistente financiero / vendedor).
- SLA de resolución de excepciones (ej., ≤ 24 h).
- Escalamiento si la excepción supera el SLA.

---

## 6. Controles de calidad de datos (DQ)

### 6.1 Dimensiones y umbrales

| Dimensión | Definición | Umbral propuesto | Fuente de medición |
|---|---|---|---|
| Completitud | % de registros con todos los campos obligatorios | ≥ 95% | `FactCalidadDatos` |
| Unicidad | % de clientes sin duplicados (CNPJ) | ≥ 99% | `DimCliente` |
| Consistencia | % de códigos de producto válidos vs. catálogo | ≥ 98% | `map_producto` |
| Validez | % de campos con formato válido (CNPJ, IE, fechas) | ≥ 95% | Reglas R1–R9 |
| Oportunidad | Tiempo entre evento y disponibilidad en dashboard | ≤ 24 h | `FactOperativo` |
| Exactitud | % de valores conciliados sin discrepancia | ≥ 98% | Conciliación |

### 6.2 Alertas y acciones

- Si un umbral no se cumple → alerta al responsable y registro en `FactCalidadDatos`.
- Si la completitud < 90% → bloquear avance a la capa conciliada.
- Si la consistencia < 95% → revisión de catálogo/mapping.

---

## 7. Estructura de presentación (vistas/pestañas) — mockups textuales

### 7.1 Vista Ejecutiva (Home)

**Componentes:**
- KPI cards (semáforo): Lead time total, Cierre contable, EBITDA, Inadimplencia, Fletes %.
- Gráfico de barras: Ingresos presupuesto vs. real (T1–T4).
- Tabla: Top 3 desvíos y acciones.
- Filtro: período (trimestre/año), línea de producto.

**Objetivo:** visión en ≤ 30 segundos para la dirección.

### 7.2 Vista Financiera

**Componentes:**
- Tabla: P&L resumido (ingresos, deducciones, CMV, lucro bruto, OPEX, EBITDA, lucro líquido) por trimestre.
- Gráfico de líneas: EBITDA presupuesto vs. real.
- Tabla: variación por línea de producto (presupuestado/real/var %/margen bruto).
- Gráfico de barras: OPEX por categoría (fletes, cancelaciones, inadimplencia, sistemas).
- Filtro: período, canal, línea.

### 7.3 Vista Operativa (SLA y pipeline)

**Componentes:**
- Tabla: SLA por etapa (baseline vs. real vs. meta) con semáforo.
- Gráfico de barras: tiempo medio por etapa.
- Kanban/pipeline: pedidos por etapa (WIP, antigüedad).
- Tabla: fletes % de facturación, divergencia CIF/FOB, días de almacenamiento.
- Filtro: período, responsable, línea.

### 7.4 Vista de Calidad de Datos (DQ)

**Componentes:**
- KPI cards: completitud, unicidad, consistencia, validez, oportunidad.
- Gráfico de líneas: evolución de DQ por semana.
- Tabla: excepciones abiertas (motivo, responsable, antigüedad).
- Filtro: fuente, período.

### 7.5 Vista de Auditoría y Trazabilidad

**Componentes:**
- Tabla: historial de prompts/decisiones (ID, fecha, etapa, artefacto).
- Tabla: cambios de reglas/umbrales (versión, fecha, responsable).
- Logs de auto-aprobaciones, alzadas y excepciones.
- Filtro: período, tipo de evento.

### 7.6 Vista de Producto (opcional)

**Componentes:**
- Tabla: líneas (participación, presup/real, var %, margen bruto, cuello principal).
- Gráfico de barras: margen bruto por línea.
- Tabla: validación de códigos vs. catálogo (errores).
- Filtro: línea, período.

---

## 8. Diccionario de indicadores (selección)

| Indicador | Fórmula | Fuente | Frecuencia | Responsable |
|---|---|---|---|---|
| Lead time total | Fecha expedición − Fecha firma propuesta | `FactOperativo` | Diaria | Asistente financiero |
| Cierre contable | Días entre cierre de mes y cierre contable | `FactOperativo` | Mensual | Contabilidad |
| EBITDA | Lucro operativo antes de intereses/impuestos | `FactVentas` | Trimestral | Controller |
| Inadimplencia B2B >90 días | Provisión PDD / receta B2B | `FactVentas` | Mensual | Crédito |
| Fletes % de facturación | Fletes y logística / ingresos brutos | `FactVentas` | Mensual | Operaciones |
| Divergencia de boletos | NF con corrección / total NF | `FactExpedicion` | Mensual | Facturación |
| Completitud de entrada | Propuestas completas / total | `FactCalidadDatos` | Diaria | Asistente financiero |
| Tiempo medio de análisis de crédito | Suma tiempos / propuestas analizadas | `FactCredito` | Semanal | Crédito |
| % auto-aprobación | Auto-aprobadas / total solicitudes | `FactCredito` | Mensual | Gerente Financiero |
| Tasa de error en NF (FPY) | NF sin corrección / total | `FactExpedicion` | Mensual | Facturación |

---

## 9. Apoyos visuales recomendados

- **KPI cards con semáforo** (verde/amarillo/rojo) para lectura rápida.
- **Gráficos de barras** para comparar presupuesto vs. real por período/línea.
- **Gráficos de líneas** para tendencias (EBITDA, fletes).
- **Tablas con formato condicional** para SLA y DQ.
- **Kanban/pipeline** para WIP por etapa.
- **Heatmap** para desvíos por categoría y período (opcional).
- **Filtros globales** (período, línea, canal, responsable) en todas las vistas.

---

## 10. Gobernanza de datos y roles

| Actividad | Responsable |
|---|---|
| Definición de estándares de datos | Responsable de datos/procesos |
| Validación de catálogo (DimProducto) | Asistente financiero + comercial |
| Gestión de excepciones DQ | Asistente financiero |
| Aprobación de cambios de modelo | Comité de gobernanza |
| Monitoreo de DQ y alertas | Responsable de datos |
| Acceso y seguridad | TI / responsable de datos |

---

## 11. Riesgos, limitaciones y datos no disponibles

- **Sin datos transaccionales por pedido:** solo agregados trimestrales; los SLA por etapa requieren instrumentación (time-study). (Dato no disponible / Requiere validación.)
- **Sin diccionario de datos ni fecha de corte** en `05`. (Dato no disponible.)
- **ERP legado sin API:** la integración puede requerir RPA o migración; viabilidad a validar.
- **Contexto Brasil (moneda/tributos)** con estudiante en México; marco legal a definir con el área legal.
- **Modelo/proveedor de IA no verificado en archivos** (declarado: `opencode/beam-free`).
- **No se modificaron** archivos del kit ni de `entregables/`.

---

## 12. Próximos pasos (Recomendación)

1. Validar el modelo de datos y el diccionario de indicadores con el equipo.
2. Definir la instrumentación de SLA por etapa (time-study) para alimentar `FactOperativo`.
3. Prototipar las vistas en una herramienta BI (Power BI / Looker / Live Artifact) usando los mockups textuales.
4. Implementar las reglas de validación en la carga (R1–R9) y la separación por capas (staging/validado/conciliado/excepciones).
5. Monitorear DQ y ajustar umbrales.

---

**Responsable de la declaración:** Auditor encargado (usuario).  
**Herramienta:** VS Code + OpenCode (SST). **Modelo:** Beam Free (`opencode/beam-free`, declarado).