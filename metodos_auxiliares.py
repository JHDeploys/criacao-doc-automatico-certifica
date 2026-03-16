import streamlit as st
import pandas as pd
from io import BytesIO
import re
import unicodedata

#------------------Funções Auxiliares--------------

#Ler Arquivo
@st.cache_data
def ler_arquivo(arquivo):
    try:
        if arquivo is None:
            return None
        
        nome = arquivo.name.lower()
        if nome.endswith(".csv"):
            try:
                return pd.read_csv(arquivo)
            except:
                return pd.read_csv(arquivo, sep=";")
            
        elif nome.endswith(".xlsx"):
            return pd.read_excel(arquivo)
        
        else:
            return st.error("Formato de arquivo não suportado. Por favor, envie um arquivo CSV ou XLSX.")
    
    except Exception as e:
        st.error("Erro ao ler o arquivo: {e}")
        return None

def ordenar(df, column):
    # Normalização
    serie = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"^\d+\s*-\s*", "", regex=True)
    )

    serie_norm = serie.str.upper()
    count_col = serie_norm.value_counts()

    branco = {
        "BRANCO/NULO", "NÃO SABE", "NÃO SABE/NÃO RESPONDEU",
        "NENHUM", "NÃO RESPONDEU", "N RESPONDEU",
        "NADA/ NENHUM", "","NÃO SABE/NÃO RESPONDEU (NÃO LER)", "BRANCO/NULO (NÃO LER)"
    }

    # ⚠️ LISTA ORDENADA (ordem semântica)
    escala_avaliacao = [
        "ÓTIMA", "ÓTIMO",
        "BOA", "BOM",
        "REGULAR",
        "RUIM",
        "PÉSSIMA",
        "APROVA",
        "DESAPROVA",
        "POSITIVA", "POSITIVO",
        "NEGATIVA", "NEGATIVO",
        "DE 16 A 24 ANOS"
    ]

    # Detecta escala somente se houver PELO MENOS 3 itens da escala
    encontrados = [v for v in escala_avaliacao if v in count_col.index]
    tem_escala = len(encontrados) >= 1

    if tem_escala:
        # Ordem fixa e controlada
        ordem_principal = encontrados

        outros = count_col[
            ~count_col.index.isin(ordem_principal) &
            ~count_col.index.isin(branco)
        ].sort_index()

        brancos = count_col[count_col.index.isin(branco)]

        ordem = ordem_principal + list(outros.index) + list(brancos.index)

    else:
        # 🔥 AQUI É RANKING, SEM EXCEÇÃO
        candidatos = (
            count_col[~count_col.index.isin(branco)]
            .sort_values(ascending=False)
        )

        brancos = count_col[count_col.index.isin(branco)]

        ordem = list(candidatos.index) + list(brancos.index)

    return ordem, count_col

    # Função para gerar DataFrame ordenado e com porcentagens
def plot_ordem_porcentagem(df, column):
    ordem, count_col = ordenar(df, column)
        
    df_plot = count_col.reset_index()
    df_plot.columns = ["candidatos", "votos"]
    df_plot["percent"] = (df_plot["votos"] / df_plot["votos"].sum() * 100).round(1)
    # Reordena conforme a ordem desejada
    df_plot = df_plot.set_index("candidatos").loc[ordem].reset_index()
    return df_plot

    # Função para estilizar as linhas (listradas) de tabelas
def striped_rows(row):
    color = '#c6dbef' if row.name % 2 == 0 else '#9ecae1'
    return [f'background-color: {color}; color: black; text-align: center'] * len(row)

# Função para dividir a tabela em duas metades e estilizar (CORRIGIDA)
def divir_tabela_estilizar(df_completo):
        
    # --- dividir a tabela em duas metades ---
    metade = len(df_completo) // 2
    df_metade1 = df_completo.iloc[:metade].copy()
    df_metade2 = df_completo.iloc[metade:].copy()

    # Adiciona uma linha de índice à segunda metade para manter a estilização de zebra
    # O índice começa onde a primeira metade parou
    df_metade2.index = range(metade, len(df_completo))

    # Função interna para aplicar estilos
    def aplicar_estilo(df):
        return (
            df.style
            .apply(striped_rows, axis=1)
            .set_table_styles([{
                'selector': 'thead th',
                'props': [
                    ('background-color', '#02124A'),
                    ('color', 'white'),
                    ('text-align', 'center'),
                    ('font-weight', 'bold')
                ]
            }])
                .hide(axis="index")
        )
        
    styled1 = aplicar_estilo(df_metade1)
    styled2 = aplicar_estilo(df_metade2)
        
    return styled1, styled2

#Função Para estilizar a tabela sem dividir
def estilizar_tabela_sem_divisao(df):

    # Garantir índice numérico para usar row.name
    df_reset = df.reset_index(drop=True)
    
    # Função para criar linhas listradas
    def striped_rows(row):
        color = '#c6dbef' if row.name % 2 == 0 else '#9ecae1'
        return [f'background-color: {color}; color: black; text-align: center'] * len(row)
    
    # Aplicar estilo
    styled = (
        df_reset.style
        .apply(striped_rows, axis=1)  # axis=1 aplica linha a linha
        .set_table_styles([{
            'selector': 'thead th',
            'props': [
                ('background-color', '#02124A'),
                ('color', 'white'),
                ('text-align', 'center'),
                ('font-weight', 'bold')
            ]
        }])
        .hide(axis="index")  # remove o índice
    )
    
    return styled

