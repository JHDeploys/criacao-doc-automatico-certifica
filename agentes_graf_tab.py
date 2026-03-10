from openai import OpenAI
from dotenv import load_dotenv
import json
import os
from metodos_auxiliares import estilizar_tabela_sem_divisao
import pandas as pd


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#====================================================================ENCONTRAR AS COLUNAS=================================================================================================
#Encontrar coluna de Rejeição:
def encontrar_rejeicao(colunas):
    prompt = f"""
    Você é um especialista em pesquisas eleitorais com 20 anos de experiência.
    Sua tarefa é identificar, entre as colunas fornecidas, qual delas representa
    o motivo de **não votar**, **não aprovar** ou **rejeitar** candidatos.

    Retorne exclusivamente **o nome exato da coluna** caso exista.
    Se não existir, retorne exatamente: COLUNA INEXISTENTE

    Colunas disponíveis:
    {chr(10).join(colunas)}
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

#Encontrar a coluna de aprovacao
def encontrar_aprovacao(colunas):

    # Garantia mínima de tipo
    if not isinstance(colunas, list) or len(colunas) == 0:
        return "COLUNA INEXISTENTE"

    prompt = f"""
    Você é um especialista em pesquisas eleitorais com 20 anos de experiência.

    Sua missão:
    Identificar, entre as colunas fornecidas, qual é a coluna que contém **motivos de votar, aprovar ou justificar a aprovação** de candidatos. 
    Essa coluna também pode incluir termos como:
    - "por que aprova"
    - "se você respondeu que aprova ou desaprova"
    - "motivo da aprovação"

    ## REGRAS FUNDAMENTAIS – SIGA SEMPRE
    1. Analise somente o nome das colunas fornecidas.
    2. Escolha **somente UMA coluna**.
    3. Retorne **exclusivamente** o nome exato da coluna, sem:
       - explicações
       - frases extras
       - comentários
       - aspas
       - texto adicional
    4. Se houver mais de uma opção possível, escolha a mais claramente ligada a
       motivos de voto, aprovação ou explicação de aprovação.
    5. Nunca invente uma coluna que não existe na lista.
    6. Não inclua motivos de mudança, pois não classifica aprovação.
    7. Se não existir, retorne exatamente: COLUNA INEXISTENTE

    Colunas disponíveis:
    {chr(10).join(colunas)}
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

