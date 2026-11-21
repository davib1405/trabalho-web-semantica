# Resultados Consolidados das Consultas SPARQL

**Disciplina:** Web Semântica e Linked Open Data  
**Instituição:** Universidade Federal Rural do Rio de Janeiro (UFRRJ) — Instituto de Ciências Exatas (ICE) / Departamento de Computação  
**Autor:** David Barros da Rosa Filho  
**Total de triplas avaliadas no grafo:** 418  
**Motor de Execução:** Python 3 + RDFLib (SPARQL 1.1 Query Engine)  

---

## Consulta 01: Quais são os docentes cadastrados e seus respectivos departamentos ou unidades acadêmicas?

* **Arquivo da consulta:** [`consulta01.rq`](consulta01.rq)

### Código SPARQL
```sparql
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
| :--- | :--- | :--- | :--- |
| `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | `ufrrj:DeptoComputacao` | Departamento de Computação |
| `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:DeptoComputacao` | Departamento de Computação |

### Explicação das Classes e Propriedades Utilizadas
* **`:Docente` (Classe):** Subclasse de `:Pessoa` que restringe o escopo da busca apenas a indivíduos com vínculo formal de magistério superior.
* **`:lotadoEm` (Object Property):** Subpropriedade de `:pertenceA`. Conecta cada instância de docente diretamente ao seu departamento acadêmico de lotação.
* **`:nomeCompleto` (Datatype Property):** Recupera a cadeia literal (`xsd:string`) com o nome civil e títulos do docente.
* **`rdfs:label` (Annotation Property):** Utilizada no alcance de `:departamento` para obter a denominação textual legível da unidade organizacional.

---

## Consulta 02: Quais discentes pertencem a determinado curso?

* **Arquivo da consulta:** [`consulta02.rq`](consulta02.rq)

### Código SPARQL
```sparql
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?discente ?nomeDiscente ?curso ?nomeCurso ?anoIngresso ?periodoAtual
WHERE {
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
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ufrrj:discente_lucas_ferreira` | Lucas Ferreira | `ufrrj:CursoSistemasInformacao` | Bacharelado em Sistemas de Informação | 2023 | 7º período |
| `ufrrj:discente_joao_pereira` | João Exemplo Pereira | `ufrrj:CursoSistemasInformacao` | Bacharelado em Sistemas de Informação | 2024 | 5º período |

### Explicação das Classes e Propriedades Utilizadas
* **`:Discente` (Classe):** Representa alunos com matrícula regular ativa na universidade.
* **`:Curso` (Classe):** Especialização de `schema:Course` que modela a graduação ofertada.
* **`:matriculadoEm` (Object Property):** Subpropriedade de `:pertenceA`. Liga o estudante ao curso de graduação.
* **`:anoIngresso` e `:periodoAtual` (Datatype Properties):** Literais que indicam temporalidade e progresso acadêmico.
* **Cláusula `VALUES`:** Permite parametrizar a consulta para qualquer URI de curso específico.

---

## Consulta 03: Quais docentes atuam em determinada área de pesquisa?

* **Arquivo da consulta:** [`consulta03.rq`](consulta03.rq)

### Código SPARQL
```sparql
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
| :--- | :--- | :--- | :--- | :--- |
| `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | Professora Associada | `ufrrj:AreaDadosAbertos` | Dados Abertos |
| `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | Professora Associada | `ufrrj:AreaEngenhariaConhecimento` | Engenharia de Conhecimento |
| `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | Professora Adjunta | `ufrrj:AreaInteligenciaArtificial` | Inteligência Artificial |
| `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | Professora Associada | `ufrrj:AreaWebSemantica` | Web Semântica |
| `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | Professora Adjunta | `ufrrj:AreaWebSemantica` | Web Semântica |

### Explicação das Classes e Propriedades Utilizadas
* **`:AreaPesquisa` / `skos:Concept` (Classe):** Modela áreas do conhecimento como conceitos de vocabulário controlado SKOS.
* **`:atuaEmArea` (Object Property):** Associa a pessoa acadêmica aos tópicos de investigação científica.
* **`skos:prefLabel` (Annotation Property):** Rótulo preferencial do conceito. O filtro `LANG(?nomeArea) = "pt"` seleciona o idioma vernáculo em conformidade com o SKOS multilingue.

---

## Consulta 04: Quais docentes e discentes participam de um mesmo projeto de pesquisa?
*(Consulta explorando relacionamentos complexos entre diferentes tipos de entidades)*

* **Arquivo da consulta:** [`consulta04.rq`](consulta04.rq)

### Código SPARQL
```sparql
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
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ufrrj:ProjetoDadosAbertos` | Projeto Exemplo de Dados Abertos | `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | `ufrrj:discente_joao_pereira` | João Exemplo Pereira |
| `ufrrj:ProjetoDadosAbertos` | Projeto Exemplo de Dados Abertos | `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | `ufrrj:discente_lucas_ferreira` | Lucas Ferreira |
| `ufrrj:ProjetoDadosAbertos` | Projeto Exemplo de Dados Abertos | `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:discente_joao_pereira` | João Exemplo Pereira |
| `ufrrj:ProjetoDadosAbertos` | Projeto Exemplo de Dados Abertos | `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:discente_lucas_ferreira` | Lucas Ferreira |
| `ufrrj:ProjetoEducacaoDigital` | Projeto de Pesquisa em Educação Digital | `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:discente_lucas_ferreira` | Lucas Ferreira |

