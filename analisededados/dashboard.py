import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Dashboard Produção", layout="wide")
st.title("📊 Dashboard de Produção Industrial")

# =========================
# CARREGAR DADOS
# =========================
@st.cache_data(ttl=5)
def carregar_dados():
    df = pd.read_excel("saida/relatorio.xlsx")
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df = df.sort_values("data")
    return df

df = carregar_dados()

# =========================
# FILTROS
# =========================
st.sidebar.header("🔎 Filtros")
maquinas = st.sidebar.multiselect("Máquina", options=df["maquina"].unique(), default=df["maquina"].unique())
turnos = st.sidebar.multiselect("Turno", options=df["turno"].unique(), default=df["turno"].unique())
df_filtrado = df[(df["maquina"].isin(maquinas)) & (df["turno"].isin(turnos))]

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)
producao_total = df_filtrado["producao"].sum()
media_movel = df_filtrado["media_movel"].iloc[-1]
media_geral = df_filtrado["media_geral"].iloc[0]  # agora existe no Excel
maximo = df_filtrado["producao"].max()

col1.metric("🏭 Produção Total", f"{producao_total:,.0f} kg")
col2.metric("📈 Média Móvel", f"{media_movel:,.0f} kg")
col3.metric("📊 Média Geral", f"{media_geral:,.0f} kg")
col4.metric("🚀 Máximo", f"{maximo:,.0f} kg")

# =========================
# GRÁFICO
# =========================
st.subheader("📈 Produção ao longo do tempo")
st.line_chart(df_filtrado.set_index("data")[["producao", "media_movel", "media_geral"]])

# =========================
# PRODUÇÃO POR MÁQUINA
# =========================
st.subheader("🏭 Produção por Máquina")
prod_maquina = df_filtrado.groupby("maquina")["producao"].sum()
st.bar_chart(prod_maquina)

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")
st.dataframe(df_filtrado)