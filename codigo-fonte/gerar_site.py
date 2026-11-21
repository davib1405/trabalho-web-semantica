#!/usr/bin/env python3
"""
Gerador Dinâmico do Portal de Perfis Acadêmicos, Consultas Interativas e Grafo LOD
Trabalho de Web Semântica e Linked Open Data - UFRRJ
Autor: David Barros da Rosa Filho
"""

import os
import json
import shutil
import rdflib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_TTL_PATH = os.path.join(BASE_DIR, "ontologia", "dados.ttl")
ONTOLOGIA_OWL_PATH = os.path.join(BASE_DIR, "ontologia", "ontologia.owl")
CONSULTAS_DIR = os.path.join(BASE_DIR, "consultas")
SITE_DIR = os.path.join(BASE_DIR, "site")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PERFIS_DIR = os.path.join(SITE_DIR, "perfis")

os.makedirs(PERFIS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

NAVBAR_HTML = """
  <nav style="background: #1e293b; padding: 0.75rem 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <div style="font-weight: bold; color: #f8fafc; font-size: 1.05rem;">
      <a href="index.html" style="color: #38bdf8; text-decoration: none;">UFRRJ &bull; Web Semântica &amp; LOD</a>
    </div>
    <div style="display: flex; gap: 1.25rem; font-size: 0.95rem; align-items: center;">
      <a href="index.html" style="color: #e2e8f0; text-decoration: none; font-weight: 500;">Início</a>
      <a href="consultas.html" style="color: #e2e8f0; text-decoration: none; font-weight: 500;">Consultas SPARQL</a>
      <a href="grafo.html" style="color: #e2e8f0; text-decoration: none; font-weight: 500;">Grafo Visual</a>
      <a href="../ontologia/dados.ttl" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 600; background: rgba(56,189,248,0.15); padding: 4px 10px; border-radius: 4px;">RDF Turtle (.ttl)</a>
      <a href="../ontologia/ontologia.owl" target="_blank" style="color: #a78bfa; text-decoration: none; font-weight: 600; background: rgba(167,139,250,0.15); padding: 4px 10px; border-radius: 4px;">Ontologia OWL</a>
    </div>
  </nav>
"""

NAVBAR_SUBDIR_HTML = """
  <nav style="background: #1e293b; padding: 0.75rem 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <div style="font-weight: bold; color: #f8fafc; font-size: 1.05rem;">
      <a href="../index.html" style="color: #38bdf8; text-decoration: none;">UFRRJ &bull; Web Semântica &amp; LOD</a>
    </div>
    <div style="display: flex; gap: 1.25rem; font-size: 0.95rem; align-items: center;">
      <a href="../index.html" style="color: #e2e8f0; text-decoration: none; font-weight: 500;">Início</a>
      <a href="../consultas.html" style="color: #e2e8f0; text-decoration: none; font-weight: 500;">Consultas SPARQL</a>
      <a href="../grafo.html" style="color: #e2e8f0; text-decoration: none; font-weight: 500;">Grafo Visual</a>
      <a href="../../ontologia/dados.ttl" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 600; background: rgba(56,189,248,0.15); padding: 4px 10px; border-radius: 4px;">RDF Turtle (.ttl)</a>
      <a href="../../ontologia/ontologia.owl" target="_blank" style="color: #a78bfa; text-decoration: none; font-weight: 600; background: rgba(167,139,250,0.15); padding: 4px 10px; border-radius: 4px;">Ontologia OWL</a>
    </div>
  </nav>
"""

def carregar_dados():
    g = rdflib.Graph()
    g.parse(ONTOLOGIA_OWL_PATH, format="turtle")
    g.parse(DADOS_TTL_PATH, format="turtle")
    return g

def extrair_perfis(g):
    query_docentes = """
    PREFIX : <http://dados.ufrrj.br/ontologia/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?uri ?nome ?cargo ?titulacao ?email ?bio ?deptoNome ?instNome ?lattes ?orcid ?pagina
    WHERE {
        ?uri a :Docente ;
             :nomeCompleto ?nome ;
             :cargoOuFuncao ?cargo ;
             :titulacao ?titulacao ;
             :emailInstitucional ?email ;
             :biografiaResumida ?bio ;
             :lotadoEm ?depto ;
             :pertenceA ?inst .
        ?depto rdfs:label ?deptoNome .
        ?inst a :Instituto ; rdfs:label ?instNome .
        OPTIONAL { ?uri :linkLattes ?lattes }
        OPTIONAL { ?uri :linkOrcid ?orcid }
        OPTIONAL { ?uri :linkPaginaPessoal ?pagina }
    }
    """

    query_discentes = """
    PREFIX : <http://dados.ufrrj.br/ontologia/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?uri ?nome ?cargo ?anoIngresso ?periodo ?email ?bio ?cursoNome ?instNome ?lattes ?orcid ?pagina
    WHERE {
        ?uri a :Discente ;
             :nomeCompleto ?nome ;
             :cargoOuFuncao ?cargo ;
             :anoIngresso ?anoIngresso ;
             :periodoAtual ?periodo ;
             :emailInstitucional ?email ;
             :biografiaResumida ?bio ;
             :matriculadoEm ?curso ;
             :pertenceA ?inst .
        ?curso rdfs:label ?cursoNome .
        ?inst a :Instituto ; rdfs:label ?instNome .
        OPTIONAL { ?uri :linkLattes ?lattes }
        OPTIONAL { ?uri :linkOrcid ?orcid }
        OPTIONAL { ?uri :linkPaginaPessoal ?pagina }
    }
    """

    docentes = []
    for row in g.query(query_docentes):
        uri = row.uri
        doc_id = str(uri).split("/")[-1]
        
        areas = [str(r.label) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?label WHERE {{
                <{uri}> :atuaEmArea ?area .
                ?area skos:prefLabel ?label .
                FILTER (LANG(?label) = 'pt')
            }}
        """)]

        disciplinas = [str(r.label) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label WHERE {{
                <{uri}> :leciona ?d .
                ?d rdfs:label ?label .
            }}
        """)]

        projetos = [{"titulo": str(r.tit), "papel": str(r.papel)} for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?tit ?papel WHERE {{
                {{ <{uri}> :coordenaProjeto ?p . BIND("Coordenador(a)" AS ?papel) }}
                UNION
                {{ <{uri}> :participaDeProjeto ?p . FILTER NOT EXISTS {{ <{uri}> :coordenaProjeto ?p }} BIND("Pesquisador(a)" AS ?papel) }}
                ?p rdfs:label ?tit .
            }}
        """)]

        grupos = [str(r.tit) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?tit WHERE {{
                <{uri}> :membroDeGrupo ?grp .
                ?grp rdfs:label ?tit .
            }}
        """)]

        publicacoes = [{"titulo": str(r.tit), "ano": str(r.ano)} for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            SELECT ?tit ?ano WHERE {{
                ?pub a :Publicacao ;
                     :temAutor <{uri}> ;
                     dcterms:title ?tit ;
                     :anoPublicacao ?ano .
            }} ORDER BY DESC(?ano)
        """)]

        docentes.append({
            "tipo": "docente",
            "id": doc_id,
            "uri": str(uri),
            "nome": str(row.nome),
            "cargo": str(row.cargo),
            "titulacao": str(row.titulacao),
            "email": str(row.email),
            "bio": str(row.bio),
            "departamento": str(row.deptoNome),
            "instituto": str(row.instNome),
            "lattes": str(row.lattes) if row.lattes else None,
            "orcid": str(row.orcid) if row.orcid else None,
            "pagina": str(row.pagina) if row.pagina else None,
            "areas": areas,
            "disciplinas": disciplinas,
            "projetos": projetos,
            "grupos": grupos,
            "publicacoes": publicacoes
        })

    discentes = []
    for row in g.query(query_discentes):
        uri = row.uri
        disc_id = str(uri).split("/")[-1]

        areas = [str(r.label) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?label WHERE {{
                <{uri}> :atuaEmArea ?area .
                ?area skos:prefLabel ?label .
                FILTER (LANG(?label) = 'pt')
            }}
        """)]

        projetos = [{"titulo": str(r.tit), "papel": "Bolsista / Integrante"} for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?tit WHERE {{
                <{uri}> :participaDeProjeto ?p .
                ?p rdfs:label ?tit .
            }}
        """)]

        publicacoes = [{"titulo": str(r.tit), "ano": str(r.ano)} for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            SELECT ?tit ?ano WHERE {{
                ?pub a :Publicacao ;
                     :temAutor <{uri}> ;
                     dcterms:title ?tit ;
                     :anoPublicacao ?ano .
            }} ORDER BY DESC(?ano)
        """)]

        discentes.append({
            "tipo": "discente",
            "id": disc_id,
            "uri": str(uri),
            "nome": str(row.nome),
            "cargo": str(row.cargo),
            "anoIngresso": str(row.anoIngresso),
            "periodo": str(row.periodo),
            "email": str(row.email),
            "bio": str(row.bio),
            "curso": str(row.cursoNome),
            "instituto": str(row.instNome),
            "lattes": str(row.lattes) if row.lattes else None,
            "orcid": str(row.orcid) if row.orcid else None,
            "pagina": str(row.pagina) if row.pagina else None,
            "areas": areas,
            "projetos": projetos,
            "publicacoes": publicacoes
        })

    return docentes, discentes

