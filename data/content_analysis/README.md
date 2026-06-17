# Análise de Conteúdo Estruturado

## Contexto
Esta pasta contém os dados resultantes da extração e classificação semântica dos cabeçalhos (`headings`) encontrados nos arquivos de contexto detectados.

## Arquivos
1. **`structure_analysis.csv`**: Contém a hierarquia de títulos extraída via Markdown parser.
   - Colunas: `repo`, `file_type`, `level` (#, ##, ###), `title_original`, `title_normalized`.
2. **`structure_analysis_classified.csv`**: Adiciona uma camada de inteligência sobre o arquivo anterior.
   - Coluna adicional: `category` (ex: `Testing Strategy`, `Architecture`, `Code Conventions`).

## Uso

