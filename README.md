<h1 align="center">📊 Projeto de Análise de Produção Industrial</h1>

<h3 align="center">
Automação de geração de relatórios, classificação de produção e análise de anomalias com Python.
</h3>

---

## 🎯 Objetivo
Este projeto simula a produção industrial de diferentes máquinas ao longo de turnos, aplicando técnicas de **Data Analytics** para:  
- Classificar a produção como **Alta, Média ou Baixa** com base em metas definidas.  
- Detectar **anomalias** quando a produção não atinge o mínimo esperado.  
- Calcular **médias móveis** e **previsões** para auxiliar na tomada de decisão.  
- Gerar **relatórios automatizados em Excel** e dashboards interativos via Streamlit.

O objetivo é fornecer uma visão completa da produção, permitindo identificar problemas, tendências e oportunidades de melhoria.

---

## 🛠 Tecnologias e Bibliotecas Utilizadas
- **Python 3.x** – Linguagem principal
- **Pandas** – Manipulação e análise de dados
- **NumPy** – Operações matemáticas
- **scikit-learn** – Modelo de regressão linear para previsão
- **Streamlit** – Dashboard interativo
- **OpenPyXL** – Geração de relatórios em Excel
- **Datetime** – Manipulação de datas e horários

---

## ⚙ Funcionalidades

1. **Geração de Dados Simulados**  
   - Produção diária de 3 máquinas (`M1`, `M2`, `M3`) em 3 turnos (`Manhã`, `Tarde`, `Noite`).  
   - Produção com variação aleatória para simular a realidade industrial.

2. **Classificação da Produção**  
   - **Alta:** produção >= 14.000 kg  
   - **Média:** produção entre 11.000 kg e 14.000 kg  
   - **Baixa:** produção < 11.000 kg  

3. **Detecção de Anomalias**  
   - Marca "Sim" quando a produção é **Baixa**, indicando que não atingiu o mínimo esperado.

4. **Média Móvel e Previsão**  
   - Média móvel de 3 períodos para análise de tendência.  
   - Regressão linear para prever a produção futura.

5. **Relatório Automatizado**  
   - Planilha Excel com todas as informações: data, máquina, turno, produção, categoria, média móvel, média geral, anomalia e previsão.  
   - Resumo por máquina com produção total.

6. **Dashboard Interativo (Streamlit)**  
   - Filtros por máquina e turno.  
   - KPIs de produção total, média móvel, média geral e máximo.  
   - Gráficos de produção ao longo do tempo e por máquina.  
   - Tabela detalhada com todos os dados.

---


