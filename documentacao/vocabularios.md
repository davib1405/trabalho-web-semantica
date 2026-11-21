# Pesquisa de Ontologias, Vocabulários e Conexões LOD

Este documento cumpre os requisitos de fundamentação teórica e metodológica da disciplina de Web Semântica, apresentando a avaliação de vocabulários existentes, critérios de escolha, justificativas de especialização e o mapeamento de conexões com a Web de Dados Abertos e Conectados (LOD).

---

## 1. Avaliação de Vocabulários e Ontologias Existentes

Para modelar o domínio acadêmico de perfis universitários, realizou-se uma pesquisa prévia na literatura e em diretórios de ontologias (como o *Linked Open Vocabularies - LOV* e as especificações oficiais do W3C).

| Vocabulário / Ontologia | Escopo Avaliado | Decisão no Projeto | Justificativa |
| :--- | :--- | :--- | :--- |
| **FOAF (*Friend of a Friend*)** | Descrição de pessoas, contatos e projetos sociais. | **Reutilização parcial e alinhamento.** | É um dos padrões mais maduros da Web Semântica. A classe `foaf:Person` e propriedades como `foaf:name` e `foaf:mbox` foram reutilizadas para garantir interoperabilidade direta com sistemas semânticos legados. Contudo, FOAF sozinho não contempla conceitos estritamente universitários (como titulação, departamentos e cursos). |
| **Schema.org** | Esquema universal para marcação web, mantido pelos principais mecanismos de busca (Google, Bing, Yahoo). | **Adoção prioritária na camada web e ontológica.** | Fundamental para descoberta na Web. Fornece `schema:Person`, `schema:CollegeOrUniversity`, `schema:ScholarlyArticle`, `schema:Course` e `schema:affiliation`. Foi embutido no HTML via JSON-LD. |
| **SKOS (*Simple Knowledge Organization System*)** | Organização de conceitos, tesauros, taxonomias e esquemas de classificação. | **Adoção fundamental para Áreas de Conhecimento.** | Permite categorizar os interesses de pesquisa dos professores e alunos (`skos:Concept`) com rótulos preferenciais (`skos:prefLabel`) e alternativos (`skos:altLabel`), além de interligação via `skos:exactMatch`. |
| **DCMI (*Dublin Core Metadata Terms*)** | Metadados gerais de autoria, temporalidade, proveniência e licenciamento. | **Reutilização mandatória para metadados.** | Padrão ISO para catalogação bibliográfica. Utilizado para `dcterms:title`, `dcterms:description`, `dcterms:license`, `dcterms:created` e `dcterms:modified`. |
| **VIVO Ontology** | Ontologia específica para atividades de pesquisa e perfis acadêmicos. | **Avaliada como referência arquitetural.** | Apresenta excelente cobertura, mas sua complexidade e volume de axiomas introduzem *overhead* desnecessário para um modelo de aplicação focado. Extraiu-se o princípio da separação de papéis sem a sobrecarga do VIVO completo. |

---

## 2. Conexões Semânticas com Dados Externos (Linked Open Data - LOD)

Para que o catálogo de perfis da UFRRJ participe efetivamente da Web de Dados Conectados, foram estabelecidas conexões semânticas com bases globais consolidadas.

### Conexão 1: Universidade Federal Rural do Rio de Janeiro (Instituição)
* **URI Local:** `http://dados.ufrrj.br/recurso/UFRRJ`
* **Entidade Externa (Wikidata):** `https://www.wikidata.org/wiki/Q3550293` (UFRRJ)
  * **Predicado Semântico:** `rdfs:seeAlso`
  * **Justificativa:** Conecta o registro institucional à página enciclopédica estruturada na Wikidata, permitindo a agentes externos obterem fundação histórica, coordenadas geográficas e dirigentes.
