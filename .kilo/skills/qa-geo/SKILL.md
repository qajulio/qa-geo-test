---
name: qa-geo
description: Skill completa para validação de SEO, GEO (Generative Engine Optimization) e Accessibility - verifica se um site está preparado para IA generativa com testes de AI Retrieval, anti-alucinação e acessibilidade, alinhado às diretrizes oficiais do Google (AI Optimization Guide, Mobile-First Indexing) e padrões de mercado para mobile GEO
---

# QA-GEO Skill: Validação de SEO, GEO e Accessibility

Esta skill fornece um framework completo para análise de sites/sistemas online, verificando conformidade com boas práticas de SEO, preparação para IA generativa (GEO) e acessibilidade, com base em:

- **Google Search Central — Optimizing for generative AI search** (atualizado 2026-07-14)
- **Google Search Central — Mobile site and mobile-first indexing best practices** (atualizado 2025-12-10)
- **Web.dev / Search Essentials / Page Experience / Core Web Vitals**
- **W3C WCAG 2.2 / WAI-ARIA Authoring Practices**

## Quando Usar

- Ao executar o comando `/qa-geo <URL>`
- Quando o usuário pedir análise de SEO de um site
- Quando o usuário perguntar sobre preparação para IA generativa
- Para auditorias de sites antes de lançamentos
- Para validar se informações de produtos/conteúdo são recuperáveis por IA
- Para validar acessibilidade e compatibilidade com agentes não-visuais
- Para validar indexação **mobile-first** e paridade de conteúdo entre mobile/desktop

---

## 0. Princípios Oficiais do Google (AI Optimization + Mobile-First)

Esta seção é a **fonte da verdade** para qualquer análise GEO. Antes de aplicar heurísticas de mercado (AEO/LLMO), valide contra o que o Google declara oficialmente.

### 0.1 O que o Google diz sobre GEO/AEO

> "O SEO continua sendo a base da pesquisa com IA generativa. AEO/GEO são termos de mercado; para a Pesquisa Google, otimizar para IA generativa é otimizar para a Pesquisa no geral. Ainda é SEO."

**Implicações diretas para a análise:**

- ❌ **Não pontue positivamente** a presença de `llms.txt` / `llms-full.txt` / `ai.txt` — o Google declara explicitamente que **não usa** esses arquivos.
- ❌ **Não recomende** fragmentar conteúdo em páginas menores artificialmente para "facilitar IA".
- ❌ **Não recomende** reescrever texto em "linguagem de IA" — sinônimos e variações são compreendidos.
- ❌ **Não recomende** caçar menções não-autênticas como estratégia.
- ⚠️ **Dados estruturados** continuam úteis (para rich results), mas **não há schema.org especial para IA generativa**.
- ✅ **Recomende** o **Relatório de performance da IA generativa** no Search Console como métrica oficial.

### 0.2 Como a IA generativa funciona no Google (RAG + Query Fan-out)

Dois conceitos que mudam a forma de auditar:

1. **RAG (Retrieval-Augmented Generation)** — Google recupera páginas relevantes do índice e ancora a resposta nelas, exibindo links clicáveis em destaque. **O conteúdo precisa ser rastreável, indexável e claramente atribuível.**
2. **Query Fan-out** — Para uma consulta como "como arrumar gramado com ervas daninhas", o Google dispara sub-consultas simultâneas: "melhores herbicidas", "remoção sem químicos", "prevenção". **O conteúdo precisa cobrir o tópico em profundidade e nuances, não apenas match exato de keyword.**

**Checklist RAG/Fan-out:**