def render_docente(p):
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": p["uri"],
        "name": p["nome"],
        "jobTitle": p["cargo"],
        "email": p["email"],
        "description": p["bio"],
        "affiliation": {
            "@type": "CollegeOrUniversity",
            "name": "Universidade Federal Rural do Rio de Janeiro",
            "subOrganization": {
                "@type": "Department",
                "name": p["departamento"]
            }
        },
        "knowsAbout": p["areas"],
        "sameAs": [l for l in [p["orcid"], p["lattes"], p["pagina"]] if l]
    }

    areas_li = "".join(f"<li>{a}</li>" for a in p["areas"])
    disc_li = "".join(f"<li>{d}</li>" for d in p["disciplinas"])
    proj_li = "".join(f"<li><strong>{proj['titulo']}</strong> — {proj['papel']}.</li>" for proj in p["projetos"])
    grp_li = "".join(f"<li><strong>{g}</strong> — membro pesquisador.</li>" for g in p["grupos"])
    pub_li = "".join(f"<li>{pub['titulo']} ({pub['ano']}).</li>" for pub in p["publicacoes"])

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Perfil acadêmico de {p['nome']} — UFRRJ. Dados vinculados à Web Semântica.">
  <title>{p['nome']} | Perfil Docente UFRRJ</title>
  <link rel="stylesheet" href="../estilos.css">
  <link rel="alternate" type="text/turtle" href="../../ontologia/dados.ttl" title="Grafo RDF em Turtle">
  <script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  {NAVBAR_SUBDIR_HTML}
  <header class="site-header">
    <div class="header-inner">
      <a href="../index.html" class="site-title">Universidade Federal Rural do Rio de Janeiro</a>
      <p class="site-subtitle">Diretório de Perfis Acadêmicos Conectados (Linked Data)</p>
    </div>
  </header>

  <main>
    <section class="profile-heading" aria-labelledby="nome">
      <img class="profile-photo" src="foto-exemplo.svg" alt="Avatar ilustrativo de {p['nome']}">
      <div>
        <p class="eyebrow">Perfil de Docente &bull; URI: <code>{p['uri']}</code></p>
        <h1 id="nome">{p['nome']}</h1>
        <p class="role">{p['cargo']} &bull; {p['titulacao']}</p>
        <p class="quick-info">{p['departamento']} &middot; {p['instituto']}</p>
      </div>
    </section>

    <div class="layout">
      <div>
        <section class="card">
          <h2>Apresentação</h2>
          <p>{p['bio']}</p>
        </section>

        <section class="card">
          <h2>Formação Acadêmica</h2>
          <ul class="clean-list">
            <li><strong>{p['titulacao']}</strong> — Universidade Federal Rural do Rio de Janeiro.</li>
          </ul>
        </section>

        <section class="card">
          <h2>Áreas de Atuação e Interesses</h2>
          <ul class="tag-list">
            {areas_li}
          </ul>
        </section>

        <section class="card">
          <h2>Disciplinas Ministradas</h2>
          <ul class="clean-list">
            {disc_li}
          </ul>
        </section>

        <section class="card">
          <h2>Projetos e Grupos de Pesquisa</h2>
          <ul class="clean-list">
            {proj_li}
            {grp_li}
          </ul>
        </section>

        <section class="card">
          <h2>Publicações Selecionadas</h2>
          <ol class="clean-list">
            {pub_li}
          </ol>
        </section>
      </div>

      <aside>
        <section class="card">
          <h2>Vínculo Institucional</h2>
          <dl class="contact-list">
            <div><dt>Instituição</dt><dd>UFRRJ</dd></div>
            <div><dt>Unidade</dt><dd>{p['instituto']}</dd></div>
            <div><dt>Departamento</dt><dd>{p['departamento']}</dd></div>
            <div><dt>E-mail</dt><dd><a href="mailto:{p['email']}">{p['email']}</a></dd></div>
          </dl>
        </section>

        <section class="card">
          <h2>Página Pessoal</h2>
          <p><a href="{p['pagina'] or '#'}" target="_blank" rel="noopener noreferrer">Acesse a página pessoal do docente</a></p>
        </section>

        <section class="card">
          <h2>Redes e Perfis Acadêmicos</h2>
          <ul class="social-links">
            <li><a href="{p['orcid'] or '#'}" rel="me" target="_blank">ORCID</a></li>
            <li><a href="{p['lattes'] or '#'}" rel="me" target="_blank">Currículo Lattes</a></li>
          </ul>
        </section>

        <section class="card" style="background: #f8fafc; border: 1px dashed #cbd5e1;">
          <h2>Metadados Semânticos</h2>
          <p style="font-size: 0.85rem; color: #475569;">Esta página contém marcação estruturada em <strong>JSON-LD</strong> e mapeamento RDF Turtle na ontologia institucional.</p>
          <p style="margin-top: 8px;"><a href="../../ontologia/dados.ttl" style="font-weight: 600; color: #0284c7;">Ver Dados em RDF Turtle (.ttl) &rarr;</a></p>
        </section>
      </aside>
    </div>
  </main>

  <footer class="site-footer">
    <p>Perfil acadêmico integrado ao ecossistema de Linked Open Data da UFRRJ. Licença <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0</a>.</p>
    <p><a href="../index.html">&larr; Voltar ao Diretório Principal</a></p>
  </footer>