* **Entidade Externa (DBpedia):** `http://dbpedia.org/resource/Federal_Rural_University_of_Rio_de_Janeiro`
  * **Predicado Semântico:** `owl:sameAs`
  * **Justificativa:** Trata-se rigorosamente do mesmo objeto físico e jurídico no mundo real. `owl:sameAs` é plenamente válido para unificar a identidade entre as duas bases de dados.

### Conexão 2: Município de Seropédica (Localização do Campus)
* **URI Local:** `http://dados.ufrrj.br/recurso/Seropedica`
* **Entidade Externa (Wikidata):** `https://www.wikidata.org/wiki/Q1002058` (Seropédica)
  * **Predicado Semântico:** `owl:sameAs`
* **Entidade Externa (DBpedia):** `http://dbpedia.org/resource/Serop%C3%A9dica`
  * **Predicado Semântico:** `rdfs:seeAlso`
  * **Justificativa:** Âncora geográfica e espacial que posiciona a sede da universidade no grafo mundial de entidades geográficas, viabilizando consultas geoespaciais semânticas futuras.

### Conexão 3: Áreas de Pesquisa e Conhecimento (SKOS & Wikidata/DBpedia)
Cada linha temática de atuação acadêmica foi alinhada conceitualmente com termos canônicos globais:
* **Web Semântica:**
  * URI Local: `http://dados.ufrrj.br/recurso/AreaWebSemantica`
  * `skos:exactMatch <https://www.wikidata.org/wiki/Q54837>` (Semantic Web)
  * `skos:closeMatch <http://dbpedia.org/resource/Semantic_Web>`
* **Inteligência Artificial:**
  * URI Local: `http://dados.ufrrj.br/recurso/AreaInteligenciaArtificial`
  * `skos:exactMatch <https://www.wikidata.org/wiki/Q11660>` (Artificial Intelligence)
  * `skos:closeMatch <http://dbpedia.org/resource/Artificial_intelligence>`
* **Dados Abertos:**
  * URI Local: `http://dados.ufrrj.br/recurso/AreaDadosAbertos`
  * `skos:exactMatch <https://www.wikidata.org/wiki/Q309903>` (Open Data)
* **Engenharia de Conhecimento:**
  * URI Local: `http://dados.ufrrj.br/recurso/AreaEngenhariaConhecimento`
  * `skos:exactMatch <https://www.wikidata.org/wiki/Q1143899>` (Knowledge Engineering)

* **Justificativa Metodológica:**
  O uso de `skos:exactMatch` e `skos:closeMatch` expressa conformidade semântica terminológica sem exigir identidade ontológica irrestrita (que ocorreria com `owl:sameAs`), respeitando a natureza conceitual das taxonomias científicas.

### Conexão 4: Identificadores Persistentes de Autoria (ORCID)
* **URI Local da Profa. Ana Silva:** `http://dados.ufrrj.br/recurso/docente_ana_silva`
  * `schema:sameAs <https://orcid.org/0000-0002-1825-0097>`
* **URI Local da Profa. Mariana Almeida:** `http://dados.ufrrj.br/recurso/docente_mariana_almeida`
  * `schema:sameAs <https://orcid.org/0000-0001-5000-0000>`
* **Justificativa:** O ORCID (*Open Researcher and Contributor ID*) é o identificador persistente global para desambiguação de pesquisadores, conectando os docentes da UFRRJ a suas publicações em bases mundiais como Crossref, Scopus e Web of Science.

---

## 3. Fontes de Dados e Licenciamento
* **Fontes:** Dados conceituais e acadêmicos modelados com base no corpo docente do Departamento de Computação e estrutura institucional da UFRRJ, utilizando dados demonstrativos e fictícios não sensíveis conforme orientado pelo docente.
* **Licença de Compartilhamento:** Creative Commons Atribuição 4.0 Internacional ([CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)), assegurando que os dados abertos possam ser livremente reutilizados, combinados e redistribuídos, desde que mantida a atribuição original.
* **Temporalidade:** Versão 1.0 fechada em novembro de 2026.
