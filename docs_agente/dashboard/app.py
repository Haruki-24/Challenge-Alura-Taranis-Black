import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Taranis Black - Dashboard Finanzas", layout="wide")

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXCEL = os.path.join(BASE, "docs_challenge", "entregables", "Taranis_Black_Modelo_Gerencial.xlsx")

@st.cache_data
def load_finanzas():
    df = pd.read_excel(EXCEL, sheet_name="Finanzas_P&L", header=3)
    df = df[df["Concepto"].notna()].copy()
    return df

@st.cache_data
def load_produtos():
    df = pd.read_excel(EXCEL, sheet_name="Productos_y_Catalogo", header=4)
    # keep block A rows with numeric presupuestado
    df = df[pd.to_numeric(df["Real anual"], errors="coerce").notna()].copy()
    df = df[~df["Línea de producto"].astype(str).str.upper().str.contains("TOTAL")]
    return df

@st.cache_data
def load_base():
    # read raw to extract section C (cuellos) as text
    df = pd.read_excel(EXCEL, sheet_name="Base_Dados_Finanzas", header=None)
    rows = []
    in_sec = False
    for _, r in df.iterrows():
        v = r.iloc[0]
        if isinstance(v, str) and v.startswith("C)"):
            in_sec = True
            continue
        if in_sec and isinstance(v, str) and v.strip() and v not in ("Métrica Operativa / Financiera",):
            if pd.isna(r.iloc[1]):
                continue
            rows.append({
                "metrica": v,
                "meta": r.iloc[1],
                "real": r.iloc[2],
                "desvio": r.iloc[3],
                "causa": r.iloc[5],
            })
    return pd.DataFrame(rows)

# ---- Header ----
st.title("Taranis Black - Dashboard Finanzas y Operaciones")
st.caption("Fuente: Taranis_Black_Modelo_Gerencial.xlsx (7 pestanas) | Challenge ONE G11 - AI for Business")

# ---- Sidebar filters ----
st.sidebar.header("Filtros")
trimestres = st.sidebar.multiselect("Trimestre", ["T1", "T2", "T3", "T4"], default=["T1", "T2", "T3", "T4"])
linhas = None
prod_df = load_produtos()
linhas = st.sidebar.multiselect("Linea de producto", sorted(prod_df["Línea de producto"].unique().tolist()),
                                default=sorted(prod_df["Línea de producto"].unique().tolist()))
canal = st.sidebar.multiselect("Canal", ["B2B", "D2C"], default=["B2B", "D2C"])

# ---- Load data ----
fin = load_finanzas()

def get_row(concepto):
    sub = fin[fin["Concepto"].astype(str).str.strip() == concepto]
    return sub.iloc[0] if not sub.empty else None

ing_row = get_row("TOTAL DE INGRESOS BRUTOS")
b2b_row = get_row("Ingreso Canal B2B Corporativo (70%)")
d2c_row = get_row("Ingreso Canal D2C / E-commerce (30%)")
ebitda_row = get_row("EBITDA (RESULTADO OPERATIVO ANTES DE JUROS/IMP.)")
lucro_row = get_row("LUCRO LÍQUIDO DEL EXERCICIO")
fletes_row = get_row("Gastos de Fretes y Logística de Entrega CD")
inad_row = get_row("Provisión para deudores Duvidosos (Inadimplencia B2B)")
cancel_row = get_row("Cancelaciones y descartes por Retraso Logístico")

# helper to sum selected trimesters for a row
def sum_tri(row, kind, sel):
    # kind: 'pres' or 'real'; columns T1 Presupuestado / T1 Real etc
    total = 0.0
    for t in sel:
        col = f"{t} {'Presupuestado' if kind == 'pres' else 'Real'}"
        v = row.get(col, 0)
        if pd.notna(v):
            total += float(v)
    return total

# ---- KPIs ----
st.subheader("KPIs consolidados (trimestres selecionados)")
c1, c2, c3, c4, c5 = st.columns(5)
if ing_row is not None:
    ing_pres = sum_tri(ing_row, "pres", trimestres)
    ing_real = sum_tri(ing_row, "real", trimestres)
    c1.metric("Ingresos brutos (Real)", f"USD {ing_real/1e6:,.2f} M", f"{(ing_real/ing_pres-1)*100:+.1f}%" if ing_pres else "")
if ebitda_row is not None:
    eb_real = sum_tri(ebitda_row, "real", trimestres)
    c2.metric("EBITDA (Real)", f"USD {eb_real/1e6:,.2f} M")
if lucro_row is not None:
    lc_real = sum_tri(lucro_row, "real", trimestres)
    c3.metric("Lucro líquido (Real)", f"USD {lc_real/1e6:,.2f} M")
if ing_row is not None and fletes_row is not None:
    fl_real = sum_tri(fletes_row, "real", trimestres)
    c4.metric("Fletes (OPEX) % ingresos", f"{(fl_real/ing_real*100):+.1f}%" if ing_real else "")
