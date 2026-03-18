import pandas as pd 
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# ================================
# CONFIGURAÇÕES
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(BASE_DIR, "saida")
os.makedirs(PASTA_SAIDA, exist_ok=True)
print("📁 Pasta de saída:", PASTA_SAIDA)

# ================================
# GERAR HORÁRIO POR TURNO 🔥
# ================================
def gerar_horario(row):
    data_base = row["data"]
    turno = str(row.get("turno", "")).lower()

    if "noite" in turno:
        inicio1 = datetime.combine(data_base, datetime.strptime("23:00", "%H:%M").time())
        fim1 = datetime.combine(data_base, datetime.strptime("23:59", "%H:%M").time())
        inicio2 = datetime.combine(data_base + timedelta(days=1), datetime.strptime("00:00", "%H:%M").time())
        fim2 = datetime.combine(data_base + timedelta(days=1), datetime.strptime("07:10", "%H:%M").time())
        inicio, fim = (inicio1, fim1) if np.random.rand() < 0.5 else (inicio2, fim2)
    elif "manhã" in turno or "manha" in turno:
        inicio = datetime.combine(data_base, datetime.strptime("07:10", "%H:%M").time())
        fim = datetime.combine(data_base, datetime.strptime("15:10", "%H:%M").time())
    else:  # tarde
        inicio = datetime.combine(data_base, datetime.strptime("15:10", "%H:%M").time())
        fim = datetime.combine(data_base, datetime.strptime("23:10", "%H:%M").time())

    delta = int((fim - inicio).total_seconds())
    segundos = np.random.randint(0, delta)
    return inicio + timedelta(seconds=segundos)

# ================================
# 1. GERAR DADOS (GARANTINDO MÁQUINAS)
# ================================
def carregar_dados():
    maquinas = ["M1", "M2", "M3"]
    produtos = ["Produto A", "Produto B", "Produto C"]
    turnos = ["Manhã", "Tarde", "Noite"]
    datas = pd.date_range(start="2026-01-01", periods=30, freq="D")

    registros = []

    # Garantir pelo menos 7 registros por máquina
    for maquina in maquinas:
        for _ in range(7):
            data = np.random.choice(datas)
            produto = np.random.choice(produtos)
            turno = np.random.choice(turnos)
            registros.append({"data": data, "maquina": maquina, "produto": produto, "turno": turno})

    df = pd.DataFrame(registros)
    df["data"] = df.apply(gerar_horario, axis=1)
    df = df.sort_values("data").reset_index(drop=True)

    # Simulação de produção
    base_maquina = {"M1": 16000, "M2": 15000, "M3": 14000}
    ajuste_turno = {"Manhã": 1.0, "Tarde": 0.95, "Noite": 0.85}
    producoes = []

    for _, row in df.iterrows():
        base = base_maquina.get(row["maquina"], 15000)
        fator_turno = ajuste_turno.get(row["turno"], 1.0)
        valor = np.random.normal(base * fator_turno, 1500)
        if np.random.rand() < 0.05:
            valor *= 0.6
        producoes.append(valor)

    df["producao"] = pd.Series(producoes).clip(lower=10000, upper=20000).astype(int)
    df["media_geral"] = df["producao"].mean()  # média geral constante

    return df

# ================================
# 2. CLASSIFICAÇÃO COM NOVA LÓGICA
# ================================
MINIMO = 11000  # valor mínimo exigido para produção

def classificar(valor):
    if valor >= 14000:
        return "Alta"
    elif valor >= MINIMO:
        return "Média"
    else:
        return "Baixa"

# ================================
# 3. MÉDIA MÓVEL
# ================================
def calcular_media_movel(df):
    df["media_movel"] = df["producao"].rolling(3, min_periods=1).mean()
    return df

# ================================
# 4. ANOMALIAS BASEADA NA CATEGORIA
# ================================
def detectar_anomalias(df):
    df["anomalia"] = df["categoria"].apply(lambda x: "Sim" if x == "Baixa" else "Não")
    return df

# ================================
# 5. PREVISÃO
# ================================
def prever(df):
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["producao"].values
    modelo = LinearRegression()
    modelo.fit(X, y)
    df["previsao"] = modelo.predict(X)
    return df

# ================================
# 6. RELATÓRIO
# ================================
def salvar_relatorio(df):
    caminho = os.path.join(PASTA_SAIDA, "relatorio.xlsx")
    df_formatado = df.sort_values("data").reset_index(drop=True).copy()
    df_formatado["data"] = df_formatado["data"].dt.strftime("%d/%m/%Y %H:%M:%S")
    df_formatado["media_movel"] = df_formatado["media_movel"].round(2)
    df_formatado["previsao"] = df_formatado["previsao"].round(2)

    # Colunas finais no Excel
    df_formatado = df_formatado[[
        "data", "maquina", "produto", "turno",
        "producao", "categoria", "media_movel",
        "media_geral",
        "anomalia", "previsao"
    ]]

    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        df_formatado.to_excel(writer, index=False, sheet_name="Dados")
        resumo = df.groupby("maquina")["producao"].sum().reset_index()
        resumo.columns = ["Máquina", "Produção Total"]
        resumo.to_excel(writer, index=False, sheet_name="Resumo")

# ================================
# EXECUÇÃO
# ================================
def main():
    print("🔄 Iniciando análise...")
    df = carregar_dados()
    df["categoria"] = df["producao"].apply(classificar)
    df = calcular_media_movel(df)
    df = detectar_anomalias(df)
    df = prever(df)
    salvar_relatorio(df)
    print("✅ Finalizado!")
    print(f"📁 Arquivos salvos na pasta: {PASTA_SAIDA}")

if __name__ == "__main__":
    main()
    os.system("streamlit run dashboard.py")