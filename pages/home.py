import streamlit as st
from pathlib import Path

# ======================================================
# Configuração da página
# ======================================================
st.set_page_config(
    page_title="Certifica Pesquisas | Automação de Relatórios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS Customizado — Identidade Visual Certifica
# ======================================================
st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== RESET DE FONTE GLOBAL ===== */
    .stApp, .stApp * {
        font-family: 'Inter', sans-serif;
    }

    /* ===== HERO SECTION ===== */
    .hero-container {
        background: linear-gradient(135deg, #02124A 0%, #0A2A6E 50%, #1A4A9E 100%);
        border-radius: 20px;
        padding: 50px 48px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(125, 201, 255, 0.15) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-container::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(125, 201, 255, 0.1) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(125, 201, 255, 0.15);
        border: 1px solid rgba(125, 201, 255, 0.3);
        color: #7DC9FF;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
    }

    .hero-title span {
        background: linear-gradient(90deg, #7DC9FF, #B3DFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: rgba(255, 255, 255, 0.75);
        line-height: 1.7;
        max-width: 620px;
        margin-bottom: 24px;
        position: relative;
        z-index: 1;
    }

    .hero-cta {
        display: inline-block;
        background: linear-gradient(135deg, #7DC9FF, #4BA3E3);
        color: #02124A !important;
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95rem;
        text-decoration: none;
        transition: all 0.3s ease;
        position: relative;
        z-index: 1;
    }

    .hero-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(125, 201, 255, 0.35);
    }

    /* ===== MÉTRICAS ===== */
    .metrics-row {
        display: flex;
        gap: 16px;
        margin-bottom: 36px;
    }

    .metric-card {
        flex: 1;
        background: var(--secondary-background-color, #f8f9fa);
        border-radius: 14px;
        padding: 22px 24px;
        border: 1px solid rgba(128, 128, 128, 0.12);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    .metric-icon {
        font-size: 1.6rem;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0e1117;
        line-height: 1;
        margin-bottom: 4px;
    }

    .metric-label {
        font-size: 0.82rem;
        color: #555;
        font-weight: 500;
    }

    /* ===== SEÇÃO DE FUNCIONALIDADES ===== */
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 6px;
    }

    .section-subheader {
        font-size: 0.95rem;
        color: var(--text-color);
        opacity: 0.6;
        margin-bottom: 28px;
    }

    .feature-card-v2 {
        background: var(--secondary-background-color, #f8f9fa);
        border-radius: 16px;
        padding: 28px 24px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .feature-card-v2:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(2, 18, 74, 0.08);
        border-color: rgba(125, 201, 255, 0.4);
    }

    .feature-card-v2::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #02124A, #7DC9FF);
        border-radius: 16px 16px 0 0;
    }

    .feature-icon-box {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(2,18,74,0.08), rgba(125,201,255,0.12));
        font-size: 1.4rem;
        margin-bottom: 16px;
    }

    .feature-card-v2 h3 {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0e1117 !important;
        margin-bottom: 8px;
    }

    .feature-card-v2 p {
        font-size: 0.88rem;
        color: #444 !important;
        line-height: 1.6;
    }

    /* ===== TIMELINE (PASSO A PASSO) ===== */
    .timeline-container {
        display: flex;
        gap: 0;
        position: relative;
        margin-top: 8px;
    }

    .timeline-step {
        flex: 1;
        text-align: center;
        padding: 20px 16px;
        position: relative;
    }

    /* Linha conectora */
    .timeline-step::after {
        content: '';
        position: absolute;
        top: 42px;
        right: -50%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #7DC9FF, rgba(125,201,255,0.3));
    }

    .timeline-step:last-child::after {
        display: none;
    }

    .timeline-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: linear-gradient(135deg, #02124A, #1A4A9E);
        color: #FFFFFF;
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 14px;
        position: relative;
        z-index: 2;
        box-shadow: 0 4px 16px rgba(2, 18, 74, 0.25);
    }

    .timeline-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0e1117;
        margin-bottom: 6px;
    }

    .timeline-desc {
        font-size: 0.82rem;
        color: #555;
        opacity: 0.6;
        line-height: 1.5;
    }

    /* ===== FOOTER ===== */
    .footer-bar {
        text-align: center;
        padding: 24px 0 8px 0;
        border-top: 1px solid rgba(128, 128, 128, 0.15);
        margin-top: 40px;
    }

    .footer-bar p {
        font-size: 0.78rem;
        color: var(--text-color);
        opacity: 0.45;
        font-weight: 500;
    }

    .footer-bar span {
        color: #7DC9FF;
        font-weight: 600;
    }

    /* ===== RESPONSIVO ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .metrics-row { flex-direction: column; }
        .timeline-container { flex-direction: column; }
        .timeline-step::after { display: none; }
    }
</style>
""", unsafe_allow_html=True)


# ======================================================
# HERO SECTION
# ======================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ Certifica Consultoria e Pesquisa</div>
    <div class="hero-title">
        Automação Inteligente<br>de <span>Relatórios Eleitorais</span>
    </div>
    <p class="hero-subtitle">
        Transforme dados brutos de pesquisas eleitorais em documentos analíticos 
        profissionais com gráficos, tabelas de cruzamento e interpretações 
        geradas por Inteligência Artificial em minutos, não em dias.
    </p>
    <div class="hero-cta">▶  Comece pelo menu acima</div>
</div>
""", unsafe_allow_html=True)





# ======================================================
# FUNCIONALIDADES
# ======================================================
st.markdown("""
<p class="section-header">✨ O que o sistema faz por você</p>
<p class="section-subheader">Cada etapa do relatório é automatizada para máxima eficiência e qualidade.</p>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">📈</div>
        <h3>Gráficos Automáticos</h3>
        <p>Gráficos de barras horizontais e verticais para análises espontâneas e estimuladas, 
        com paleta de cores profissional e rótulos automáticos.</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">🔀</div>
        <h3>Cruzamento de Dados</h3>
        <p>Tabelas cruzadas por sexo, idade, escolaridade, renda e localidade. 
        Gráficos comparativos lado a lado para cada variável social.</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">🧠</div>
        <h3>Interpretação com IA</h3>
        <p>Análises qualitativas geradas automaticamente por GPT: categorização de respostas abertas, 
        motivos de aprovação, rejeição e problemas da cidade.</p>
    </div>
    """, unsafe_allow_html=True)

with f4:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">📄</div>
        <h3>Relatório Word Completo</h3>
        <p>Documento .docx profissional com capa, subcapas, sumário, especificações técnicas, 
        gráficos e tabelas — pronto para entrega ao cliente.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ======================================================
# COMO FUNCIONA — TIMELINE
# ======================================================
st.markdown("""
<p class="section-header">⚙️ Fluxo de trabalho</p>
<p class="section-subheader">Do upload à entrega em 4 passos simples.</p>

<div class="timeline-container">
    <div class="timeline-step">
        <div class="timeline-number">1</div>
        <div class="timeline-title">Upload</div>
        <div class="timeline-desc">Envie a base de dados da pesquisa em formato Excel ou CSV.</div>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">2</div>
        <div class="timeline-title">Análise</div>
        <div class="timeline-desc">O sistema identifica colunas, limpa dados e gera gráficos e tabelas automaticamente.</div>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">3</div>
        <div class="timeline-title">Revisão</div>
        <div class="timeline-desc">Revise os resultados gerados, adicione cruzamentos personalizados e ajuste o que precisar.</div>
    </div>
    <div class="timeline-step">
        <div class="timeline-number">4</div>
        <div class="timeline-title">Download</div>
        <div class="timeline-desc">Exporte o relatório completo em Word, pronto para impressão e entrega.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ======================================================
# PÁGINAS DO SISTEMA
# ======================================================
st.write("")
st.markdown("""
<p class="section-header">🗂️ Páginas do sistema</p>
<p class="section-subheader">Navegue pelo menu superior para acessar cada módulo.</p>
""", unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">📊</div>
        <h3>Espontâneas / Estimuladas</h3>
        <p>Geração automática dos gráficos e tabelas de intenção de voto espontânea e estimulada.</p>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">🔀</div>
        <h3>Cruzamento de Dados</h3>
        <p>Tabelas e gráficos cruzados por variáveis sociais (sexo, idade, etc.) e localidades.</p>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">💬</div>
        <h3>Perguntas Abertas</h3>
        <p>Categorização das respostas abertas via IA: rejeição, aprovação e problemas da cidade.</p>
    </div>
    """, unsafe_allow_html=True)

with p4:
    st.markdown("""
    <div class="feature-card-v2">
        <div class="feature-icon-box">📑</div>
        <h3>Geração do Documento</h3>
        <p>Consolida todos os gráficos e tabelas em um relatório Word profissional para download.</p>
    </div>
    """, unsafe_allow_html=True)


# ======================================================
# RODAPÉ
# ======================================================
st.markdown("""
<div class="footer-bar">
    <p>Sistema desenvolvido para <span>Certifica Consultoria e Pesquisa</span> © 2026 · Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)
