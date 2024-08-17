import pandas as pd
import streamlit as st
import plotly.express as px
def mudar_nome(nome):
    if nome == 1:
        return 'Não Respondeu'
    elif nome == 2:
        return 'Pública'
    elif nome == 3:
        return 'Privada'
    return nome

def mudar_valor_sexo(sexo):
    if sexo == "M":
        return 'Masculino'
    return "Feminino"

def choice_select(choice):
    if choice == "Linguagens, Códigos e suas Tecnologias":
        return 'NU_NOTA_LC'
    elif choice == "Matemática e suas Tecnologias":
        return "NU_NOTA_MT"
    elif choice == "Ciências da Natureza e suas Tecnologias":
        return "NU_NOTA_CN"
    elif choice == "Ciências Humanas e suas Tecnologias":
        return "NU_NOTA_CH"
    return "NU_NOTA_REDACAO"


areas_enem = [
    "Linguagens, Códigos e suas Tecnologias" ,
    "Matemática e suas Tecnologias",
    "Ciências da Natureza e suas Tecnologias",
    "Ciências Humanas e suas Tecnologias",
    "Redação",
]

faixa_etaria_labels = {
    1: "Menor de 17 anos",
    2: "17 anos",
    3: "18 anos",
    4: "19 anos",
    5: "20 anos",
    6: "21 anos",
    7: "22 anos",
    8: "23 anos",
    9: "24 anos",
    10: "25 anos",
    11: "Entre 26 e 30 anos",
    12: "Entre 31 e 35 anos",
    13: "Entre 36 e 40 anos",
    14: "Entre 41 e 45 anos",
    15: "Entre 46 e 50 anos",
    16: "Entre 51 e 55 anos",
    17: "Entre 56 e 60 anos",
    18: "Entre 61 e 65 anos",
    19: "Entre 66 e 70 anos",
    20: "Maior de 70 anos",
}

faixas_renda = {
    'Q': 'Mais de R$ 19.960,00',
    'P': 'De R$ 14.970,01 até R$ 19.960,00',
    'O': 'De R$ 11.976,01 até R$ 14.970,00',
    'N': 'De R$ 9.980,01 até R$ 11.976,00',
    'M': 'De R$ 8.982,01 até R$ 9.980,00',
    'L': 'De R$ 7.984,01 até R$ 8.982,00',
    'K': 'De R$ 6.986,01 até R$ 7.984,00',
    'J': 'De R$ 5.988,01 até R$ 6.986,00',
    'I': 'De R$ 4.990,01 até R$ 5.988,00',
    'H': 'De R$ 3.992,01 até R$ 4.990,00',
    'G': 'De R$ 2.994,01 até R$ 3.992,00',
    'F': 'De R$ 2.495,01 até R$ 2.994,00',
    'E': 'De R$ 1.996,01 até R$ 2.495,00',
    'D': 'De R$ 1.497,01 até R$ 1.996,00',
    'C': 'De R$ 998,01 até R$ 1.497,00',
    'B': 'Até R$ 998,00',
    'A': 'Nenhuma renda.'
}


nivel_educacional = {
    'A': 'Nunca estudou.',
    'B': 'Não completou a 4ª série/5º ano do Ensino Fundamental.',
    'C': 'Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.',
    'D': 'Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.',
    'E': 'Completou o Ensino Médio, mas não completou a Faculdade.',
    'F': 'Completou a Faculdade, mas não completou a Pós-graduação.',
    'G': 'Completou a Pós-graduação.',
    'H': 'Não sei.'
}


st.set_page_config(layout="wide")
st.title(
    "Análise dos Dados do ENEM 2019: Um Foco em Feira de Santana",
)
df = pd.read_csv("ENEM_FEIRA_DE_SANTANA.csv", encoding="utf-8", sep=",")
# df = pd.read_csv("MICRODADOS_ENEM_2019.csv", encoding="ISO-8859-1", sep=";")
# filtered_df = df.query('NO_MUNICIPIO_PROVA == "Feira de Santana"')
# filtered_df.to_csv("ENEM_FEIRA_DE_SANTANA.csv")
df["media"] = df[
    ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
].mean(axis=1)

df["TP_ESCOLA"] = df["TP_ESCOLA"].apply(mudar_nome)
df["TP_SEXO"] = df["TP_SEXO"].apply(mudar_valor_sexo)
#st.dataframe(df)


fig = px.pie(
    df,
    names="TP_SEXO",
    title="Proporção de candidatos por gênero",
    labels={"TP_SEXO": "SEXO"},
)