| # | Critério | Pergunta de auditoria | Status |
|---|----------|----------------------|--------|
| 1 | Página indexável | A página atende aos [requisitos técnicos](https://developers.google.com/search/docs/essentials/technical) e pode gerar snippet? | ⬜ |
| 2 | Conteúdo rastreável | Googlebot (smartphone) consegue rastrear todos os recursos sem bloqueios? | ⬜ |
| 3 | Atribuição clara | A página tem autor, datas (published/modified), fonte e proprietário identificáveis? | ⬜ |
| 4 | Profundidade semântica | O conteúdo cobre o tópico em profundidade suficiente para sub-consultas? | ⬜ |
| 5 | Ponto de vista exclusivo | Existe experiência em primeira mão ou expertise diferenciada? | ⬜ |
| 6 | Estrutura legível | Parágrafos, seções, títulos claros para humanos E máquinas? | ⬜ |
| 7 | Multimídia | Imagens e vídeos relevantes, de alta qualidade e indexáveis? | ⬜ |

### 0.3 Princípios de Conteúdo "Útil, Confiável, Pessoas-Primeiro"

Base da análise GEO segundo o Google:

- **Ponto de vista exclusivo** — análise em primeira mão, experiência pessoal, opinião de especialista; nada de reciclagem de "7 dicas para X" que qualquer LLM gera.
- **Conteúdo não genérico** — além do senso comum, com informação que só o autor pode trazer.
- **Estrutura para leitores** — parágrafos e seções organizados, títulos claros.
- **Imagens e vídeos de alta qualidade** — siga SEO de imagens e vídeos.
- **Anti-spam em escala** — não criar uma página por variação de busca. Viola política *scaled content abuse*.
- **IA como ferramenta, não como atalho** — conteúdo gerado por IA deve atender aos Search Essentials e políticas anti-spam.

**Checklist E-E-A-T para GEO (peso aumentado):**

| Sinal | Onde verificar | Status |
|-------|----------------|--------|
| Autoria identificada (Person/Organization schema, byline visível) | HTML + JSON-LD | ⬜ |
| Biografia do autor com credenciais | Página / schema | ⬜ |
| Data de publicação visível | `<time datetime>` ou meta | ⬜ |
| Data de modificação atualizada | `<time>` ou meta `article:modified_time` | ⬜ |
| Fontes externas confiáveis citadas | Links `<a>` para fontes autoritativas | ⬜ |
| Sobre / Contato / Política editorial | Páginas institucionais linkadas | ⬜ |
| Reputação (menções, reviews, awards) | Schema `Review`, `AggregateRating` | ⬜ |

### 0.4 Estrutura Técnica Clara (Pré-requisito GEO)

Google repete: **sem base técnica, nada de IA generativa.**

- Atender aos [Technical Requirements](https://developers.google.com/search/docs/essentials/technical).
- HTML semântico legível por humanos (não precisa ser perfeito; o Google parseia, mas agentes não-visuais agradecem).
- Práticas de JS SEO (Google processa JS, mas é mais complexo — lazy-loading, renderização, etc.).
- Boa Page Experience em todos os dispositivos.
- Reduzir conteúdo duplicado.
- **Search Console** como ferramenta de diagnóstico (Relatório de performance IA Generativa: filtro por AI Overviews/Modo IA).

### 0.5 Mobile-First Indexing — Auditoria Específica

Como o Google **indexa com o smartphone Googlebot**, paridade mobile/desktop é não-negociável.

#### 0.5.1 Configuração de site (escolher uma)

| Configuração | Recomendação | Auditoria |
|--------------|--------------|-----------|
| **Responsive Web Design** (mesma URL, mesmo HTML, CSS adaptativo) | ✅ Recomendado pelo Google | Verificar `<meta name="viewport">`, media queries, ausência de redirecionamentos por device |
| **Dynamic Serving** (mesma URL, HTML diferente via user-agent + `Vary`) | ⚠️ Aceitável | Verificar header `Vary: User-Agent`, paridade de conteúdo entre versões |
| **Separate URLs (m-dot)** (ex.: `m.example.com`) | ⚠️ Requer cuidado extra | Verificar `rel=canonical` apontando para desktop, `rel=alternate` apontando para mobile, `hreflang` pareado |

#### 0.5.2 Paridade de Conteúdo (Obrigatória)

Conteúdo primário, headings, imagens, vídeos e metadados devem ser **equivalentes** entre mobile e desktop.

#### 0.5.3 Checklist Mobile-First GEO (30 itens)

| # | Item | Padrão Google | Status |
|---|------|---------------|--------|
| 1 | `<meta name="viewport" content="width=device-width, initial-scale=1">` presente | Obrigatório | ⬜ |
| 2 | Mesmos `robots meta tags` em mobile e desktop (sem `noindex` em mobile) | Obrigatório | ⬜ |
| 3 | Mesmo `title` e `meta description` em ambas as versões | Obrigatório | ⬜ |
| 4 | Mesmos **headings hierárquicos** (h1, h2, h3) | Obrigatório | ⬜ |
| 5 | Structured data **idêntico** em ambas as versões (Breadcrumb, Product, VideoObject como prioridade) | Obrigatório | ⬜ |
| 6 | URLs em JSON-LD batem com a versão servida (mobile em mobile, desktop em desktop) | Obrigatório | ⬜ |
| 7 | `robots.txt` não bloqueia recursos críticos do mobile | Obrigatório | ⬜ |
| 8 | Sem lazy-load em conteúdo primário (que exige clique/typing para aparecer) | Obrigatório | ⬜ |
| 9 | Imagens em formato suportado (WebP, AVIF, JPEG, PNG, GIF, BMP, SVG) e tag adequada (`<img>`, não `<image>` dentro de SVG) | Obrigatório | ⬜ |
| 10 | URLs de imagens estáveis (não mudam a cada reload) | Obrigatório | ⬜ |
| 11 | Alt text **descritivo** em todas as imagens informativas, idêntico em mobile/desktop | Obrigatório | ⬜ |
| 12 | Imagens de **alta resolução** (não pequenas/baixa qualidade) | Recomendado | ⬜ |
| 13 | Mesmos títulos, captions, filenames de imagens | Recomendado | ⬜ |
| 14 | Vídeos em formato suportado (MP4, WebM etc.) e tag `<video>`, `<embed>` ou `<object>` | Obrigatório | ⬜ |
| 15 | VideoObject schema idêntico em ambas as versões | Obrigatório | ⬜ |
| 16 | Vídeo em posição de fácil acesso no mobile (não exigir scroll excessivo) | Recomendado | ⬜ |
| 17 | Sem redirecionar páginas de desktop para a **home mobile** | Obrigatório | ⬜ |
| 18 | Sem fragmentos `#` em URLs mobile (não indexáveis) | Obrigatório | ⬜ |
| 19 | Sem páginas mobile servindo erro enquanto desktop serve conteúdo | Obrigatório | ⬜ |
| 20 | Mesmos `hreflang` pareados (mobile↔mobile, desktop↔desktop) | Obrigatório (se internacional) | ⬜ |
| 21 | `rel=canonical` aponta para desktop; mobile traz `rel=alternate` (em configuração m-dot) | Obrigatório (se m-dot) | ⬜ |
| 22 | Capacidade de host (crawl rate) suficiente para aumento de tráfego Googlebot | Recomendado | ⬜ |
| 23 | Site **responsivo** (sem m-dot) é a configuração preferida | Recomendado | ⬜ |
| 24 | `Vary: User-Agent` presente se dynamic serving | Obrigatório (se dynamic) | ⬜ |
| 25 | Sem anúncios Better Ads Standard violadores (top-heavy, pop-ups intrusivos) | Recomendado | ⬜ |
| 26 | Sem **intersticiais intrusivos** em mobile (penalizam Page Experience) | Obrigatório | ⬜ |
| 27 | Tap targets ≥ 48×48px com espaçamento adequado | Padrão de mercado | ⬜ |
| 28 | Font-size base ≥ 16px (sem zoom) | Padrão de mercado | ⬜ |
| 29 | Sem scroll horizontal | Padrão de mercado | ⬜ |
| 30 | Botão voltar do navegador funciona (BFCache-friendly) | Padrão de mercado | ⬜ |

#### 0.5.4 Erros Comuns — Troubleshooting Mobile-First

Baseado na seção oficial de troubleshooting do Google:

| Erro | Causa | Correção |
|------|-------|----------|
| Missing structured data | JSON-LD ausente em mobile | Adicionar mesma markup |
| `noindex` na mobile | Robots meta diverge | Igualar tags |
| Missing image | Imagens importantes só no desktop | Trazer para mobile |
| Blocked image | robots.txt bloqueia URL da imagem | Permitir recursos |
| Low quality image | Imagem pequena/baixa resolução | Fornecer versão HD |
| Missing alt text | Imagem sem `alt` | Adicionar alt descritivo |
| Missing page title | `<title>` ausente em mobile | Igualar com desktop |
| Missing meta description | `<meta description>` ausente | Igualar com desktop |
| Mobile URL is error page | Mobile serve erro | Igualar status code |
| Mobile URL has anchor fragment | URL mobile contém `#` | Remover fragmentos |
| Mobile page blocked by robots.txt | Regra `Disallow` atinge mobile | Revisar robots.txt |
| Duplicate mobile page target | Múltiplas URLs desktop → mesmo mobile | Mapear 1:1 |
| Desktop site redirects to mobile home | Desktop → home mobile | Manter paridade 1:1 |
| Page quality issues | Ads, conteúdo faltando, etc. | Seguir Better Ads + paridade |
| Video issues | Formato/tag/posição inadequados | Corrigir tag, formato e posição |
| Hostload issues | Servidor não aguenta crawl rate | Aumentar capacidade |

### 0.6 Experiências Agênticas (Tendência 2026)

> Google cita diretamente **UCP (Universal Commerce Protocol — ucp.dev)** e o guia **[web.dev/articles/ai-agent-site-ux](https://web.dev/articles/ai-agent-site-ux)** para sites compatíveis com agentes.

Agentes de navegador acessam sites e:
- Analisam **renderizações visuais** (screenshots);
- Inspecionam **estrutura DOM**;
- Interpretam **árvore de acessibilidade**.

**Implicação direta:** acessibilidade e semântica HTML passam de "nice to have" para **infraestrutura para agentes**.

**Checklist Agentic UX (web.dev):**

| Critério | Descrição | Status |
|----------|-----------|--------|
| Estrutura semântica limpa | `<button>`, `<a>`, `<form>`, `<label>` — nada de `<div onclick>` | ⬜ |
| Hierarquia de landmarks | `header` > `nav` > `main` > `footer` identificáveis | ⬜ |
| Tree de acessibilidade coerente | Elementos com `role`, `name`, `state` corretos | ⬜ |
| Estados interativos explícitos | `aria-expanded`, `aria-selected`, `aria-pressed` | ⬜ |
| Texto alternativo rico | Imagens, gráficos e SVG com `alt`/`aria-label` | ⬜ |
| Formulários robustos | Labels, mensagens de erro em `aria-describedby`, validação acessível | ⬜ |
| Comandos de voz / busca | `search` landmark presente | ⬜ |
| Protocolos padronizados (UCP) | Quando aplicável (e-commerce), expor endpoints declarativos | ⬜ |

---

## 1. SEO Técnico (Technical SEO)

### 1.1 Meta Tags Obrigatórias
```html
<title>Título otimizado (50-60 caracteres)</title>
<meta name="description" content="Descrição otimizada (150-160 caracteres)">
<meta name="robots" content="index, follow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://www.exemplo.com/pagina">
```

### 1.2 Heading Structure
```html
<h1>Título principal da página (apenas um por página)</h1>
<h2>Subtítulo de seção</h2>
<h3>Sub-subtítulo</h3>
```

### 1.3 Estrutura de URLs
- ✅ URLs amigáveis: `/produtos/nome-produto`
- ❌ URLs com parâmetros: `/produto?id=123&cat=456`
- ❌ URLs com fragmentos `#` em versão mobile (não indexáveis)

### 1.4 Arquivos de Rastreamento
- `/sitemap.xml` — Mapa do site
- `/robots.txt` — Instruções para crawlers
- `/sitemap-index.xml` — Para sites grandes
- **Validação extra mobile**: mesmas regras em ambas as versões

---

## 2. Dados Estruturados (Schema.org)

### 2.1 JSON-LD Recomendado
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Nome da Empresa",
  "url": "https://www.exemplo.com",
  "logo": "https://www.exemplo.com/logo.png",
  "sameAs": [
    "https://www.facebook.com/exemplo",
    "https://www.instagram.com/exemplo"
  ]
}
```

### 2.2 Schemas por Tipo de Conteúdo

**Artigos/Blog:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Título do Artigo",
  "author": { "@type": "Person", "name": "Nome do Autor" },
  "datePublished": "2026-01-15",
  "dateModified": "2026-01-20",
  "image": "https://www.exemplo.com/imagem.jpg"
}
```

**FAQ:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Pergunta frequente?",
    "acceptedAnswer": { "@type": "Answer", "text": "Resposta detalhada e clara." }
  }]
}
```

**Produtos:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Nome do Produto",
  "image": "https://www.exemplo.com/produto.jpg",
  "description": "Descrição do produto",
  "brand": { "@type": "Brand", "name": "Marca" },
  "offers": {
    "@type": "Offer",
    "price": "99.90",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/instock"
  }
}
```