if b2b_row is not None and inad_row is not None:
    b2b_real = sum_tri(b2b_row, "real", trimestres)
    inad_real = sum_tri(inad_row, "real", trimestres)
    c5.metric("Inadimplencia B2B %", f"{(inad_real/b2b_real*100):+.1f}%" if b2b_real else "")

# ---- Charts row 1 ----
colA, colB = st.columns(2)
with colA:
    st.subheader("Ingresos brutos: Presupuesto vs. Real")
    if ing_row is not None:
        data = []
        for t in trimestres:
            data.append({"Trimestre": t, "Tipo": "Presupuestado", "USD": float(ing_row[f"{t} Presupuestado"])})
            data.append({"Trimestre": t, "Tipo": "Real", "USD": float(ing_row[f"{t} Real"])})
        ddf = pd.DataFrame(data)
        fig = px.bar(ddf, x="Trimestre", y="USD", color="Tipo", barmode="group",
                     color_discrete_map={"Presupuestado": "#2E5C8A", "Real": "#A6A6A6"})
        fig.update_layout(yaxis_title="USD", height=320)
        st.plotly_chart(fig, width="stretch")

with colB:
    st.subheader("EBITDA por trimestre")
    if ebitda_row is not None:
        data = []
        for t in trimestres:
            data.append({"Trimestre": t, "Tipo": "Presupuestado", "USD": float(ebitda_row[f"{t} Presupuestado"])})
            data.append({"Trimestre": t, "Tipo": "Real", "USD": float(ebitda_row[f"{t} Real"])})
        ddf = pd.DataFrame(data)
        fig = px.line(ddf, x="Trimestre", y="USD", color="Tipo", markers=True,
                      color_discrete_map={"Presupuestado": "#2E5C8A", "Real": "#C00000"})
        fig.update_layout(yaxis_title="USD", height=320)
        st.plotly_chart(fig, width="stretch")

# ---- Products ----
st.subheader("Ingresos y margen por línea de producto")
pdf_prod = load_produtos()
if linhas:
    pdf_prod = pdf_prod[pdf_prod["Línea de producto"].isin(linhas)]
st.dataframe(pdf_prod[["Línea de producto", "Participación (%)", "Presupuestado anual",
                       "Real anual", "Variación (%)", "Margen bruto medio",
                       "Cuello de botella principal observado"]], width="stretch")

colC, colD = st.columns(2)
with colC:
    st.subheader("Margen bruto por línea")
    fig = px.bar(pdf_prod, x="Línea de producto", y="Margen bruto medio", color="Línea de producto")
    fig.update_layout(yaxis_tickformat=".1%", height=300, showlegend=False)
    st.plotly_chart(fig, width="stretch")
with colD:
    st.subheader("Ingresos Real por línea")
    fig = px.pie(pdf_prod, names="Línea de producto", values="Real anual", hole=0.4)
    fig.update_layout(height=300)
    st.plotly_chart(fig, width="stretch")

# ---- OPEX ----
st.subheader("OPEX por categoría (trimestres selecionados)")
opex_rows = []
for name, row in [("Fletes y logística", fletes_row), ("Cancelaciones/reentregas", cancel_row),
                   ("Gastos admin. y sistemas", get_row("Gastos administrativos y sistemas Legados")),
                   ("Inadimplencia (PDD)", inad_row),
                   ("Marketing", get_row("Marketing Institucional y Generación de Demanda")),
                   ("Gastos comerciales", get_row("Gastos comerciales y ventas (Comisiones y SDRs)"))]:
    if row is not None:
        opex_rows.append({"Categoría": name, "USD": sum_tri(row, "real", trimestres)})
opex_df = pd.DataFrame(opex_rows)
if not opex_df.empty:
    fig = px.bar(opex_df, x="Categoría", y="USD", color="Categoría")
    fig.update_layout(height=320, showlegend=False, yaxis_title="USD")
    st.plotly_chart(fig, width="stretch")

# ---- Operativo ----
st.subheader("Métricas operativas y SLA")
base_df = load_base()
if not base_df.empty:
    st.dataframe(base_df, width="stretch")

# ---- DQ ----
st.subheader("Calidad de datos (DQ) - resumen")
dq = pd.read_excel(EXCEL, sheet_name="Control_Calidad_DQ", header=3)
# summary block is below; read raw
raw = pd.read_excel(EXCEL, sheet_name="Control_Calidad_DQ", header=None)
summ = []
for i in range(len(raw)):
    a = raw.iloc[i, 0]
    b = raw.iloc[i, 1]
    if isinstance(a, str) and a.strip() and not (isinstance(b, float) and pd.isna(b)):
        if a not in ("data_carga",):
            summ.append({"Métrica": a, "Valor": str(b)})
if summ:
    st.dataframe(pd.DataFrame(summ), width="stretch")

# ---- Footer ----
st.markdown("---")
st.caption("Fuente de datos: docs_challenge/entregables/Taranis_Black_Modelo_Gerencial.xlsx | "
           "Trazabilidad: docs_agente/historial_prompts.md | Declaración de entorno: docs_agente/00_entorno_y_configuracion.md")