#Função para limpar nome de arquivo
def limpar_nome_arquivo(texto, max_len=80):
    # Remove acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    # Lowercase
    texto = texto.lower()
    # Remove caracteres inválidos
    texto = re.sub(r"[^\w\s-]", "", texto)
    # Substitui espaços por _
    texto = re.sub(r"\s+", "_", texto)
    # Limita tamanho
    return texto[:max_len]


#Criar o Botão de Baixar tabela Excel:
def baixar_excel(df, coluna, key):
    excel_file = BytesIO()
    df.to_excel(excel_file, "Tabela_Excel", engine="openpyxl")
    excel_file.seek(0)
    
    st.download_button(
            "⬇️ Baixar Tabela (Excel)",
            data=excel_file,
            file_name="Tabela_Excel.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=key
        )

def baixar_grafico(fig, nome, key):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Baixar gráfico",
        data=buffer,
        file_name=f"{nome}.png",
        mime="image/png",
        key=key
    )

import re

def limpar_nome_coluna(texto):
    if texto is None:
        return ""

    # Caso venha lista ou array (ex: retorno de filtro)
    if isinstance(texto, (list, tuple)):
        texto = texto[0]

    texto = str(texto)

    # Remove colchetes, aspas simples, duplas e crases
    texto = re.sub(r"[\[\]'\"`]", "", texto)

    # Normaliza espaços
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


#Encontrar Candidatos e seus motivos de Rejeição
def encontrar_candidatos(df, votos, rejeicao):

    if isinstance(votos, list):
        votos = votos[0] if len(votos) > 0 else None

    if isinstance(rejeicao, list):
        rejeicao = rejeicao[0] if len(rejeicao) > 0 else None

    if (
        not isinstance(votos, str)
        or not isinstance(rejeicao, str)
        or votos not in df.columns
        or rejeicao not in df.columns
    ):
        return {}

    # Seleciona apenas as colunas necessárias e remove respostas vazias
    base = df[[votos, rejeicao]].dropna()

    # Limpeza de prefixos tipo "01 -", "02-", "03- ", etc.
    base[votos] = (base[votos].astype(str).str.strip().str.replace(r"^\d+\s*-\s*", "", regex=True))

    # Padroniza tudo para "capitalizado"
    base[votos] = base[votos].str.strip().str.upper()
    candidatos = base[votos].unique()

    # Lista de exclusão robusta
    excluir = [
        "BRANCO/NULO", "BRANCO", "NULO",
        "NÃO SABE", "NÃO SABE/NÃO RESPONDEU",
        "NENHUM", "NÃO RESPONDEU",
        "SEM RESPOSTA", "NS/NR", "OUTROS", "OUTRO",
        "NÃO SABE/ NÃO RESPONDEU", "NÃO SABE/NÃO RESPONDEU (NÃO LER)"
    ]

    # Identifica candidatos válidos
    candidatos = [c for c in candidatos if c not in excluir]

    # Criar dicionário: {candidato: lista_de_respostas}
    respostas_por_candidato = {}

    for cand in candidatos:
        respostas = (
            base.loc[base[votos] == cand, rejeicao]
            .dropna()
            .astype(str)
            .tolist()
        )
        respostas_por_candidato[cand] = respostas

    return respostas_por_candidato


def func_tab_interpretacao_candidato(
    df,
    coluna_candidato,
    tipo_tab,
    func_encontrar,
    func_criar_tab,
    func_criar_interpretacao
):
    respostas = func_encontrar(df, coluna_candidato, tipo_tab)

    resultados = {}        # tabelas
    interpretacoes = {}    # textos

    status = st.empty()

    for nome_candidato, lista in respostas.items():
        status.info(f"Analisando: {nome_candidato}")

        # Cria tabela
        tabela = func_criar_tab(lista, nome_candidato)
        resultados[nome_candidato] = tabela

        # Cria interpretação
        interpretacao = func_criar_interpretacao(tabela)
        interpretacoes[nome_candidato] = interpretacao

    status.empty()

    # =========================
    # Exibição no Streamlit
    # =========================
    for nome_candidato in resultados:
        st.subheader(f"Candidato(a): {nome_candidato}")

        st.dataframe(resultados[nome_candidato], use_container_width=True)

        baixar_excel(
            resultados[nome_candidato],
            f"{tipo_tab}_{nome_candidato}",
            f"Tabela_{tipo_tab}_{nome_candidato}"
        )

        st.markdown("**Interpretação:**")
        st.write(interpretacoes[nome_candidato])

        st.divider()

    return resultados, interpretacoes

def func_tab_interpretacao_cidade(df, coluna,  criar_tab_func, interpretar_func):
    tabela = criar_tab_func(df, coluna)
    st.write(tabela)
    download_key = f"Problemas_Cidade_{coluna}"
    baixar_excel(tabela, coluna, download_key)
    interpretacao = interpretar_func(tabela)
    st.write(interpretacao)

    return tabela, interpretacao


def func_tab_interpretacao_abt(df, coluna, criar_tab_func, interpretar_func):
    tabela = criar_tab_func(df, coluna)
    st.write(tabela)
    download_key = f"Problemas_Cidade_{coluna}"
    baixar_excel(tabela, coluna, download_key)
    interpretacao = interpretar_func(tabela)
    st.write(interpretacao)

    return tabela, interpretacao
