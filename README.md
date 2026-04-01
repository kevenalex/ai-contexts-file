# Pesquisa: Engenharia de Contexto para Agentes de IA

Este projeto tem como objetivo analisar como repositórios populares de código aberto utilizam arquivos de configuração para agentes de IA, como AGENTS.md, CLAUDE.md, GEMINI.md, etc.

## Estrutura de pastas

- scripts/:
  - Arquivos de lógica: (ranking.py, detect_via_api.py, detect_via_clone.py) são os motores do projeto - Execução de ranking, coleta e classificação dos dados.
  - Arquivos de execução: (run_ranking.py, run_detect_context.py) arquivos para replicabilidade dos resultados e configurações de variáveis de execução.
- notebooks/: Pasta contendo os arquivos Jupyter Notebook para análise visual e estatística dos dados coletados.
- seart-data/: Pasta dedicada para alocar os dados advindos da busca do SEART.
- output_rankings/: Pasta onde o sistema salvará as tabelas de repositórios já classificados.
- output_detection/: Pasta onde o sistema salvará os resultados da busca por arquivos de contexto.

## Preparação do ambiente

Para garantir que o código funcione corretamente, você deve criar um ambiente virtual e instalar as bibliotecas necessárias uma única vez:

1. Crie o ambiente: python -m venv .venv
2. Ative o ambiente: source .venv/bin/activate
3. Instale as bibliotecas: pip install -r requirements.txt

## Fluxo de execução

O processo de pesquisa é dividido em três etapas:

### Etapa 1: Ranqueamento de Repositórios

Nesta etapa, o script lê os dados brutos e define quais são os repositórios mais importantes (maduros e populares).

Como usar:
1. Abra o arquivo scripts/run_ranking.py.
2. Altere a variável INPUT_FILE para o caminho do seu arquivo JSON (ex: "seart-data/dados.json").
3. Salve o arquivo e execute no terminal - a partir da root do projeto:
  > python scripts/run_ranking.py

Exemplo de Entrada: Um arquivo JSON com milhares de repositórios do GitHub.
Exemplo de Saída: Um arquivo CSV na pasta output_rankings/ contendo os repositórios ordenados por uma pontuação (rank_score).

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

O arquivo .env é ignorado pelo Git automaticamente para sua segurança.

---