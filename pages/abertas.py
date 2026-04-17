import streamlit as st

from metodos_auxiliares import (
    ler_arquivo, func_tab_interpretacao_abt
)

from agentes_graf_tab import (
    interpretar_tabela, criar_tab_abt_geral, criar_title_graf_tab
)

# ======================================================
# 🔹 Inicialização global do session_state (PADRÃO)
# ======================================================
def init_session_state():
    defaults = {
        "df": None,
        "nome_arquivo": None,

        "tabelas_doc_abertas": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# ======================================================
# 🔹 Função padronizada de salvamento
# ======================================================
def salvar_tabela(lista_destino, pagina, titulo, tabela, interpretacao=""):
    lista_destino.append({
        "pagina": pagina,
        "titulo": titulo,
        "tabela": tabela,
        "interpretacao": interpretacao
    })

# ======================================================
# 🧹 Limpeza CONTROLADA da página
# ======================================================
def limpar_estado_abertas():
    st.session_state.tabelas_doc_abertas = [
        t for t in st.session_state.tabelas_doc_abertas
        if t["pagina"] != "abertas"
    ]


# ======================================================
# 🧠 Interface
# ======================================================
st.title("📝 Página das Perguntas Abertas")

if st.button("🧹 Limpar análises desta página"):
    limpar_estado_abertas()
    st.success("Análises removidas com sucesso.")
    st.rerun()

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
    st.info("Por favor, faça o upload de um arquivo para começar.")
    st.stop()

# ======================================================
# 🧹 Pré-processamento
# ======================================================
df.columns = (
    df.columns.str.strip()
    .str.replace('\n', ' ', regex=False)
    .str.replace('\r', ' ', regex=False)
    .str.replace('  ', ' ', regex=False)
)

st.subheader("📄 Prévia do Dataset")
st.dataframe(df.head())
st.divider()


df_abt = df.columns[df.columns.str.lower().str.contains("abt")].tolist()
st.info(f"Colunas abertas identificadas: {df_abt}")

# ======================================================
# 🧩 Demais perguntas abertas
# ======================================================


outras = [c for c in df_abt if c != "COLUNA INEXISTENTE"]

for coluna in outras:
    titulo = criar_title_graf_tab(coluna)
    st.markdown(f"## 🔍 Analisando a coluna: **{titulo}**")
    tabelas, interpretacoes = func_tab_interpretacao_abt(
        df,
        titulo,
        criar_tab_abt_geral,
        interpretar_tabela
    )

    salvar_tabela(
        st.session_state.tabelas_doc_abertas,
        "abertas",
        f"{titulo}",
        tabelas.data,
        interpretacoes
    )
