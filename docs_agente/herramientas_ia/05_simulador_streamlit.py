import os, re, json
import streamlit as st

st.set_page_config(page_title="Simulador de Triaje - Taranis Black", layout="wide")

st.title("Simulador de Triaje y Estandarizacion de Email")
st.caption("Simula la entrada de un correo/propuesta y ejecuta triaje + validacion R1-R9 + correo estandarizado (sin n8n).")

# ---- Example proposal ----
EXEMPLO = """Prezados,
Segue proposta comercial para aquisicao de 10 cadeiras Taranis ErgoPro Executive (codigo ERG-EXEC)
para a empresa Acme Corp Ltda, CNPJ 12.345.678/0001-90, IE 123.456.789, endereco Rua Demo 100, Sao Paulo/SP.
Valor unitario: USD 3.490,00. Total: USD 34.900,00.
Condicao de pagamento: 30 dias. FOB.
Data de entrega solicitada: 2026-02-15.
Vendedor: Carlos Silva.
"""

texto = st.text_area("Texto da proposta / correo", value=EXEMPLO, height=200)

col1, col2 = st.columns(2)
with col1:
    n8n_url = st.text_input("URL webhook n8n (opcional)", value="", placeholder="http://localhost:5678/webhook/triaje")
with col2:
    modo = st.selectbox("Modo", ["Demo (local)", "Integrado (webhook n8n)"])