</body>
</html>
"""

def render_discente(p):
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": p["uri"],
        "name": p["nome"],
        "jobTitle": p["cargo"],
        "email": p["email"],
        "description": p["bio"],
        "alumniOf": {
            "@type": "CollegeOrUniversity",
            "name": "Universidade Federal Rural do Rio de Janeiro"
        },
        "knowsAbout": p["areas"],
        "sameAs": [l for l in [p["orcid"], p["lattes"], p["pagina"]] if l]
    }

    areas_li = "".join(f"<li>{a}</li>" for a in p["areas"])
    proj_li = "".join(f"<li><strong>{proj['titulo']}</strong> — {proj['papel']}.</li>" for proj in p["projetos"])
    pub_li = "".join(f"<li>{pub['titulo']} ({pub['ano']}).</li>" for pub in p["publicacoes"])

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Perfil acadêmico de {p['nome']} — UFRRJ. Dados vinculados à Web Semântica.">
  <title>{p['nome']} | Perfil Discente UFRRJ</title>
  <link rel="stylesheet" href="../estilos.css">
  <link rel="alternate" type="text/turtle" href="../../ontologia/dados.ttl" title="Grafo RDF em Turtle">
  <script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  {NAVBAR_SUBDIR_HTML}
  <header class="site-header">
    <div class="header-inner">
      <a href="../index.html" class="site-title">Universidade Federal Rural do Rio de Janeiro</a>
      <p class="site-subtitle">Diretório de Perfis Acadêmicos Conectados (Linked Data)</p>
    </div>
  </header>

  <main>
    <section class="profile-heading" aria-labelledby="nome">
      <img class="profile-photo" src="foto-exemplo.svg" alt="Avatar ilustrativo de {p['nome']}">
      <div>
        <p class="eyebrow">Perfil de Discente &bull; URI: <code>{p['uri']}</code></p>
        <h1 id="nome">{p['nome']}</h1>
        <p class="role">{p['cargo']} &bull; {p['curso']}</p>
        <p class="quick-info">{p['instituto']} &middot; Ingresso: {p['anoIngresso']} &middot; {p['periodo']}</p>
      </div>
    </section>

    <div class="layout">
      <div>
        <section class="card">
          <h2>Apresentação</h2>
          <p>{p['bio']}</p>
        </section>

        <section class="card">
          <h2>Formação Acadêmica</h2>
          <ul class="clean-list">
            <li><strong>{p['curso']}</strong> — Universidade Federal Rural do Rio de Janeiro.</li>
            <li>Ingresso: {p['anoIngresso']} &middot; Período atual: {p['periodo']}.</li>
          </ul>
        </section>

        <section class="card">
          <h2>Áreas de Interesse</h2>
          <ul class="tag-list">
            {areas_li}
          </ul>
        </section>

        <section class="card">
          <h2>Projetos e Atividades Acadêmicas</h2>
          <ul class="clean-list">
            {proj_li}
          </ul>
        </section>

        <section class="card">
          <h2>Produções e Trabalhos</h2>
          <ol class="clean-list">
            {pub_li}
          </ol>
        </section>
      </div>

      <aside>
        <section class="card">
          <h2>Vínculo Institucional</h2>
          <dl class="contact-list">
            <div><dt>Instituição</dt><dd>UFRRJ</dd></div>
            <div><dt>Unidade</dt><dd>{p['instituto']}</dd></div>
            <div><dt>Curso</dt><dd>{p['curso']}</dd></div>
            <div><dt>E-mail</dt><dd><a href="mailto:{p['email']}">{p['email']}</a></dd></div>
          </dl>
        </section>

        <section class="card">
          <h2>Página Pessoal</h2>
          <p><a href="{p['pagina'] or '#'}" target="_blank" rel="noopener noreferrer">Acesse a página do estudante</a></p>
        </section>

        <section class="card">
          <h2>Redes e Perfis Acadêmicos</h2>
          <ul class="social-links">
            <li><a href="{p['orcid'] or '#'}" rel="me" target="_blank">ORCID</a></li>
            <li><a href="{p['lattes'] or '#'}" rel="me" target="_blank">Currículo Lattes</a></li>
          </ul>
        </section>

        <section class="card" style="background: #f8fafc; border: 1px dashed #cbd5e1;">
          <h2>Metadados Semânticos</h2>
          <p style="font-size: 0.85rem; color: #475569;">Esta página contém marcação estruturada em <strong>JSON-LD</strong> e mapeamento RDF Turtle na ontologia institucional.</p>
          <p style="margin-top: 8px;"><a href="../../ontologia/dados.ttl" style="font-weight: 600; color: #0284c7;">Ver Dados em RDF Turtle (.ttl) &rarr;</a></p>
        </section>
      </aside>
    </div>
  </main>

  <footer class="site-footer">
    <p>Perfil acadêmico integrado ao ecossistema de Linked Open Data da UFRRJ. Licença <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0</a>.</p>
    <p><a href="../index.html">&larr; Voltar ao Diretório Principal</a></p>
  </footer>
</body>
</html>
"""

