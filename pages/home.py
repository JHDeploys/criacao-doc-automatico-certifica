import streamlit as st
from pathlib import Path

# Configuração inicial da página (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Certifica Pesquisas | Automação de Relatórios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada para dar uma cara mais profissional
st.markdown("""
    <style>
    /* Título principal usando a cor primária do tema */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0px;
    }
    /* Subtítulo usando a cor de texto padrão, um pouco mais transparente */
    .subtitle {
        font-size: 1.5rem;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 30px;
    }
    
    /* Cartões de Funcionalidades dinâmicos */
    .feature-card {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid var(--primary-color);
        height: 100%;
    }

    /* Caixas de Passo a Passo dinâmicas */
    .step-box {
        text-align: center;
        padding: 20px;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.2); /* Borda sutil e neutra */
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Garante que títulos e textos dentro dos cards usem a cor do tema */
    .feature-card h3, .feature-card p, .step-box h2, .step-box h4, .step-box p {
        color: var(--text-color) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO (HERO SECTION) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="main-title">Automação de Relatórios Eleitorais</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transforme dados brutos em documentos analíticos padronizados em questão de minutos.</p>', unsafe_allow_html=True)
    st.write("""
        Bem-vindo ao sistema inteligente da **Certifica Pesquisas**. Esta plataforma foi desenvolvida para 
        eliminar o trabalho manual na elaboração de relatórios de pesquisa quantitativa, garantindo 
        velocidade, precisão estatística e análises aprofundadas com Inteligência Artificial.
    """)
    st.info("👆 **Utilize o menu acima para iniciar um novo processamento.**")

with col2:
    # Imagem ilustrativa ou logo da empresa (substitua a URL pela sua imagem)
    st.image(Path.cwd() / "logos" / "1-capa.png", use_container_width=True)


st.divider()

# --- FUNCIONALIDADES ---
st.header("✨ Principais Funcionalidades")
st.write("O que o sistema faz nos bastidores para gerar o seu relatório:")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Geração DOCX Nativa</h3>
        <p>Criação automática de documentos Word já formatados em layout paisagem, com cabeçalhos, rodapés, margens ajustadas e sumário (TOC) dinâmico.</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🧠 Análise com IA (LLM)</h3>
        <p>Integração com Inteligência Artificial para ler os dados das tabelas e redigir análises descritivas e insights automáticos para cada questão da pesquisa.</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🧹 Limpeza Inteligente</h3>
        <p>Uso de Regex e padronização automática para limpar bases de dados complexas de múltiplas cidades antes da geração dos gráficos e tabelas.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Espaçamento

# --- COMO FUNCIONA (PASSO A PASSO) ---
st.header("⚙️ Como Funciona")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown("""
    <div class="step-box">
        <h2>1️⃣</h2>
        <h4>Upload</h4>
        <p>Faça o upload da base de dados bruta (Excel/CSV).</p>
    </div>
    """, unsafe_allow_html=True)

with step2:
    st.markdown("""
    <div class="step-box">
        <h2>2️⃣</h2>
        <h4>Limpeza</h4>
        <p>Limpeza automatica dos dados brutos para garantir qualidade e consistência.</p>
    </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
    <div class="step-box">
        <h2>3️⃣</h2>
        <h4>Processamento</h4>
        <p>O sistema cruza os dados, gera tabelas de frequência e chama a IA.</p>
    </div>
    """, unsafe_allow_html=True)

with step4:
    st.markdown("""
    <div class="step-box">
        <h2>4️⃣</h2>
        <h4>Download</h4>
        <p>Baixe o relatório final em .docx, pronto para entrega ao cliente.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- RODAPÉ ---
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>Sistema desenvolvido para Certifica Pesquisas © 2026</p>", unsafe_allow_html=True)