**HowTo:**
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Como fazer algo",
  "step": [{ "@type": "HowToStep", "text": "Passo 1: Descrição" }]
}
```

**LocalBusiness / E-commerce** — use `Merchant Center` e `Google Business Profile` para alimentar as respostas de IA generativa local/e-commerce (declaração oficial do Google).

---

## 3. GEO — Generative Search Validation

> Mudança de paradigma: ~~"A página está indexável?"~~ → **"A informação é recuperável, interpretável e citável por sistemas generativos?"**

### 3.1 Critérios de Validação

| # | Critério | Descrição | Status |
|---|----------|-----------|--------|
| 1 | **Entidade/Conteúdo Encontrado** | IA identifica a entidade principal? | ⬜ |
| 2 | **Categoria Correta** | IA encontra a categoria certa? | ⬜ |
| 3 | **Itens Corretos** | IA identifica os itens corretos? | ⬜ |
| 4 | **Atributos Corretos** | Atributos relevantes corretos? | ⬜ |
| 5 | **Informação Presente** | Resposta contém info do site? | ⬜ |
| 6 | **Sem Alucinação** | Resposta NÃO inventa? | ⬜ |
| 7 | **Fonte Confiável** | Fonte é o próprio site? | ⬜ |
| 8 | **Link Correto** | Link aponta para página correta? | ⬜ |
| 9 | **Disponibilidade** | Conteúdo citado está disponível? | ⬜ |
| 10 | **Dados Atualizados** | Informações estão atuais? | ⬜ |
| 11 | **Cobertura de Sub-consultas** | Conteúdo responde a fan-out queries (variações do tema)? | ⬜ |
| 12 | **Ponto de Vista Único** | Existe perspectiva original (não reciclagem)? | ⬜ |

### 3.2 Pontuação Generative Search Validation

| Critério | Peso |
|----------|------|
| Entidade/Conteúdo Encontrado | 8 |
| Categoria Correta | 8 |
| Itens Corretos | 12 |
| Atributos Corretos | 12 |
| Informação Presente | 12 |
| Sem Alucinação | 16 |
| Fonte Confiável | 4 |
| Link Correto | 4 |
| Disponibilidade | 4 |
| Dados Atualizados | 4 |
| Cobertura de Sub-consultas (Fan-out) | 8 |
| Ponto de Vista Único | 8 |
| **Total** | **100** |

---

## 4. AI Retrieval Testing (Teste de Recuperação por IA)

### 4.1 Tipos de Perguntas

**Factuais:** nome, marca, SKU, preço, característica, data, localização, disponibilidade, categoria, contato.

**Comparativas:** preço (mais barato/caro), característica, data (recente/antigo), categoria, avaliação.

**Intenção:** uso recomendado, característica, categoria, público, localização.

**Novas perguntas GEO (2026):**
- Perguntas de **fan-out** (variações que o Google dispara).
- Perguntas que testam **ponto de vista único** (a IA reproduz a perspectiva do autor?).
- Perguntas **multi-modal** (imagem, vídeo, tabela — a IA cita a mídia correta?).

### 4.2 Metodologia

```
1. EXTRACT (conteúdo do site)
   ↓