def render_index(docentes, discentes):
    doc_cards = "".join([f"""
      <article class="card profile-item" style="margin-bottom: 1.5rem;">
        <div style="display: flex; gap: 1rem; align-items: center;">
          <img src="foto-exemplo.svg" width="60" height="60" alt="Avatar" style="border-radius: 50%;">
          <div>
            <h3 style="margin: 0; font-size: 1.2rem;"><a href="perfis/{d['id']}.html" style="color: #1e3c72; text-decoration: none;">{d['nome']}</a></h3>
            <p style="margin: 2px 0; color: #64748b; font-size: 0.9rem;">{d['cargo']} &bull; {d['departamento']}</p>
            <p style="margin: 4px 0; font-size: 0.85rem;"><strong>Áreas:</strong> {", ".join(d['areas'])}</p>
          </div>
        </div>
        <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 8px;">
          <span style="font-size: 0.8rem; color: #94a3b8;">URI: <code>{d['uri']}</code></span>
          <a href="perfis/{d['id']}.html" style="font-weight: 600; color: #0284c7; text-decoration: none;">Ver Perfil Completo &rarr;</a>
        </div>
      </article>
    """ for d in docentes])

    disc_cards = "".join([f"""
      <article class="card profile-item" style="margin-bottom: 1.5rem;">
        <div style="display: flex; gap: 1rem; align-items: center;">
          <img src="foto-exemplo.svg" width="60" height="60" alt="Avatar" style="border-radius: 50%;">
          <div>
            <h3 style="margin: 0; font-size: 1.2rem;"><a href="perfis/{d['id']}.html" style="color: #1e3c72; text-decoration: none;">{d['nome']}</a></h3>
            <p style="margin: 2px 0; color: #64748b; font-size: 0.9rem;">{d['cargo']} &bull; {d['curso']}</p>
            <p style="margin: 4px 0; font-size: 0.85rem;"><strong>Áreas:</strong> {", ".join(d['areas'])}</p>
          </div>
        </div>
        <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 8px;">
          <span style="font-size: 0.8rem; color: #94a3b8;">URI: <code>{d['uri']}</code></span>
          <a href="perfis/{d['id']}.html" style="font-weight: 600; color: #0284c7; text-decoration: none;">Ver Perfil Completo &rarr;</a>
        </div>
      </article>
    """ for d in discentes])

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Diretório de Perfis Acadêmicos da UFRRJ integrados à Web Semântica e Linked Open Data.">
  <title>Portal de Perfis Acadêmicos | UFRRJ - Web Semântica</title>
  <link rel="stylesheet" href="estilos.css">
  <link rel="alternate" type="text/turtle" href="../ontologia/dados.ttl" title="Grafo RDF em Turtle">
