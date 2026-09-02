---
description: Gerar relatorio da analise QA-GEO em Markdown (.md), texto puro (.txt) e HTML dashboard, com opcao de servir em localhost
agent: qa-geo-specialist
subtask: true
---

# QA-GEO Report - Gerar relatorio (.md, .txt, .html)

Voce e o gerador de relatorios da analise QA-GEO. Materializa o resultado da auditoria em tres formatos complementares usando a skill `qa-geo-report`.

## Site/Alvo: $ARGUMENTS

## Modo de Uso

### Modo 1 - A partir de uma URL (analise + relatorio)

```
/qa-geo-report https://www.exemplo.com.br
```

Passos:
1. Executar a analise QA-GEO completa (skill `qa-geo`)
2. Estruturar o resultado no **schema JSON canonico** (abaixo)
3. Invocar `generate_report.py` para gerar MD + TXT + HTML
4. Perguntar ao usuario se deseja abrir o HTML em `http://localhost:8080/relatorio.html`

### Modo 2 - A partir de um JSON existente

```
/qa-geo-report caminho/relatorio.json
```

Passos:
1. Carregar o JSON canonico
2. Gerar os 3 formatos
3. Opcionalmente servir o HTML

## Schema Canonico do Relatorio (JSON)

```json
{
  "metadata": {
    "url": "https://www.exemplo.com.br",
    "data": "2026-09-02T01:30:00Z",
    "versao_skill": "qa-geo@1.0.0",
    "fontes_oficiais": [
      "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide",
      "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"
    ]
  },
  "scores": {
    "seo": 82,
    "geo": 75,
    "generative_search": 80,
    "ai_retrieval": 88,
    "anti_hallucination": 95,
    "accessibility": 70,
    "mobile_first_geo": 78,
    "overall": 81
  },
  "status": "Bom",
  "checks": {
    "anti_patterns": [
      { "id": "llms_txt", "detected": false, "severity": "info", "note": "OK" },
      { "id": "noindex_mobile", "detected": false, "severity": "critical" },
      { "id": "lazy_load_primary", "detected": false, "severity": "critical" },
      { "id": "structured_data_parity", "detected": true, "severity": "high",
        "note": "Faltam schemas Breadcrumb, Product, VideoObject em /produtos" }
    ],
    "mobile_first": {
      "viewport_ok": true,
      "content_parity_ok": true,
      "metadata_parity_ok": true,
      "structured_data_parity_ok": false,
      "images_ok": true,
      "videos_ok": true,
      "no_anti_patterns_ok": true
    },
    "seo_tecnico": {
      "title": { "ok": true, "value": "Loja Exemplo - Produtos" },
      "meta_description": { "ok": true, "value": "..." },
      "viewport": { "ok": true, "value": "width=device-width, initial-scale=1" },
      "robots": { "ok": true, "value": "index, follow" },
      "canonical": { "ok": true, "value": "https://www.exemplo.com/" },
      "h1_unique": { "ok": true, "value": "Loja Exemplo" },
      "sitemap_xml": { "ok": true },
      "robots_txt": { "ok": true }
    },
    "structured_data": [
      { "type": "Organization", "present": true },
      { "type": "Breadcrumb", "present": false },
      { "type": "Product", "present": false }
    ],
    "accessibility": {
      "semantic_html": 10,
      "landmarks": 6,
      "headings": 12,
      "alt_text": 9,
      "labels": 8,
      "buttons": 6,
      "links": 7,
      "tables": 4,
      "aria": 8,
      "non_visual": 4,
      "mobile_first_a11y": 7,
      "agentic_ux": 6
    }
  },
  "findings": [
    {
      "id": "F001",
      "category": "mobile_first",
      "severity": "high",
      "title": "Structured data ausente na versao mobile",
      "description": "...",
      "recommendation": "...",
      "reference": "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"
    }
  ],
  "ai_retrieval_tests": {
    "factual": [
      { "pergunta": "...", "site": "...", "ia": "...", "match": true }
    ],
    "comparative": [],
    "intencao": [],
    "fan_out": [],
    "unique_pov": [],
    "multi_modal": []
  },
  "anti_hallucination_tests": {
    "total_perguntas": 10,
    "alucinacoes_detectadas": 0,
    "resultados": []
  },
  "recomendacoes_top5": [
    {
      "titulo": "...",
      "impacto": "Alto",
      "esforco": "Baixo",
      "referencia": "https://..."
    }
  ],
  "plano_acao": [
    { "ordem": 1, "acao": "...", "prazo": "1 semana" }
  ]
}
```

