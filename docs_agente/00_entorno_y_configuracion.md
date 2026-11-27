# Declaración de Entorno y Configuración — Proyecto Taranis Black (Finanzas)

**Proyecto / Caso:** Challenge Taranis Black — Especialización en Finanzas (auditoría y mejora de procesos).  
**Carpeta de trabajo:** `C:\Users\gezec\Documents\ONE\G11\challenge\proyecto`  
**Fecha de declaración:** 2026-11-26  
**Estado:** Borrador inicial (trazabilidad de entorno propio).

---

## 1. Identificación del proyecto y alcance (Hecho / Evidencia en archivo)

- **AGENTS.md** del proyecto define el rol del agente, las reglas operativas, la estructura de carpetas y los estándares de auditoría.
- **Kit oficial de datos:** `docs_challenge/taranis_black/` (archivos originales; no modificables).
- **Guía oficial del informe:** `docs_challenge/Guia_oficial_informe_ES.pdf`.
- **Informe base de referencia:** `docs_challenge/Informe_Ruta_4_finanzas_ES.docx`.
- **Entregables revisados (reservados):** `docs_challenge/entregables/`.
- **Documentación generada por el agente:** `docs_agente/` (única carpeta autorizada para borradores/documentos nuevos).

## 2. Herramienta y entorno de trabajo

| Elemento | Declaración |
|---|---|
| Editor / IDE | Visual Studio Code |
| Extensión de IA | OpenCode (SST) |
| Sistema operativo | Windows (win32) |
| Shell de trabajo | PowerShell |
| Ruta del proyecto | `C:\Users\gezec\Documents\ONE\G11\challenge\proyecto` |

## 3. Modelo / IA declarado

| Elemento | Declaración |
|---|---|
| Modelo seleccionado por el usuario | Beam Free |
| Identificador asumido en OpenCode | `opencode/beam-free` |
| Verificación en archivos del proyecto | **No verificado en archivos** — no existe `opencode.json` ni configuración visible en el proyecto que confirme el proveedor/modelo. El identificador se registra según declaración del usuario y debe confirmarse si cambia. |

> Nota de auditoría: si el modelo/proveedor activo cambia durante el challenge, actualizar esta sección y registrar el cambio en `docs_agente/historial_prompts.md`.

## 4. Entorno de análisis — Python (`.venv`)

- **Ubicación:** `C:\Users\gezec\Documents\ONE\G11\challenge\proyecto\.venv`
- **Versión de Python:** 3.13.2
- **Intérprete:** `C:\Users\gezec\Documents\ONE\G11\challenge\proyecto\.venv\Scripts\python.exe`
- **Origen:** entorno virtual creado con `python -m venv` (Python base `C:\Users\gezec\AppData\Local\Programs\Python\Python313`).
- **Paquetes instalados (snapshot `pip list --format=freeze`):**

```
et_xmlfile==2.0.0
numpy==2.5.5
openpyxl==3.1.5
pandas==3.1.1
pip==26.3
pypdf==7.2.0
python-dateutil==4.0.0
tzdata==2026.6
```

- **Uso previsto:** lectura/auditoría/cálculo sobre `.xlsx`, `.csv` y `.pdf` del kit de datos.
- **Limitación:** no existe `requirements.txt` en el proyecto. Se recomienda generarlo para reproducibilidad (`pip freeze > requirements.txt`) si el usuario lo aprueba.

## 5. Estructura de carpetas y reglas de integridad

- `docs_challenge/` y `docs_challenge/taranis_black/`: fuente de entrada (kit oficial). **No modificar ni sobrescribir.**
- `docs_challenge/entregables/`: reservada para documentos revisados/aprobados por el auditor. **No escribir sin instrucción explícita.**
- `docs_agente/`: única carpeta para documentos/borradores generados por el agente.
- `.venv/`: entorno Python (ignorado por Git mediante su `.gitignore` interno).

## 6. Control de versiones (Git)

- **Repositorio:** ya inicializado en la raíz del proyecto.
- **Rama actual:** `main`.
- **Remoto:** `origin` → `https://github.com/Haruki-24/Challenge-Alura-Taranis-Black.git`.
- **Último commit de referencia:** `b30e436` — "Carga de archivos en repositorio principal".
- **Notas:** los archivos de `docs_agente/` se versionarán a medida que se generen. No se realizaron cambios al kit ni a los archivos base.

## 7. Limitaciones y datos no verificados (Auditoría)

- Modelo/proveedor: **Dato no verificado en archivos — confirmado por declaración del usuario.**
- No existe `requirements.txt`: **Dato no disponible / Requiere validación** (recomendado crearlo).
- No existe configuración de OpenCode a nivel de proyecto (`.opencode.json`/similar): **Dato no disponible.**
- Cualquier cifra, hallazgo o causa de negocio deberá respaldarse en los archivos del kit antes de registrarse como evidencia verificada.

## 8. Declaración

Declaro que el entorno descrito corresponde al utilizado para el desarrollo del challenge Taranis Black (Finanzas), y que los archivos originales del kit se mantienen intactos.  
**Responsable de la declaración:** Auditor encargado (usuario).  
**Herramienta:** VS Code + OpenCode (SST).  
**Modelo:** Beam Free (`opencode/beam-free`, declarado).