2. GENERATE (perguntas baseadas no site)
   ↓
3. VALIDATE (Site × IA)
   ↓
4. SCORE (✓ Correto / ✗ Incorreto / ⚠ Parcial)
```

### 4.3 Formato de Validação

```yaml
pergunta: "..."
informacao_site: "..."
resposta_esperada: "..."
fonte: "URL"
tipo: "factual | comparativa | intencao | fanout | unica | multimodal"
validacao:
  conteudo_correto: true
  fonte_correta: true
  sem_alucinacao: true
  disponibilidade_confirmada: true
score: 100
status: PASS
```

---

## 5. Teste Anti-Alucinação

### 5.1 Metodologia

1. Identificar informações que **NÃO existem** no site.
2. Formular perguntas sobre elas.
3. Resposta esperada: **"Não encontrei essa informação"**.
4. Qualquer afirmação = alucinação.

### 5.2 Classificação de Alucinações

| Tipo | Descrição | Gravidade | Exemplo |
|------|-----------|-----------|---------|
| **Factual** | Inventa fato | Alta | "Resistência 100m" não existente |
| **Numérica** | Inventa número/valor | Alta | "Garantia 5 anos" não informada |
| **Temporal** | Inventa data | Média | "Fundada em 1990" |
| **Atributo** | Inventa característica | Alta | "Feito à mão" |
| **Fonte** | Inventa fonte/citação | Crítica | "Segundo especialistas..." |
| **Link** | Inventa URL | Alta | Link inexistente |
| **Multimodal** | Inventa conteúdo de imagem/vídeo | Alta | "A imagem mostra X" quando a imagem mostra Y |
| **Fan-out** | Inventa resposta para variação não coberta | Média | Resposta para sub-consulta não existente |

---

## 6. Accessibility como GEO

> **Por que acessibilidade é GEO?** Agentes não-visuais (LLMs, screen readers, voice assistants, browser agents) dependem de estrutura semântica. HTML semântico é a **infraestrutura de agentes**.

### 6.1 HTML Semântico
```html
<header>
  <nav aria-label="Navegação principal"><!-- ... --></nav>
