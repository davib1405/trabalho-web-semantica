# Decisões de Modelagem Conceitual e Ontológica

Este documento detalha as decisões tomadas durante a concepção da ontologia de perfis acadêmicos da **Universidade Federal Rural do Rio de Janeiro (UFRRJ)**, justificando as escolhas arquiteturais, estruturais e ontológicas adotadas.

---

## 1. Separação entre Vínculo Institucional e Papéis Acadêmicos
Uma das decisões primordiais deste projeto — herdada e aprofundada a partir da proposta conceitual inicial desenvolvida na disciplina — foi a **separação ontológica entre o vínculo institucional e os papéis/atividades acumuláveis**.

* **O Problema da Abordagem Ingênua:**
  Em muitos cadastros legados, tenta-se criar classes compostas como `Docente-Pesquisador-Coordenador` ou `Discente-Bolsista-Monitor`. Essa abordagem gera explosão combinatória de classes, duplicações de registros e inconsistências quando o indivíduo altera sua função transitória (por exemplo, ao concluir uma bolsa ou finalizar um mandato de coordenação).

* **A Solução Adotada:**
  1. **Vínculo Institucional:** Representa o enquadramento formal e duradouro do indivíduo perante a universidade. Define as subclasses disjuntas da classe `:Pessoa`, tais como `:Docente` e `:Discente`.
  2. **Papéis e Atividades Transitórias:** Representados por meio de propriedades e relações de participação:
     * O docente tem a propriedade `:coordenaProjeto` ou `:participaDeProjeto`.
     * O discente participa de projetos como membro ou bolsista (`:participaDeProjeto`).
     * As funções de gestão, orientação e monitoria são modeladas como relações dinâmicas entre instâncias (`:orienta`, `:leciona`, `:membroDeGrupo`), preservando a estabilidade da identidade da pessoa.

---

## 2. Reutilização e Alinhamento com Vocabulários Padrão
Em conformidade com as boas práticas de Linked Open Data (W3C Best Practices for Publishing Linked Data), evitou-se a tentação de "reinventar a roda". Adotou-se o princípio da **especialização e alinhamento**:

1. **FOAF (*Friend of a Friend*):**
   * A classe `:Pessoa` foi definida como subclasse de `foaf:Person`.
   * A classe `:Projeto` alinha-se com `foaf:Project`.
   * A propriedade de correio eletrônico institucional herda semântica de `foaf:mbox`.

2. **Schema.org:**
   * Utilizado massivamente para garantir interoperabilidade direta com robôs de busca da Web moderna.
   * `:Pessoa` alinha-se a `schema:Person`.
   * `:Docente` e `:Discente` são instâncias de `schema:Person` associadas a `schema:CollegeOrUniversity` via `schema:affiliation` e `schema:alumniOf`.
   * `:UnidadeAcademica` especializa `schema:Organization`.
   * `:Disciplina` e `:Curso` alinham-se a `schema:Course`.
   * `:Publicacao` especializa `schema:ScholarlyArticle`.

3. **SKOS (*Simple Knowledge Organization System*):**
   * As **Áreas de Pesquisa e Interesses** foram modeladas como conceitos SKOS (`skos:Concept`).
   * Foram empregados rótulos preferenciais multilingues (`skos:prefLabel` em `@pt` e `@en`), termos alternativos (`skos:altLabel`) e relações de equivalência conceitual (`skos:exactMatch` e `skos:closeMatch`) apontando para identificadores semânticos da Wikidata e DBpedia.

4. **Dublin Core Metadata Terms (DCMI Terms):**
   * Empregado para metadados bibliográficos e descritivos: `dcterms:title`, `dcterms:description`, `dcterms:license`, `dcterms:created`, `dcterms:modified` e `dcterms:publisher`.

---

## 3. Estratégia de Identificação por URIs e Namespaces
Foram estabelecidos dois esquemas de namespace HTTP claros e ortogonais:

* **Namespace de Ontologia (T-Box - Terminologia):**
  `http://dados.ufrrj.br/ontologia/` (prefixo `:` padrão)
  Abriga os conceitos abstratos, classes, *Object Properties* e *Datatype Properties*.

