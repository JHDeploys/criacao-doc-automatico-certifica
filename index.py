import streamlit as st

pg = st.navigation([
    st.Page("pages/home.py", title="Pagina Inicial"),
    st.Page("pages/espont_estim.py", title="Espontâneas/Estimuladas"),
    st.Page("pages/cruzamento.py", title="Cruzamento de Dados"),
    st.Page("pages/abertas.py", title="Perguntas Abertas"),
    st.Page("pages/doc.py", title="Criacao_Documento"),
], position="top")

pg.run()