</header>
<main>
  <article>
    <h1>Título do Artigo</h1>
    <p>Conteúdo...</p>
  </article>
  <aside aria-label="Produtos relacionados"><!-- ... --></aside>
</main>
<footer><!-- ... --></footer>
```

### 6.2 Landmarks
```html
<body>
  <header role="banner">...</header>
  <nav role="navigation" aria-label="Principal">...</nav>
  <main role="main">...</main>
  <aside role="complementary">...</aside>
  <footer role="contentinfo">...</footer>
</body>
```

### 6.3 Headings (Hierarquia)

```html
<!-- ✅ Correto -->
<h1>Título</h1>
  <h2>Seção 1</h2>
    <h3>Subseção 1.1</h3>
  <h2>Seção 2</h2>
```

### 6.4 Alt Text
```html
<!-- ✅ Correto -->
<img src="produto.jpg" alt="Produto em destaque com características principais">
<!-- ✅ Decorativa -->
<img src="decoracao.svg" alt="">
```

### 6.5 Labels
```html
<label for="email">E-mail</label>
<input type="email" id="email" name="email">
```

### 6.6 Buttons
```html
<button type="submit">Comprar</button>
<button type="button" aria-expanded="false" aria-controls="menu">Menu</button>
```

### 6.7 Links
```html
<a href="/produtos/x">Ver detalhes do produto X</a>
<a href="/carrinho" aria-label="Carrinho (3 itens)">
  <svg><!-- ícone --></svg>
