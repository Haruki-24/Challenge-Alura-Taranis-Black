# Gobernanza, Ética y Cumplimiento — IA para Finanzas (Taranis Black)

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Documento:** `docs_agente/04_gobernanza_etica_cumplimiento.md`  
**Fecha:** 2026-11-26  
**Etapa:** Gobernanza y ética (Ruta 0, Etapa 3).  
**Base tomada:** diagnóstico inicial, plan TO-BE, matriz de priorización, kit de datos y plantilla oficial.  
**Marco legal principal:** Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP, México), a solicitud del usuario. Se señalan también consideraciones de la LGPD (Brasil) por el contexto simulado de la empresa.  
**Estado:** Borrador inicial (pendiente de revisión del auditor).

---

## 1. Resumen ejecutivo

- Se establece un marco de **gobernanza de IA y datos** para el rediseño del flujo B2B, con política de IA responsable (permite/prohíbe), gestión de riesgos de sesgo e incumplimiento, comité de gobernanza y auditoría periódica.
- La protección de datos se aborda bajo la **LFPDPPP (México)** como marco principal solicitado, con notas de la **LGPD (Brasil)** por el contexto simulado de Taranis Black (CNPJ, Serasa, CD Joinville/SC).
- Se define trazabilidad de decisiones (prompts, reglas, excepciones) alineada con `docs_agente/historial_prompts.md`.

---

## 2. Base y alcance

### 2.1 Fuentes (Hecho / Evidencia)

- `docs_agente/01_diagnostico_inicial_datos_y_flujo.md`, `02_plan_to_be.md`, `03_matriz_esfuerzo_impacto_y_metricas.md`.
- `docs_challenge/Informe_Ruta_4_finanzas_ES.docx` (plantilla oficial, Etapa 3).
- `docs_challenge/taranis_black/05_Finanzas_Presupuesto_vs_Real.xlsx`, `06_Descripcion_del_proceso_operativo_SIPOC.pdf`.
- Contexto simulado: empresa brasileña (CNPJ, Serasa, ICMS, CD Joinville/SC).

### 2.2 Alcance

- **Incluye:** política de IA responsable, riesgos de sesgo e incumplimiento, comité y auditoría, protección de datos, trazabilidad.
- **No incluye:** políticas legales definitivas ni asesoría jurídica; el documento es un lineamiento de consultoría a validar con el área legal.

---

## 3. Política de IA responsable (propuesta)

### 3.1 Lo que se permite

- Clasificación y extracción de datos de correos/propuestas (IA generativa) para estructurar campos.
- Automatización de flujos de datos estructurados (IA tradicional) y generación de resúmenes (IA generativa).
- Agente RAG para consultar políticas internas de crédito y generar resúmenes de solicitudes.
- Motor de reglas de negocio (IA tradicional) para auto-aprobación bajo umbrales definidos.
- Detección de anomalías en datos financieros.
- Generación automática de NF a partir de datos validados.
- Dashboards de SLA y BI para visibilidad.

### 3.2 Lo que se prohíbe

- Decisiones de crédito de alto riesgo sin supervisión humana (alzada).
- Uso de datos personales sin base legal o fuera de la finalidad declarada.
- Modificación automática de límites de crédito sin aprobación humana.
- Envío automático de datos a terceros no autorizados.
- Uso de IA para discriminar clientes por criterios no justificados (sesgo).
- Eliminación o alteración de logs de decisión sin auditoría.

### 3.3 Supervisión humana (Human-in-the-Loop)

- Correos fuera de formato o datos faltantes → aclaración humana.
- Consulta manual al buró de crédito (Serasa) → participación humana para consultar y validar.
- Discrepancias en registros críticos → revisión humana antes de enviar/cobrar.
- Excepciones al motor de reglas → revisión del Gerente Financiero.

---

## 4. Riesgos de sesgo e incumplimiento

### 4.1 Riesgos de sesgo

| Riesgo | Descripción | Mitigación |
|---|---|---|
| Sesgo histórico en reglas de crédito | El motor puede perpetuar criterios pasados que excluyen clientes viables | Revisar umbrales periódicamente; auditar decisiones rechazadas; diversificar datos de entrenamiento |
| Sesgo en clasificación de correos | La IA generativa puede malinterpretar formatos no estándar | Human-in-the-Loop en excepciones; métricas de precisión |
| Sesgo por línea de producto | Priorización que favorece líneas de mayor margen | Revisar métricas por línea; gobernanza del comité |

### 4.2 Riesgos de incumplimiento (LFPDPPP — México)

