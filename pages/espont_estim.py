import streamlit as st
import re
import unicodedata

from metodos_auxiliares import ler_arquivo, baixar_excel, baixar_grafico
from metodos_criar_graf_tab import (
    grafico_barras_espontanea,
    tabela_espontanea
)
from agentes_graf_tab import criar_title_graf

# ======================================================
# 🔹 Configuração da página
# ======================================================
st.set_page_config(
    page_title="Análises Espontâneas e Estimuladas",
    layout="wide"
)

st.title("📊 Gráficos e Tabelas Espontâneos e Estimulados")

PAGINA_ESPONTANEA = "espontanea"
PAGINA_ESTIMULADA = "estimulada"


# ======================================================
# 🔹 Inicialização global do session_state (PADRÃO)
# ======================================================
def init_session_state():
    defaults = {
        "df": None,
        "nome_arquivo": None,
        "tabelas_doc_intencoes": [],
        "graficos_doc_intencoes": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# ======================================================
# 🔹 Funções padronizadas de salvamento
# ======================================================
def salvar_tabela(lista_destino, pagina, titulo, tabela):
    lista_destino.append({
        "pagina": pagina,
        "titulo": titulo,
        "tabela": tabela.copy(),
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
# 🧹 Limpeza CONTROLADA
# ======================================================
def limpar_estado_espontaneo_estimulada():
    for chave in ["tabelas_doc_intencoes", "graficos_doc_intencoes"]:
        st.session_state[chave] = [
            item for item in st.session_state[chave]
            if item["pagina"] not in {PAGINA_ESPONTANEA, PAGINA_ESTIMULADA}
        ]


if st.button("🧹 Limpar análises desta página"):
    limpar_estado_espontaneo_estimulada()
    st.success("Análises removidas com sucesso.")
    st.rerun()


# ======================================================
# 🔹 Utilitário
# ======================================================
def limpar_nome_arquivo(texto, max_len=80):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    texto = re.sub(r"\s+", "_", texto)
    return texto[:max_len]

# ======================================================
# 📂 Upload
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
    st.info("📌 Por favor, faça o upload de um arquivo para começar.")
    st.stop()


st.subheader("📄 Prévia do Dataset")
st.dataframe(df.head(), use_container_width=True)
st.divider()

# ======================================================
# 📈 Espontâneas
# ======================================================
st.subheader("📈 Espontâneas")

espontaneas = df.columns[
    df.columns.str.contains(r"espont[aâ]nea", case=False, regex=True) & 
    (~df.columns.str.contains("abt", case=False))
]

df[espontaneas] = (df[espontaneas]
                    .apply(lambda x: 
                            x.str.strip()
                           .str.replace(r"(?i)^\s*\(outros?\)\s*", "", regex=True)
                           .str.replace(r"^\d+\s*[-–]\s*", "", regex=True)
                           .str.replace(r"\s+", " ", regex=True)
                           .str.strip()
                        )
                    )

for col in espontaneas:
    #title = criar_title_graf(col)
    is_prefeito = bool(re.search("prefeito|prefeita", col.lower()))

    st.write(col)

    if is_prefeito:
        grafico = grafico_barras_espontanea(df, col, col)
        st.pyplot(grafico)

        baixar_grafico(
            grafico,
            limpar_nome_arquivo(col),
            f"Grafico_Espontanea_{col}"
        )

        salvar_grafico(
            st.session_state.graficos_doc_intencoes,
            PAGINA_ESPONTANEA,
            #f"(ESPONTÂNEA) {col}",
            f"{col}",
            grafico
        )

    else:
        df_doc, tabela = tabela_espontanea(df, col)
        st.dataframe(tabela, use_container_width=True)

        baixar_excel(
            df_doc,
            col,
            f"Tabela_Espontanea_{limpar_nome_arquivo(col)}.xlsx"
        )

        salvar_tabela(
            st.session_state.tabelas_doc_intencoes,
            PAGINA_ESPONTANEA,
            #f"(ESPONTÂNEA) {col}",
            f"{col}",
            df_doc
        )

# ======================================================
# ➕ Espontâneas manuais
# ======================================================
faltantes_espont = st.multiselect(
    "Adicionar colunas faltantes para análise espontânea:",
    df.columns,
    key="faltantes_espont"
)

for col in faltantes_espont:
    #title = criar_title_graf(col)
    is_prefeito = bool(re.search("prefeito|prefeita", col.lower()))

    st.write(col)

    if is_prefeito:
        grafico = grafico_barras_espontanea(df, col, col)
        st.pyplot(grafico)

        salvar_grafico(
            st.session_state.graficos_doc_intencoes,
            PAGINA_ESPONTANEA,
            #f"(ESPONTÂNEA) {col}",
            col,
            grafico
        )
    else:
        df_doc, tabela = tabela_espontanea(df, col)
        st.dataframe(tabela, use_container_width=True)

        salvar_tabela(
            st.session_state.tabelas_doc_intencoes,
            PAGINA_ESPONTANEA,
            #f"(ESPONTÂNEA) {col}",
            col,
            df_doc
        )


st.divider()


# ======================================================
# 📊 Estimuladas
# ======================================================
st.subheader("📊 Estimuladas")

estimuladas = df.columns[
    df.columns.str.lower().str.contains("estimulada|estimuladas")
]

df[estimuladas] = (df[estimuladas]
                    .apply(lambda x: 
                           x.str.strip()
                           .str.replace(r"\(outros?\)", "", regex=True)
                           .str.replace(r"^\d+\s*[-–]\s*", "", regex=True)
                           .str.replace(r"\s+", " ", regex=True)
                           .str.upper()
                           .str.strip()
                        )
                    )

for col in estimuladas:
    #title = criar_title_graf(col)

    st.write(col)
    grafico = grafico_barras_espontanea(df, col, col)
    st.pyplot(grafico)

    baixar_grafico(
        grafico,
        limpar_nome_arquivo(col),
        f"Grafico_Estimulada_{col}"
    )

    salvar_grafico(
        st.session_state.graficos_doc_intencoes,
        PAGINA_ESTIMULADA,
        #f"(ESTIMULADA) {col}",
        col,
        grafico
    )

# ======================================================
# ➕ Estimuladas manuais
# ======================================================
faltantes_estimulada = st.multiselect(
    "Adicionar colunas faltantes para análise estimulada:",
    df.columns,
    key="faltantes_estimulada"
)

for col in faltantes_estimulada:
    #title = criar_title_graf(col)

    st.write(col)
    grafico = grafico_barras_espontanea(df, col, col)
    st.pyplot(grafico)

    salvar_grafico(
        st.session_state.graficos_doc_intencoes,
        PAGINA_ESTIMULADA,
        #f"(ESTIMULADA) {col}",
        col,
        grafico
    )