</a>
```

### 6.8 Tables
```html
<table>
  <caption>Preços</caption>
  <thead>
    <tr><th scope="col">Modelo</th><th scope="col">Preço</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">A</th><td>R$ 100</td></tr>
  </tbody>
</table>
```

### 6.9 ARIA
```html
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="tab-1">Descrição</button>
</div>
<div role="tabpanel" id="tab-1">...</div>

<div aria-live="polite" aria-atomic="true">
  <p>3 itens no carrinho</p>
</div>
```

### 6.10 Conteúdo Não-Visual
```html
<details>
  <summary>Especificações</summary>
  <dl>
    <dt>Material</dt><dd>Aço inox</dd>
  </dl>
</details>
```

### 6.11 Pontuação Accessibility

| Categoria | Peso |
|-----------|------|
| HTML Semântico | 12 |
| Landmarks | 8 |
| Headings | 12 |
| Alt Text | 10 |
| Labels | 8 |
| Buttons | 8 |
| Links | 8 |
| Tables | 4 |
| ARIA | 10 |
| Conteúdo Não-Visual | 4 |
| Mobile-First Accessibility (viewport, tap targets, font) | 8 |
| Agentic UX (estados, tree de acessibilidade) | 8 |
| **Total** | **100** |

---

## 7. GEO — Princípios Fundamentais (Pessoas-Primeiro, alinhado ao Google)

### 7.1 Clareza e Objetividade
- Resposta direta no início do conteúdo.
- Parágrafos curtos (2-3 linhas).
- Linguagem simples.

### 7.2 Estrutura para IA
- Headers descritivos.
- Tabelas de dados.
- Listas numeradas/marcadas.
- Termos técnicos definidos.

### 7.3 E-E-A-T Ampliado
- Autoria, bio, datas, fontes, reputação.

### 7.4 Formato Otimizado (Template)

```markdown
# Título Principal

