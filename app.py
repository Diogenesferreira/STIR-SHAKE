import streamlit as st
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import base64
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
import random
import warnings

pd.set_option("display.max_columns", None)
warnings.filterwarnings('ignore')

import pandas as pd
import glob

def load_csv_file(file_path):
    return pd.read_csv(file_path, encoding='iso-8859-1', sep=';')



def example():
    colored_header(
        label="POC STIR SHAKE - ATN X TIM",
        description="Relatório dedicado a compartilhar os dados brutos de discagem do Projeto Stir-Shake",
        color_name="blue-70",
    )

example()

def report_final():
    analysis_report = """
## Observação Inicial

Antes de apresentar a análise detalhada dos dados, é importante destacar que o lead utilizado para ambas as rotas foi o mesmo, seguindo a mesma quantidade, ordem e estratégia, garantindo uma medição justa dos resultados. Além disso, é relevante mencionar que a forma como utilizamos a base de dados foi um "one shot", termo utilizado pela nossa equipe para bases em que realizamos apenas uma discagem, visando evitar o estresse de um possível cliente em potencial, de uma base com alta conversão.

## Análise dos Dados

Nesta seção, analisamos a performance das rotas 0303 e Stir Shake em relação ao interesse em atendimento (%ALÔ) e discagem.

### Interesse em Atendimento (%ALÔ)

- **Rota 0303:** O percentual de interesse em atendimento foi de 2.68%.
- **Stir Shake:** O percentual de interesse em atendimento foi de 3.44%.

**Diferença:** A rota Stir Shake apresentou um percentual de interesse em atendimento significativamente maior em comparação com a rota 0303, com uma diferença de 0.76 pontos percentuais.

### Alô ou Interesse em atendimento

- **Rota 0303:** O volume de alô foi de 2171.
- **Stir Shake:** O volume de alô foi de 2810.

**Diferença:** Embora o volume de atendimento na rota Stir Shake tenha sido maior, a diferença absoluta em relação à rota 0303 foi de 639 chamadas.

### Estimativa de Melhoria Percentual

**Observação:** É importante ressaltar que a tecnologia subjacente ainda está em fase de ajustes e melhorias contínuas. Além disso, a análise atual considera o fato de que o 0303 ainda está sendo binado no lugar do DDR. Futuras mudanças, como a remoção efetiva do 0303, podem resultar em melhorias significativas no desempenho das métricas analisadas.
"""

    return analysis_report

st.markdown(report_final())



# Carregar os DataFrames
stirshaken_df = load_csv_file("Stir_Shaken.csv")  # Substitua "stirshaken.csv" pelo nome do arquivo Stir Shaken
stirshaken_detalhado_df = load_csv_file("poc_disc.csv")  # Substitua "detalhado.csv" pelo nome do arquivo detalhado


# Função para baixar o DataFrame em formato CSV
def download_df(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados_discagem.csv">Baixar base de discagem</a>'
    return href


# Mensagem de aviso e botão de download
st.write('Caso seja necessário, baixe a base detalhada de discagem no botão abaixo:')
st.markdown(download_df(stirshaken_detalhado_df), unsafe_allow_html=True)

style_metric_cards()


# Adicionando espaço entre o cabeçalho e as métricas
st.write("")

# Colunas para as métricas
col_metric_1, col_metric_2, col_metric_3, col_metric_4, col_metric_5   = st.columns([4, 4, 4, 4, 4])

# Métricas na primeira linha
qtd_discado = '{:,.0f}'.format(stirshaken_df.loc[0, 'DISCADO']).replace(',', '.')
with col_metric_1:
    st.metric(label="DISCADO", value=qtd_discado, delta=qtd_discado, delta_color="off")

qtd_alo_stirshaken = '{:,.0f}'.format(stirshaken_df.loc[0, 'ALÔ URA']).replace(',', '.')
with col_metric_2:
    st.metric(label="ALÔ", value=qtd_alo_stirshaken, delta=-2171)

alo_percent = stirshaken_df.loc[0, '%ALÔ']
alo_percent_str = '{:.2f}%'.format(alo_percent)
with col_metric_3:
    st.metric(label="%ALO", value=alo_percent_str, delta=-2.78)

interesse_tranfer = stirshaken_df.loc[0, 'TRAN_AG']
with col_metric_4:
    st.metric(label="INTERESSE", value=interesse_tranfer, delta=-51)

interesse_percent = stirshaken_df.loc[0, '%DTMF']
interesse_percent_str = '{:.2f}%'.format(interesse_percent)
with col_metric_5:
    st.metric(label="PRODUÇÃO", value=interesse_percent_str, delta=2.35)



st.write('---')

# Criando gráficos de pizza para ALÔ URA e %DTMF
fig1 = px.pie(stirshaken_df, values='ALÔ URA', names='TIPO_BASE', title='INTERESSE EM ATENDER A BINA', color_discrete_sequence=px.colors.qualitative.Pastel)
fig2 = px.pie(stirshaken_df, values='%DTMF', names='TIPO_BASE', title='INTERESSE NA COMPRA APÓS ATENDIMENTO', color_discrete_sequence=px.colors.qualitative.Pastel)

# Exibindo os gráficos lado a lado em colunas
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)


# Exibindo o título da tabela com tamanho reduzido
st.markdown("<h2 style='text-align: center;'>VISÃO TABELA</h2>", unsafe_allow_html=True)

# Exibindo a tabela
st.table(stirshaken_df)

# Função para criar o quadro explicativo com a análise final
