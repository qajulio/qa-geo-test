#!/usr/bin/env python3
"""qa-geo-report generator - gera relatorio QA-GEO em MD, TXT e HTML (stdlib only)."""
import argparse, json, sys, os
import html as html_lib
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"

def score_color(score):
    if score >= 90: return "#10B981"
    if score >= 70: return "#3B82F6"
    if score >= 50: return "#F59E0B"
    return "#EF4444"

def score_status(score):
    if score >= 90: return "Excelente"
    if score >= 70: return "Bom"
    if score >= 50: return "Atencao"
    return "Critico"

def safe_load_json(path):
    if not path.exists():
        sys.exit(f"Erro: arquivo JSON nao encontrado: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Erro: JSON invalido em {path}: {e}")

def render_markdown(data):
    md = []
    md.append(f"# Relatorio QA-GEO: {data['metadata']['url']}")
    md.append("")
    md.append(f"**Data**: {data['metadata'].get('data', datetime.utcnow().isoformat() + 'Z')}")
    md.append(f"**Versao da skill**: {data['metadata'].get('versao_skill', 'qa-geo@1.0.0')}")
    md.append("")
    if data['metadata'].get('fontes_oficiais'):
        md.append("**Fontes oficiais consultadas**:")
        for src in data['metadata']['fontes_oficiais']:
            md.append(f"- <{src}>")
        md.append("")
    md.append("## Resumo Executivo - Scores")
    md.append("")
    md.append("| Categoria | Score | Status |")
    md.append("|-----------|------:|--------|")
    labels = {
        "seo": "SEO", "geo": "GEO",
        "generative_search": "Generative Search Validation",
        "ai_retrieval": "AI Retrieval",
        "anti_hallucination": "Anti-Hallucination",
        "accessibility": "Accessibility",
        "mobile_first_geo": "Mobile-First GEO (novo)",
        "overall": "Overall",
    }
    for k, label in labels.items():
        s = data['scores'].get(k, 0)
        md.append(f"| {label} | {s} | {score_status(s)} |")
    md.append("")
    md.append(f"**Status Final**: {data.get('status', score_status(data['scores'].get('overall', 0)))}")
    md.append("")
    md.append("## Anti-Padroes GEO Detectados")
    md.append("")
    md.append("> Baseado nas diretrizes oficiais do Google Search Central.")
    md.append("")
    detected = [a for a in data['checks'].get('anti_patterns', []) if a.get('detected')]
    if not detected:
        md.append("Nenhum anti-padrao GEO critico detectado.")
    else:
        md.append("| ID | Severidade | Nota |")
        md.append("|----|------------|------|")
        for a in detected:
            md.append(f"| `{a.get('id','')}` | {a.get('severity','')} | {a.get('note','')} |")
    md.append("")
    md.append("## Mobile-First Findings")
    md.append("")
    mf = data['checks'].get('mobile_first', {})
    md.append("| Item | Status |")
    md.append("|------|--------|")
    for k, v in mf.items():
        status = "OK" if v else "FAIL"
        md.append(f"| {k} | {status} |")
    md.append("")
    md.append("## SEO Tecnico")
    md.append("")
    seo = data['checks'].get('seo_tecnico', {})
    md.append("| Item | OK | Valor |")
    md.append("|------|:--:|-------|")
    for k, v in seo.items():
        if isinstance(v, dict):
            md.append(f"| {k} | {'OK' if v.get('ok') else 'FAIL'} | {v.get('value','')} |")
        else:
            md.append(f"| {k} | {'OK' if v else 'FAIL'} | |")
    md.append("")
    md.append("## Structured Data")
    md.append("")
    md.append("| Tipo | Presente |")
    md.append("|------|----------|")
    for sd in data['checks'].get('structured_data', []):
        md.append(f"| {sd.get('type','')} | {'Sim' if sd.get('present') else 'Nao'} |")
    md.append("")
    md.append("## Accessibility")
    md.append("")
    a = data['checks'].get('accessibility', {})
    md.append("| Componente | Pontos |")
    md.append("|------------|-------:|")
    for k, v in a.items():
        md.append(f"| {k} | {v} |")
    a_total = sum(a.values()) if a else 0
    md.append(f"| **Total** | **{a_total}/100** |")
    md.append("")
    md.append("## Findings")
    md.append("")
    for f in data.get('findings', []):
        md.append(f"### {f.get('id','')} - {f.get('title','')}")
        md.append("")
        md.append(f"- **Categoria**: {f.get('category','')}")
        md.append(f"- **Severidade**: {f.get('severity','')}")
        md.append(f"- **Descricao**: {f.get('description','')}")
        md.append(f"- **Recomendacao**: {f.get('recommendation','')}")
        if f.get('reference'):
            md.append(f"- **Referencia oficial**: <{f['reference']}>")
        md.append("")
    md.append("## AI Retrieval Test Results")
    md.append("")
    rt = data.get('ai_retrieval_tests', {})
    for tipo in ['factual', 'comparative', 'intencao', 'fan_out', 'unique_pov', 'multi_modal']:
        testes = rt.get(tipo, [])
        if testes:
            md.append(f"### Perguntas {tipo}")
            md.append("")
            md.append("| Pergunta | Site | IA | Match |")
            md.append("|----------|------|-----|-------|")
            for t in testes:
                match = "OK" if t.get('match') else "FAIL"
                md.append(f"| {t.get('pergunta','')} | {t.get('site','')} | {t.get('ia','')} | {match} |")
            md.append("")
    md.append("## Anti-Hallucination Test Results")
    md.append("")
    ah = data.get('anti_hallucination_tests', {})
    md.append(f"- Total de perguntas: {ah.get('total_perguntas', 0)}")
    md.append(f"- Alucinacoes detectadas: {ah.get('alucinacoes_detectadas', 0)}")
    md.append("")
    md.append("## Recomendacoes Prioritarias (Top 5)")
    md.append("")
    md.append("| # | Titulo | Impacto | Esforco |")
    md.append("|---|--------|---------|---------|")
    for i, r in enumerate(data.get('recomendacoes_top5', [])[:5], 1):
        md.append(f"| {i} | {r.get('titulo','')} | {r.get('impacto','')} | {r.get('esforco','')} |")
    md.append("")
    md.append("## Plano de Acao")
    md.append("")
    md.append("| # | Acao | Prazo |")
    md.append("|---|------|-------|")
    for p in data.get('plano_acao', []):
        md.append(f"| {p.get('ordem','')} | {p.get('acao','')} | {p.get('prazo','')} |")
    md.append("")
    md.append("## Referencias Oficiais")
    md.append("")
    refs = [
        ("Google Search Central - Optimizing for generative AI search",
         "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide"),
        ("Google Search Central - Mobile site and mobile-first indexing",
         "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"),
        ("Google Search Central - Search Essentials",
         "https://developers.google.com/search/docs/essentials"),
        ("web.dev - AI agent site UX",
         "https://web.dev/articles/ai-agent-site-ux"),
        ("UCP - Universal Commerce Protocol",
         "https://ucp.dev/latest/"),
    ]
    for title, url in refs:
        md.append(f"- [{title}]({url})")
    md.append("")
    return "\n".join(md)