</head>
<body>
  {NAVBAR_HTML}
  <header class="site-header">
    <div class="header-inner">
      <h1 class="site-title">Universidade Federal Rural do Rio de Janeiro</h1>
      <p class="site-subtitle">Diretório de Perfis Acadêmicos &bull; Web Semântica e Linked Open Data (LOD)</p>
    </div>
  </header>

  <main style="max-width: 1000px; margin: 2rem auto; padding: 0 1rem;">
    <section class="card" style="margin-bottom: 2rem; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white;">
      <h2 style="color: white; margin-top: 0;">Ecossistema de Dados Abertos e Interligados</h2>
      <p style="font-size: 1.05rem; line-height: 1.6; opacity: 0.95;">
        Este portal disponibiliza os perfis de docentes e discentes da UFRRJ estruturados semanticamente.
        Todas as informações apresentadas foram geradas a partir do <strong>grafo RDF/Turtle</strong> da ontologia institucional, permitindo consultas semânticas em <strong>SPARQL</strong> e interoperabilidade com fontes de dados globais (Wikidata, DBpedia e ORCID).
      </p>
      <div style="margin-top: 1.5rem; display: flex; gap: 1rem; flex-wrap: wrap;">
        <a href="consultas.html" style="background: #38bdf8; color: #0f172a; padding: 10px 18px; border-radius: 6px; font-weight: bold; text-decoration: none;">🔍 Ver Consultas SPARQL Interativas</a>
        <a href="grafo.html" style="background: rgba(255,255,255,0.2); color: white; padding: 10px 18px; border-radius: 6px; font-weight: bold; text-decoration: none; border: 1px solid white;">🕸️ Explorar Grafo Visual</a>
        <a href="../ontologia/dados.ttl" style="background: white; color: #1e3c72; padding: 10px 18px; border-radius: 6px; font-weight: bold; text-decoration: none;">💾 Baixar RDF Turtle (.ttl)</a>
      </div>
    </section>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
      <section>
        <h2 style="border-bottom: 2px solid #1e3c72; padding-bottom: 8px; color: #1e3c72;">Perfis de Docentes ({len(docentes)})</h2>
        {doc_cards}
      </section>

      <section>
        <h2 style="border-bottom: 2px solid #1e3c72; padding-bottom: 8px; color: #1e3c72;">Perfis de Discentes ({len(discentes)})</h2>
        {disc_cards}
      </section>
    </div>

    <section class="card" style="margin-top: 2rem;">
      <h2>Recursos e Evidências do Projeto</h2>
      <ul class="clean-list">
        <li><strong>Repositório Estruturado:</strong> Em conformidade estrita com o documento do trabalho acadêmico (UFRRJ).</li>
        <li><strong>Conexões LOD Externas:</strong> UFRRJ (<a href="https://www.wikidata.org/wiki/Q3550293" target="_blank">Wikidata Q3550293</a>, <a href="http://dbpedia.org/resource/Federal_Rural_University_of_Rio_de_Janeiro" target="_blank">DBpedia</a>), Seropédica (<a href="https://www.wikidata.org/wiki/Q1002058" target="_blank">Wikidata Q1002058</a>), Áreas de Pesquisa SKOS (<a href="https://www.wikidata.org/wiki/Q54837" target="_blank">Web Semântica</a>, <a href="https://www.wikidata.org/wiki/Q11660" target="_blank">IA</a>, <a href="https://www.wikidata.org/wiki/Q309903" target="_blank">Dados Abertos</a>) e <a href="https://orcid.org/" target="_blank">ORCIDs</a>.</li>
        <li><strong>Perguntas de Competência:</strong> Todas as 6 consultas SPARQL implementadas e validadas com 100% de sucesso.</li>
        <li><strong>Licença de Dados:</strong> <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">Creative Commons Attribution 4.0 International (CC-BY 4.0)</a>.</li>
      </ul>
    </section>
  </main>

  <footer class="site-footer">
    <p>Trabalho de Web Semântica e Linked Open Data &bull; UFRRJ / ICE / Departamento de Computação</p>
    <p>Autor: David Barros da Rosa Filho &bull; 2026</p>
  </footer>
