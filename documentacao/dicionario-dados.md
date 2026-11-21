# Dicionário de Dados Semântico

Este documento descreve detalhadamente cada campo, propriedade de objeto e propriedade de dados utilizada na modelagem e publicação dos perfis acadêmicos da UFRRJ, incluindo tipos, cardinalidade, restrições e justificativas.

---

## 1. Entidades Principais (Classes)

| Classe (URI) | Classe Padrão Alinhada | Descrição Semântica | Exemplo de Instância |
| :--- | :--- | :--- | :--- |
| `:Pessoa` | `foaf:Person`, `schema:Person` | Ser humano que possui vínculo ativo com a universidade. | `ufrrj:docente_ana_silva` |
| `:Docente` | Subclasse de `:Pessoa` | Servidor público pertencente ao corpo docente institucional. | `ufrrj:docente_mariana_almeida` |
| `:Discente` | Subclasse de `:Pessoa` | Estudante regularmente matriculado em curso da instituição. | `ufrrj:discente_joao_pereira` |
| `:UnidadeAcademica`| `schema:Organization` | Órgão ou subdivisão estrutural da universidade. | `ufrrj:InstitutoCienciasExatas` |
| `:Instituto` | Subclasse de `:UnidadeAcademica` | Grande centro agregador de departamentos e cursos. | `ufrrj:InstitutoCienciasExatas` |
| `:Departamento` | Subclasse de `:UnidadeAcademica` | Divisão básica responsável pela lotação e gestão didática. | `ufrrj:DeptoComputacao` |
| `:Curso` | `schema:Course` | Programa de formação acadêmica superior. | `ufrrj:CursoSistemasInformacao` |
| `:AreaPesquisa` | `skos:Concept` | Domínio de especialização ou linha de investigação científica. | `ufrrj:AreaWebSemantica` |
| `:Projeto` | `foaf:Project`, `schema:ResearchProject`| Iniciativa formal de pesquisa, ensino ou extensão. | `ufrrj:ProjetoDadosAbertos` |
| `:GrupoPesquisa` | `schema:ResearchProject` | Coletivo permanente cadastrado em diretórios de pesquisa. | `ufrrj:GrupoSistemasInteligentes` |
| `:Publicacao` | `dcterms:BibliographicResource`, `schema:ScholarlyArticle` | Artigo em periódico, conferência ou documento científico. | `ufrrj:Pub2024DadosConectados` |
| `:Disciplina` | `schema:Course` | Componente curricular lecionado em cursos de graduação. | `ufrrj:DiscWebSemantica` |

---

## 2. Propriedades de Objeto (Object Properties)

As propriedades de objeto definem relações semânticas entre entidades identificadas por URIs.

| Propriedade (URI) | Domínio | Alcance (Range) | Cardinalidade | Descrição / Regra Semântica |
| :--- | :--- | :--- | :--- | :--- |
| `:pertenceA` | `:Pessoa` | `:UnidadeAcademica` | 1..N | Conecta qualquer pessoa (docente ou discente) à sua unidade macro. |
| `:lotadoEm` | `:Docente` | `:Departamento` | 1..1 | Especialização de `:pertenceA`. Define o departamento oficial do docente. |
| `:matriculadoEm` | `:Discente` | `:Curso` | 1..1 | Especialização de `:pertenceA`. Define o curso formal do discente. |
| `:vinculadoAInstituto`| `:Departamento` ou `:Curso` | `:Instituto` | 1..1 | Estabelece a hierarquia entre cursos/departamentos e o Instituto mantenedor. |
| `:cursoOferecidoPor`| `:Curso` | `:UnidadeAcademica` | 1..N | Conecta o curso ao departamento responsável por sua administração. |
| `:atuaEmArea` | `:Pessoa` | `:AreaPesquisa` | 1..N | Conecta o indivíduo a áreas temáticas de conhecimento modeladas em SKOS. |
| `:participaDeProjeto`| `:Pessoa` | `:Projeto` | 0..N | Associa docentes e discentes a projetos de pesquisa em andamento. |
| `:coordenaProjeto` | `:Docente` | `:Projeto` | 0..N | Subpropriedade de `:participaDeProjeto`. Indica coordenação formal pelo docente. |
| `:membroDeGrupo` | `:Pessoa` | `:GrupoPesquisa` | 0..N | Relaciona pesquisadores a grupos de pesquisa certificados. |
| `:autorDe` | `:Pessoa` | `:Publicacao` | 0..N | Relaciona o indivíduo a publicações científicas de sua autoria. |
| `:temAutor` | `:Publicacao` | `:Pessoa` | 1..N | Inversa de `:autorDe`. Permite identificar coautores de cada publicação. |
| `:orienta` | `:Docente` | `:Discente` | 0..N | Expressa a relação formal de orientação acadêmica e científica. |
| `:leciona` | `:Docente` | `:Disciplina` | 0..N | Relaciona as matérias lecionadas pelo docente nos cursos da universidade. |

---

## 3. Propriedades de Dados (Datatype Properties)

As propriedades de dados associam valores literais e tipos de dados XML Schema (`xsd`) às entidades.

| Propriedade (URI) | Domínio | Tipo de Dado (`xsd`) | Obrigatório? | Regra de Validação / Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `:nomeCompleto` | `:Pessoa` | `xsd:string` | Sim | Nome civil completo do indivíduo. Deve ter no mínimo 2 palavras. |
| `:cargoOuFuncao` | `:Pessoa` | `xsd:string` | Sim | Título formal (ex: "Professora Associada", "Discente de Graduação"). |
| `:titulacao` | `:Docente` | `xsd:string` | Sim | Titulação máxima acadêmica (ex: "Doutorado em Ciência da Computação"). |
| `:anoIngresso` | `:Discente` | `xsd:integer` | Sim | Ano letivo de entrada na UFRRJ (4 dígitos inteiros, ex: 2024). |
| `:periodoAtual` | `:Discente` | `xsd:string` | Sim | Identificação da fase atual do aluno (ex: "5º período"). |
| `:emailInstitucional`| `:Pessoa` | `xsd:string` | Sim | Endereço de correio eletrônico institucional (terminado em `@ufrrj.br`). |
| `:biografiaResumida`| `:Pessoa` | `xsd:string` | Não | Texto descritivo da trajetória acadêmica e profissional. |
| `:anoPublicacao` | `:Publicacao` | `xsd:integer` | Sim | Ano em que a obra foi publicada (4 dígitos inteiros). |
| `:linkLattes` | `:Pessoa` | `xsd:anyURI` | Não | URI pública apontando para a plataforma Lattes do CNPq. |
| `:linkOrcid` | `:Pessoa` | `xsd:anyURI` | Não | URI persistente no padrão `https://orcid.org/0000-0000-0000-0000`. |
| `:linkPaginaPessoal`| `:Pessoa` | `xsd:anyURI` | Não | URI da página pessoal do indivíduo. |
| `dcterms:title` | Vários | `xsd:string` | Sim | Título legível de projetos, publicações ou cursos. |
| `dcterms:license` | Dataset | `xsd:anyURI` | Sim | Licença aberta atribuída aos dados (`https://creativecommons.org/licenses/by/4.0/`). |
| `dcterms:modified` | Dataset | `xsd:date` | Sim | Data da última alteração no grafo de conhecimento (`AAAA-MM-DD`). |
