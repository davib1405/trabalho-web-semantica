# Requisitos do Sistema de Perfis Acadêmicos Conectados

## 1. Requisitos Funcionais (RF)

| ID | Descrição | Status / Implementação |
| :--- | :--- | :--- |
| **RF01** | O sistema deve disponibilizar páginas web públicas de perfis acadêmicos navegáveis por qualquer navegador padrão. | Implementado (`site/index.html` e `site/perfis/*.html`). |
| **RF02** | O sistema deve apresentar no mínimo 2 perfis completos de docentes e 2 perfis completos de discentes. | Implementado (4 perfis: Ana Silva, Mariana Almeida, João Pereira e Lucas Ferreira). |
| **RF03** | A geração das páginas web deve ser automatizada a partir de fonte de dados estruturada, vedando o desenvolvimento de páginas manuais isoladas. | Implementado via script Python `gerar_site.py` alimentado diretamente pelo grafo RDF. |
| **RF04** | Cada perfil deve exibir informações contextuais essenciais: nome, cargo/papel, unidade acadêmica, curso/departamento, biografia, áreas de interesse, disciplinas, projetos, grupos de pesquisa, publicações e links de redes acadêmicas. | Implementado em conformidade com o layout HTML/CSS do professor. |
| **RF05** | O sistema deve permitir a resolução de consultas semânticas em SPARQL 1.1 para responder a 6 perguntas de competência institucional. | Implementado e validado em `consultas/consulta01.rq` a `consulta06.rq`. |
| **RF06** | Cada página de perfil deve incorporar metadados semânticos em formato de máquina (JSON-LD embutido no `<head>` e links para a serialização Turtle). | Implementado em 100% das páginas geradas. |
| **RF07** | O sistema deve disponibilizar um portal índice que relacione os perfis e forneça links para download dos arquivos de ontologia e dados RDF. | Implementado em `site/index.html`. |

---

## 2. Requisitos de Web Semântica e Dados Conectados (RLOD)

| ID | Descrição | Status / Implementação |
| :--- | :--- | :--- |
| **RLOD01** | Definir um modelo conceitual do domínio com entidades, atributos e relacionamentos formais. | Implementado em `documentacao/ontologia.md` e `documentacao/diagrama.md`. |
| **RLOD02** | Elaborar um Dicionário de Dados contendo nome, tipo, cardinalidade, restrições e descrição semântica de cada propriedade. | Implementado em `documentacao/dicionario-dados.md`. |
| **RLOD03** | Desenvolver e documentar uma Ontologia de Aplicação formal em OWL/RDF com hierarquias de classes, propriedades de objeto, propriedades de dados, domínios e alcances. | Implementado em `ontologia/ontologia.owl`. |
| **RLOD04** | Atribuir URIs persistentes e padronizadas para cada entidade (`http://dados.ufrrj.br/recurso/...` e `http://dados.ufrrj.br/ontologia/...`). | Implementado no grafo RDF. |
| **RLOD05** | Estabelecer conexões semânticas com no mínimo 3 recursos externos da Web (LOD), devidamente justificadas e sem uso indevido de `owl:sameAs`. | Implementado: UFRRJ (Wikidata/DBpedia), Seropédica (Wikidata/DBpedia), Áreas SKOS (Wikidata/DBpedia) e Pesquisadores (ORCID). |
| **RLOD06** | Especificar licença de uso aberto (Creative Commons CC-BY 4.0), data de atualização e autoria dos dados. | Implementado em metadados do Dataset (`dados.ttl` e `ontologia.owl`). |

---

## 3. Requisitos Não Funcionais (RNF)

| ID | Descrição | Justificativa Técnica |
| :--- | :--- | :--- |
| **RNF01** | **Interoperabilidade Semântica:** A ontologia e os dados devem ser serializados no padrão W3C Turtle (`.ttl`) e OWL/RDF XML (`.owl`). | Garante compatibilidade com o ecossistema W3C, Protégé, Apache Jena, RDF4J e Python `rdflib`. |
| **RNF02** | **Proteção de Dados e Privacidade:** Nenhuma informação sensível (CPF, matrícula, telefone pessoal, SIAPE) deve ser exposta publicamente. | Conformidade com as diretrizes da LGPD (Lei nº 13.709/2018) e o enunciado do trabalho. |
| **RNF03** | **Reprodutibilidade:** Toda a execução das consultas SPARQL e da compilação do site deve ser reproduzível por meio de scripts documentados e executáveis. | Scripts `gerar_site.py` e `executar_consultas.py` disponíveis em `codigo-fonte/`. |
| **RNF04** | **Conformidade Visual:** A camada de apresentação deve respeitar o design responsivo e a folha de estilos `estilos.css` fornecida pelo docente. | Utilização integral da folha de estilos oficial sem quebra visual. |
| **RNF05** | **Manutenibilidade:** Separação estrita entre dados brutos (grafo de conhecimento RDF), regras conceituais (ontologia OWL), lógica de aplicação (scripts) e templates de visualização. | Arquitetura desacoplada recomendada pela engenharia de software e Web Semântica. |