def extract(text):
    d = {}
    # CNPJ
    m = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', text)
    d['cliente_cnpj'] = m.group(0) if m else None
    # IE
    m = re.search(r'IE\s*[: ]*\s*([\d\.\-]+)', text, re.IGNORECASE)
    d['ie'] = m.group(1).strip() if m else None
    # Razao social (heuristica: empresa X Ltda/Corp/SA)
    m = re.search(r'empresa\s+([A-Za-zÀ-ÿ\s]+(?:Ltda|Corp|SA|Inc|LLC))', text, re.IGNORECASE)
    d['cliente_razao'] = m.group(1).strip() if m else None
    # Endereco
    m = re.search(r'endereco\s+([^\.]+)', text, re.IGNORECASE)
    d['direccion'] = m.group(1).strip() if m else None
    # Codigo produto
    m = re.search(r'codigo\s+([A-Z0-9\-]+)', text, re.IGNORECASE)
    d['produto_codigo'] = m.group(1).strip() if m else None
    # Quantidade
    m = re.search(r'(\d+)\s*(?:cadeiras|unidades|un\.|pcs)', text, re.IGNORECASE)
    d['quantidade'] = int(m.group(1)) if m else None
    # Valor unitario
    m = re.search(r'Valor unitario:\s*USD\s*([\d\.,]+)', text, re.IGNORECASE)
    d['valor_unit'] = float(m.group(1).replace('.', '').replace(',', '.')) if m else None
    # Valor total
    m = re.search(r'Total:\s*USD\s*([\d\.,]+)', text, re.IGNORECASE)
    d['valor_total'] = float(m.group(1).replace('.', '').replace(',', '.')) if m else None
    # Condicao pagamento
    m = re.search(r'Condicao de pagamento:\s*(\d+)', text, re.IGNORECASE)
    d['condicao_pagamento'] = m.group(1) if m else None
    # CIF/FOB
    m = re.search(r'\b(CIF|FOB)\b', text, re.IGNORECASE)
    d['cif_fob'] = m.group(1).upper() if m else None
    # Data entrega
    m = re.search(r'Data de entrega solicitada:\s*(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
    d['data_entrega'] = m.group(1) if m else None
    # Vendedor
    m = re.search(r'Vendedor:\s*([A-Za-zÀ-ÿ\s]+)', text, re.IGNORECASE)
    d['vendedor'] = m.group(1).strip() if m else None
    return d

def validar(d):
    errors = []
    # R1 CNPJ
    if not d.get('cliente_cnpj'):
        errors.append('R1: CNPJ faltante')
    else:
        if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', d['cliente_cnpj']):
            errors.append('R1: formato de CNPJ invalido')
    # R2 IE
    if not d.get('ie'):
        errors.append('R2: IE faltante')
    # R3 Razao social
    if not d.get('cliente_razao'):
        errors.append('R3: Razon social faltante')
    # R4 Direccion
    if not d.get('direccion'):
        errors.append('R4: Direccion faltante')
    # R5 Codigo produto
    if not d.get('produto_codigo'):
        errors.append('R5: Codigo de producto faltante')
    # R6 Quantidade / valor
    if not d.get('quantidade') or d['quantidade'] <= 0:
        errors.append('R6: Cantidad invalida')
    if not d.get('valor_unit') or d['valor_unit'] <= 0:
        errors.append('R6: Valor unitario invalido')
    if not d.get('valor_total') or d['valor_total'] <= 0:
        errors.append('R6: Valor total invalido')
    # R7 Condicao pagamento
    if d.get('condicao_pagamento') not in ('30', '60', '90'):
        errors.append('R7: Condicion de pago invalida (30/60/90)')
    # R8 CIF/FOB
    if d.get('cif_fob') not in ('CIF', 'FOB'):
        errors.append('R8: CIF/FOB invalido')
    # R9 Completude
    campos_obrig = ['cliente_cnpj', 'cliente_razao', 'ie', 'direccion', 'produto_codigo', 'quantidade', 'valor_unit', 'valor_total', 'condicao_pagamento', 'cif_fob', 'vendedor']
    faltantes = [c for c in campos_obrig if not d.get(c)]
    if faltantes:
        errors.append('R9: Campos obligatorios faltantes: ' + ', '.join(faltantes))
    return errors

def clasificar(d):
    valor = d.get('valor_total') or 0
    if valor > 50000:
        return 'Urgente'
    if valor > 10000:
        return 'Alta'
    return 'Normal'

def correo_estandarizado(d, erros, prioridad):
    status = 'Validado' if not erros else 'Excecao'
    resumo_rag = 'Solicitud clasificada como ' + prioridad + '. ' + ('Sin campos faltantes.' if not erros else 'Campos faltantes: ' + ', '.join(erros))
    return f"""Asunto: [TRIAGE] {d.get('cliente_razao','N/A')} - USD {d.get('valor_total','N/A')} - Prioridad: {prioridad}

Empresa: {d.get('cliente_razao','N/A')} (CNPJ: {d.get('cliente_cnpj','N/A')})
IE: {d.get('ie','N/A')} | Direccion: {d.get('direccion','N/A')}
Producto: {d.get('produto_codigo','N/A')} ({d.get('quantidade','N/A')} un. x USD {d.get('valor_unit','N/A')})
Valor total: USD {d.get('valor_total','N/A')}
Condicion de pago: {d.get('condicao_pagamento','N/A')} dias
Flete: {d.get('cif_fob','N/A')}
Fecha de entrega solicitada: {d.get('data_entrega','N/A')}
Vendedor: {d.get('vendedor','N/A')}

Validaciones R1-R9: {status}
Clasificacion: {'B2B Corporativo' if d.get('cliente_cnpj') else 'D2C'} | Prioridad: {prioridad}

Resumen (RAG): {resumo_rag}

---
Este correo fue generado automaticamente por el flujo de triaje de Taranis Black.
Supervision humana requerida para excepciones.
"""

if st.button("Procesar propuesta"):
    d = extract(texto)
    erros = validar(d)
    prioridad = clasificar(d)
    email = correo_estandarizado(d, erros, prioridad)

    st.subheader("Datos extraidos")
    st.json(d)

    st.subheader("Clasificacion y prioridad")
    c1, c2 = st.columns(2)
    c1.metric("Tipo", "B2B Corporativo" if d.get('cliente_cnpj') else "D2C / Otro")
    c2.metric("Prioridad", prioridad)

    st.subheader("Validaciones R1-R9")
    if erros:
        for e in erros:
            st.error(e)
    else:
        st.success("Todas las validaciones pasaron (R1-R9 OK)")

    st.subheader("Correo estandarizado generado")
    st.code(email, language="text")

    if modo == "Integrado (webhook n8n)" and n8n_url:
        import requests
        try:
            payload = {"texto": texto, "dados": d, "prioridad": prioridad, "erros": erros}
            resp = requests.post(n8n_url, json=payload, timeout=10)
            st.success(f"Enviado a n8n: HTTP {resp.status_code}")
            st.json(resp.json() if resp.headers.get('content-type','').startswith('application/json') else {"response": resp.text})
        except Exception as e:
            st.error(f"Error al enviar a n8n: {e}")
    else:
        st.info("Modo demo: no se envio a n8n. Activa el modo integrado para enviar el payload.")

st.markdown("---")
st.caption("Simulador de triaje - Taranis Black | Fuentes: docs_agente/herramientas_ia/ | Trazabilidad: docs_agente/historial_prompts.md")