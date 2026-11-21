# Resultados Consolidados das Consultas SPARQL

**Disciplina:** Web Semântica e Linked Open Data (UFRRJ)

**Autor:** David Barros da Rosa Filho

**Total de triplas avaliadas no grafo:** 418

---

## Consulta 01: Quais são os docentes cadastrados e seus respectivos departamentos ou unidades acadêmicas?

**Arquivo da consulta:** [`consulta01.rq`](../consulta01.rq)

### Código SPARQL
```sparql
# Consulta 1: Quais são os docentes cadastrados e seus respectivos departamentos ou unidades acadêmicas?
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?docente ?nomeDocente ?departamento ?nomeDepartamento
WHERE {
    ?docente a :Docente ;
             :nomeCompleto ?nomeDocente ;
             :lotadoEm ?departamento .
    ?departamento rdfs:label ?nomeDepartamento .
}
ORDER BY ?nomeDocente
```

### Resultado Obtido (2 registros)

| docente | nomeDocente | departamento | nomeDepartamento |
| --- | --- | --- | --- |
| http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | http://dados.ufrrj.br/recurso/DeptoComputacao | Departamento de Computação |
| http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/DeptoComputacao | Departamento de Computação |

---

## Consulta 02: Quais discentes pertencem a determinado curso?

**Arquivo da consulta:** [`consulta02.rq`](../consulta02.rq)

### Código SPARQL
```sparql
# Consulta 2: Quais discentes pertencem a determinado curso?
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?discente ?nomeDiscente ?curso ?nomeCurso ?anoIngresso ?periodoAtual
WHERE {
    # Filtro ou busca para o curso de Sistemas de Informação
    VALUES ?curso { <http://dados.ufrrj.br/recurso/CursoSistemasInformacao> }
    ?curso rdfs:label ?nomeCurso .
    
    ?discente a :Discente ;
              :nomeCompleto ?nomeDiscente ;
              :matriculadoEm ?curso ;
              :anoIngresso ?anoIngresso ;
              :periodoAtual ?periodoAtual .
}
ORDER BY ?anoIngresso ?nomeDiscente
```

### Resultado Obtido (2 registros)

| discente | nomeDiscente | curso | nomeCurso | anoIngresso | periodoAtual |
| --- | --- | --- | --- | --- | --- |
| http://dados.ufrrj.br/recurso/discente_lucas_ferreira | Lucas Ferreira | http://dados.ufrrj.br/recurso/CursoSistemasInformacao | Bacharelado em Sistemas de Informação | 2023 | 7º período |
| http://dados.ufrrj.br/recurso/discente_joao_pereira | João Exemplo Pereira | http://dados.ufrrj.br/recurso/CursoSistemasInformacao | Bacharelado em Sistemas de Informação | 2024 | 5º período |

---

## Consulta 03: Quais docentes atuam em determinada área de pesquisa?

**Arquivo da consulta:** [`consulta03.rq`](../consulta03.rq)

### Código SPARQL
```sparql
# Consulta 3: Quais docentes atuam em determinada área de pesquisa?
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?docente ?nomeDocente ?cargo ?area ?nomeArea
WHERE {
    ?docente a :Docente ;
             :nomeCompleto ?nomeDocente ;
             :cargoOuFuncao ?cargo ;
             :atuaEmArea ?area .
    ?area skos:prefLabel ?nomeArea .
    FILTER (LANG(?nomeArea) = "pt")
}
ORDER BY ?nomeArea ?nomeDocente
```

### Resultado Obtido (5 registros)

| docente | nomeDocente | cargo | area | nomeArea |
| --- | --- | --- | --- | --- |
| http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | Professora Associada | http://dados.ufrrj.br/recurso/AreaDadosAbertos | Dados Abertos |
| http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | Professora Associada | http://dados.ufrrj.br/recurso/AreaEngenhariaConhecimento | Engenharia de Conhecimento |
| http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | Professora Adjunta | http://dados.ufrrj.br/recurso/AreaInteligenciaArtificial | Inteligência Artificial |
| http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | Professora Associada | http://dados.ufrrj.br/recurso/AreaWebSemantica | Web Semântica |
| http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | Professora Adjunta | http://dados.ufrrj.br/recurso/AreaWebSemantica | Web Semântica |

---

## Consulta 04: Quais docentes e discentes participam de um mesmo projeto de pesquisa?

**Arquivo da consulta:** [`consulta04.rq`](../consulta04.rq)

### Código SPARQL
```sparql
# Consulta 4: Quais docentes e discentes participam de um mesmo projeto de pesquisa?
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?projeto ?tituloProjeto ?docente ?nomeDocente ?discente ?nomeDiscente
WHERE {
    ?projeto a :Projeto ;
             rdfs:label ?tituloProjeto .
    
    # Docente participante do projeto
    ?docente a :Docente ;
             :nomeCompleto ?nomeDocente ;
             :participaDeProjeto ?projeto .
             
    # Discente participante do mesmo projeto
    ?discente a :Discente ;
              :nomeCompleto ?nomeDiscente ;
              :participaDeProjeto ?projeto .
}
ORDER BY ?tituloProjeto ?nomeDocente ?nomeDiscente
```

### Resultado Obtido (5 registros)

