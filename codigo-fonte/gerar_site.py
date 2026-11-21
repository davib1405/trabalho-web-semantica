#!/usr/bin/env python3
"""
Gerador Dinâmico de Perfis Acadêmicos a partir do Grafo RDF/Turtle
Trabalho de Web Semântica e Linked Open Data - UFRRJ
Autor: David Barros da Rosa Filho
"""

import os
import json
import rdflib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_TTL_PATH = os.path.join(BASE_DIR, "ontologia", "dados.ttl")
ONTOLOGIA_OWL_PATH = os.path.join(BASE_DIR, "ontologia", "ontologia.owl")
SITE_DIR = os.path.join(BASE_DIR, "site")
PERFIS_DIR = os.path.join(SITE_DIR, "perfis")

os.makedirs(PERFIS_DIR, exist_ok=True)

def carregar_dados():
    g = rdflib.Graph()
    g.parse(ONTOLOGIA_OWL_PATH, format="turtle")
    g.parse(DADOS_TTL_PATH, format="turtle")
    return g

def extrair_perfis(g):
    query_docentes = """
    PREFIX : <http://dados.ufrrj.br/ontologia/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX schema: <http://schema.org/>
    PREFIX dcterms: <http://purl.org/dc/terms/>

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
    PREFIX schema: <http://schema.org/>

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
        
        # Áreas
        areas = [str(r.label) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?label WHERE {{
                <{uri}> :atuaEmArea ?area .
                ?area skos:prefLabel ?label .
                FILTER (LANG(?label) = 'pt')
            }}
        """)]

        # Disciplinas
        disciplinas = [str(r.label) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label WHERE {{
                <{uri}> :leciona ?d .
                ?d rdfs:label ?label .
            }}
        """)]

        # Projetos
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

        # Grupos de pesquisa
        grupos = [str(r.tit) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?tit WHERE {{
                <{uri}> :membroDeGrupo ?grp .
                ?grp rdfs:label ?tit .
            }}
        """)]

        # Publicações
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

        # Áreas
        areas = [str(r.label) for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?label WHERE {{
                <{uri}> :atuaEmArea ?area .
                ?area skos:prefLabel ?label .
                FILTER (LANG(?label) = 'pt')
            }}
        """)]

        # Projetos
        projetos = [{"titulo": str(r.tit), "papel": "Bolsista / Integrante"} for r in g.query(f"""
            PREFIX : <http://dados.ufrrj.br/ontologia/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?tit WHERE {{
                <{uri}> :participaDeProjeto ?p .
                ?p rdfs:label ?tit .
            }}
        """)]

        # Publicações
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
        <a href="../ontologia/dados.ttl" style="background: white; color: #1e3c72; padding: 8px 16px; border-radius: 6px; font-weight: bold; text-decoration: none;">Baixar RDF Turtle (.ttl)</a>
        <a href="../ontologia/ontologia.owl" style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold; text-decoration: none; border: 1px solid white;">Ver Ontologia OWL</a>
        <a href="../consultas/resultados_consolidados.md" style="background: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold; text-decoration: none; border: 1px solid white;">Consultas SPARQL</a>
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

def main():
    print("[1/3] Conectando ao Grafo RDF da Ontologia...")
    g = carregar_dados()
    docentes, discentes = extrair_perfis(g)
    print(f"      Encontrados {len(docentes)} docentes e {len(discentes)} discentes no Grafo RDF.")

    print("[2/3] Gerando páginas individuais dos perfis com JSON-LD embutido...")
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

    print("[3/3] Gerando portal principal (index.html)...")
    index_html = render_index(docentes, discentes)
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"      -> Portal gerado com sucesso: {index_path}")

    # Salva também um espelho em formato JSON para fins didáticos/documentação
    json_path = os.path.join(BASE_DIR, "codigo-fonte", "dados_extraidos_rdf.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"docentes": docentes, "discentes": discentes}, f, ensure_ascii=False, indent=2)
    print(f"      -> Exportação estruturada em JSON salva em: {json_path}")

    print("\n[SUCESSO] Aplicação Web e perfis gerados a partir da fonte de dados semântica!")

if __name__ == "__main__":
    main()