#Encontrar Problemas na cidade
def encontrar_problemas(colunas):
    prompt = f"""
    Você é um especialista em pesquisas eleitorais com 20 anos de experiência.
    Sua tarefa é identificar, entre as colunas fornecidas, qual delas representa
    os principais problemas enfrentados na cidade da pesquisa.

    Retorne exclusivamente **o nome exato da coluna**.
    Se não existir, retorne exatamente: COLUNA INEXISTENTE

    Colunas disponíveis:
    {chr(10).join(colunas)}
        """

    response = client.chat.completions.create(
            model="gpt-5.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

    return response.choices[0].message.content.strip()

#=============================================================================CRIAR TABELAS COM AS COLUNAS=============================================================================
# Agente de IA para montar a tabela de rejeição
def criar_tab_espontanea_rejeicao(lista, candidato):
    prompt = f"""
    Você atuará como especialista internacional em ciência política, estratégia, sociologia, comunicação, marketing e pesquisa de opinião, 
    com 20 anos de experiência em análises qualitativas e quantitativas. Você considerará a diversidade cultural, a dinâmica regional e a complexidade dos contextos globais. 
    Você analisará implicações políticas e sociais em escala internacional e criará estratégias adaptadas a diferentes públicos, mercados e cenários críticos. 
    Você antecipará tendências e entregará recomendações práticas, precisas e contextualizadas.
    Você sempre escreverá com:
    •	Voz ativa
    •	Clareza e concisão
    •	Linguagem simples
    •	Comunicação direta

    ##  REGRAS FUNDAMENTAIS – SIGA SEMPRE:                         

    1. Você está analisando EXCLUSIVAMENTE os motivos de **REJEIÇÃO** do candidato: **{candidato}**.
    2. Não confunda com outros candidatos. Se algum nome diferente aparecer, ignore completamente.
    3. Se a frase for ambígua, ASSUMA que se refere ao candidato {candidato}.
    4. Ignore TOTALMENTE elogios, apoios ou argumentos positivos.
    5. NÃO invente motivos. Use SOMENTE o que aparece nas falas.
    6. Em caso de preferencias por outro candidato classifique como: PREFERÊNCIA POR OUTRO CANDIDATO.
    6. **AS CATEGORIAS DEVEM TER LABELS NÃO MUITO LONGOS**, obrigatoriamente:
        - sem explicações adicionais
        - **NUNCA usar parênteses, apenas "/" quando necessário**
        - Letras Maiúsculas
    7. A saída deve ser APENAS um JSON válido, exatamente no formato exigido.

    **Sua Missão**:
    Missão Geral
    Você receberá transcrições de grupos focais ou respostas abertas de pesquisas. Você entregará uma análise completa em três etapas:
        1.	padronização e quantificação em categorias
        2.	apresentação dos resultados em tabela

    1. Padronização e Quantificação:
    Você agrupará as falas em categorias temáticas padronizadas, como:
    •	Saúde
    •	Segurança
    •	Infraestrutura
    •	Atendimento
    •	Gestão
    •	Economia
    •	Outros temas relacionados ao conteúdo analisado

    Você poderá criar novas categorias sempre que o conteúdo exigir.

    Para cada categoria, você calculará apenas:
    •	Porcentagem simples sobre o total de menções identificadas
    Quando possível, você também indicará se as menções são predominantemente positivas, negativas ou neutras.
    A tabela deve ser colocada em ordem decrescente com relação as porcentantagens calculadas.

    2. Apresentação da Tabela Final

    A saída deve ser **somente um JSON**, no formato:

            {{
                "resultados": [
                    {{"RANK": "1º", "MOTIVOS QUE LEVAM A REJEITAR {candidato}": "Exemplo", "%": 0.00}}
                ]
            }}

        A lista de falas (todas referentes ao candidato {candidato}) é a seguinte:
    {lista}
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        response_format={"type":"json_object"},
        messages=[{
            "role": "user",
            "content":prompt
        }]
    )

    data = json.loads(response.choices[0].message.content)

    df = pd.DataFrame(data["resultados"])
    df["%"] = df["%"].astype(float).round(2)
    df["%"] = df['%'].astype(str) + "%"
    styled = estilizar_tabela_sem_divisao(df)
    return styled

#Criar Tabela de Aprovação
def criar_tab_espontanea_aprovacao(lista, candidato):
    prompt = f"""
    Você atuará como especialista internacional em ciência política, estratégia, sociologia, comunicação, marketing e pesquisa de opinião, 
    com 20 anos de experiência em análises qualitativas e quantitativas. Você considerará a diversidade cultural, a dinâmica regional e a complexidade dos contextos globais. 
    Você analisará implicações políticas e sociais em escala internacional e criará estratégias adaptadas a diferentes públicos, mercados e cenários críticos. 
    Você antecipará tendências e entregará recomendações práticas, precisas e contextualizadas.
    Você sempre escreverá com:
    •	Voz ativa
    •	Clareza e concisão
    •	Linguagem simples
    •	Comunicação direta

    ## REGRAS FUNDAMENTAIS – SIGA SEMPRE

    1. Você está analisando EXCLUSIVAMENTE os motivos de **APROVAÇÃO** do candidato **{candidato}**.  
    2. Não confunda com outros candidatos. Se algum nome diferente aparecer, ignore completamente.  
    3. Se a frase for ambígua, ASSUMA que se refere ao candidato {candidato}.  
    4. Ignore totalmente críticas, rejeições ou argumentos negativos.  
    5. NÃO invente motivos. Use **somente** o que aparece nas falas.  
    6. *AS CATEGORIAS DEVEM TER LABELS NÃO MUITO LONGOS*, obrigatoriamente:
        - sem explicações adicionais
        - *NUNCA usar parênteses, apenas "/" quando necessário*
        - Letras Maiúsculas
    7. A saída deve ser APENAS um JSON válido, exatamente no formato exigido.


    ## MISSÃO GERAL
    Você agrupará as falas em categorias temáticas padronizadas, como:
    •	Saúde
    •	Segurança
    •	Infraestrutura
    •	Atendimento
    •	Gestão
    •	Economia
    •	Outros temas relacionados ao conteúdo analisado

    Você poderá criar novas categorias sempre que o conteúdo exigir.

    Para cada categoria, você calculará apenas:
    •	Porcentagem simples sobre o total de menções identificadas
    Quando possível, você também indicará se as menções são predominantemente positivas, negativas ou neutras.
    A tabela deve ser colocada em ordem decrescente com relação as porcentantagens calculadas.


    2. APRESENTAÇÃO DA TABELA FINAL

    A saída deve ser **somente um JSON**, no formato:

        {{
            "resultados": [
                {{"RANK": "1º", "MOTIVOS QUE LEVAM A APROVAR {candidato}": "Exemplo", "%": 0.00}}
            ]
        }}

    A lista de falas (todas referentes ao candidato {candidato}) é a seguinte:
    {lista}
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        response_format={"type":"json_object"},
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    data = json.loads(response.choices[0].message.content)

    df = pd.DataFrame(data["resultados"])
    df["%"] = df["%"].astype(float).round(2)
    df["%"] = df["%"].astype(str) + "%"
    styled = estilizar_tabela_sem_divisao(df)
    return styled


# Criar as tabelas de problemas na cidade
def criar_tab_problemas_cidade(df, cidade):
    cidade = df[cidade].dropna().astype(str).tolist()
    prompt = f"""
    Você atuará como especialista internacional em políticas públicas, sociologia urbana,
    planejamento de cidades, análise de opinião pública e comportamento social.
    Ao longo de 20 anos de experiência você já analisou pesquisas de percepção urbana em centenas de municípios.

    Sua missão é analisar EXCLUSIVAMENTE:
    **os PRINCIPAIS PROBLEMAS que a cidade enfrenta atualmente**, com base nas falas fornecidas.

    ## REGRAS FUNDAMENTAIS
    1. Analise SOMENTE problemas da cidade.
    2. NÃO invente nenhum problema que não esteja nas falas.
    3. **AS CATEGORIAS DEVEM TER LABELS NÃO MUITO LONGOS**, obrigatoriamente:
        - sem explicações adicionais
        - **NUNCA usar parênteses, apenas "/" quando necessário**
        - Letras Maiúsculas
    4. Se a fala for genérica, classifique corretamente em SERVIÇOS PÚBLICOS, GESTÃO, INFRAESTRUTURA ou OUTROS.
    5. ## **SEMPRE** apresentar a tabela em ordem **DECRESCENTE** com base na **PORCENTAGEM CALCULADA**.
    6. Saída APENAS em JSON, formato:

        {{
            "resultados": [
                {{"RANK": "1º", "PRINCIPAIS PROBLEMAS DA CIDADE": "Exemplo", "%": 0.00}}
            ]
        }}

    -------------------------------------------------------------------
    AQ ESTAO OS DADOS:
    {cidade}
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}]
    )

    data = json.loads(response.choices[0].message.content)
    df_result = pd.DataFrame(data["resultados"])
    df_result["%"] = df_result["%"].astype(float).round(2)
    df_result["%"] = df_result["%"].astype(str) + "%"

    styled = estilizar_tabela_sem_divisao(df_result)
    return styled


#Interpretar os resultados das tabelas 
def interpretar_tabela(tabela):
    if isinstance(tabela, pd.io.formats.style.Styler):
        tabela = tabela.data

    tabela = tabela.to_markdown()

    prompt = f"""
        Você atuará como um especialista internacional em ciência política, opinião pública,
        comportamento eleitoral, metodologia de pesquisa, análise de dados e comunicação estratégica.
        Possui mais de 25 anos de experiência conduzindo estudos qualitativos e quantitativos,
        pesquisas eleitorais, diagnósticos de percepção social e análises estratégicas.

        Sua tarefa é produzir uma ANÁLISE QUALITATIVA INSTITUCIONAL, clara, profunda e
        estrategicamente contextualizada, baseada EXCLUSIVAMENTE nos ELEMENTOS CENTRAIS
        presentes na TABELA FINAL gerada pelo Agente 1.

        ---

        ## FOCO DA ANÁLISE (OBRIGATÓRIO)

        O FOCO deve seguir ESTRITAMENTE o TEMA da tabela analisada:
        - Se a tabela tratar de APROVAÇÃO → analise os MOTIVOS DE APROVAÇÃO.
        - Se tratar de REJEIÇÃO → analise os MOTIVOS DE REJEIÇÃO.
        - Se tratar de PROBLEMAS → analise os PROBLEMAS PERCEBIDOS.
        - Se tratar de EXPECTATIVAS → analise as EXPECTATIVAS EXPRESSAS.
        - Se tratar de IMAGEM → analise os TRAÇOS DE IMAGEM ASSOCIADOS.
        - Se tratar de AVALIAÇÃO GERAL → analise os CRITÉRIOS DE AVALIAÇÃO.

        Não desvie do tema em hipótese alguma.

        ---

        ## REGRAS FUNDAMENTAIS — SIGA RIGOROSAMENTE

        1. Analise APENAS conteúdos diretamente relacionados ao tema da tabela.
        2. Ignore totalmente conteúdos fora do foco.
        3. Não invente números, percentuais, categorias ou motivos.
        4. Não descreva a tabela — INTERPRETE qualitativamente.
        5. Linguagem:
        - Formal institucional
        - Clara, fluida e acessível
        - Baixo tecnicismo
        6. Não extrapole além do que os dados permitem.
        7. Nunca use listas genéricas; cada ponto deve estar claramente ancorado nas falas.

        ---

        ## FORMATO OBRIGATÓRIO DA RESPOSTA  
        ⚠️ **A resposta DEVE seguir EXATAMENTE este padrão estrutural** ⚠️

        ### TÍTULO
        Utilize o formato:
        **# ANÁLISE QUALITATIVA DAS RESPOSTAS REFERENTE A [TEMA DA TABELA]**

        ---

        ### INTRODUÇÃO
        Escreva um parágrafo introdutório explicando:
        - O contexto geral do tema analisado
        - O sentido predominante das percepções registradas
        - A importância do tema para o cenário analisado  
        Sem números inventados e sem repetir a tabela.

        ---

        ### PRINCIPAIS TEMAS IDENTIFICADOS
        Organize a análise em **eixos temáticos claros**, coerentes com o conteúdo da tabela.

        Cada eixo deve conter:
        - Um título claro
        - Subtópicos explicativos em bullet points
        - Interpretação qualitativa das falas, com aprofundamento analítico

        Exemplo de estrutura (ADAPTAR AO TEMA REAL):
        - Tema central 1
        • Subaspecto interpretado  
        • Subaspecto interpretado  
        - Tema central 2
        • Subaspecto interpretado  
        • Subaspecto interpretado  

        ---

        ### PERCEPÇÃO GERAL
        Elabore um parágrafo síntese abordando:
        - O sentimento predominante
        - A direção geral da avaliação (positiva, negativa, ambígua ou crítica)
        - A lógica discursiva que sustenta essa percepção

        ---

        ### CONCLUSÃO
        Apresente uma conclusão:
        - Objetiva
        - Estratégica
        - Fiel aos dados
        - Sem especulação
        - Sem recomendações fora do que os dados permitem

        A conclusão deve amarrar os principais achados qualitativos e reforçar o sentido geral das percepções analisadas.

        ---

        ### TABELA A SER ANALISADA:
        {tabela}
        """


    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return response.choices[0].message.content

def criar_title_graf(col):
    prompt = f"""
    Você é um analista de dados especializado em visualização de informações.
    Sua tarefa é gerar um título claro, conciso e informativo para um gráfico com base no nome da seguinte coluna:
    {col}

    Regras para criação do título:
    Retorne apenas o título final, SEM aspas, SEM comentários adicionais e TODO EM MAIÚSCULO.
    
    A frase deve ser direta e profissional, contendo no máximo 90 caracteres, incluindo espaços.

    Voce deve ignorar todos os prefixos da coluna, como "(LIS)", "(ESPONTÂNEA", "(OBJ)", "(ESTIMULADA", e quaisquer outros, 
    e criar um título a partir do nome da coluna, sem incluir esses termos.

    Exemplo de saída esperada:
    Se a coluna for "(ESPONTÂNEA) SE A ELEIÇÃO PARA PREFEITO(A) FOSSE HOJE, EM QUEM VOCÊ VOTARIA?", o título deve ser:

    SE A ELEIÇÃO PARA PREFEITO(A) FOSSE HOJE, EM QUEM VOCÊ VOTARIA?
    
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def criar_tab_abt_geral(df, coluna):
    falas = df[coluna].dropna().astype(str).tolist()

    prompt = f"""
    Você atuará EXCLUSIVAMENTE como ORGANIZADOR DE TEMAS.

    Seu papel é AGRUPAR as falas por similaridade de conteúdo,
    criando categorias consistentes, consolidadas e não redundantes.

    ============================================================
    OBJETIVO PRINCIPAL
    Identificar PADRÕES REAIS nas falas e AGRUPAR respostas
    que tratem do MESMO ASSUNTO, mesmo que usem palavras diferentes.
    ============================================================

    ============================================================
    REGRA DE CONSOLIDAÇÃO (OBRIGATÓRIA)

    Se dois rótulos representarem o MESMO TEMA,
    eles DEVEM ser UNIFICADOS.

    Exemplos de consolidação correta:
    - "FALTA DE MÉDICO" + "FALTA DE MÉDICOS" → "FALTA DE MÉDICO"
    - "SAÚDE RUIM" + "PROBLEMAS NA SAÚDE" → um único rótulo
    - "ESTRADA ESBURACADA" + "BURACO NAS RUAS" → um único rótulo
    - "SEGURANÇA" + "FALTA DE SEGURANÇA" → consolidar se forem semanticamente iguais

    É PROIBIDO criar categorias duplicadas ou quase idênticas.

    Antes de gerar o JSON, você DEVE verificar:
    - Existe algum rótulo muito parecido com outro?
    - Algum pode ser fundido?
    Se sim, consolide.

    ============================================================
    REGRA DE ESPECIFICIDADE

    - NÃO generalize temas específicos em macrotemas.
      Errado: "FALTA DE MÉDICO" → "SAÚDE"
      Certo:  "FALTA DE MÉDICO"

    - Só use macrotema se as falas forem realmente amplas.

    ============================================================
    REGRA SOBRE NÃO-OPINIÃO

    Existe apenas um rótulo permitido:
    "NÃO SABE / NÃO OPINOU"

    Use SOMENTE quando a fala for exclusivamente não-opinião
    e não contiver nenhum conteúdo temático.

    Se houver conteúdo junto, classifique pelo conteúdo.

    ============================================================
    REGRAS GERAIS

    1. NÃO analisar, explicar ou opinar.
    2. NÃO inventar temas.
    3. NÃO mencionar nomes próprios/candidatos.
    4. "OUTROS" apenas se realmente necessário (<5%).
    5. No máximo 20 rótulos totais.
    6. Rótulos devem ser:
       - CURTOS
       - EM LETRAS MAIÚSCULAS
       - Sem parênteses
       - "/" apenas se necessário
    7. Ordenar do maior para o menor %.

    ============================================================
    VERIFICAÇÃO FINAL (OBRIGATÓRIA)

    Antes de gerar o JSON:
    - Verifique se há rótulos redundantes
    - Verifique se há categorias excessivamente fragmentadas
    - Garanta que temas semanticamente iguais foram consolidados

    Se houver fragmentação indevida, REORGANIZE.

    ============================================================
    FORMATO (JSON APENAS)

    {{
      "resultados": [
        {{"RANK":"1º","TEMAS/ASSUNTOS":"EXEMPLO","%":0.00}}
      ]
    }}

    ============================================================

    FALAS:
    {falas}
    """

    response = client.chat.completions.create(
        model="gpt-5.1",
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    data = json.loads(response.choices[0].message.content)

    df = pd.DataFrame(data["resultados"])
    df["%"] = df["%"].astype(float).round(2)
    df["%"] = df["%"].astype(str) + "%"
    styled = estilizar_tabela_sem_divisao(df)
    return styled

def gerar_cabecalho_arquivo(nome_arquivo):
    prompt = f"""
Você receberá APENAS o nome de um arquivo de pesquisa eleitoral (CSV ou XLSX).

Sua tarefa é extrair, EXCLUSIVAMENTE a partir do nome do arquivo, as seguintes informações:
- Cidade
- Dia
- Mês (por extenso, em português)
- Ano

O nome do arquivo é a única fonte de informação e nele sempre terá essas informações de forma clara e explícita.
- Primeiro vem "questionario" ou pesquisa
- Depois o nome da cidade
- Depois a data onde o mês pode ser escrito por extenso ou em número, ou nos dois formatos.

REGRAS OBRIGATÓRIAS:
1. Não invente informações.
2. Se algum dado não estiver explícito no nome do arquivo, use "N/I".
3. Não explique o raciocínio.
4. Não use aspas, markdown ou emojis.
5. Retorne APENAS uma única frase, exatamente no formato abaixo.

FORMATO DA SAÍDA (obrigatório):
Pesquisa de Opinião - Cidade - dia de mes de ano PROIBIDA A DIVULGAÇÃO

Nome do arquivo:
{nome_arquivo}
"""

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def criar_paleta_cruzamento(n):
    prompt = f"""
        Você é um especialista em teoria das cores e visualização de dados.

        Sua tarefa é gerar uma paleta de cores para gráficos seguindo regras rígidas.

        REGRAS OBRIGATÓRIAS:

        1) A paleta deve conter EXATAMENTE {n} cores.
        2) As cores devem estar ordenadas do AZUL MAIS ESCURO para o AZUL MAIS CLARO, com o mais escuro sendo esse: "#0B1F4A" e o mais claro esse:"#B3DFFF"
        3) Deve haver ALTA DISTINÇÃO VISUAL entre cores consecutivas.
        4) Todas as cores devem ser adequadas para visualização em gráficos (boa legibilidade).
        5) Se e somente se {n} > 10:
        - Após os tons de azul, você pode adicionar tons de cinza.
        - Nunca use branco (#FFFFFF).
        - Os cinzas devem ir do mais claro para o mais escuro a partir da décima barra, sendo o cinza mais claro esse: "#E0E0E0" e o mais escuro esse: "#4D4D4D".
        6) Não repetir cores.
        7) Não usar gradientes quase idênticos.
        8) Sempre usar formato hexadecimal válido (#RRGGBB).

        FORMATO DE SAÍDA (OBRIGATÓRIO):
        - Retorne APENAS uma lista Python.
        - Não escreva nenhuma explicação.
        - Não escreva texto antes ou depois.
        - Não use markdown.
        - Apenas a lista.

        Exemplo de formato correto:

        [
        "#0A1F44",
        "#0F3A73",
        "#1457A6"
        ]

        Agora gere a paleta com exatamente {n} cores.
        """

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def gerar_titulo_subcapa(nome_arquivo):
    prompt = f"""
Você receberá APENAS o nome de um arquivo de pesquisa eleitoral (CSV ou XLSX).

Sua tarefa é extrair, EXCLUSIVAMENTE a partir do nome do arquivo, as seguintes informações:
- Cidade
- Dia
- Mês (por extenso, em português)
- Ano

O nome do arquivo é a única fonte de informação e nele sempre terá essas informações de forma clara e explícita.
- Primeiro vem "questionario" ou pesquisa
- Depois o nome da cidade, o que você deve usar para criar o título da subcapa
- Depois a data onde o mês pode ser escrito por extenso ou em número, ou nos dois formatos.

REGRAS OBRIGATÓRIAS:
1. Não invente informações.
2. Se algum dado não estiver explícito no nome do arquivo, use "N/I".
3. Não explique o raciocínio.
4. Não use aspas, markdown ou emojis.
5. Retorne APENAS uma única frase, exatamente no formato abaixo.

FORMATO DA SAÍDA OBRIGATÓRIO:
PESQUISA ELEITORAL\nCIDADE\nMÊS - ANO

Nome do arquivo:
{nome_arquivo}
"""

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