| projeto | tituloProjeto | docente | nomeDocente | discente | nomeDiscente |
| --- | --- | --- | --- | --- | --- |
| http://dados.ufrrj.br/recurso/ProjetoDadosAbertos | Projeto Exemplo de Dados Abertos | http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | http://dados.ufrrj.br/recurso/discente_joao_pereira | João Exemplo Pereira |
| http://dados.ufrrj.br/recurso/ProjetoDadosAbertos | Projeto Exemplo de Dados Abertos | http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | http://dados.ufrrj.br/recurso/discente_lucas_ferreira | Lucas Ferreira |
| http://dados.ufrrj.br/recurso/ProjetoDadosAbertos | Projeto Exemplo de Dados Abertos | http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/discente_joao_pereira | João Exemplo Pereira |
| http://dados.ufrrj.br/recurso/ProjetoDadosAbertos | Projeto Exemplo de Dados Abertos | http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/discente_lucas_ferreira | Lucas Ferreira |
| http://dados.ufrrj.br/recurso/ProjetoEducacaoDigital | Projeto de Pesquisa em Educação Digital e Inclusão Tecnológica | http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/discente_lucas_ferreira | Lucas Ferreira |

---

## Consulta 05: Quais publicações estão associadas a determinado docente e quem são seus coautores?

**Arquivo da consulta:** [`consulta05.rq`](../consulta05.rq)

### Código SPARQL
```sparql
# Consulta 5: Quais publicações estão associadas a determinado docente e quem são seus coautores?
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?docente ?nomeDocente ?publicacao ?tituloPublicacao ?anoPublicacao ?coautor ?nomeCoautor
WHERE {
    ?docente a :Docente ;
             :nomeCompleto ?nomeDocente .
             
    ?publicacao a :Publicacao ;
                dcterms:title ?tituloPublicacao ;
                :anoPublicacao ?anoPublicacao ;
                :temAutor ?docente, ?coautor .
                
    ?coautor :nomeCompleto ?nomeCoautor .
    
    # Exclui o próprio docente da lista de coautores
    FILTER (?coautor != ?docente)
}
ORDER BY ?nomeDocente ?anoPublicacao ?tituloPublicacao ?nomeCoautor
```

### Resultado Obtido (5 registros)

| docente | nomeDocente | publicacao | tituloPublicacao | anoPublicacao | coautor | nomeCoautor |
| --- | --- | --- | --- | --- | --- | --- |
| http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | http://dados.ufrrj.br/recurso/Pub2024DadosConectados | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | http://dados.ufrrj.br/recurso/discente_joao_pereira | João Exemplo Pereira |
| http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | http://dados.ufrrj.br/recurso/Pub2024DadosConectados | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida |
| http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/Pub2024DadosConectados | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | http://dados.ufrrj.br/recurso/discente_joao_pereira | João Exemplo Pereira |
| http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/Pub2024DadosConectados | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva |
| http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | http://dados.ufrrj.br/recurso/Pub2025IAeAcessibilidade | Aplicações de inteligência artificial na acessibilidade de dados abertos universitários | 2025 | http://dados.ufrrj.br/recurso/discente_lucas_ferreira | Lucas Ferreira |

---

## Consulta 06: Quais pessoas estão vinculadas a uma unidade acadêmica específica, independentemente de serem docentes ou discentes?

**Arquivo da consulta:** [`consulta06.rq`](../consulta06.rq)

### Código SPARQL
```sparql
# Consulta 6: Quais pessoas estão vinculadas a uma unidade acadêmica específica, independentemente de serem docentes ou discentes?
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?unidade ?nomeUnidade ?tipoPessoa ?pessoa ?nomePessoa ?emailInstitucional
WHERE {
    # Unidade acadêmica selecionada (ex: Instituto de Ciências Exatas)
    VALUES ?unidade { <http://dados.ufrrj.br/recurso/InstitutoCienciasExatas> }
    ?unidade rdfs:label ?nomeUnidade .
    
    # Pessoa vinculada diretamente ou por vínculo institucional
    ?pessoa :pertenceA ?unidade ;
            a ?tipoPessoa ;
            :nomeCompleto ?nomePessoa ;
            :emailInstitucional ?emailInstitucional .
            
    # Filtra apenas os tipos de pessoas acadêmicas
    FILTER (?tipoPessoa IN (:Docente, :Discente))
}
ORDER BY ?tipoPessoa ?nomePessoa
```

### Resultado Obtido (4 registros)

| unidade | nomeUnidade | tipoPessoa | pessoa | nomePessoa | emailInstitucional |
| --- | --- | --- | --- | --- | --- |
| http://dados.ufrrj.br/recurso/InstitutoCienciasExatas | Instituto de Ciências Exatas (ICE) | http://dados.ufrrj.br/ontologia/Discente | http://dados.ufrrj.br/recurso/discente_joao_pereira | João Exemplo Pereira | joao.pereira@ufrrj.br |
| http://dados.ufrrj.br/recurso/InstitutoCienciasExatas | Instituto de Ciências Exatas (ICE) | http://dados.ufrrj.br/ontologia/Discente | http://dados.ufrrj.br/recurso/discente_lucas_ferreira | Lucas Ferreira | lucas.ferreira@ufrrj.br |
| http://dados.ufrrj.br/recurso/InstitutoCienciasExatas | Instituto de Ciências Exatas (ICE) | http://dados.ufrrj.br/ontologia/Docente | http://dados.ufrrj.br/recurso/docente_ana_silva | Profa. Dra. Ana Exemplo da Silva | anaexemplo@ufrrj.br |
| http://dados.ufrrj.br/recurso/InstitutoCienciasExatas | Instituto de Ciências Exatas (ICE) | http://dados.ufrrj.br/ontologia/Docente | http://dados.ufrrj.br/recurso/docente_mariana_almeida | Profa. Dra. Mariana Almeida | mariana.almeida@ufrrj.br |

---