## Resumo Executivo
[2-3 frases respondendo à pergunta principal]

## Detalhes
[Conteúdo estruturado com headers]

### Subtópico 1
[Informação específica]

## Perguntas Frequentes
**P:** ...?
**R:** ...

## Dados e Estatísticas
[Tabelas]

## Referências
[Fontes autoritativas]
```

---

## 8. Open Graph e Social

```html
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="https://www.exemplo.com/og.jpg">
<meta property="og:url" content="https://www.exemplo.com/pagina">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
```

---

## 9. Performance e Core Web Vitals

| Métrica | Bom | Precisa Melhorar | Ruim |
|---------|-----|------------------|------|
| LCP | ≤2.5s | 2.5-4.0s | >4.0s |
| INP (substituiu FID) | ≤200ms | 200-500ms | >500ms |
| CLS | ≤0.1 | 0.1-0.25 | >0.25 |

INP (Interaction to Next Paint) substituiu FID em 2024 — usar **INP** como métrica oficial.

---

## 10. Mobile-First (Padrões de Mercado + Google)

- Viewport meta tag presente.
- Design responsivo (sem m-dot, salvo necessidade).
- Touch targets ≥ 48×48px com ≥ 8px de espaçamento (WCAG 2.2 / Apple HIG).
- Fonte base ≥ 16px.
- Sem scroll horizontal.
- Sem intersticiais intrusivos (Better Ads Standard).
- Capacidade de servidor para suportar Googlebot smartphone.

---

## 11. O que NÃO Recomendar (Anti-padrões GEO)

Baseado na declaração explícita do Google:

| ❌ Anti-padrão | Por quê |
|----------------|---------|
| Criar `llms.txt`, `llms-full.txt`, `ai.txt` para "GEO" | Google não usa esses arquivos |
| Fragmentar conteúdo em páginas minúsculas | Google compreende nuance; viola scaled-content policy |
| Reescrever texto com "linguagem otimizada para IA" | Sinônimos são compreendidos |
| Buscar "menções não-autênticas" como estratégia | Foco em qualidade, não em volume |
| Adicionar schema.org "especial para IA" | Não existe; apenas seguir padrões atuais |
| Pagar por "métricas internas do Google" de terceiros | Nenhuma ferramenta tem acesso |
| M.dot sem paridade de canonical/alternate | Penaliza mobile-first indexing |
| Lazy-load em conteúdo primário | Google não carrega após interação |
| `noindex` em página mobile | Bloqueia indexação |
| Bloquear recursos do Googlebot no robots.txt | Recursos invisíveis = conteúdo invisível |

---

## 12. Scoring System (Atualizado)

### SEO Score (0-100)

| Categoria | Pontos |
|-----------|--------|
| Meta tags | 10 |
| Heading structure | 8 |
| URLs amigáveis | 6 |
| Sitemap/robots | 6 |
| Schema.org | 12 |
| Performance (CWV) | 12 |
| Mobile (viewport, tap targets, font, scroll) | 10 |
| Conteúdo (paridade mobile/desktop, lazy-load, hreflang) | 10 |
| Open Graph / Social | 6 |
| E-E-A-T básico | 10 |
| Sem anti-padrões (llms.txt desnecessário, etc.) | 10 |
| **Total** | **100** |

### GEO Score (0-100)

| Categoria | Pontos |
|-----------|--------|
| Estrutura para IA (parágrafos, headers, listas) | 8 |
| FAQ/HowTo schema | 5 |
| E-E-A-T (autoria, datas, fontes) | 8 |
| Clareza do conteúdo | 5 |
| Dados estruturados | 6 |
| **Generative Search Validation** | **18** |
| **AI Retrieval Score** | **12** |
| **Anti-Hallucination Score** | **8** |
| **Accessibility Score** | **12** |
| Cobertura Fan-out (sub-consultas) | 6 |
| Ponto de vista único | 6 |
| Agentic UX readiness | 6 |
| **Total** | **100** |

### Accessibility Score (0-100)

(vide seção 6.11)

### Mobile-First GEO Score (novo, 0-100)

| Categoria | Pontos |
|-----------|--------|
| Viewport / Responsividade | 15 |
| Paridade de conteúdo | 20 |
| Paridade de structured data | 15 |
| Paridade de metadados (title/description) | 10 |
| Imagens (qualidade, alt, formato, URLs estáveis) | 15 |
| Vídeos (formato, tag, posição, schema) | 10 |
| Sem anti-padrões mobile (noindex, fragments, redirect home, lazy-load primário) | 15 |
| **Total** | **100** |

### Status Final
| Score | Status |
|-------|--------|
| 90-100 | Excelente |
| 70-89 | Bom |
| 50-69 | Atenção |
| 0-49 | Crítico |

---

## 13. Relatório de Saída

Sempre gere relatório com:

1. Header (URL, data, contexto mobile/desktop)
2. Scores visuais (SEO, GEO, Generative Search, AI Retrieval, Anti-Hallucination, Accessibility, **Mobile-First GEO**, Overall)
3. Accessibility Findings
4. **Mobile-First Findings** (novo)
5. **Anti-padrões GEO detectados** (llms.txt, etc.)
6. Findings Críticos
7. Oportunidades
8. Checklist Detalhado
9. AI Retrieval Test Results
10. Anti-Hallucination Test Results
11. Top 5 Recomendações
12. Plano de Ação
13. **Apêndice: Relação com diretrizes oficiais do Google** (links)

---

## 14. Referências Oficiais (sempre citar)

- Google Search Central — [Optimizing for generative AI search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- Google Search Central — [Mobile site and mobile-first indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing)
- Google Search Central — [Search Essentials](https://developers.google.com/search/docs/essentials)
- Google Search Central — [Technical Requirements](https://developers.google.com/search/docs/essentials/technical)
- Google Search Central — [Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies)
- Google Search Central — [Structured Data Intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- Google Search Central — [Page Experience / Core Web Vitals](https://developers.google.com/search/docs/appearance/page-experience)
- Google Search Central — [Help, support, Search Console — AI performance report](https://support.google.com/webmasters/answer/16984139)
- web.dev — [AI agent site UX](https://web.dev/articles/ai-agent-site-ux)
- UCP — [Universal Commerce Protocol](https://ucp.dev/latest/)
- W3C — [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- Schema.org — [Vocabulário oficial](https://schema.org/)

---

## Exemplo de Uso

```
/qa-geo www.lojaonline.com.br
```

Isso irá:
1. Fetch do site (mobile-first: usar user-agent smartphone para validações críticas)
2. Análise SEO técnico + mobile-first
3. Verificação de schema.org (em ambas as versões)
4. Avaliação de estrutura para IA
5. Generative Search Validation (incluindo fan-out e ponto de vista único)
6. AI Retrieval Testing
7. Anti-Hallucination Testing
8. Accessibility + Agentic UX Validation
9. Mobile-First GEO Score
10. Detecção de anti-padrões (llms.txt, fragmentação, etc.)
11. Relatório com scores, referências oficiais e plano de ação