# Proposta do Sistema de Perfis Acadêmicos Conectados

## 1. Visão Geral e Contextualização
O presente projeto tem por finalidade o desenvolvimento dos artefatos conceituais, semânticos e computacionais necessários para integrar o diretório de páginas de perfis acadêmicos de docentes e discentes da **Universidade Federal Rural do Rio de Janeiro (UFRRJ)** à **Web Semântica** e ao movimento de **Linked Open Data (LOD)**.

Em sistemas institucionais convencionais, as páginas de membros da universidade costumam ser ilhas de informação isoladas em formato HTML textual, o que impede a interoperabilidade entre sistemas acadêmicos, dificulta buscas estruturadas por competências e impede que agentes de software interpretem relações ricas (tais como coautoria em artigos, participação conjunta em projetos de pesquisa e vinculação departamental).

Com a aplicação dos padrões estabelecidos pelo **World Wide Web Consortium (W3C)** — notadamente RDF (*Resource Description Framework*), OWL (*Web Ontology Language*), SKOS (*Simple Knowledge Organization System*) e a linguagem de consulta SPARQL —, os dados acadêmicos deixam de ser simples textos para se tornarem um **Grafo de Conhecimento Acadêmico**, navegável tanto por seres humanos quanto por algoritmos e sistemas federados.

---

## 2. Objetivo do Projeto
Modelar, estruturar, representar e publicar um catálogo demonstrativo de perfis de docentes e discentes, demonstrando:
1. **Modelagem Semântica Rigorosa:** Definição de ontologia de aplicação formal baseada na realidade acadêmica da UFRRJ.
2. **Reutilização de Vocabulários e Ontologias Padrão:** Adoção de Schema.org, FOAF (*Friend of a Friend*), Dublin Core Metadata Terms (DCMI) e SKOS.
3. **Interligação com o Ecossistema Global (LOD):** Vinculação dos recursos locais com entidades canônicas da **Wikidata**, **DBpedia** e identificadores de autores (**ORCID**).
4. **Geração Dinâmica de Páginas Web:** Eliminação de páginas estáticas desconectadas através de um gerador em Python acoplado diretamente ao grafo RDF.
5. **Comprovação de Competência Semântica:** Resposta automatizada às 6 perguntas de competência institucional via consultas SPARQL 1.1 validadas.

---

## 3. Público-Alvo
* **Comunidade Acadêmica da UFRRJ:** Discentes em busca de orientadores, linhas de pesquisa, grupos de estudo e projetos de iniciação científica; docentes buscando parceiros para pesquisas interdisciplinares.
* **Comunidade Científica Externa:** Pesquisadores de outras universidades nacionais e internacionais buscando especialistas em áreas temáticas como Web Semântica, Inteligência Artificial e Dados Abertos.
* **Mecanismos de Busca e Agentes Inteligentes:** Robôs de indexação (como Google Scholar, Bing e Wikidata bots) capazes de consumir metadados em JSON-LD e RDF para enriquecimento semântico.
* **Gestão Universitária:** Pró-Reitorias de Pesquisa e Pós-Graduação, Coordenações de Cursos e Diretorias de Instituto que necessitam de dados estruturados para relatórios e prestação de contas.

---

## 4. Tipos de Perfil Contemplados
A proposta contempla dois tipos principais de atores acadêmicos:

1. **Docente:**
   * Foco na produção científica, orientação acadêmica, disciplinas lecionadas, coordenação de projetos de pesquisa e vinculação departamental formal.
   * Instâncias implementadas:
     * *Profa. Dra. Ana Exemplo da Silva* (Professora Associada, Depto. de Computação / ICE)
     * *Profa. Dra. Mariana Almeida* (Professora Adjunta, Depto. de Computação / ICE)

2. **Discente:**
   * Foco na trajetória formativa, curso de graduação, período letivo, interesses acadêmicos, participação como bolsista/membro de projetos e produção inicial (artigos e trabalhos técnicos).
   * Instâncias implementadas:
     * *João Exemplo Pereira* (Graduando em Sistemas de Informação, ICE)
     * *Lucas Ferreira* (Graduando em Sistemas de Informação, ICE)

---

## 5. Justificativa das Informações Selecionadas
A seleção de atributos e relacionamentos observou o princípio da **relevância acadêmica** e da **privacidade**:

| Campo / Relação | Justificativa Acadêmica | Tratamento de Privacidade |
| :--- | :--- | :--- |
| **Nome Completo e Cargo** | Identificação pública primária do indivíduo na instituição. | Informação estritamente pública. |
| **Vínculo Institucional** | Distingue papéis formais e permanentes (docente efetivo, aluno) de atividades transitórias. | Público. |
| **Unidade / Curso / Depto.** | Ancora o indivíduo na estrutura organizacional universitária (ICE / Depto. de Computação). | Público institucional. |
| **Áreas de Atuação (SKOS)** | Facilita a indexação temática e a descoberta de especialistas por meio de termos controlados. | Público. |
| **Projetos de Pesquisa** | Evidencia as frentes ativas de geração de conhecimento e a colaboração docente-discente. | Público institucional. |
| **Publicações Acadêmicas** | Mede a difusão do conhecimento e explicita a rede de coautorias científicas. | Dados bibliográficos públicos. |
| **Identificadores (ORCID, Lattes)** | Promove a desambiguação internacional de autores e preserva a identidade persistente. | Links públicos autorizados. |
| **Dados Sensíveis (CPF, SIAPE, Matrícula)** | **Excluídos deliberadamente** do grafo público em conformidade com a LGPD e o enunciado da atividade. | Não publicados. |
