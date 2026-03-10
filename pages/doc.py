import streamlit as st
from metodos_docx import gerar_relatorio_docx
from agentes_graf_tab import gerar_cabecalho_arquivo, gerar_titulo_subcapa
import re
import unicodedata

# ======================================================
# 🔹 Inicialização defensiva do session_state
# ======================================================
def init_session_state_relatorio_page():
    defaults = {
        "nome_arquivo": None,
        "tabelas_doc_intencoes": [],
        "graficos_doc_intencoes": [],
        "tabelas_doc_questoes": [],
        "graficos_doc_questoes": [],
        "tabelas_doc_localidades": [],
        "graficos_doc_localidades": [],
        "tabelas_doc_abertas": []
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session_state_relatorio_page()

# ======================================================
# 📄 Cabeçalho da página
# ======================================================
st.markdown("## 📄 Geração de Relatório")
st.markdown(
    "Consolide automaticamente **todos os gráficos e tabelas gerados** "
    "em um relatório Word pronto para entrega."
)

# ======================================================
# 📌 Cabeçalho do documento
# ======================================================
nome_arquivo = st.session_state.get("nome_arquivo")
cabecalho = gerar_cabecalho_arquivo(nome_arquivo)
titulo_subcapa = gerar_titulo_subcapa(nome_arquivo)
# ======================================================
# 📊 Consolidação do conteúdo
# ======================================================
graficos = (
    st.session_state.graficos_doc_intencoes
    + st.session_state.graficos_doc_questoes
    + st.session_state.graficos_doc_localidades
)

tabelas = (
    st.session_state.tabelas_doc_intencoes
    + st.session_state.tabelas_doc_questoes
    + st.session_state.tabelas_doc_localidades
    +st.session_state.tabelas_doc_abertas
)

# ======================================================
# 🚨 Validação de conteúdo
# ======================================================
if not graficos and not tabelas:
    st.warning("⚠️ Nenhum gráfico ou tabela foi gerado ainda.")
    st.info(
        "📌 Volte às páginas de análise, gere cruzamentos ou gráficos "
        "e depois retorne para montar o relatório."
    )
    st.stop()

# ======================================================
# 📈 Resumo visual
# ======================================================
with st.container():
    col1, col2 = st.columns(2)

    cor_graficos = "#d9534f" if len(graficos) == 0 else "#28a745"
    cor_tabelas = "#d9534f" if len(tabelas) == 0 else "#28a745"

    with col1:
        st.markdown(
            f"""
            <div style="padding:1rem; border-radius:10px; text-align:center; border:1px solid #eee;">
                <div style="font-size:0.9rem; color:#666;">Gráficos incluídos</div>
                <div style="font-size:2.2rem; font-weight:700; color:{cor_graficos};">
                    {len(graficos)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="padding:1rem; border-radius:10px; text-align:center; border:1px solid #eee;">
                <div style="font-size:0.9rem; color:#666;">Tabelas incluídas</div>
                <div style="font-size:2.2rem; font-weight:700; color:{cor_tabelas};">
                    {len(tabelas)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()

def slug_filename(texto: str, max_len: int = 120) -> str:
    if not texto:
        return "relatorio"
    # tira quebras de linha
    texto = " ".join(str(texto).splitlines())
    # remove acentos
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    # limpa caracteres proibidos em nomes de arquivo
    texto = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", texto)
    # troca espaços por _
    texto = re.sub(r"\s+", "_", texto.strip())
    return texto[:max_len] or "relatorio"

nome_doc = slug_filename(titulo_subcapa) + ".docx"
# ======================================================
# 📤 Exportação
# ======================================================
st.markdown("### 📤 Exportação")

if st.button("📄 Gerar relatório Word", use_container_width=True):
    with st.spinner("Gerando relatório Word..."):
        docx_buffer = gerar_relatorio_docx(cabecalho, titulo_subcapa)

    st.download_button(
        label="⬇️ Baixar relatório Word",
        data=docx_buffer,
        file_name=nome_doc,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )