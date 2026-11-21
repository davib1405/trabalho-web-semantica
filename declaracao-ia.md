# Declaração do Uso de Ferramentas de Inteligência Artificial

Em estrito cumprimento ao **Item 9** das diretrizes da disciplina de Web Semântica e Linked Open Data (Prof. Dr. Tiago Cruz de França - UFRRJ), este documento formaliza de maneira transparente, ética e verificável a utilização de ferramentas de Inteligência Artificial generativa no desenvolvimento do presente trabalho acadêmico.

---

## 1. Ferramentas Utilizadas e Finalidades

| Ferramenta de IA | Modelo / Versão | Finalidade Específica no Projeto |
| :--- | :--- | :--- |
| **Antigravity (Google DeepMind)** | Gemini 3.8 Flash (High) | Automação na estruturação do repositório, apoio na redação de scripts em Python (`rdflib`), validação sintática das consultas SPARQL e estruturação das marcações JSON-LD. |
| **Python rdflib Automation** | rdflib v7.6.0 | Mecanismo determinístico local utilizado para carregar a ontologia, executar o parser e rodar as 6 consultas SPARQL contra o grafo real, garantindo ausência de alucinações. |

---

## 2. Síntese dos Prompts e Pedidos Relevantes

A interação com o assistente inteligente foi conduzida com foco na engenharia de conhecimento, consistência semântica e atendimento aos critérios de avaliação da universidade:

1. **Prompt de Modelagem Ontológica:**
   > *"Com base no documento conceitual prévio sobre perfis universitários na UFRRJ, estruture uma ontologia formal em OWL/Turtle contendo as classes `:Docente`, `:Discente`, `:UnidadeAcademica`, `:Curso`, `:Projeto` e `:Publicacao`. Garanta alinhamento formal com FOAF, Schema.org e SKOS, evitando a explosão de classes e diferenciando vínculo institucional de papéis transitórios."*

2. **Prompt de Consultas SPARQL 1.1:**
   > *"Elabore e valide as 6 consultas SPARQL obrigatórias para responder exatamente às 6 perguntas de competência institucional do enunciado. Assegure que as consultas explorem relações entre entidades distintas (coautoria, participação conjunta em projetos e hierarquia organizacional) e exporte os resultados para validação."*

3. **Prompt de Geração Dinâmica da Aplicação Web:**
   > *"Crie um script em Python que conecte ao grafo RDF via `rdflib`, extraia dinamicamente os 4 perfis acadêmicos (2 docentes e 2 discentes) e renderize as páginas HTML utilizando a estrutura e o arquivo `estilos.css` fornecidos pelo professor. Embuta dados estruturados em JSON-LD em cada perfil."*

---

## 3. Partes Geradas ou Modificadas com Auxílio de IA

1. **Scripts de Automação:**
   * `codigo-fonte/gerar_site.py`: Script gerador do portal e das páginas de perfil a partir do grafo RDF.
   * `codigo-fonte/executar_consultas.py`: Script automatizado para execução das consultas SPARQL e geração dos relatórios tabulares.
2. **Serializações Semânticas:**
   * Arquivo de ontologia canônica (`ontologia/ontologia.owl`).
   * Arquivo de dados de instâncias (`ontologia/dados.ttl`).
3. **Estrutura das Consultas:**
   * Consultas SPARQL 1 a 6 (`consultas/consulta01.rq` a `consulta06.rq`).
4. **Documentação Técnica:**
   * Dicionário de dados, especificações de vocabulários e diagrama conceitual.

---

## 4. Metodologia de Verificação e Validação Humana

Nenhum artefato gerado por IA foi aceito de forma cega. Adotou-se o seguinte protocolo de verificação:

1. **Validação Sintática Formal do RDF/OWL:**
   * O arquivo `dados.ttl` e `ontologia.owl` foram parseados em tempo de compilação pelo parser rigoroso do `rdflib` no Python 3.14, confirmando zero erros de sintaxe ou violação de prefixos.
2. **Validação das Consultas SPARQL:**
   * Todas as 6 consultas foram executadas diretamente contra o grafo em memória (`g.query()`). Verificou-se manualmente se cada resultado correspondia exatamente aos fatos do domínio acadêmico (ex: coautores corretos, alunos do curso de SI, projetos compartilhados).
3. **Auditoria de `owl:sameAs`:**
   * Foi realizada inspeção minuciosa para garantir que `owl:sameAs` foi empregado estritamente para entidades de mesma identidade física/jurídica (UFRRJ e Seropédica), utilizando `skos:exactMatch` para conceitos temáticos e `schema:sameAs` para identificadores ORCID.
4. **Validação da Camada Web:**
   * As páginas HTML geradas foram abertas e inspecionadas em navegadores modernos, assegurando que o layout responsivo, imagens SVG e fontes de estilos CSS funcionam sem falhas.

---

## 5. Declaração de Domínio dos Integrantes

Os integrantes declaram pleno domínio sobre os conceitos de Web Semântica envolvidos (triplas RDF, URIs, ontologias OWL, vocabulários controlados, namespaces, SPARQL 1.1 e Linked Open Data), estando inteiramente aptos a defender oralmente as decisões de projeto, explicar qualquer trecho de código ou modificar o modelo e consultas durante a arguição com o professor.
