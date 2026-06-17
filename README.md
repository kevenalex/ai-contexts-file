# Pesquisa: Engenharia de Contexto para Agentes de IA

Este projeto tem como objetivo analisar como repositórios populares de código aberto utilizam arquivos de configuração para agentes de IA, como AGENTS.md, CLAUDE.md, GEMINI.md, etc.

## Estrutura do Repositório (Architecture/Structure)
- `scripts/`: Contém a lógica central de processamento.
    - `ranking/ranking.py`, `ranking/run_ranking.py`: Motor e script de entrada da Etapa 1 (módulo Python — ver instruções de execução abaixo).
    - `detect_via_api.py`, `detect_via_clone.py`, `run_detect_context.py`: Motor e script de entrada da Etapa 2.
- `notebooks/`: Análise visual e estatística dos dados.
- `data/`: Centraliza todos os arquivos de dados do projeto.
    - `input_data/`: Dados brutos de entrada, intocáveis (JSON do SEART).
    - `analysis_data/`: Dados transformados pelos scripts (destino atual da Etapa 1; em migração — coletas antigas ainda estão em `output_rankings/`).
  
    - `context_detection/`: Resultados da Etapa 2 (CSV com detecção binária de arquivos).
    - `content_analysis/`: Resultados de extração de estrutura e classificação de cabeçalhos.
    - `testing_analysis/`: Dados extraídos para validação de fidelidade de testes.
- `.env`: Armazena o `GITHUB_TOKEN` (não comitar).

## Stack Tecnológica (Tech Stack)
- **Linguagem:** Python 3.x
- **Bibliotecas Principais:** Pandas, NumPy, Requests, Python-dotenv.
- **Visualização:** Matplotlib, Seaborn, Jupyter Notebook.

## Configuração e Instalação (Setup)
1. Criar ambiente virtual: `python -m venv .venv`
2. Ativar ambiente: `source .venv/bin/activate`
3. Instalar dependências: `pip install -r requirements.txt`
4. Configurar `.env`: Adicionar `GITHUB_TOKEN=seu_token`. (Necessário para evitar bloqueios por excesso de acessos na API do GitHub).

## Fluxo de Trabalho (Workflow)
O processo deve seguir rigorosamente estas etapas:

1. **Ranqueamento (Etapa 1):** 
   - **Objetivo:** Lê os dados brutos e define os repositórios mais importantes (maduros e populares).
   - **Arquivo:** `scripts/ranking/run_ranking.py`
   - **Variáveis principais:** `INPUT_FILE` (em `data/input_data/`), `OUTPUT_FOLDER` (`data/analysis_data/`).
   - **Execução:** `python -m scripts.ranking.run_ranking` (a partir da raiz do projeto — necessário rodar como módulo por causa do import `scripts.ranking.ranking`).

2. **Detecção (Etapa 2):** 
   - **Objetivo:** Verifica quais repositórios do ranking possuem arquivos para IA.
   - **Arquivo:** `scripts/run_detect_context.py`
   - **Variáveis principais:** `MODE` ("API" ou "CLONE"), `INPUT_CSV` (em `data/output_rankings/`), `OUTPUT_FOLDER` (`data/context_detection/`).
   - **Execução:** `python scripts/run_detect_context.py`

3. **Análise de Conteúdo e Fidelidade (Etapa 3):**
   - **Objetivo:** Extrair estrutura, classificar e validar o conteúdo dos arquivos detectados.
   - **Scripts:** `extract_content_structure.py`, `classify_headings.py`, `extract_testing_details.py`.
   - **Saídas:** Alocadas em `data/content_analysis/` e `data/testing_analysis/`.

### Etapa 1: Ranqueamento de Repositórios

Nesta etapa, o script lê os dados brutos e define quais são os repositórios mais importantes (maduros e populares).

Como usar:
1. Abra o arquivo scripts/ranking/run_ranking.py.
2. Altere a variável INPUT_FILE para o caminho do seu arquivo JSON (ex: "data/input_data/dados.json").
3. Salve o arquivo e execute no terminal - a partir da raiz do projeto:
  > python -m scripts.ranking.run_ranking

Exemplo de Entrada: Um arquivo JSON com milhares de repositórios do GitHub.
Exemplo de Saída: Um arquivo CSV na pasta analysis_data/ contendo os repositórios ordenados por uma pontuação (rank_score).

### Etapa 2: Detecção de Contexto de IA

Nesta etapa, o script pega a lista gerada na Etapa 1 e verifica quais daqueles repositórios possuem arquivos para IA.

Como usar:
1. Abra o arquivo scripts/run_detect_context.py.
2. Defina o MODE como "API" ou "CLONE".
3. Ajuste a variável INPUT_CSV para apontar para o arquivo gerado na Etapa 1.
4. Salve o arquivo e execute no terminal:
  > python scripts/run_detect_context.py

Exemplo de Entrada: O arquivo CSV gerado pelo ranking (ex: ranked_dados.csv).
Exemplo de Saída: Um novo arquivo CSV na pasta output_detection/ com colunas indicando 0 ou 1 para a presença de arquivos como AGENTS.md e CLAUDE.md.

### Etapa 3: Análise e Visualização

Nesta etapa, utilizamos os notebooks para transformar os dados coletados em gráficos e insights.

Como usar:
1. Com o ambiente virtual ativo, execute: jupyter notebook
2. Abra a pasta notebooks/ e escolha um dos arquivos:
  - analysis_data.ipynb: Gera gráficos de distribuição e adesão para uma única coleta de dados.
  - analysis_comparison.ipynb: Compara resultados de datas diferentes para mostrar a evolução temporal da adesão.

## Uso do Token do GitHub

Para evitar bloqueios por excesso de acessos na API do GitHub, você deve:
1. Criar um arquivo chamado .env na raiz do projeto.
2. Escrever dentro dele: GITHUB_TOKEN=seu_token_aqui

---
