# Documentação Formal da Ontologia de Aplicação

Este documento descreve as especificações técnicas formais da ontologia de perfis acadêmicos desenvolvida para a UFRRJ, abrangendo hierarquias, axiomas, domínios, alcances e propriedades.

---

## 1. Metadados Gerais da Ontologia

| Atributo | Valor / Definição |
| :--- | :--- |
| **URI da Ontologia** | `http://dados.ufrrj.br/ontologia/` |
| **Prefixo Padrão** | `:` ou `ufrrj-ont:` |
| **Título** | Ontologia de Perfis Acadêmicos da UFRRJ |
| **Autor** | David Barros da Rosa Filho |
| **Instituição** | Universidade Federal Rural do Rio de Janeiro (ICE / Depto. de Computação) |
| **Formato Canônico** | OWL 2 DL / W3C Turtle (`ontologia/ontologia.owl`) |
| **Licença** | Creative Commons Attribution 4.0 International (CC-BY 4.0) |
| **Versão** | 1.0.0 (Novembro de 2026) |

---

## 2. Hierarquia de Classes

```text
owl:Thing
├── foaf:Person / schema:Person
│   └── :Pessoa
│       ├── :Docente
│       └── :Discente
├── schema:Organization / foaf:Organization
│   └── :UnidadeAcademica
│       ├── :Instituto
│       └── :Departamento
├── schema:Course
│   ├── :Curso
│   └── :Disciplina
├── skos:Concept
│   └── :AreaPesquisa
├── foaf:Project / schema:ResearchProject
│   └── :Projeto
│       └── :ProjetoPesquisa
├── schema:ResearchProject
│   └── :GrupoPesquisa
├── dcterms:BibliographicResource / schema:ScholarlyArticle
│   └── :Publicacao
└── schema:EducationalOccupationalCredential
    └── :FormacaoAcademica
```

---

## 3. Especificação das Propriedades de Objeto (Object Properties)

### 3.1 `:pertenceA`
* **Definição:** Relação genérica de vínculo institucional entre uma pessoa e uma unidade acadêmica.
* **Domínio:** `:Pessoa`
* **Alcance:** `:UnidadeAcademica`

### 3.2 `:lotadoEm`
* **Definição:** Indica o departamento específico em que o docente está formalmente lotado.
* **Superpropriedade:** `:pertenceA`
* **Domínio:** `:Docente`
* **Alcance:** `:Departamento`

### 3.3 `:matriculadoEm`
* **Definição:** Indica o curso de graduação ou pós-graduação no qual o discente possui matrícula regular.
* **Superpropriedade:** `:pertenceA`
* **Domínio:** `:Discente`
* **Alcance:** `:Curso`

### 3.4 `:vinculadoAInstituto`
* **Definição:** Modela a hierarquia universitária onde departamentos e cursos estão subordinados a um instituto.
* **Domínio:** `owl:unionOf (:Departamento :Curso)`
* **Alcance:** `:Instituto`

### 3.5 `:atuaEmArea`
* **Definição:** Conecta pessoas acadêmicas a conceitos controlados de linhas de pesquisa e interesses (SKOS).
* **Domínio:** `:Pessoa`
* **Alcance:** `:AreaPesquisa`

### 3.6 `:participaDeProjeto`
* **Definição:** Expressa a participação ativa de qualquer indivíduo acadêmico em um projeto formal.
* **Domínio:** `:Pessoa`
* **Alcance:** `:Projeto`

### 3.7 `:coordenaProjeto`
* **Definição:** Identifica o docente que exerce a liderança ou coordenação oficial do projeto.
* **Superpropriedade:** `:participaDeProjeto`
* **Domínio:** `:Docente`
* **Alcance:** `:Projeto`

### 3.8 `:autorDe` e `:temAutor`
* **Definição:** Relação bidirecional entre autores acadêmicos e suas produções intelectuais.
* **Axioma:** `:autorDe owl:inverseOf :temAutor`
* **Domínio de `:autorDe`:** `:Pessoa` | **Alcance:** `:Publicacao`
* **Domínio de `:temAutor`:** `:Publicacao` | **Alcance:** `:Pessoa`

### 3.9 `:orienta`
* **Definição:** Relação pedagógica e científica entre um orientador docente e um orientando discente.
* **Domínio:** `:Docente`
* **Alcance:** `:Discente`

### 3.10 `:leciona`
* **Definição:** Relaciona o docente às disciplinas ministradas sob sua responsabilidade.
* **Domínio:** `:Docente`
* **Alcance:** `:Disciplina`

---

## 4. Especificação das Propriedades de Dados (Datatype Properties)

* **`:nomeCompleto`:** Domínio `:Pessoa`, Alcance `xsd:string` (Subpropriedade de `foaf:name` e `schema:name`).
* **`:cargoOuFuncao`:** Domínio `:Pessoa`, Alcance `xsd:string`.
* **`:titulacao`:** Domínio `:Docente`, Alcance `xsd:string`.
* **`:anoIngresso`:** Domínio `:Discente`, Alcance `xsd:integer`.
* **`:periodoAtual`:** Domínio `:Discente`, Alcance `xsd:string`.
* **`:emailInstitucional`:** Domínio `:Pessoa`, Alcance `xsd:string` (Subpropriedade de `foaf:mbox` e `schema:email`).
* **`:biografiaResumida`:** Domínio `:Pessoa`, Alcance `xsd:string`.
* **`:anoPublicacao`:** Domínio `:Publicacao`, Alcance `xsd:integer`.
* **`:linkLattes`:** Domínio `:Pessoa`, Alcance `xsd:anyURI`.
* **`:linkOrcid`:** Domínio `:Pessoa`, Alcance `xsd:anyURI`.
* **`:linkPaginaPessoal`:** Domínio `:Pessoa`, Alcance `xsd:anyURI`.

---

## 5. Validação da Ontologia
A ontologia foi submetida a teste sintático e estrutural utilizando o motor RDFLib e parser Turtle/OWL 2. O grafo resultante conta com **195 triplas ontológicas** sem inconsistências lógicas, estando apto para inferência e consultas SPARQL.