</body>
</html>
"""

def render_consultas_html(g):
    perguntas = {
        1: ("Docentes e Departamentos", "Quais são os docentes cadastrados e seus respectivos departamentos ou unidades acadêmicas?"),
        2: ("Discentes por Curso", "Quais discentes pertencem a determinado curso?"),
        3: ("Docentes por Área de Pesquisa", "Quais docentes atuam em determinada área de pesquisa?"),
        4: ("Docentes e Discentes no Mesmo Projeto", "Quais docentes e discentes participam de um mesmo projeto de pesquisa?"),
        5: ("Publicações e Coautores", "Quais publicações estão associadas a determinado docente e quem são seus coautores?"),
        6: ("Pessoas por Unidade Acadêmica", "Quais pessoas estão vinculadas a uma unidade acadêmica específica (ICE)?")
    }

    consultas_dados = []
    for i in range(1, 7):
        arq_rq = os.path.join(CONSULTAS_DIR, f"consulta0{i}.rq")
        with open(arq_rq, "r", encoding="utf-8") as f:
            query_str = f.read()

        res = g.query(query_str)
        vars_names = [str(v) for v in res.vars]
        rows = []
        for r in res:
            rows.append([str(r[v]) if r[v] is not None else "" for v in res.vars])

        consultas_dados.append({
            "num": i,
            "titulo": perguntas[i][0],
            "pergunta": perguntas[i][1],
            "sparql": query_str.strip(),
            "vars": vars_names,
            "rows": rows
        })

    json_consultas = json.dumps(consultas_dados, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Consultas SPARQL Interativas | UFRRJ - Web Semântica</title>
  <link rel="stylesheet" href="estilos.css">
  <style>
    .tab-btn {{
      padding: 10px 16px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      color: #334155;
      transition: all 0.2s;
    }}
    .tab-btn.active {{
      background: #1e3c72;
      color: white;
      border-color: #1e3c72;
    }}
    pre.code-box {{
      background: #0f172a;
      color: #38bdf8;
      padding: 1.25rem;
      border-radius: 8px;
      overflow-x: auto;
      font-family: 'Consolas', monospace;
      font-size: 0.9rem;
      line-height: 1.5;
    }}
    table.result-tbl {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
      background: white;
    }}
    table.result-tbl th, table.result-tbl td {{
      border: 1px solid #e2e8f0;
      padding: 10px 12px;
      text-align: left;
      font-size: 0.9rem;
    }}
    table.result-tbl th {{
      background: #f8fafc;
      color: #1e293b;
      font-weight: 600;
    }}
    table.result-tbl tr:hover {{
      background: #f1f5f9;
    }}
  </style>
</head>
<body>
  {NAVBAR_HTML}
  <header class="site-header">
    <div class="header-inner">
      <h1 class="site-title">Consultas SPARQL 1.1 &bull; Evidências de Competência</h1>
      <p class="site-subtitle">Execução interativa contra o Grafo de Conhecimento RDF da UFRRJ</p>
    </div>
  </header>

  <main style="max-width: 1050px; margin: 2rem auto; padding: 0 1rem;">
    <section class="card" style="margin-bottom: 1.5rem;">
      <h2 style="margin-top: 0;">Selecione a Consulta SPARQL para Visualizar:</h2>
      <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem;">
        <button class="tab-btn active" onclick="mostrarConsulta(1)">Consulta 01: Docentes & Deptos</button>
        <button class="tab-btn" onclick="mostrarConsulta(2)">Consulta 02: Discentes por Curso</button>
        <button class="tab-btn" onclick="mostrarConsulta(3)">Consulta 03: Áreas de Pesquisa</button>
        <button class="tab-btn" onclick="mostrarConsulta(4)">Consulta 04: Projetos Compartilhados</button>
        <button class="tab-btn" onclick="mostrarConsulta(5)">Consulta 05: Publicações & Coautores</button>
        <button class="tab-btn" onclick="mostrarConsulta(6)">Consulta 06: Pessoas no ICE</button>
      </div>
    </section>

    <section class="card" id="painel-consulta">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
        <h2 id="q-titulo" style="color: #1e3c72; margin-top: 0;"></h2>
        <span id="q-badge" style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem;"></span>
      </div>
      <p id="q-pergunta" style="font-size: 1.1rem; color: #334155; font-weight: 500;"></p>

      <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem;">Código SPARQL da Consulta</h3>
      <pre class="code-box" id="q-sparql"></pre>

      <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem;">Resultado Retornado pelo Grafo RDF</h3>
      <div id="q-tabela-container" style="overflow-x: auto;"></div>
    </section>
  </main>

  <footer class="site-footer">
    <p>Consultas SPARQL validadas via RDFLib 7.6.0 &bull; UFRRJ Linked Open Data</p>
  </footer>

  <script>
    const consultas = {json_consultas};

    function mostrarConsulta(num) {{
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {{
        if (idx === num - 1) btn.classList.add('active');
        else btn.classList.remove('active');
      }});

      const c = consultas.find(item => item.num === num);
      if (!c) return;

      document.getElementById('q-titulo').innerText = 'Consulta 0' + c.num + ': ' + c.titulo;
      document.getElementById('q-pergunta').innerText = '"' + c.pergunta + '"';
      document.getElementById('q-badge').innerText = c.rows.length + ' registros retornados';
      document.getElementById('q-sparql').innerText = c.sparql;

      let html = '<table class="result-tbl"><thead><tr>';
      c.vars.forEach(v => {{
        html += '<th>' + v + '</th>';
      }});
      html += '</tr></thead><tbody>';

      c.rows.forEach(r => {{
        html += '<tr>';
        r.forEach(cel => {{
          if (cel.startsWith('http://dados.ufrrj.br/recurso/')) {{
            const id = cel.split('/').pop();
            html += '<td><code>ufrrj:' + id + '</code></td>';
          }} else if (cel.startsWith('http')) {{
            html += '<td><a href="' + cel + '" target="_blank">' + cel + '</a></td>';
          }} else {{
            html += '<td>' + cel + '</td>';
          }}
        }});
        html += '</tr>';
      }});
      html += '</tbody></table>';

      document.getElementById('q-tabela-container').innerHTML = html;
    }}

    // Inicia com a primeira consulta
    mostrarConsulta(1);
  </script>
</body>
</html>
"""

