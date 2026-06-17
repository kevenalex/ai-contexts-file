# Scripts

Módulos de processamento (lógica central) e scripts de entrada (`run_*.py`) do pipeline de pesquisa. Ver `README.md` na raiz do projeto para o fluxo de execução completo (Etapas 1-3).

## Atribuição de Código

- **`ranking.py`**: O algoritmo de ranqueamento (score de popularidade + maturidade, com penalidades para repositórios educacionais/baixo teor de código) foi copiado/adaptado do material suplementar do artigo *"Context Engineering for AI Agents in Open-Source Software"*, disponível em https://zenodo.org/records/18368326 (arquivo `1_data-collection/ranking.py`).

## Demais Scripts

- `run_ranking.py`: Script de entrada da Etapa 1 — configura `INPUT_FILE`/`OUTPUT_FOLDER` e chama `rank_repositories()`.
- `detect_via_api.py`, `detect_via_clone.py`, `run_detect_context.py`: Detecção de arquivos de contexto de IA (Etapa 2).
- `extract_content_structure.py`, `classify_headings.py`, `extract_testing_details.py`: Extração e classificação de conteúdo/estrutura dos arquivos de contexto (Etapa 3).