### Explicação das Classes e Propriedades Utilizadas
* **Relação Tripartida (Entidade Intermediária):** Esta consulta não recupera apenas atributos; ela conecta três classes distintas: `:Docente`, `:Discente` e `:Projeto`.
* **`:participaDeProjeto` (Object Property):** Propriedade que converge a atuação de docentes e alunos em uma mesma iniciativa científica. Como `:coordenaProjeto` é subpropriedade de `:participaDeProjeto`, o grafo reconhece a coordenação como participação direta.

---

## Consulta 05: Quais publicações estão associadas a determinado docente e quem são seus coautores?
*(Consulta explorando relacionamentos complexos de coautoria entre pares científicos)*

* **Arquivo da consulta:** [`consulta05.rq`](consulta05.rq)

### Código SPARQL
```sparql
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

| docente | nomeDocente | publicacao | tituloPublicacao | ano | coautor | nomeCoautor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | `ufrrj:Pub2024DadosConectados` | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | `ufrrj:discente_joao_pereira` | João Exemplo Pereira |
| `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | `ufrrj:Pub2024DadosConectados` | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida |
| `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:Pub2024DadosConectados` | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva |
| `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:Pub2024DadosConectados` | Publicação sobre dados conectados e interoperabilidade acadêmica | 2024 | `ufrrj:discente_joao_pereira` | João Exemplo Pereira |
| `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `ufrrj:Pub2025IAeAcessibilidade` | Aplicações de inteligência artificial na acessibilidade de dados abertos universitários | 2025 | `ufrrj:discente_lucas_ferreira` | Lucas Ferreira |

### Explicação das Classes e Propriedades Utilizadas
* **`:Publicacao` (Classe):** Alinhada a `dcterms:BibliographicResource` e `schema:ScholarlyArticle`.
* **`:temAutor` (Object Property):** Relaciona o artefato científico a todas as pessoas que contribuíram para a sua autoria.
* **`FILTER (?coautor != ?docente)`:** Operador de negação de igualdade por URI para impedir que a consulta retorne o próprio docente como seu próprio coautor.

---

## Consulta 06: Quais pessoas estão vinculadas a uma unidade acadêmica específica, independentemente de serem docentes ou discentes?
*(Consulta explorando polimorfismo ontológico e hierarquia de classes)*

* **Arquivo da consulta:** [`consulta06.rq`](consulta06.rq)

### Código SPARQL
```sparql
PREFIX : <http://dados.ufrrj.br/ontologia/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?unidade ?nomeUnidade ?tipoPessoa ?pessoa ?nomePessoa ?emailInstitucional
WHERE {
    VALUES ?unidade { <http://dados.ufrrj.br/recurso/InstitutoCienciasExatas> }
    ?unidade rdfs:label ?nomeUnidade .
    
    ?pessoa :pertenceA ?unidade ;
            a ?tipoPessoa ;
            :nomeCompleto ?nomePessoa ;
            :emailInstitucional ?emailInstitucional .
            
    FILTER (?tipoPessoa IN (:Docente, :Discente))
}
ORDER BY ?tipoPessoa ?nomePessoa
```

### Resultado Obtido (4 registros)

| unidade | nomeUnidade | tipoPessoa | pessoa | nomePessoa | emailInstitucional |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ufrrj:InstitutoCienciasExatas` | ICE | `:Discente` | `ufrrj:discente_joao_pereira` | João Exemplo Pereira | `joao.pereira@ufrrj.br` |
| `ufrrj:InstitutoCienciasExatas` | ICE | `:Discente` | `ufrrj:discente_lucas_ferreira` | Lucas Ferreira | `lucas.ferreira@ufrrj.br` |
| `ufrrj:InstitutoCienciasExatas` | ICE | `:Docente` | `ufrrj:docente_ana_silva` | Profa. Dra. Ana Exemplo da Silva | `anaexemplo@ufrrj.br` |
| `ufrrj:InstitutoCienciasExatas` | ICE | `:Docente` | `ufrrj:docente_mariana_almeida` | Profa. Dra. Mariana Almeida | `mariana.almeida@ufrrj.br` |

### Explicação das Classes e Propriedades Utilizadas
* **Polimorfismo de `:Pessoa`:** A consulta trata tanto instâncias de `:Docente` quanto de `:Discente` sob o mesmo padrão de grafo.
* **`:pertenceA` (Object Property):** Propriedade ancestral compartilhada na taxonomia institucional.
* **`FILTER (?tipoPessoa IN (:Docente, :Discente))`:** Filtra a instanciação direta para categorizar explicitamente o papel de cada pessoa encontrada na unidade institucional avaliada.