def render_grafo_html():
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Grafo de Conhecimento Interativo | UFRRJ - Web Semântica</title>
  <link rel="stylesheet" href="estilos.css">
  <style>
    #canvas-grafo {{
      width: 100%;
      height: 600px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      background: #f8fafc;
      display: block;
      cursor: grab;
    }}
    .legend-tag {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  {NAVBAR_HTML}
  <header class="site-header">
    <div class="header-inner">
      <h1 class="site-title">Grafo de Conhecimento Interativo (LOD Network)</h1>
      <p class="site-subtitle">Visualização topológica das entidades acadêmicas e conexões da Web Semântica</p>
    </div>
  </header>

  <main style="max-width: 1100px; margin: 2rem auto; padding: 0 1rem;">
    <section class="card" style="margin-bottom: 1.5rem;">
      <h2 style="margin-top: 0;">Explore os Vínculos Semânticos</h2>
      <p style="color: #64748b;">
        Este mapa renderiza o grafo RDF integrado da UFRRJ. Você pode <strong>arrastar os nós</strong> com o mouse para reposicioná-los e inspecionar a malha de relacionamentos entre professores, discentes, unidades acadêmicas, projetos e recursos de Linked Open Data externos.
      </p>
      <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1rem;">
        <span class="legend-tag" style="background: #e0f2fe; color: #0369a1;">● Docentes (Ana Silva, Mariana Almeida)</span>
        <span class="legend-tag" style="background: #f0fdf4; color: #15803d;">● Discentes (João Pereira, Lucas Ferreira)</span>
        <span class="legend-tag" style="background: #fef3c7; color: #b45309;">● Unidades e Cursos (ICE, DCC, BSI)</span>
        <span class="legend-tag" style="background: #f3e8ff; color: #7e22ce;">● Projetos de Pesquisa</span>
        <span class="legend-tag" style="background: #ffe4e6; color: #be123c;">● LOD Externo (Wikidata, DBpedia, ORCID)</span>
      </div>
    </section>

    <div class="card" style="padding: 10px;">
      <canvas id="canvas-grafo" width="1050" height="600"></canvas>
    </div>
  </main>

  <footer class="site-footer">
    <p>Grafo gerado a partir de <code>ontologia/dados.ttl</code> e <code>ontologia/ontologia.owl</code> &bull; UFRRJ</p>
  </footer>

  <script>
    const canvas = document.getElementById('canvas-grafo');
    const ctx = canvas.getContext('2d');

    const nodes = [
      {{ id: 'ufrrj', label: 'UFRRJ', type: 'unidade', x: 525, y: 70, r: 28, color: '#f59e0b' }},
      {{ id: 'ice', label: 'ICE', type: 'unidade', x: 525, y: 170, r: 24, color: '#f59e0b' }},
      {{ id: 'dcc', label: 'Depto Computação', type: 'unidade', x: 340, y: 250, r: 22, color: '#f59e0b' }},
      {{ id: 'bsi', label: 'Curso BSI', type: 'unidade', x: 710, y: 250, r: 22, color: '#f59e0b' }},
      
      {{ id: 'ana', label: 'Dra. Ana Silva', type: 'docente', x: 230, y: 350, r: 24, color: '#0284c7' }},
      {{ id: 'mariana', label: 'Dra. Mariana Almeida', type: 'docente', x: 420, y: 350, r: 24, color: '#0284c7' }},
      
      {{ id: 'joao', label: 'João Pereira', type: 'discente', x: 640, y: 350, r: 22, color: '#16a34a' }},
      {{ id: 'lucas', label: 'Lucas Ferreira', type: 'discente', x: 820, y: 350, r: 22, color: '#16a34a' }},

      {{ id: 'proj_dados', label: 'Proj. Dados Abertos', type: 'projeto', x: 450, y: 470, r: 24, color: '#9333ea' }},
      {{ id: 'proj_edu', label: 'Proj. Educação Digital', type: 'projeto', x: 700, y: 470, r: 24, color: '#9333ea' }},

      {{ id: 'pub2024', label: 'Pub. 2024 (Conectados)', type: 'pub', x: 300, y: 470, r: 20, color: '#6366f1' }},

      {{ id: 'wkd_ufrrj', label: 'Wikidata (UFRRJ Q3550293)', type: 'lod', x: 780, y: 70, r: 20, color: '#e11d48' }},
      {{ id: 'orcid_ana', label: 'ORCID (Ana Silva)', type: 'lod', x: 90, y: 350, r: 18, color: '#e11d48' }},
      {{ id: 'wkd_ia', label: 'Wikidata (IA Q11660)', type: 'lod', x: 920, y: 470, r: 18, color: '#e11d48' }}
    ];

    const edges = [
      {{ from: 'ice', to: 'ufrrj', label: ':pertenceA' }},
      {{ from: 'dcc', to: 'ice', label: ':vinculadoA' }},
      {{ from: 'bsi', to: 'ice', label: ':vinculadoA' }},
      
      {{ from: 'ana', to: 'dcc', label: ':lotadoEm' }},
      {{ from: 'mariana', to: 'dcc', label: ':lotadoEm' }},

      {{ from: 'joao', to: 'bsi', label: ':matriculadoEm' }},
      {{ from: 'lucas', to: 'bsi', label: ':matriculadoEm' }},

      {{ from: 'ana', to: 'proj_dados', label: ':coordena' }},
      {{ from: 'mariana', to: 'proj_dados', label: ':participaDe' }},
      {{ from: 'joao', to: 'proj_dados', label: ':participaDe' }},
      {{ from: 'lucas', to: 'proj_dados', label: ':participaDe' }},

      {{ from: 'mariana', to: 'proj_edu', label: ':coordena' }},
      {{ from: 'lucas', to: 'proj_edu', label: ':participaDe' }},

      {{ from: 'ana', to: 'joao', label: ':orienta' }},
      {{ from: 'mariana', to: 'lucas', label: ':orienta' }},

      {{ from: 'ana', to: 'pub2024', label: ':autorDe' }},
      {{ from: 'mariana', to: 'pub2024', label: ':autorDe' }},
      {{ from: 'joao', to: 'pub2024', label: ':autorDe' }},

      {{ from: 'ufrrj', to: 'wkd_ufrrj', label: 'owl:sameAs' }},
      {{ from: 'ana', to: 'orcid_ana', label: 'schema:sameAs' }},
      {{ from: 'proj_edu', to: 'wkd_ia', label: 'skos:match' }}
    ];

    let draggedNode = null;
    let dragOffsetX = 0;
    let dragOffsetY = 0;

    function draw() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Edges
      edges.forEach(e => {{
        const src = nodes.find(n => n.id === e.from);
        const tgt = nodes.find(n => n.id === e.to);
        if (!src || !tgt) return;

        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.lineTo(tgt.x, tgt.y);
        ctx.strokeStyle = e.label.includes('sameAs') || e.label.includes('match') ? '#f43f5e' : '#94a3b8';
        ctx.lineWidth = e.label.includes('sameAs') ? 2 : 1.5;
        if (e.label.includes('sameAs') || e.label.includes('orienta')) {{
          ctx.setLineDash([4, 4]);
        }} else {{
          ctx.setLineDash([]);
        }}
        ctx.stroke();
        ctx.setLineDash([]);

        // Label
        const midX = (src.x + tgt.x) / 2;
        const midY = (src.y + tgt.y) / 2;
        ctx.fillStyle = '#475569';
        ctx.font = '10px sans-serif';
        ctx.fillText(e.label, midX + 3, midY - 3);
      }});

      // Nodes
      nodes.forEach(n => {{
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(n.label, n.x, n.y + n.r + 14);
      }});
    }}

    canvas.addEventListener('mousedown', (e) => {{
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      nodes.forEach(n => {{
        const dist = Math.hypot(n.x - mouseX, n.y - mouseY);
        if (dist <= n.r) {{
          draggedNode = n;
          dragOffsetX = n.x - mouseX;
          dragOffsetY = n.y - mouseY;
          canvas.style.cursor = 'grabbing';
        }}
      }});
    }});

    canvas.addEventListener('mousemove', (e) => {{
      if (!draggedNode) return;
      const rect = canvas.getBoundingClientRect();
      draggedNode.x = e.clientX - rect.left + dragOffsetX;
      draggedNode.y = e.clientY - rect.top + dragOffsetY;
      draw();
    }});

    window.addEventListener('mouseup', () => {{
      draggedNode = null;
      canvas.style.cursor = 'grab';
    }});

    draw();
  </script>
