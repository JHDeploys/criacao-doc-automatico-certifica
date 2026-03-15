import streamlit as st
import pandas as pd

from metodos_auxiliares import ler_arquivo, baixar_excel
from metodos_criar_graf_tab import (
    agrupar_tabelas,
    criar_graf_barras_lado
)
from agentes_graf_tab import criar_title_graf

# ======================================================
# 🔹 Inicialização global do session_state (OBRIGATÓRIA)
# ======================================================
def init_session_state():
    defaults = {
        "df": None,
        "nome_arquivo": None,

        # Documento final
        "tabelas_doc_questoes": [],
        "graficos_doc_questoes": [],
        "tabelas_doc_localidades": [],
        "graficos_doc_localidades": [],

        # UI
        "contador_cruzamentos": 1
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ======================================================
# 🔹 Funções utilitárias de salvamento (PADRONIZADAS)
# ======================================================
def salvar_tabela(lista_destino, pagina, titulo, df_doc):
    lista_destino.append({
        "pagina": pagina,
        "titulo": titulo,
        "tabela": df_doc.copy(),
        "interpretacao": ""
    })


def salvar_grafico(lista_destino, pagina, titulo, grafico):
    lista_destino.append({
        "pagina": pagina,
        "titulo": titulo,
        "grafico": grafico,
        "interpretacao": ""
    })


# ======================================================
# 🧹 Limpeza CONTROLADA (não automática!)
# ======================================================
def limpar_estado_cruzamentos():
    for chave in [
        "tabelas_doc_questoes",
        "graficos_doc_questoes",
        "tabelas_doc_localidades",
        "graficos_doc_localidades"
    ]:
        st.session_state[chave] = [
            item for item in st.session_state[chave]
            if item["pagina"] != "cruzamento"
        ]


# ======================================================
# 🧠 Interface
# ======================================================
st.title("📊 Página dos Cruzamentos de Dados")

if st.button("🧹 Limpar cruzamentos desta página"):
    limpar_estado_cruzamentos()
    st.success("Cruzamentos removidos com sucesso.")
    st.rerun()


# ======================================================
# 📂 Upload de dados
# ======================================================
arquivo = st.file_uploader(
    "📂 Adicione o arquivo CSV ou Excel",
    type=["csv", "xlsx"]
)

if arquivo:
    st.session_state.df = ler_arquivo(arquivo)
    st.session_state.nome_arquivo = arquivo.name
    st.success("Arquivo carregado com sucesso!")


df = st.session_state.df

if df is None:
    st.info("Por favor, faça o upload de um arquivo para começar.")
    st.stop()

 
st.subheader("📄 Prévia do Dataset")
st.dataframe(df.head())
st.divider()


# ======================================================
# 🔎 Identificação de colunas
# ======================================================
bairros = df.columns[df.columns.str.lower().str.contains("bairro")]
zonas = df.columns[df.columns.str.lower().str.contains("zona")]
localidades = pd.Index(list(bairros) + list(zonas))

sexo = df.columns[df.columns.str.lower().str.contains("sexo|genero|gênero")]
idade = df.columns[df.columns.str.lower().str.contains(r"^idade$|faixa etaria|faixa etária|quantos anos|qual sua idade")]
escolaridade = df.columns[df.columns.str.lower().str.contains("escolaridade|escola")]
renda = df.columns[df.columns.str.lower().str.contains("renda")]
sociais = pd.Index(list(sexo) + list(idade) + list(escolaridade) + list(renda))

variaveis_excluir = df.columns[df.columns.str.lower().str.contains(
    "data|duracao|duração|latitude|longitude|usuario|bom dia|boa tarde|boa noite|"
    "entrevistador|localizacao|localização|audio|áudio|usuário|longitud|abt|"
    "espontanea|espontânea|zona|bairro|sexo|genero|gênero|idade|faixa etaria|"
    "faixa etária|escolaridade|escola|renda|vota em"
)]

colunas_base = df.columns[df.columns.isin(localidades) | df.columns.isin(sociais)]
colunas_excluir = list(variaveis_excluir) + list(colunas_base)
col_alvo = df.drop(columns=colunas_excluir)

st.subheader("📌 Colunas Disponíveis para Cruzamento")
st.dataframe(pd.DataFrame(col_alvo.columns, columns=["Colunas"]), height=300)
st.divider()


# ======================================================
# 📍 Cruzamento por Localidades
# ======================================================
st.subheader("📍 Cruzamento por Localidades")

for coluna in col_alvo:
    titulo = criar_title_graf(coluna)
    st.info(coluna)

    df_doc, tabela = agrupar_tabelas(df, localidades, coluna)
    st.dataframe(tabela)

    salvar_tabela(
        st.session_state.tabelas_doc_localidades,
        "cruzamento",
        f"CRUZAMENTO: {titulo} X BAIRROS",
        df_doc
    )

    baixar_excel(tabela, coluna, f"localidades_{coluna}")


# ======================================================
# 🧑 Cruzamento por Questões Sociais
# ======================================================
st.subheader("🧑 Cruzamento por Questões Sociais")

for coluna in col_alvo:
    titulo = criar_title_graf(coluna)
    st.info(coluna)

    df_doc, tabela = agrupar_tabelas(df, sociais, coluna)
    st.dataframe(tabela)

    salvar_tabela(
        st.session_state.tabelas_doc_questoes,
        "cruzamento",
        f"CRUZAMENTO: {titulo}",
        df_doc
    )

    baixar_excel(tabela, coluna, f"sociais_{coluna}")

# ======================================================
# 📊 Gráficos por Sexo
# ======================================================
st.subheader("🧑👩 Gráficos por Cruzamento Social")

for coluna in col_alvo:
    title = criar_title_graf(coluna)
    def ajustar_variavel_plot(df, variavel, coluna):
        df_doc, _ = agrupar_tabelas(df, variavel, coluna)

        df_plot = (
        df_doc
        .query("VARIÁVEIS != 'TOTAL'")
        .drop(columns=["TOTAL"])
        .melt(
            id_vars="VARIÁVEIS",
            var_name="Resposta",
            value_name="Percentual"
            )
        )
        return df_plot

    variaveis = [sexo, idade, escolaridade, renda]
    nomes_variaveis = ["SEXO", "IDADE", "ESCOLARIDADE", "RENDA"]

    for var, nome_var in zip(variaveis, nomes_variaveis):
        df_plot = ajustar_variavel_plot(df, var, coluna)
        st.info(f"{coluna} por {nome_var}")

        graf = criar_graf_barras_lado(df_plot, "Resposta", "Percentual", "VARIÁVEIS", nome_var)
        st.pyplot(graf)

        salvar_grafico(
        st.session_state.graficos_doc_questoes,
        "cruzamento",
        f"CRUZAMENTO: {title} X {nome_var}",
        graf
    )

# ======================================================
# 🔧 Cruzamento Personalizado
# ======================================================
st.divider()
st.subheader("🔧 Cruzamento Personalizado")

def bloco_cruzamento(idx):
    st.markdown(f"### 🔄 Cruzamento {idx}")

    variaveis = st.multiselect(
        "Colunas para linhas:",
        df.columns,
        key=f"cruzamento_variaveis_{idx}"
    )

    cruzamentos = st.multiselect(
        "Colunas para colunas:",
        df.columns,
        key=f"cruzamento_colunas_{idx}"
    )

    if variaveis and cruzamentos:
        for col in cruzamentos:
            titulo = f"{variaveis} X {col}"
            st.info(titulo)

            df_doc, tabela = agrupar_tabelas(df, variaveis, col)
            st.dataframe(tabela)

            salvar_tabela(
                st.session_state.tabelas_doc_intencoes,
                "cruzamento",
                titulo,
                df_doc
            )



for i in range(1, st.session_state.contador_cruzamentos + 1):
    bloco_cruzamento(i)

if st.button("➕ Adicionar outro cruzamento"):
    st.session_state.contador_cruzamentos += 1
    st.rerun()