- **Finalidad:** los datos personales (clientes, CNPJ-equivalentes, contactos) deben usarse solo para la finalidad declarada (gestión de crédito y facturación).
- **Consentimiento/aviso de privacidad:** informar a los clientes sobre el tratamiento de sus datos; obtener consentimiento cuando corresponda.
- **Derechos ARCO:** garantizar acceso, rectificación, cancelación y oposición de los titulares.
- **Seguridad:** medidas técnicas y administrativas para proteger los datos (acceso por rol, cifrado, logs).
- **Transferencias:** si los datos se transfieren a terceros (buró, CD, proveedores), documentar y garantizar protección equivalente.
- **Retención:** definir plazos de conservación y eliminación segura.

### 4.3 Consideraciones de la LGPD (Brasil) por contexto simulado

- Taranis Black opera con CNPJ, Serasa y CD en Brasil; si los datos de clientes brasileños se tratan, aplican los principios de la LGPD (finalidad, adecuación, necesidad, libre acceso, calidad, transparencia, seguridad, prevención, no discriminación, responsabilidad).
- **Transferencia internacional:** si el estudiante/procesamiento está en México y los datos son de Brasil, documentar la transferencia y las bases legales (consentimiento, contrato, interés legítimo).
- Recomendación: definir la jurisdicción aplicable y la base legal con el área legal antes de implementar.

---

## 5. Comité y auditoría

### 5.1 Composición del comité de gobernanza

| Rol | Responsabilidad |
|---|---|
| Gerente Financiero | Presidencia del comité; aprobación de reglas de crédito |
| Responsable de datos/procesos | Calidad de datos, repositorio único, métricas |
| Representante comercial | Perspectiva de ventas y clientes |
| Representante de operaciones (CD) | Expedición y logística |
| Asesor legal (consultivo) | Cumplimiento LFPDPPP/LGPD |

### 5.2 Frecuencia y funciones

- **Reuniones:** mensuales (revisión de métricas, excepciones, incidentes) y trimestrales (revisión de reglas y umbrales).
- **Funciones:** aprobar cambios a reglas de crédito, revisar auditorías, gestionar incidentes de datos/IA, validar políticas.
- **Auditoría:** revisión periódica de logs de decisiones (auto-aprobaciones, alzadas, excepciones), calidad de datos y cumplimiento de la política de IA.

---

## 6. Protección de datos y minimización

- **Minimización:** recopilar solo los datos necesarios para crédito y facturación (CNPJ, IE, dirección, historial).
- **Acceso por rol:** vendedor, asistente, gerencia y CD acceden solo a lo necesario.
- **Cifrado y seguridad:** datos en tránsito y en reposo; respaldos; control de accesos.
- **Retención y eliminación:** definir plazos (ej., datos de clientes inactivos) y eliminación segura.
- **Derechos de los titulares:** canal para solicitudes ARCO (México) / derechos del titular (Brasil).

---

## 7. Trazabilidad y registro de decisiones

- Registrar prompts, reglas y cambios en `docs_agente/historial_prompts.md` y en logs del sistema.
- Trazabilidad de decisiones de crédito: auto-aprobación, alzada, excepciones y su justificación.
- Versionado de reglas y umbrales (matriz de alzada) para auditoría.
- Evidencias para la tabla de evidencias de la guía oficial (enlaces públicos de prompts, skills, hojas, capturas).

---

## 8. Alineación a la guía oficial (Ruta 0, Etapa 3)

- **Política de IA responsable:** §3 (permite/prohíbe).
- **Riesgos y protección de datos:** §4 y §6 (sesgo, incumplimiento LFPDPPP/LGPD, minimización).
- **Comité y auditoría:** §5 y §7 (composición, frecuencia, trazabilidad).
- **Tabla de evidencias:** registrar entregables al final de la etapa.

---

## 9. Riesgos y limitaciones

- El documento es un lineamiento de consultoría; requiere validación legal para ser política definitiva.
- La LFPDPPP se aplicó a solicitud del usuario; el contexto simulado es brasileño (LGPD), por lo que la jurisdicción final debe definirse con el área legal.
- No se modificaron archivos del kit ni de `entregables/`.

---

## 10. Próximos pasos (Recomendación)

1. Validar la política y los riesgos con el área legal (México y, si aplica, Brasil).
2. Formalizar el comité y definir el calendario de auditorías.
3. Implementar la trazabilidad de decisiones en el TO-BE.
4. Preparar el entregable final consolidado y la tabla de evidencias (guía oficial).

---

**Responsable de la declaración:** Auditor encargado (usuario).  
**Herramienta:** VS Code + OpenCode (SST). **Modelo:** Beam Free (`opencode/beam-free`, declarado).