# Conta a quantidade de participantes em cada faixa etária
faixa_etaria_counts = df["TP_FAIXA_ETARIA"].value_counts().sort_index()
df['Q006'] = df['Q006'].map(faixas_renda)
# Substitui os valores numéricos pelas descrições das faixas etárias
faixa_etaria_counts.index = faixa_etaria_counts.index.map(faixa_etaria_labels)
df_filtrado = df.loc[df['TP_ESCOLA'] != 'Não Respondeu']

# Agrupar e calcular a média para as categorias do pai
media_por_categoria_pai = df.groupby('Q001')['media'].mean().reset_index()
media_por_categoria_pai.columns = ['Categoria', 'Media']
media_por_categoria_pai['Descricao'] = media_por_categoria_pai['Categoria'].map(nivel_educacional)
media_por_categoria_pai['Tipo'] = 'Pai'  # Identificar que é a linha do pai

# Agrupar e calcular a média para as categorias da mãe
media_por_categoria_mae = df.groupby('Q002')['media'].mean().reset_index()
media_por_categoria_mae.columns = ['Categoria', 'Media']
media_por_categoria_mae['Descricao'] = media_por_categoria_mae['Categoria'].map(nivel_educacional)
media_por_categoria_mae['Tipo'] = 'Mãe'  # Identificar que é a linha da mãe
media_por_categoria = pd.concat([media_por_categoria_pai, media_por_categoria_mae])
#media_por_categoria = df_filtrado.groupby('Q001')['media'].mean().reset_index()
#media_por_categoria.columns = ['Categoria', 'Media']
#media_por_categoria['Descricao'] = media_por_categoria['Categoria'].map(nivel_educacional)
# Cria o gráfico de barras
fig1 = px.bar(
    faixa_etaria_counts,
    x=faixa_etaria_counts.values,  # Quantidade de idades (frequência)
    y=faixa_etaria_counts.index,  # Faixas etárias
    orientation="h",  # Gráfico horizontal
    title="Distribuição por Faixa Etária",
    labels={"x": "Quantidade de Participantes", "TP_FAIXA_ETARIA": "Faixa Etária"},
)
fig1.update_layout(
    yaxis_title="Faixa Etária",
    yaxis=dict(
        tickmode="linear",
        tickvals=faixa_etaria_counts.index,
    )
)
fig2 = px.box(
    df,
    x="TP_SEXO",
    y="media",
    title="Média das provas por sexo",
    labels={"TP_SEXO": "Sexo", "media": "Média", "M": "masculino"},
)
fig3 = px.box(
    df_filtrado,
    x="TP_ESCOLA",
    y="media",
    title="Média das provas por tipo de escolaridade",
    labels={"TP_ESCOLA": "Rede de ensino", "media": "Média das Notas", "M": "masculino"},
)

fig4 = px.pie(df_filtrado, names="TP_ESCOLA", hole=.3,title="Proporção por tipo de Escolaridade", labels={"TP_ESCOLA": "Rede de Ensino"})

col1, col2 = st.columns(2)

choice = st.selectbox("Selecione a área", areas_enem)
select = choice_select(choice)
fig5 = px.ecdf(df_filtrado, y= select, color="TP_ESCOLA", ecdfnorm = None, labels={ "TP_ESCOLA": "Rede de ensino", "NU_NOTA_LC":"Nota Linguagens, Códigos e suas Tecnologias" ,
    "NU_NOTA_MT":"Nota Matemática e suas Tecnologias",
    "NU_NOTA_CN" : "Nota Ciências da Natureza e suas Tecnologias",
    "NU_NOTA_CH" : "Nota Ciências Humanas e suas Tecnologias",
    "NU_NOTA_REDACAO" : "Nota Redação"})
fig6 = px.histogram(df, y="Q006", x="media",histfunc='avg',  category_orders={"Q006": faixas_renda.values()}, title="Média das Notas do ENEM por Faixa de Renda Familiar", labels= {"Q006": "Renda Familiar"}) 
fig6.update_xaxes(title_text="Média das Notas")
fig7 = px.line(media_por_categoria, x="Categoria",color="Tipo", y="Media", title="Média das Notas do ENEM por Grau de escolaridade dos pais", hover_data={"Descricao": True}, markers= True)
st.plotly_chart(fig5)


col3, col4 = st.columns(2)
col1.plotly_chart(fig)
col2.plotly_chart(fig2)
col3.plotly_chart(fig3)
col4.plotly_chart(fig4)
st.plotly_chart(fig1)
col5, col6 = st.columns(2)
col5.plotly_chart(fig7)
col6.plotly_chart(fig6)

    

