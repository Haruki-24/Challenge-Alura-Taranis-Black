# Triaje y Estandarización de Email — Extracción y Validación de Propuestas

**Proyecto / Caso:** Challenge Taranis Black — Ruta 4 (Finanzas y Operaciones).  
**Carpeta:** `docs_agente/herramientas_ia/`  
**Fecha:** 2026-11-27

---

## 1. Objetivo

Automatizar el triaje (clasificación y priorización) de correos/propuestas entrantes y la estandarización del formato de email para:
- Extraer campos clave de la propuesta (CNPJ, IE, razón social, dirección, códigos de producto, cantidad, valor, condiciones, CIF/FOB).
- Validar los campos según las reglas R1–R9.
- Clasificar la propuesta por prioridad (urgente, normal, baja) y tipo (B2B, D2C).
- Generar un correo estandarizado con los campos estructurados para el flujo de crédito.
- Reducir el tiempo de triaje de ~2-4 h a ≤ 1 h (meta).

## 2. Triaje: clasificación y priorización

### 2.1 Clasificación por tipo

| Tipo | Criterio | Acción |
|---|---|---|
| B2B Corporativo | CNPJ + empresa + monto > USD 1.000 | Flujo completo (crédito + facturación + expedición) |
| D2C / E-commerce | Persona física o monto bajo | Flujo simplificado (pago anticipado) |
| Consulta / Duda | Sin propuesta formal | Respuesta automática con información del catálogo |
| Spam / Irrelevante | No relacionado con ventas | Archivar / ignorar |

### 2.2 Priorización

| Prioridad | Criterio | SLA de triaje |
|---|---|---|
| Urgente | Cliente existente + monto > USD 50.000 + fecha de entrega próxima | ≤ 30 min |
| Alta | Cliente existente + monto > USD 10.000 | ≤ 1 h |
| Normal | Nuevo cliente o monto ≤ USD 10.000 | ≤ 4 h |
| Baja | Consulta o propuesta incompleta | ≤ 24 h |

### 2.3 Implementación en n8n

```
[IMAP Trigger / Webhook] → [Extracción de texto (PDF/OCR)] → [LLM: clasificar tipo y prioridad] → [Validación R1-R9] → [Rama por prioridad] → [Correo estandarizado]
```

## 3. Estandarización de email: campos y validaciones

### 3.1 Campos a extraer

| Campo | Tipo | Obligatorio | Regla de validación |
|---|---|---|---|
| `cliente_cnpj` | string | Sí | R1: formato y dígito verificador |
| `cliente_razao` | string | Sí | R3: coincidencia con tarjeta CNPJ |
| `ie` | string | Sí | R2: formato por UF |
| `direccion` | string | Sí | R4: comprobante actualizado |
| `produto_codigo` | string | Sí | R5: existencia en Dim_Productos (catálogo) |
| `quantidade` | integer | Sí | R6: > 0 |
| `valor_unit` | decimal | Sí | R6: > 0 |
| `valor_total` | decimal | Sí | R6: cantidad × valor_unit |
| `condicao_pagamento` | enum (30/60/90) | Sí | R7: valores permitidos |
| `cif_fob` | enum (CIF/FOB) | Sí | R8: coherencia con catálogo |
| `data_entrega` | date | No | Formato ISO 8601 |
| `vendedor` | string | Sí | Identificación del consultor B2B |

### 3.2 Validaciones R1–R9 (resumen)

| Regla | Campo | Validación | Acción si falla |
|---|---|---|---|
| R1 | CNPJ | Formato y dígito verificador | Rechazar y solicitar corrección |
| R2 | IE | Formato por UF | Rechazar y solicitar corrección |
| R3 | Razón social | Coincidencia con tarjeta CNPJ | Devolver para aclaración |
| R4 | Dirección | Comprobante actualizado | Devolver para aclaración |
| R5 | Códigos de producto | Existencia en catálogo | Bloquear y alertar |
| R6 | Cantidad / valor | > 0 y dentro de límites | Rechazar |
| R7 | Condiciones de pago | Valores permitidos (30/60/90) | Rechazar |
| R8 | CIF/FOB | Coherencia con catálogo y propuesta | Alertar y validar |
| R9 | Completitud | Todos los campos obligatorios | Devolver lista de faltantes |

### 3.3 Correo estandarizado (plantilla de salida)

```
Asunto: [TRIAGE] Propuesta {cliente_razao} — USD {valor_total} — Prioridad: {prioridad}

Empresa: {cliente_razao} (CNPJ: {cliente_cnpj})
IE: {ie} | Dirección: {direccion}
Producto: {produto_codigo} ({quantidade} un. × USD {valor_unit})
Valor total: USD {valor_total}
Condición de pago: {condicao_pagamento} días
Flete: {cif_fob}
Fecha de entrega solicitada: {data_entrega}
Vendedor: {vendedor}

Validaciones R1-R9: {status_validacion}
Clasificación: {clasificacion} | Prioridad: {prioridad}

Resumen (RAG): {resumen_rag}

---
Este correo fue generado automáticamente por el flujo de triaje de Taranis Black.
Supervisión humana requerida para excepciones.
```

### 3.4 Implementación en n8n

```
[IMAP Trigger] → [Descargar PDF] → [OCR/Extracción de texto] → [LLM: extraer campos JSON] → [Code Node: validar R1-R9] → [IF: válido?] → [Correo estandarizado / Excepción]
```

- **Nodo IMAP:** monitorea la bandeja `financiero@taranisblack.com.br`.
- **Nodo OCR:** extrae texto del PDF (Tesseract o servicio cloud).
- **Nodo LLM:** envía el texto al LLM con un prompt de extracción que devuelve JSON.
- **Nodo Code (Python/JS):** valida R1-R9 y clasifica prioridad.
- **Nodo IF:** si válido → correo estandarizado; si inválido → excepción y notificación al vendedor.
- **Nodo Email:** envía el correo estandarizado al asistente financiero.

## 4. Métricas de éxito

| Métrica | Baseline | Meta |
|---|---|---|
| Tiempo de triaje | ~2-4 h | ≤ 1 h |
| Tasa de rechazo por datos faltantes | ~30-40% | ≤ 5% |
| % de propuestas clasificadas automáticamente | 0% | ≥ 80% |
| Precisión de extracción de campos | No medido | ≥ 90% |

## 5. Integración con el simulador Streamlit

El simulador (`05_simulador_streamlit.py`) permite probar el flujo de triaje y estandarización sin n8n ni correo real:
- El usuario pega el texto de una propuesta (o usa un ejemplo).
- El simulador ejecuta clasificación, extracción y validación localmente (con reglas R1-R9).
- Muestra el correo estandarizado generado y las excepciones detectadas.
- Opcionalmente, envía el payload a un webhook de n8n real (modo integrado).

## 6. Implementación sugerida

1. **Crear el workflow en n8n** con los nodos descritos (ver `04_flujo_n8n.md`).
2. **Configurar el nodo LLM** con el prompt de extracción (ver sección 3.3).
3. **Implementar las validaciones R1-R9** en un Code node (Python o JS).
4. **Probar con el simulador** en modo demo (sin n8n) y en modo integrado (con n8n).
5. **Validar** con propuestas completas e incompletas.
6. **Documentar** los resultados y capturas para la tabla de evidencias.
"