def render_text(data):
    lines = []
    lines.append("=" * 78)
    lines.append(f"RELATORIO QA-GEO: {data['metadata']['url']}".center(78))
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"Data: {data['metadata'].get('data', datetime.utcnow().isoformat() + 'Z')}")
    lines.append(f"Versao: {data['metadata'].get('versao_skill', 'qa-geo@1.0.0')}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("RESUMO EXECUTIVO - SCORES")
    lines.append("-" * 78)
    labels = {
        "seo": "SEO", "geo": "GEO",
        "generative_search": "Generative Search Validation",
        "ai_retrieval": "AI Retrieval",
        "anti_hallucination": "Anti-Hallucination",
        "accessibility": "Accessibility",
        "mobile_first_geo": "Mobile-First GEO",
        "overall": "Overall",
    }
    for k, label in labels.items():
        s = data['scores'].get(k, 0)
        lines.append(f"  {label:<35} {s:>4}/100  [{score_status(s)}]")
    lines.append("")
    lines.append(f"Status Final: {data.get('status', score_status(data['scores'].get('overall', 0)))}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("ANTI-PADROES GEO DETECTADOS")
    lines.append("-" * 78)
    detected = [a for a in data['checks'].get('anti_patterns', []) if a.get('detected')]
    if not detected:
        lines.append("  Nenhum anti-padrao GEO critico detectado.")
    else:
        for a in detected:
            lines.append(f"  [{a.get('severity','').upper():8}] {a.get('id','')}")
            if a.get('note'):
                lines.append(f"             {a.get('note','')}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("MOBILE-FIRST FINDINGS")
    lines.append("-" * 78)
    mf = data['checks'].get('mobile_first', {})
    for k, v in mf.items():
        status = "  OK  " if v else " FAIL "
        lines.append(f"  [{status}] {k}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("FINDINGS")
    lines.append("-" * 78)
    for f in data.get('findings', []):
        lines.append(f"  {f.get('id','')} - {f.get('title','')}")
        lines.append(f"    Categoria:   {f.get('category','')}")
        lines.append(f"    Severidade:  {f.get('severity','')}")
        lines.append(f"    Descricao:   {f.get('description','')}")
        lines.append(f"    Recomend.:   {f.get('recommendation','')}")
        if f.get('reference'):
            lines.append(f"    Referencia:  {f.get('reference','')}")
        lines.append("")
    lines.append("-" * 78)
    lines.append("AI RETRIEVAL TEST RESULTS")
    lines.append("-" * 78)
    rt = data.get('ai_retrieval_tests', {})
    for tipo in ['factual', 'comparative', 'intencao', 'fan_out', 'unique_pov', 'multi_modal']:
        testes = rt.get(tipo, [])
        if testes:
            total = len(testes)
            hits = sum(1 for t in testes if t.get('match'))
            lines.append(f"  {tipo:<15} {hits}/{total} corretos")
    lines.append("")
    lines.append("-" * 78)
    lines.append("ANTI-HALLUCINATION TEST RESULTS")
    lines.append("-" * 78)
    ah = data.get('anti_hallucination_tests', {})
    lines.append(f"  Total de perguntas:        {ah.get('total_perguntas', 0)}")
    lines.append(f"  Alucinacoes detectadas:    {ah.get('alucinacoes_detectadas', 0)}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("RECOMENDACOES PRIORITARIAS (TOP 5)")
    lines.append("-" * 78)
    for i, r in enumerate(data.get('recomendacoes_top5', [])[:5], 1):
        lines.append(f"  {i}. {r.get('titulo','')}")
        lines.append(f"     Impacto: {r.get('impacto','')}  |  Esforco: {r.get('esforco','')}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("PLANO DE ACAO")
    lines.append("-" * 78)
    for p in data.get('plano_acao', []):
        lines.append(f"  {p.get('ordem','')}. {p.get('acao','')}  (prazo: {p.get('prazo','')})")
    lines.append("")
    lines.append("-" * 78)
    lines.append("REFERENCIAS OFICIAIS")
    lines.append("-" * 78)
    refs = [
        ("Optimizing for generative AI search",
         "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide"),
        ("Mobile site and mobile-first indexing",
         "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"),
        ("Search Essentials",
         "https://developers.google.com/search/docs/essentials"),
        ("web.dev - AI agent site UX",
         "https://web.dev/articles/ai-agent-site-ux"),
        ("UCP - Universal Commerce Protocol",
         "https://ucp.dev/latest/"),
    ]
    for title, url in refs:
        lines.append(f"  - {title}")
        lines.append(f"    {url}")
    lines.append("")
    lines.append("=" * 78)
    return "\n".join(lines)

def render_html(data):
    title = f"Relatorio QA-GEO - {data['metadata']['url']}"
    scores = data['scores']
    metadata = data['metadata']

    def score_card(k, label):
        s = scores.get(k, 0)
        color = score_color(s)
        return f"""
        <div class="card" role="article" aria-label="Score {label}">
          <div class="card-header">
            <span class="card-label">{html_lib.escape(label)}</span>
            <span class="card-status" style="background:{color}">{score_status(s)}</span>
          </div>
          <div class="card-score" style="color:{color}">{s}<span class="card-score-max">/100</span></div>
          <div class="card-bar" role="progressbar" aria-valuenow="{s}" aria-valuemin="0" aria-valuemax="100" aria-label="Score {html_lib.escape(label)}">
            <div class="card-bar-fill" style="width:{s}%;background:{color}"></div>
          </div>
        </div>"""

    scores_html = "\n".join([
        score_card("seo", "SEO"),
        score_card("geo", "GEO"),
        score_card("generative_search", "Generative Search"),
        score_card("ai_retrieval", "AI Retrieval"),
        score_card("anti_hallucination", "Anti-Hallucination"),
        score_card("accessibility", "Accessibility"),
        score_card("mobile_first_geo", "Mobile-First GEO"),
        score_card("overall", "Overall"),
    ])

    ap = data['checks'].get('anti_patterns', [])
    if ap:
        rows = []
        for a in ap:
            sev = a.get('severity', 'info').lower()
            color = {"critical": "#EF4444", "high": "#F97316", "medium": "#F59E0B", "info": "#6B7280"}.get(sev, "#6B7280")
            status = "Detectado" if a.get('detected') else "OK"
            status_color = "#EF4444" if a.get('detected') else "#10B981"
            rows.append(f"<tr><td><code>{html_lib.escape(a.get('id',''))}</code></td>"
                        f"<td><span class='badge' style='background:{color}'>{sev.upper()}</span></td>"
                        f"<td><span style='color:{status_color};font-weight:600'>{status}</span></td>"
                        f"<td>{html_lib.escape(a.get('note',''))}</td></tr>")
        anti_patterns_html = f"""
        <table>
          <thead><tr><th>ID</th><th>Severidade</th><th>Status</th><th>Nota</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>"""
    else:
        anti_patterns_html = "<p>Nenhum anti-padrao GEO detectado.</p>"

    mf = data['checks'].get('mobile_first', {})
    if mf:
        rows = []
        for k, v in mf.items():
            ok = bool(v)
            color = "#10B981" if ok else "#EF4444"
            status = "OK" if ok else "FAIL"
            rows.append(f"<tr><td>{html_lib.escape(k)}</td><td><span style='color:{color};font-weight:600'>{status}</span></td></tr>")
        mf_html = f"<table><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    else:
        mf_html = "<p>Sem dados de mobile-first.</p>"

    seo = data['checks'].get('seo_tecnico', {})
    if seo:
        rows = []
        for k, v in seo.items():
            if isinstance(v, dict):
                ok = bool(v.get('ok'))
                val = v.get('value', '')
            else:
                ok = bool(v)
                val = ''
            color = "#10B981" if ok else "#EF4444"
            status = "OK" if ok else "FAIL"
            rows.append(f"<tr><td>{html_lib.escape(k)}</td><td><span style='color:{color};font-weight:600'>{status}</span></td><td><code>{html_lib.escape(str(val))}</code></td></tr>")
        seo_html = f"<table><thead><tr><th>Item</th><th>Status</th><th>Valor</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    else:
        seo_html = "<p>Sem dados de SEO tecnico.</p>"

    sd_list = data['checks'].get('structured_data', [])
    if sd_list:
        rows = []
        for sd in sd_list:
            ok = bool(sd.get('present'))
            color = "#10B981" if ok else "#EF4444"
            status = "Sim" if ok else "Nao"
            rows.append(f"<tr><td>{html_lib.escape(sd.get('type',''))}</td><td><span style='color:{color};font-weight:600'>{status}</span></td></tr>")
        sd_html = f"<table><thead><tr><th>Tipo</th><th>Presente</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    else:
        sd_html = "<p>Sem dados de structured data.</p>"

    a = data['checks'].get('accessibility', {})
    a_total = sum(a.values()) if a else 0
    if a:
        rows = []
        for k, v in a.items():
            rows.append(f"<tr><td>{html_lib.escape(k)}</td><td style='text-align:right'>{v}</td></tr>")
        rows.append(f"<tr style='font-weight:700;background:#F3F4F6'><td>Total</td><td style='text-align:right'>{a_total}/100</td></tr>")
        a_html = f"<table><thead><tr><th>Componente</th><th>Pontos</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    else:
        a_html = "<p>Sem dados de accessibility.</p>"

    findings = data.get('findings', [])
    if findings:
        items = []
        for f in findings:
            sev = f.get('severity', 'info').lower()
            color = {"critical": "#EF4444", "high": "#F97316", "medium": "#F59E0B", "low": "#10B981", "info": "#6B7280"}.get(sev, "#6B7280")
            items.append(f"""
            <details class="finding" open>
              <summary>
                <span class="finding-id">{html_lib.escape(f.get('id',''))}</span>
                <span class="finding-title">{html_lib.escape(f.get('title',''))}</span>
                <span class="badge" style="background:{color}">{sev.upper()}</span>
              </summary>
              <div class="finding-body">
                <p><strong>Categoria:</strong> {html_lib.escape(f.get('category',''))}</p>
                <p><strong>Descricao:</strong> {html_lib.escape(f.get('description',''))}</p>
                <p><strong>Recomendacao:</strong> {html_lib.escape(f.get('recommendation',''))}</p>
                {f'<p><strong>Referencia oficial:</strong> <a href="{html_lib.escape(f["reference"])}" target="_blank" rel="noopener">{html_lib.escape(f["reference"])}</a></p>' if f.get('reference') else ''}
              </div>
            </details>""")
        findings_html = "\n".join(items)
    else:
        findings_html = "<p>Nenhum finding critico.</p>"

    rt = data.get('ai_retrieval_tests', {})
    rt_sections = []
    for tipo, label in [('factual','Factuais'),('comparative','Comparativas'),('intencao','Intencao'),
                        ('fan_out','Fan-out'),('unique_pov','Unique POV'),('multi_modal','Multi-modal')]:
        testes = rt.get(tipo, [])
        if not testes:
            continue
        rows = []
        for t in testes:
            match = bool(t.get('match'))
            color = "#10B981" if match else "#EF4444"
            status = "OK" if match else "FAIL"
            rows.append(f"<tr><td>{html_lib.escape(t.get('pergunta',''))}</td>"
                        f"<td>{html_lib.escape(str(t.get('site','')))}</td>"
                        f"<td>{html_lib.escape(str(t.get('ia','')))}</td>"
                        f"<td><span style='color:{color};font-weight:600'>{status}</span></td></tr>")
        total = len(testes)
        hits = sum(1 for t in testes if t.get('match'))
        rt_sections.append(f"""
        <h4>{label} ({hits}/{total} corretos)</h4>
        <table>
          <thead><tr><th>Pergunta</th><th>Site</th><th>IA</th><th>Match</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>""")
    rt_html = "\n".join(rt_sections) if rt_sections else "<p>Sem testes de AI Retrieval.</p>"

    ah = data.get('anti_hallucination_tests', {})
    ah_html = f"""
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-label">Total de perguntas</div><div class="kpi-value">{ah.get('total_perguntas',0)}</div></div>
      <div class="kpi"><div class="kpi-label">Alucinacoes detectadas</div><div class="kpi-value" style="color:#EF4444">{ah.get('alucinacoes_detectadas',0)}</div></div>
    </div>"""

    recs = data.get('recomendacoes_top5', [])[:5]
    if recs:
        items = []
        for i, r in enumerate(recs, 1):
            imp = r.get('impacto', '')
            imp_color = {"Alto": "#EF4444", "Medio": "#F59E0B", "Baixo": "#10B981"}.get(imp, "#6B7280")
            items.append(f"""
            <li>
              <span class="rec-number">{i}</span>
              <div class="rec-body">
                <div class="rec-title">{html_lib.escape(r.get('titulo',''))}</div>
                <div class="rec-meta">
                  <span class="badge" style="background:{imp_color}">Impacto: {html_lib.escape(imp)}</span>
                  <span class="badge" style="background:#6B7280">Esforco: {html_lib.escape(r.get('esforco',''))}</span>
                </div>
                {f'<a href="{html_lib.escape(r["referencia"])}" target="_blank" rel="noopener" class="rec-ref">Referencia oficial</a>' if r.get('referencia') else ''}
              </div>
            </li>""")
        recs_html = f"<ol class='rec-list'>{''.join(items)}</ol>"
    else:
        recs_html = "<p>Sem recomendacoes prioritarias.</p>"

    plan = data.get('plano_acao', [])
    if plan:
        rows = []
        for p in plan:
            rows.append(f"<tr><td>{p.get('ordem','')}</td><td>{html_lib.escape(p.get('acao',''))}</td><td>{html_lib.escape(p.get('prazo',''))}</td></tr>")
        plan_html = f"<table><thead><tr><th>#</th><th>Acao</th><th>Prazo</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    else:
        plan_html = "<p>Sem plano de acao definido.</p>"

    refs = [
        ("Optimizing for generative AI search", "https://developers.google.com/search/docs/fundamentals/ai-optimization-guide"),
        ("Mobile site and mobile-first indexing", "https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing"),
        ("Search Essentials", "https://developers.google.com/search/docs/essentials"),
        ("web.dev - AI agent site UX", "https://web.dev/articles/ai-agent-site-ux"),
        ("UCP - Universal Commerce Protocol", "https://ucp.dev/latest/"),
    ]
    refs_html = "\n".join([f'<li><a href="{u}" target="_blank" rel="noopener">{html_lib.escape(t)}</a></li>' for t, u in refs])

    data_str = html_lib.escape(metadata.get('data', datetime.utcnow().isoformat() + 'Z'))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Relatorio QA-GEO - {html_lib.escape(metadata['url'])} - validacao de SEO, GEO, Mobile-First Indexing, AI Optimization e Accessibility">
<meta property="og:title" content="Relatorio QA-GEO: {html_lib.escape(metadata['url'])}">
<meta property="og:type" content="website">
<title>{html_lib.escape(title)}</title>
<style>
  :root {{ --bg: #F9FAFB; --fg: #111827; --muted: #6B7280; --card: #FFFFFF;
    --border: #E5E7EB; --accent: #3B82F6; --shadow: 0 1px 3px rgba(0,0,0,.1); }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         background:var(--bg); color:var(--fg); line-height:1.5; }}
  header.page {{ background:linear-gradient(135deg,#1E40AF,#7C3AED); color:#fff; padding:32px 24px; }}
  header.page .url {{ font-size:1.4rem; font-weight:700; word-break:break-all; }}
  header.page .meta {{ opacity:.9; margin-top:6px; font-size:.9rem; }}
  main {{ max-width:1200px; margin:0 auto; padding:24px; }}
  section {{ background:var(--card); border:1px solid var(--border); border-radius:12px;
            padding:24px; margin-bottom:24px; box-shadow:var(--shadow); }}
  h2 {{ margin-top:0; padding-bottom:8px; border-bottom:2px solid var(--border); }}
  h4 {{ margin:16px 0 8px; color:var(--muted); }}
  .grid {{ display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); }}
  .card {{ background:#fff; border:1px solid var(--border); border-radius:10px; padding:16px; }}
  .card-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }}
  .card-label {{ font-weight:600; color:var(--muted); font-size:.85rem; }}
  .card-status {{ color:#fff; font-size:.7rem; padding:2px 8px; border-radius:10px; font-weight:600; }}
  .card-score {{ font-size:2.4rem; font-weight:700; line-height:1; }}
  .card-score-max {{ font-size:1rem; color:var(--muted); font-weight:500; }}
  .card-bar {{ height:6px; background:#E5E7EB; border-radius:3px; margin-top:12px; overflow:hidden; }}
  .card-bar-fill {{ height:100%; transition:width .6s ease; }}
  table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
  th, td {{ padding:8px 12px; text-align:left; border-bottom:1px solid var(--border); }}
  th {{ background:#F3F4F6; font-weight:600; }}
  code {{ background:#F3F4F6; padding:2px 6px; border-radius:4px; font-size:.85em; }}
  .badge {{ display:inline-block; color:#fff; padding:2px 8px; border-radius:10px;
           font-size:.7rem; font-weight:600; margin-right:4px; }}
  details.finding {{ border:1px solid var(--border); border-radius:8px; padding:8px 12px; margin-bottom:8px; }}
  details.finding[open] {{ background:#FAFBFC; }}
  details.finding summary {{ cursor:pointer; display:flex; align-items:center; gap:10px; padding:4px 0; }}
  .finding-id {{ font-family:monospace; font-weight:700; color:var(--accent); }}
  .finding-title {{ flex:1; font-weight:500; }}
  .finding-body {{ margin-top:8px; padding-top:8px; border-top:1px dashed var(--border); }}
  .kpi-row {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; }}
  .kpi {{ background:#F3F4F6; padding:16px; border-radius:8px; text-align:center; }}
  .kpi-label {{ color:var(--muted); font-size:.85rem; }}
  .kpi-value {{ font-size:2rem; font-weight:700; color:var(--fg); margin-top:4px; }}
  ol.rec-list {{ list-style:none; padding:0; margin:0; }}
  ol.rec-list li {{ display:flex; gap:12px; padding:12px; border:1px solid var(--border);
                   border-radius:8px; margin-bottom:8px; background:#fff; }}
  .rec-number {{ background:var(--accent); color:#fff; width:32px; height:32px; border-radius:50%;
                display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0; }}
  .rec-body {{ flex:1; }}
  .rec-title {{ font-weight:600; margin-bottom:6px; }}
  .rec-meta {{ display:flex; gap:6px; flex-wrap:wrap; }}
  .rec-ref {{ display:inline-block; margin-top:6px; color:var(--accent); text-decoration:none; font-size:.85rem; }}
  .rec-ref:hover {{ text-decoration:underline; }}
  footer.page {{ text-align:center; padding:24px; color:var(--muted); font-size:.85rem; }}
  @media (max-width:640px) {{
    header.page {{ padding:20px 16px; }} main {{ padding:16px; }} section {{ padding:16px; }}
    .card-score {{ font-size:1.8rem; }} }}
  @media print {{
    body {{ background:#fff; }} section {{ box-shadow:none; border:1px solid #ccc; page-break-inside:avoid; }}
    header.page {{ background:#1E40AF; -webkit-print-color-adjust:exact; print-color-adjust:exact; }} }}
</style>
</head>
<body>
<header class="page" role="banner">
  <div class="url">{html_lib.escape(metadata['url'])}</div>
  <div class="meta">Data: {data_str} | Versao: {html_lib.escape(metadata.get('versao_skill','qa-geo@1.0.0'))} | Status: <strong>{html_lib.escape(data.get('status', score_status(scores.get('overall',0))))}</strong></div>
</header>
<main>
  <section aria-labelledby="scores"><h2 id="scores">Scores</h2><div class="grid">{scores_html}</div></section>
  <section aria-labelledby="anti-patterns"><h2 id="anti-patterns">Anti-Padroes GEO Detectados</h2><p>Baseado nas diretrizes oficiais do Google Search Central.</p>{anti_patterns_html}</section>
  <section aria-labelledby="mobile-first"><h2 id="mobile-first">Mobile-First Findings</h2>{mf_html}</section>
  <section aria-labelledby="seo-tecnico"><h2 id="seo-tecnico">SEO Tecnico</h2>{seo_html}</section>
  <section aria-labelledby="structured-data"><h2 id="structured-data">Structured Data</h2>{sd_html}</section>
  <section aria-labelledby="accessibility"><h2 id="accessibility">Accessibility</h2>{a_html}</section>
  <section aria-labelledby="findings"><h2 id="findings">Findings</h2>{findings_html}</section>
  <section aria-labelledby="ai-retrieval"><h2 id="ai-retrieval">AI Retrieval Test Results</h2>{rt_html}</section>
  <section aria-labelledby="anti-hallucination"><h2 id="anti-hallucination">Anti-Hallucination Test Results</h2>{ah_html}</section>
  <section aria-labelledby="recomendacoes"><h2 id="recomendacoes">Recomendacoes Prioritarias (Top 5)</h2>{recs_html}</section>
  <section aria-labelledby="plano-acao"><h2 id="plano-acao">Plano de Acao</h2>{plan_html}</section>
  <section aria-labelledby="referencias"><h2 id="referencias">Referencias Oficiais</h2><ul>{refs_html}</ul></section>
</main>
<footer class="page"><p>Relatorio gerado pela skill <strong>qa-geo-report</strong> | Alinhado com Google Search Central</p></footer>
</body>
</html>"""

def main():
    ap = argparse.ArgumentParser(description="Gera relatorio QA-GEO em MD, TXT e HTML")
    ap.add_argument("--json", required=True, help="Caminho do JSON canonico")
    ap.add_argument("--output-dir", required=True, help="Diretorio de saida")
    ap.add_argument("--serve", action="store_true", help="Servir HTML em localhost apos gerar")
    ap.add_argument("--port", type=int, default=8080, help="Porta do servidor local")
    args = ap.parse_args()
    data = safe_load_json(Path(args.json))
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "relatorio.md"
    txt_path = out_dir / "relatorio.txt"
    html_path = out_dir / "relatorio.html"
    md_path.write_text(render_markdown(data), encoding="utf-8")
    txt_path.write_text(render_text(data), encoding="utf-8")
    html_path.write_text(render_html(data), encoding="utf-8")
    print(f"[OK] Markdown:  {md_path}")
    print(f"[OK] Texto:     {txt_path}")
    print(f"[OK] HTML:      {html_path}")
    if args.serve:
        import subprocess
        serve_script = SCRIPT_DIR / "serve_report.py"
        print(f"\n[INFO] Iniciando servidor local na porta {args.port}...")
        print(f"[INFO] Abra http://localhost:{args.port}/relatorio.html no navegador")
        print(f"[INFO] Pressione Ctrl+C para parar\n")
        try:
            subprocess.run([sys.executable, str(serve_script),
                          "--directory", str(out_dir), "--port", str(args.port)], check=True)
        except KeyboardInterrupt:
            print("\n[INFO] Servidor parado.")

if __name__ == "__main__":
    main()
