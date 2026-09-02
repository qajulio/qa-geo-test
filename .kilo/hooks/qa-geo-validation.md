---
name: qa-geo-validation
description: Hook para validacao automatica de SEO, GEO e Mobile-First Indexing antes de publicacoes, alinhado com Google Search Central
events:
  - pre-commit
  - pre-push
---

# QA-GEO Validation Hook

Este hook executa validacoes de SEO, GEO (Generative Engine Optimization) e Mobile-First Indexing automaticamente em momentos especificos do workflow, com base nas diretrizes oficiais do Google Search Central.

## Referencias Oficiais

- [Optimizing for generative AI search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Mobile site and mobile-first indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing)
- [Search Essentials](https://developers.google.com/search/docs/essentials)

## Eventos

### pre-commit
Executa validacao basica de SEO + GEO em arquivos HTML/Markdown modificados.

### pre-push
Executa validacao completa (incluindo Mobile-First parity) antes de push para repositorio.

## Validacoes Automaticas

### Para Arquivos HTML

#### SEO Basico
- [ ] Title tag presente e com tamanho adequado (50-60 chars)
- [ ] Meta description presente (150-160 chars)
- [ ] H1 unico por pagina
- [ ] Imagens com alt text descritivo
- [ ] Links com texto ancora descritivo
- [ ] Canonical URL definida

#### Mobile-First
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">` presente
- [ ] Sem lazy-load em conteudo primario (Google nao dispara interacoes)
- [ ] Imagens em formato suportado (WebP/AVIF/JPEG/PNG/GIF/BMP/SVG)
- [ ] Sem tag `<image>` dentro de SVG (Google nao indexa)
- [ ] Videos em tag suportada (`<video>`, `<embed>`, `<object>`)

#### GEO Readiness
- [ ] HTML semantico (header, nav, main, article, aside, footer)
- [ ] Landmarks com aria-label
- [ ] Hierarquia de headings (h1 > h2 > h3)
- [ ] Autor e datas (published/modified) identificaveis
- [ ] E-E-A-T signals (sobre/contato linkados, fontes citadas)
- [ ] FAQ/HowTo schema quando aplicavel

#### Anti-Padroes GEO (sinalizar)
- [ ] Nenhum `llms.txt`/`llms-full.txt`/`ai.txt` (Google nao usa)
- [ ] Nenhum `<div onclick>` (usar `<button>`)
- [ ] Nenhum "AI-rewriting" artificial

### Para Arquivos Markdown
- [ ] Frontmatter com title e description
- [ ] Headers hierarquicos
- [ ] Imagens com alt text
- [ ] Links internos validos

### Para Sites em Producao

#### SEO Tecnico
- [ ] Schema.org valido (JSON-LD)
- [ ] Sitemap acessivel
- [ ] robots.txt presente
- [ ] Open Graph tags

#### Mobile-First Indexing (CRITICO)
- [ ] Paridade de conteudo mobile vs desktop
- [ ] Paridade de structured data (mesmos schemas, URLs corretas)
- [ ] Paridade de metadados (title/description identicos)
- [ ] Sem `noindex` em mobile
- [ ] Sem fragmentos `#` em URLs mobile
- [ ] Sem redirect de desktop para home mobile
- [ ] Error page status igual em ambas versoes
- [ ] Better Ads Standard compliance
- [ ] Sem intersticiais intrusivos em mobile

#### GEO / AI Optimization
- [ ] E-E-A-T signals presentes (autoria, datas, fontes, sobre/contato)
- [ ] Schema.org para FAQ/HowTo quando aplicavel
- [ ] Imagens de alta qualidade com alt descritivo
- [ ] Videos com VideoObject schema
- [ ] Sem fragmentos `#` (afeta mobile-first)

## Configuracao

```json
{
  "hooks": {
    "pre-commit": [
      {
        "name": "qa-geo-basic",
        "command": "qa-geo validate --basic",
        "files": ["*.html", "*.md", "*.mdx"]
      }
    ],
    "pre-push": [
      {
        "name": "qa-geo-full",
        "command": "qa-geo validate --full --mobile-first",
        "url": "$DEPLOY_URL"
      }
    ]
  }
}
```

## Comandos Disponiveis

### Validacao Basica
```bash
qa-geo validate --basic
```
Verifica arquivos locais modificados (SEO + GEO basico).

### Validacao Completa (com Mobile-First)
```bash
qa-geo validate --full https://www.site.com.br
```
Verifica site em producao com user-agent smartphone, incluindo paridade mobile/desktop.

### Validacao de Schema
```bash
qa-geo validate --schema https://www.site.com.br
```
Verifica apenas dados estruturados (JSON-LD, Microdata, RDFa).

### Validacao de Performance
```bash
qa-geo validate --performance https://www.site.com.br
```
Verifica Core Web Vitals (LCP, INP, CLS).

### Validacao Mobile-First
```bash
qa-geo validate --mobile-first https://www.site.com.br
```
Verifica paridade mobile vs desktop, viewport, structured data, imagens, videos.

### Validacao GEO / AI
```bash
qa-geo validate --geo https://www.site.com.br
```
Verifica E-E-A-T, RAG-readiness, fan-out coverage, anti-padroes GEO (llms.txt, etc.).

## Integracao com CI/CD

### GitHub Actions
```yaml
name: QA-GEO Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run QA-GEO Mobile-First
        run: |
          npx qa-geo validate --full --mobile-first ${{ secrets.SITE_URL }}
      - name: Run QA-GEO GEO/AI
        run: |
          npx qa-geo validate --geo ${{ secrets.SITE_URL }}
```

### GitLab CI
```yaml
qa-geo:
  stage: test
  script:
    - npx qa-geo validate --full --mobile-first $SITE_URL
    - npx qa-geo validate --geo $SITE_URL
  only:
    - main
```

## Saida do Hook

O hook retorna:
- **0**: Sucesso - todas as validacoes passaram
- **1**: Aviso - problemas nao criticos encontrados (ex.: melhorias de GEO)
- **2**: Erro - problemas criticos que bloqueiam publicacao (ex.: noindex em mobile, noindex de conteudo primario)

## Anti-Padroes Detectados Automaticamente

O hook sinaliza automaticamente:

| Anti-Padrao | Gravidade | Fonte |
|-------------|-----------|-------|
| Presenca de `llms.txt` / `llms-full.txt` / `ai.txt` | Info | Google AI Optimization Guide |
| `noindex` em pagina mobile | Critical | Google Mobile-First Indexing |
| Lazy-load em conteudo primario | Critical | Google Mobile-First Indexing |
| Bloqueio de recursos Googlebot | Critical | Google Search Essentials |
| Structured data ausente em mobile | High | Google Mobile-First Indexing |
| Imagens sem alt text | High | Google Images SEO |
| Tag `<image>` dentro de SVG | High | Google Mobile-First Indexing |
| Fragmentos `#` em URL mobile | Medium | Google Mobile-First Indexing |
| Conteudo mobile < desktop | High | Google Mobile-First Indexing |
| Intersticiais intrusivos em mobile | Medium | Google Page Experience |
| m-dot sem canonical/alternate pairing | High | Google Mobile-First Indexing |
| Tap targets < 48px | Medium | WCAG 2.2 / Apple HIG |
| Font-size base < 16px | Medium | WCAG 2.2 / Mobile UX |
| `<div onclick>` ao inves de `<button>` | Medium | WAI-ARIA Authoring Practices |

## Exemplo de Relatorio

```
[QA-GEO] Validacao iniciada (mobile-first + GEO)...
[QA-GEO] Verificando meta tags... OK
[QA-GEO] Verificando viewport... OK
[QA-GEO] Verificando structured data parity... OK
[QA-GEO] Verificando paridade de conteudo mobile/desktop... OK
[QA-GEO] Verificando paridade de metadata... OK
[QA-GEO] Verificando imagens (formato/alt/URLs estaveis)... OK
[QA-GEO] Verificando schema.org... OK
[QA-GEO] Verificando performance... OK
[QA-GEO] Verificando E-E-A-T... OK
[QA-GEO] Anti-padroes GEO: nenhum llms.txt/ai.txt detectado OK
[QA-GEO] Detectando fragmentacao artificial... OK
[QA-GEO] Detectando noindex em mobile... OK

Resultado: 0 critical, 0 warning, 0 info
Status: APPROVED
```

### Exemplo com Avisos

```
[QA-GEO] Validacao iniciada...
[QA-GEO] Verificando meta tags... OK
[QA-GEO] Verificando viewport... OK
[QA-GEO] Verificando structured data parity... OK
[QA-GEO] Verificando paridade de conteudo mobile/desktop... OK
[QA-GEO] Verificando paridade de metadata... OK
[QA-GEO] Verificando imagens (formato/alt/URLs estaveis)... OK
[QA-GEO] Verificando schema.org... WARN (1)
[QA-GEO] Verificando performance... OK
[QA-GEO] Verificando E-E-A-T... OK
[QA-GEO] Anti-padroes GEO: detectado llms.txt (nao utilizado pelo Google) INFO
[QA-GEO] Detectando fragmentacao artificial... OK
[QA-GEO] Detectando noindex em mobile... OK

Resultado: 0 critical, 1 warning, 1 info
Status: APPROVED WITH WARNINGS
```

### Exemplo Bloqueado

```
[QA-GEO] Validacao iniciada...
[QA-GEO] Verificando meta tags... OK
[QA-GEO] Verificando viewport... OK
[QA-GEO] Verificando structured data parity... FAIL (paridade de schema quebrada)
[QA-GEO] Verificando paridade de conteudo mobile/desktop... OK
[QA-GEO] Verificando paridade de metadata... OK
[QA-GEO] Verificando imagens (formato/alt/URLs estaveis)... OK
[QA-GEO] Verificando schema.org... FAIL
[QA-GEO] Verificando performance... OK
[QA-GEO] Verificando E-E-A-T... OK
[QA-GEO] Anti-padroes GEO: nenhum detectado OK
[QA-GEO] Detectando fragmentacao artificial... OK
[QA-GEO] Detectando noindex em mobile... FAIL (noindex detectado em /produtos)

Resultado: 3 critical, 0 warning, 0 info
Status: BLOCKED
```
