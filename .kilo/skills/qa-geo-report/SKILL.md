---
name: qa-geo-report
description: Gera relatorios da analise QA-GEO em formatos Markdown (.md), texto puro (.txt) e HTML (com servidor local automatico). Inclui templates responsivos, dashboard de scores e anexos com referencias ao Google Search Central.
---

# QA-GEO Report Generator

Skill que materializa o resultado da analise QA-GEO em tres formatos complementares:

1. **Markdown** (`.md`) - para versionamento em Git, wiki, README
2. **Texto puro** (`.txt`) - para log, e-mail, anexos legados
3. **HTML** (`.html`) - dashboard visual com graficos, abrir no navegador OU servir em `http://localhost:<porta>`

## Quando Usar

- Ao final de uma analise `/qa-geo <URL>`
- Quando o usuario pedir "gerar relatorio", "exportar resultado", "mostrar relatorio"
- Para publicar a auditoria em wiki/Git/Pages
- Para apresentar a stakeholders nao-tecnicos (HTML)
- Para anexar a e-mails/tickets (TXT)

## Estrutura da Skill

```
.kilo/skills/qa-geo-report/
  SKILL.md              <- este arquivo
  scripts/
    generate_report.py  <- gerador principal (MD + TXT + HTML)
    serve_report.py     <- servidor HTTP local para abrir HTML
  templates/
    report.md.tpl       <- template Markdown
    report.txt.tpl      <- template texto puro
    report.html.tpl     <- template HTML (dashboard)
```

## Fluxo de Uso

```
1. Agente QA-GEO executa analise (coleta dados: scores, findings, testes)
       |
       v
2. Estrutura JSON canonica do relatorio (schema abaixo)
       |
       v
3. generate_report.py -j <relatorio.json> -o <dir_saida>
       |
       +--> relatorio.md
       +--> relatorio.txt
       +--> relatorio.html
       |
       v
4. (Opcional) serve_report.py -p 8080 -d <dir_saida>
       |
       v
5. Abre http://localhost:8080/relatorio.html no navegador
```

## Schema Canonico do Relatorio (JSON)

O agente QA-GEO deve produzir o relatorio no seguinte JSON antes de invocar o gerador:

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
      { "id": "content_fragmentation", "detected": false, "severity": "info" },
      { "id": "ai_rewriting", "detected": false, "severity": "info" },
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
      "title": { "ok": true, "value": "Loja Exemplo - Produtos de Qualidade" },
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
      { "type": "Product", "present": false },
      { "type": "VideoObject", "present": false }
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
      "description": "O JSON-LD de Breadcrumb nao esta presente em /produtos/x quando acessado via smartphone Googlebot.",
      "recommendation": "Adicionar o mesmo JSON-LD no HTML mobile e desktop, garantindo que as URLs no schema correspondam a versao servida.",
      "reference": "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"
    }
  ],
  "ai_retrieval_tests": {
    "factual": [
      { "pergunta": "Qual o preco do produto X?", "site": "R$ 99,90",
        "ia": "R$ 99,90", "match": true }
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
      "titulo": "Adicionar structured data Breadcrumb em mobile",
      "impacto": "Alto",
      "esforco": "Baixo",
      "referencia": "https://developers.google.com/search/docs/appearance/structured-data/breadcrumb"
    }
  ],
  "plano_acao": [
    { "ordem": 1, "acao": "Implementar paridade de JSON-LD mobile/desktop", "prazo": "1 semana" }
  ]
}
```

## Comandos

### 1. Gerar relatorio (MD + TXT + HTML)

```bash
python .kilo/skills/qa-geo-report/scripts/generate_report.py \
  --json <relatorio.json> \
  --output-dir <dir_saida>
```

Saida:
- `<dir_saida>/relatorio.md`
- `<dir_saida>/relatorio.txt`
- `<dir_saida>/relatorio.html`

### 2. Servir HTML em localhost

```bash
python .kilo/skills/qa-geo-report/scripts/serve_report.py \
  --directory <dir_saida> \
  --port 8080
```

Abrir no navegador: `http://localhost:8080/relatorio.html`

### 3. Tudo em um (gerar + servir)

```bash
python .kilo/skills/qa-geo-report/scripts/generate_report.py \
  --json <relatorio.json> \
  --output-dir <dir_saida> \
  --serve --port 8080
```

## Templates (resumo)

### Markdown (`report.md.tpl`)
- Header com URL, data, fontes oficiais
- Tabela de scores (SEO, GEO, Generative Search, AI Retrieval, Anti-Hallucination, Accessibility, Mobile-First GEO, Overall)
- Secoes: Accessibility, Mobile-First, Anti-Padroes GEO, Generative Search, AI Retrieval, Anti-Hallucination, Findings, Recomendacoes, Plano de Acao
- Codigo em blocos para exemplos de fix
- Links para Google Search Central

### Texto Puro (`report.txt.tpl`)
- Mesma estrutura, sem formatacao Markdown
- Ideal para `cat`, `less`, e-mail em texto, logs
- ASCII box-drawing para tabelas
- Comprimento limitado (sem code blocks longos)

### HTML (`report.html.tpl`)
- Dashboard responsivo (CSS Grid)
- Cards de scores com barra de progresso colorida (verde/amarelo/vermelho)
- Tabelas para findings, testes, anti-padroes
- Secoes colapsaveis (details/summary)
- Print-friendly (CSS @media print)
- Sem dependencias externas (zero JS framework) - JS minimo para interatividade basica
- Self-contained (CSS inline, sem CDN)
- Acessivel (landmarks, alt, aria)
- SEO-friendly (meta description, og:tags)

## Cores e Thresholds (consistente entre formatos)

| Score | Cor | Status |
|-------|-----|--------|
| 90-100 | Verde (#10B981) | Excelente |
| 70-89 | Azul (#3B82F6) | Bom |
| 50-69 | Amarelo (#F59E0B) | Atencao |
| 0-49 | Vermelho (#EF4444) | Critico |

## Integracao com o Agent `qa-geo-specialist`

O agent **DEVE**:

1. Conduzir a analise conforme skill `qa-geo` (SKILL.md original)
2. Estruturar o resultado no schema JSON canonico desta skill
3. Invocar `generate_report.py` ao final da analise
4. Perguntar ao usuario se deseja abrir o HTML em localhost

Exemplo de integracao no agent (ja adicionado em `qa-geo-specialist.md`):

```markdown
## Output Standards
...
- Apos analise, invocar skill `qa-geo-report` para gerar MD/TXT/HTML
- Por padrao, oferecer servir o HTML em `http://localhost:8080`
```

## Validacao da Skill

Para testar localmente:

```bash
# 1. Gerar relatorio de exemplo
python .kilo/skills/qa-geo-report/scripts/generate_report.py \
  --json .kilo/skills/qa-geo-report/examples/exemplo.json \
  --output-dir /tmp/qa-geo-out

# 2. Verificar saida
ls -la /tmp/qa-geo-out/

# 3. Servir
python .kilo/skills/qa-geo-report/scripts/serve_report.py \
  --directory /tmp/qa-geo-out \
  --port 8080

# 4. Abrir no navegador
start http://localhost:8080/relatorio.html
```

## Notas

- Todos os scripts sao standalone (apenas stdlib Python 3.8+)
- Nenhuma dependencia externa
- Servidor local e single-threaded (uso local apenas, NAO expor)
- HTML e self-contained (pode ser aberto offline)
- MD segue CommonMark
- TXT e ASCII-only (sem Unicode)
