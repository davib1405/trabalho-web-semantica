# Diagrama Conceitual da Ontologia de Perfis Acadêmicos

Este diagrama ilustra as classes, relacionamentos (Object Properties) e propriedades de dados que compõem o modelo ontológico da UFRRJ.

```mermaid
classDiagram
    direction TB

    class Pessoa {
        +string nomeCompleto
        +string emailInstitucional
        +string cargoOuFuncao
        +string biografiaResumida
        +anyURI linkLattes
        +anyURI linkOrcid
        +anyURI linkPaginaPessoal
    }

    class Docente {
        +string titulacao
    }

    class Discente {
        +int anoIngresso
        +string periodoAtual
    }

    class UnidadeAcademica {
        +string nome
    }

    class Instituto
    class Departamento
    class Curso {
        +string nomeCurso
    }

    class AreaPesquisa {
        +string prefLabel
        +string altLabel
    }

    class Projeto {
        +string title
        +string description
    }

    class Publicacao {
        +string title
        +int anoPublicacao
    }

    class Disciplina {
        +string courseCode
        +string name
    }

    Pessoa <|-- Docente : subClassOf
    Pessoa <|-- Discente : subClassOf
    UnidadeAcademica <|-- Instituto : subClassOf
    UnidadeAcademica <|-- Departamento : subClassOf

    Pessoa --> UnidadeAcademica : pertenceA
    Docente --> Departamento : lotadoEm
    Discente --> Curso : matriculadoEm
    Departamento --> Instituto : vinculadoAInstituto
    Curso --> Instituto : vinculadoAInstituto
    Curso --> Departamento : cursoOferecidoPor

    Pessoa --> AreaPesquisa : atuaEmArea
    Pessoa --> Projeto : participaDeProjeto
    Docente --> Projeto : coordenaProjeto
    Docente --> Discente : orienta
    Docente --> Disciplina : leciona

    Pessoa --> Publicacao : autorDe
    Publicacao --> Pessoa : temAutor
```

---

## 2. Diagrama de Instâncias e Relacionamentos do Grafo (RDF Data Graph)

```mermaid
flowchart LR
    subgraph Docentes
        Ana["Profa. Dra. Ana Silva"]
        Mariana["Profa. Dra. Mariana Almeida"]
    end

    subgraph Discentes
        Joao["João Exemplo Pereira"]
        Lucas["Lucas Ferreira"]
    end

    subgraph Unidades
        ICE["Instituto de Ciências Exatas (ICE)"]
        DCC["Depto de Computação"]
        BSI["Curso Sist. de Informação"]
    end

    subgraph Projetos
        ProjDados["Projeto Dados Abertos"]
        ProjEdu["Projeto Educação Digital"]
    end

    subgraph Publicacoes
        Pub2024["Pub 2024: Dados Conectados"]
        Pub2025["Pub 2025: IA e Acessibilidade"]
    end

    subgraph LOD_Externo["Linked Open Data (LOD)"]
        WKD_UFRRJ["Wikidata: UFRRJ (Q3550293)"]
        DBP_UFRRJ["DBpedia: UFRRJ"]
        ORCID_Ana["ORCID: Ana Silva"]
        WKD_IA["Wikidata: IA (Q11660)"]
        WKD_Sem["Wikidata: Semantic Web (Q54837)"]
    end

    %% Vínculos Institucionais
    Ana -->|lotadoEm| DCC
    Mariana -->|lotadoEm| DCC
    DCC -->|vinculadoAInstituto| ICE
    Joao -->|matriculadoEm| BSI
    Lucas -->|matriculadoEm| BSI
    BSI -->|vinculadoAInstituto| ICE

    Ana -->|pertenceA| ICE
    Mariana -->|pertenceA| ICE
    Joao -->|pertenceA| ICE
    Lucas -->|pertenceA| ICE

    %% Projetos
    Ana -->|coordenaProjeto| ProjDados
    Mariana -->|participaDeProjeto| ProjDados
    Joao -->|participaDeProjeto| ProjDados
    Lucas -->|participaDeProjeto| ProjDados

    Mariana -->|coordenaProjeto| ProjEdu
    Lucas -->|participaDeProjeto| ProjEdu

    %% Orientação
    Ana -->|orienta| Joao
    Mariana -->|orienta| Lucas

    %% Publicações
    Ana -->|autorDe| Pub2024
    Mariana -->|autorDe| Pub2024
    Joao -->|autorDe| Pub2024

    Mariana -->|autorDe| Pub2025
    Lucas -->|autorDe| Pub2025

    %% Conexões LOD
    ICE -.->|seeAlso| WKD_UFRRJ
    ICE -.->|sameAs| DBP_UFRRJ
    Ana -.->|sameAs| ORCID_Ana
    ProjDados -.->|skos:exactMatch| WKD_Sem
    ProjEdu -.->|skos:exactMatch| WKD_IA
```
