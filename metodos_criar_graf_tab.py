import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from metodos_auxiliares import  ordenar, plot_ordem_porcentagem, estilizar_tabela_sem_divisao
from agentes_graf_tab import criar_paleta_cruzamento
import ast

#-----------------------------------------------------Espontâneas---------------------------------------------------------------------------
def grafico_barras_espontanea(df, coluna, title):
    # Geração do gráfico
    df_plot = plot_ordem_porcentagem(df, coluna)
            
    fig, ax = plt.subplots(figsize=(15, 8))
    ax = sns.barplot(data=df_plot, y="candidatos", x="percent", color="#02124A", width=0.6)
    
    # Ajuste do título para quebrar em linhas
    for i in range(80, len(title)):
        if title[i] == " ":
            title = title[:i] + "\n" + title[i+1:]
            break

    plt.xlabel("")
    #plt.title(title, fontsize=18, fontweight='bold', y=1.04)
    plt.ylabel("")

    plt.yticks(fontsize=16)
    plt.xticks([])
    ax.set_frame_on(False)
    
    # Adiciona rótulos nas barras
    for bar in ax.patches:
        width = bar.get_width()
        plt.text(
            width + (ax.get_xlim()[1] * 0.005),
            bar.get_y() + bar.get_height() / 2,
            f"{width:.1f}%",
            va="center", ha="left",
            fontsize=20, fontweight="bold"
        )
    
    # Ajusta o layout do gráfico
    plt.tight_layout()
    
    return fig

# Criar as Tabelas da Análise Espontânea
def tabela_espontanea(df, coluna):
    # Criação da tabela com os dados da porcentagem
    df_table = plot_ordem_porcentagem(df, coluna)[["candidatos", "percent"]]
    df_table.columns = ["CANDIDATO", "%"]
    df_table["%"] = df_table["%"].round(1).astype(str) + "%"

    # Adiciona a coluna "Rank"
    df_table["RANK"] = [f"{i}º" for i in range(1, len(df_table) + 1)]
    ordem = ["RANK"] + [col for col in df_table.columns if col != "RANK"]
    df_table = df_table[ordem]
    
    # Estiliza a tabela
    styled_table = estilizar_tabela_sem_divisao(df_table)
    
    return df_table, styled_table

#-----------------------------------------------------Estimuladas---------------------------------------------------------------------------
def grafico_barras_estimulada(df, colum, title):
    # Geração do gráfico
    df_plot = plot_ordem_porcentagem(df, colum)
    
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.set_style("darkgrid")

    if df_plot["candidatos"].nunique() < 4:
        width = 0.8
    else:
        width = 0.4

    ax = sns.barplot(df_plot, x="candidatos", y="percent", color="#02124A", width=width)
    
    # Ajuste do título para quebrar em linhas
    for i in range(80, len(title)):
        if title[i] == " ":
            title = title[:i] + "\n" + title[i+1:]
            break
    
    #plt.title(title, fontsize=18, fontweight='bold', y=1.04)
    plt.xlabel("")
    plt.ylabel("")
    fig.canvas.draw()

    labels = ax.get_xticklabels()
    novos_labels = []
    for lbl in labels:
        texto = lbl.get_text()
        if len(texto) > 18:
            for i in range(12, len(texto)):
                if texto[i] == " ":
                    texto = texto[:i] + "\n" + texto[i+1:]
                    break
        novos_labels.append(texto)

    ax.set_xticklabels(novos_labels, fontsize=11)
    plt.yticks([])
    ax.set_frame_on(False)
    
    # Adiciona os valores nas barras
    for bar in ax.patches:
        height = bar.get_height()
        x_pos = bar.get_x() + bar.get_width() / 2
        ax.text(
            x_pos,
            height + 0.5,
            f"{height:.1f}%",
            ha="center", va="bottom", fontsize=20, fontweight="bold"
        )
    
    # Ajusta o layout do gráfico
    plt.tight_layout()
    
    return fig

#-----------------------------------------Função para gerar a tabela de cruzamento entre variáveis---------------------------------
# --- FUNÇÃO 1: tabela_cruzamento ---
def tabela_cruzamento(df_in, column1, column2):
    # Usamos .copy() para evitar SettingWithCopyWarning
    df = df_in.copy() 
    
    # 1. Limpeza de Dados
    for col in [column1, column2]:
        if col is not None and col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                # Remoção de prefixos como "1 - ", etc.
                df[col] = df[col].str.replace(r"^\d+\s-\s", "", regex=True)
            
    ordem, _ = ordenar(df, column2)

    # 2. Criação e Normalização da Tabela
    grupo = df.groupby([column1, column2]).size().reset_index(name="count")
    table = grupo.pivot(index=column1, columns=column2, values="count").fillna(0)
    
    # Normalização por linha (percentual dentro de cada grupo)
    table = table.div(table.sum(axis=1), axis=0) * 100

    # Adiciona a coluna TOTAL, que é sempre 100.0 neste tipo de normalização
    table["TOTAL"] = 100
    
    # 3. Ordenação e Formatação
    colunas_ordenadas = [col for col in ordem if col in table.columns]
    table = table[colunas_ordenadas + ["TOTAL"]]

    # Arredonda (em número) antes de formatar
    table = table.round(1) 

    # Remove título do índice e das colunas para limpeza visual
    table = table.rename_axis(None, axis=0).rename_axis(None, axis=1)
    
    return table # Retorna a tabela em formato numérico (float)