</body>
</html>
"""

def sincronizar_docs():
    """Copia todo o conteúdo do site gerado para docs/ facilitando o GitHub Pages imediato."""
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    shutil.copytree(SITE_DIR, DOCS_DIR)
    print(f"      -> Pasta docs/ sincronizada com sucesso para suporte nativo ao GitHub Pages!")

def main():
    print("[1/4] Conectando ao Grafo RDF da Ontologia...")
    g = carregar_dados()
    docentes, discentes = extrair_perfis(g)
    print(f"      Encontrados {len(docentes)} docentes e {len(discentes)} discentes no Grafo RDF.")

    print("[2/4] Gerando páginas individuais dos perfis com JSON-LD embutido...")
    for doc in docentes:
        caminho = os.path.join(PERFIS_DIR, f"{doc['id']}.html")
        html = render_docente(doc)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"      -> Perfil docente gerado: {doc['id']}.html")

    for disc in discentes:
        caminho = os.path.join(PERFIS_DIR, f"{disc['id']}.html")
        html = render_discente(disc)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"      -> Perfil discente gerado: {disc['id']}.html")

    print("[3/4] Gerando portal principal, consultas interativas e grafo visual...")
    index_html = render_index(docentes, discentes)
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    consultas_html = render_consultas_html(g)
    with open(os.path.join(SITE_DIR, "consultas.html"), "w", encoding="utf-8") as f:
        f.write(consultas_html)

    grafo_html = render_grafo_html()
    with open(os.path.join(SITE_DIR, "grafo.html"), "w", encoding="utf-8") as f:
        f.write(grafo_html)

    # Salva também um espelho em formato JSON para fins didáticos/documentação
    json_path = os.path.join(BASE_DIR, "codigo-fonte", "dados_extraidos_rdf.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"docentes": docentes, "discentes": discentes}, f, ensure_ascii=False, indent=2)

    print("[4/4] Sincronizando pasta docs/ para publicação no GitHub Pages...")
    sincronizar_docs()

    print("\n[SUCESSO] Todo o ecossistema web semântico foi compilado e publicado em site/ e docs/!")

if __name__ == "__main__":
    main()