## Comandos

### 1. Apenas gerar (MD + TXT + HTML)

```bash
python .kilo/skills/qa-geo-report/scripts/generate_report.py \
  --json <relatorio.json> \
  --output-dir <dir_saida>
```

Saida:
- `<dir_saida>/relatorio.md`
- `<dir_saida>/relatorio.txt`
- `<dir_saida>/relatorio.html`

### 2. Gerar e servir HTML em localhost

```bash
python .kilo/skills/qa-geo-report/scripts/generate_report.py \
  --json <relatorio.json> \
  --output-dir <dir_saida> \
  --serve --port 8080
```

Abrir: `http://localhost:8080/relatorio.html`

### 3. Servir um relatorio ja gerado

```bash
python .kilo/skills/qa-geo-report/scripts/serve_report.py \
  --directory <dir_saida> \
  --port 8080
```

## Fluxo de Execucao

```
1. Receber $ARGUMENTS (URL ou caminho JSON)
       |
       v
2. Se URL: executar analise QA-GEO completa
       v
   Se JSON: ler arquivo
       |
       v
3. Montar/validar schema JSON canonico
       |
       v
4. Salvar JSON em <output-dir>/relatorio.json
       |
       v
5. Executar generate_report.py
       |
       v
6. Listar arquivos gerados
       |
       v
7. Perguntar ao usuario:
   "Deseja abrir o HTML em http://localhost:8080/relatorio.html? (s/n)"
   - Se sim: executar serve_report.py em background
   - Se nao: informar o caminho do relatorio.html
```

## Diretorio de Saida Padrao

- `<workspace>/qa-geo-out/<timestamp>/` para gerar relatorios completos
- Ou respeitar `--output-dir` se fornecido pelo usuario

Exemplo:
```
C:\QAI\qa-geo\qa-geo-out\2026-09-02_013045\
  relatorio.json
  relatorio.md
  relatorio.txt
  relatorio.html
```

## Pre-requisitos

- Python 3.8+ instalado e no PATH
- Apenas stdlib (sem `pip install` necessario)

## Saida Esperada (Exemplo)

```
[OK] Markdown:  C:\QAI\qa-geo\qa-geo-out\2026-09-02_013045\relatorio.md
[OK] Texto:     C:\QAI\qa-geo\qa-geo-out\2026-09-02_013045\relatorio.txt
[OK] HTML:      C:\QAI\qa-geo\qa-geo-out\2026-09-02_013045\relatorio.html

Deseja abrir o HTML em http://localhost:8080/relatorio.html? (s/n)
```

## Validacao da Skill

Para testar com o JSON de exemplo:

```bash
# 1. Gerar relatorio
python .kilo/skills/qa-geo-report/scripts/generate_report.py \
  --json .kilo/skills/qa-geo-report/examples/exemplo.json \
  --output-dir qa-geo-out/teste

# 2. Verificar saida
ls qa-geo-out/teste/

# 3. Servir
python .kilo/skills/qa-geo-report/scripts/serve_report.py \
  --directory qa-geo-out/teste \
  --port 8080

# 4. Abrir
start http://localhost:8080/relatorio.html
```

## Notas

- HTML e self-contained (CSS inline, sem CDN) - funciona offline
- MD segue CommonMark (compatibilidade GitHub/GitLab)
- TXT e ASCII-only (sem Unicode) - ideal para e-mail e logs antigos
- Servidor HTTP e single-threaded, uso APENAS local (127.0.0.1)

Inicie a geracao agora para: $ARGUMENTS