# --- FUNÇÃO 2: agrupar_tabelas ---
def agrupar_tabelas(df, variaveis, target):
    tabelas = []
    
    # 1. Geração das Tabelas Individuais
    for var in variaveis:
        # Tabela em formato NUMÉRICO
        tab = tabela_cruzamento(df.copy(), var, target).reset_index() 
        tab.columns = ["VARIÁVEIS"] + list(tab.columns[1:])
        tabelas.append(tab)
    
    # 2. Concatenação Inicial (agora com números)
    final_table = pd.concat(tabelas, ignore_index=True)
    
    # 3. Criação da Linha de TOTAL DA AMOSTRA (Distribuição Marginal)
    
    # Valores de target limpos para garantir correspondência com as colunas da tabela
    df_temp = df.copy()
    if df_temp[target].dtype == 'object':
        df_temp[target] = df_temp[target].astype(str).str.strip().str.replace(r"^\d+\s-\s", "", regex=True)
    
    # Calcula a distribuição percentual numérica
    total_counts = df_temp[target].value_counts(normalize=True).mul(100).round(1)
    
    total_row_data = {"VARIÁVEIS": "TOTAL"}
    
    # Preenche os valores do TOTAL GERAL nas colunas de target
    for col in final_table.columns[1:-1]:
        # Usa .get() para obter o valor numérico. Usa 0.0 se não existir.
        total_row_data[col] = total_counts.get(col, 0.0) 
        
    total_row_data["TOTAL"] = 100 # O total geral é sempre 100.0%

    total_row = pd.DataFrame([total_row_data], columns=final_table.columns)

    # 4. Anexação e Organização Final (Ainda em formato numérico)
    final_table = pd.concat([final_table, total_row], ignore_index=True)
    final_table = final_table.rename_axis(None, axis=0).rename_axis(None, axis=1)
    
    # 5. Estilização e Formatação Final
    # Aplica o estilo inicial (retorna pd.Styler object)
    styled_table = estilizar_tabela_sem_divisao(final_table)
    
    # Formata todos os números para 1 casa decimal e adiciona o sinal de porcentagem
    styled_table = styled_table.format("{:.1f}%", subset=final_table.columns[1:])
    
    # Define a função de destaque para a linha TOTAL
    def destacar_total(row):
        is_total = row.VARIÁVEIS == "TOTAL"
        # Estilo de fundo e fonte
        style = 'background-color: #02124A; color: white; font-weight: bold'
        
        # Aplica o estilo se for a linha TOTAL
        return [style] * len(row) if is_total else [''] * len(row)

    # Aplica o destaque na linha TOTAL
    styled_table = styled_table.apply(destacar_total, axis=1)

    return final_table, styled_table


def criar_graf_barras_lado(df, x, y, hue, tipo_cruzamento):
    fig, ax = plt.subplots(figsize=(15, 8))

    n_categorias = df[hue].nunique()

    paleta_raw = criar_paleta_cruzamento(n_categorias)
    try:
        paleta_IA = ast.literal_eval(paleta_raw)
    except:
        paleta_IA = sns.color_palette("Blues_r", n_categorias).as_hex()

    if tipo_cruzamento == "SEXO":
        palette = ["#B3DFFF", "#14045D"]
    else:
        palette = paleta_IA

    sns.barplot(
        data=df,
        x=x,
        y=y,
        hue=hue,
        ax=ax,
        palette=palette,
        edgecolor="none"
        )
    
    #ax.set_title(f"{cruza} por Sexo")
    ax.set_ylabel("%")
    ax.set_xlabel("")
    ax.set_ylabel(" ")
    ax.set_yticklabels([])
    ax.set_yticks([])

    fig.canvas.draw()
    labels = ax.get_xticklabels()
    novos_labels = []
    for lbl in labels:
        texto = lbl.get_text()
        if len(texto) > 18:
            for i in range(12, len(texto)):
                if texto[i] == " ":
                    texto = texto[:i] + "\n" + texto[i+1:]
                    break
        novos_labels.append(texto)

    ax.set_xticklabels(novos_labels, fontsize=11)
    plt.yticks([])
    ax.set_frame_on(False)
    
    font_size_barras = max(4, 18 - n_categorias)
    for bar in ax.patches:
        height = bar.get_height()

        if height <= 0:
                continue
        x_pos = bar.get_x() + bar.get_width() / 2
        ax.text(
            x_pos,
            height + 0.5,
            f"{height:.0f}%",
            ha="center", va="bottom", fontsize=font_size_barras, fontweight="bold"
        )
    
    leg = ax.legend(
    title=tipo_cruzamento,
    loc="best",
    borderaxespad=0,
    fontsize=14,
    title_fontsize=16,
    framealpha=0.85,
    frameon=False
    )

    leg.get_title().set_fontweight("bold")


    plt.tight_layout()
    return fig