* **Namespace de Recursos e Instâncias (A-Box - Asserções):**
  `http://dados.ufrrj.br/recurso/` (prefixo `ufrrj:`)
  Abriga as entidades do mundo real:
  * Docentes: `http://dados.ufrrj.br/recurso/docente_ana_silva`
  * Discentes: `http://dados.ufrrj.br/recurso/discente_joao_pereira`
  * Unidades: `http://dados.ufrrj.br/recurso/InstitutoCienciasExatas`
  * Departamentos: `http://dados.ufrrj.br/recurso/DeptoComputacao`
  * Cursos: `http://dados.ufrrj.br/recurso/CursoSistemasInformacao`
  * Projetos: `http://dados.ufrrj.br/recurso/ProjetoDadosAbertos`
  * Publicações: `http://dados.ufrrj.br/recurso/Pub2024DadosConectados`

Essa separação facilita a resolução de dereferenciabilidade, a modularização e a publicação federada.

---

## 4. Uso Cauteloso e Semanticamente Correto de `owl:sameAs`
Conforme advertido expressamente nas instruções da disciplina:
> *"Não utilizar `owl:sameAs` como sinônimo genérico de associação: essa propriedade expressa identidade entre recursos."*

Adotou-se o seguinte rigor semântico:
* **Uso Legítimo de `owl:sameAs`:**
  Utilizado **exclusivamente** quando o recurso local e o recurso externo representam rigorosamente a mesma entidade no mundo real.
  * `ufrrj:UFRRJ owl:sameAs <http://dbpedia.org/resource/Federal_Rural_University_of_Rio_de_Janeiro>` (Ambos denotam a mesmíssima pessoa jurídica e campus da UFRRJ).
  * `ufrrj:Seropedica owl:sameAs <https://www.wikidata.org/wiki/Q1002058>` (Denotam exatamente o mesmo município fluminense).

* **Uso de Vocabulários Específicos para Outras Associações:**
  * Para correlação entre pesquisadores e seus identificadores ORCID: utilizou-se `schema:sameAs` ou a propriedade específica `:linkOrcid`, evitando afirmar identidade estrita de grafo onde um recurso é uma página/registro de autoridade e outro é a pessoa física.
  * Para conceitos temáticos: utilizou-se `skos:exactMatch` e `skos:closeMatch` (por exemplo, ligando o conceito local de Web Semântica ao conceito Q54837 da Wikidata), o que expressa equivalência conceitual sem unificar de modo forçado ontologias distintas.
  * Para fontes de referência e documentação externa complementar: utilizou-se `rdfs:seeAlso`.

---

## 5. Modelagem das Relações Complexas para Suporte a SPARQL
Para garantir que as **6 perguntas de competência** pudessem ser respondidas de forma limpa, direta e com alto desempenho, foram concebidas relações n-árias e bidirecionais quando relevante:

1. **Coautoria de Publicações:**
   A publicação `:Publicacao` possui múltiplas asserções `:temAutor`, associando tanto docentes quanto discentes. A propriedade inversa `:autorDe` permite a navegação bidirecional. Na consulta SPARQL 05, o filtro `FILTER (?coautor != ?docente)` isola os colaboradores sem auto-associação.
2. **Participação Compartilhada em Projetos:**
   Docentes coordenadores e membros participantes convergem para a propriedade genérica `:participaDeProjeto` (da qual `:coordenaProjeto` é subpropriedade). Assim, consultas que cruzam docentes e alunos vinculados ao mesmo projeto (Consulta 04) operam diretamente sobre o mesmo recurso `:Projeto`.
3. **Pertencimento Institucional Unificado:**
   Tanto docentes quanto discentes declaram a propriedade `:pertenceA ufrrj:InstitutoCienciasExatas`. Os docentes refinam essa relação com `:lotadoEm ufrrj:DeptoComputacao`, enquanto discentes utilizam `:matriculadoEm ufrrj:CursoSistemasInformacao`. Como o Departamento e o Curso declaram `:vinculadoAInstituto ufrrj:InstitutoCienciasExatas`, consultas como a Pergunta 06 recuperam todas as pessoas da unidade com máxima expressividade.
