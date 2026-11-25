# Sistema de Perfis Acadêmicos Conectados à Web Semântica e LOD
### Universidade Federal Rural do Rio de Janeiro (UFRRJ)
**Instituto de Ciências Exatas (ICE) — Departamento de Computação**  
**Disciplina:** Web Semântica e Linked Open Data  
**Docente:** Prof. Dr. Tiago Cruz de França  
**Discentes / Autores:** David Barros da Rosa Filho, Lucyan Ovídio da Silva Soares e Mariana Corrêa de Medeiros.  

* 🌐 **Endereço Público do Site (GitHub Pages):** [https://davib1405.github.io/trabalho-web-semantica/](https://davib1405.github.io/trabalho-web-semantica/)
* 📦 **Repositório Oficial no GitHub:** [https://github.com/davib1405/trabalho-web-semantica](https://github.com/davib1405/trabalho-web-semantica)
* 🔍 **Consultas SPARQL Interativas Online:** [https://davib1405.github.io/trabalho-web-semantica/consultas.html](https://davib1405.github.io/trabalho-web-semantica/consultas.html)
* 🕸️ **Grafo Semântico Interativo Online:** [https://davib1405.github.io/trabalho-web-semantica/grafo.html](https://davib1405.github.io/trabalho-web-semantica/grafo.html)  

---

## 1. Visão Geral do Projeto
Este projeto implementa uma solução completa e de nível profissional para a modelagem, estruturação, publicação e consulta semântica de perfis acadêmicos de docentes e discentes da UFRRJ.

O projeto transforma páginas universitárias convencionais em um **Grafo de Conhecimento Acadêmico (Knowledge Graph)** plenamente integrado aos padrões do W3C e ao ecossistema de **Linked Open Data (LOD)**, viabilizando buscas federadas, relacionamentos ricos de coautoria e projetos compartilhados, bem como consultas complexas em **SPARQL 1.1**.

---

## 2. Estrutura Completa do Repositório

O projeto segue com exatidão a estrutura recomendada no enunciado oficial da disciplina:

```text
trabalho_web_semantica/
├── README.md                           # Visão geral, instruções de reprodução e estrutura
├── declaracao-ia.md                    # Declaração ética e técnica do uso de IA (Item 9)
├── proposta/                           # Documentos da concepção da proposta
│   ├── descricao.md                    # Objetivo, público-alvo, funcionalidades e dados
│   ├── requisitos.md                   # Requisitos funcionais, semânticos e não-funcionais
│   └── decisoes-modelagem.md           # Decisões de design, separação vínculo/papéis e LOD
├── documentacao/                       # Documentação técnica formal
│   ├── dicionario-dados.md             # Dicionário de dados, tipos, regras e cardinalidades
│   ├── vocabularios.md                 # Avaliação de vocabulários e justificativas LOD
│   ├── ontologia.md                    # Especificação formal da ontologia em OWL 2
│   ├── diagrama.md                     # Diagramas conceituais em Mermaid
│   └── diagrama.svg                    # Diagrama vetorial visual de classes e instâncias
├── ontologia/                          # Arquivos formais da ontologia e dados RDF
│   ├── ontologia.owl                   # Ontologia OWL 2 em sintaxe Turtle
│   ├── ontologia_rdfxml.owl            # Ontologia OWL 2 em formato RDF/XML (Protégé)
│   └── dados.ttl                       # Grafo de conhecimento com os dados e links LOD
├── consultas/                          # As 6 consultas SPARQL de competência
│   ├── consulta01.rq                   # Q1: Docentes e departamentos
│   ├── consulta02.rq                   # Q2: Discentes por curso
│   ├── consulta03.rq                   # Q3: Docentes por área temática
│   ├── consulta04.rq                   # Q4: Docentes e discentes no mesmo projeto
│   ├── consulta05.rq                   # Q5: Publicações de docente e coautores
│   ├── consulta06.rq                   # Q6: Pessoas vinculadas a unidade acadêmica
│   ├── resultados_consolidados.md      # Relatório consolidado com códigos e tabelas
│   └── resultados/                     # Resultados individuais em .txt e .csv
│       ├── resultado01.csv / .txt
│       ├── resultado02.csv / .txt
│       ├── resultado03.csv / .txt
│       ├── resultado04.csv / .txt
│       ├── resultado05.csv / .txt
│       └── resultado06.csv / .txt
├── codigo-fonte/                       # Código de automação em Python
│   ├── gerar_site.py                   # Gerador de páginas HTML a partir do RDF
│   ├── executar_consultas.py           # Executor automático das consultas SPARQL
│   └── dados_extraidos_rdf.json        # Exportação espelho dos dados do grafo
├── exemplos/perfis/                    # Exemplos e modelos de referência do professor
│   ├── docente_original.html
│   ├── discente_original.html
│   └── estilos.css
└── site/                               # Aplicação Web gerada pronta para publicação
    ├── index.html                      # Portal e diretório de perfis acadêmicos
    ├── estilos.css                     # Folha de estilos oficial
    ├── foto-exemplo.svg                # Avatar vetorial responsivo
    └── perfis/                         # Perfis dinâmicos individuais com JSON-LD
        ├── docente_ana_silva.html
        ├── docente_mariana_almeida.html
        ├── discente_joao_pereira.html
        └── discente_lucas_ferreira.html
```

---

## 3. Instruções Rápidas para Reproduzir a Demonstração

### Pré-requisitos
* Python 3.8+ instalado.
* Biblioteca `rdflib` instalada:
  ```bash
  pip install rdflib
  ```

### Passo 1: Executar e Validar as Consultas SPARQL
Para rodar todas as 6 consultas SPARQL contra o grafo RDF e gerar novamente os arquivos de resultado em CSV, TXT e Markdown:
```bash
python codigo-fonte/executar_consultas.py
```
*Saída esperada:* 6 consultas executadas com 100% de sucesso e salvamento em `consultas/resultados/`.

### Passo 2: Gerar Dinamicamente o Site a partir do Grafo RDF
Para demonstrar que o site é gerado programaticamente a partir da fonte de dados semântica (eliminando HTMLs manuais soltos):
```bash
python codigo-fonte/gerar_site.py
```
*Saída esperada:* Geração dos 4 perfis HTML individuais com **JSON-LD** e do portal principal `index.html`.

### Passo 3: Abrir e Navegar no Site Localmente
Basta abrir o arquivo `site/index.html` em qualquer navegador:
* No Windows via terminal:
  ```powershell
  Start-Process "site\index.html"
  ```
* Ou clicando duas vezes sobre `site/index.html` no gerenciador de arquivos.

---

## 4. As 6 Perguntas de Competência e Resultados SPARQL

| # | Pergunta em Linguagem Natural | Consulta | Entidades Cruzadas | Status |
| :-: | :--- | :--- | :--- | :-: |
| **Q1** | *Quais são os docentes cadastrados e seus departamentos?* | [`consulta01.rq`](consultas/consulta01.rq) | Docente $\rightarrow$ Departamento | ✅ Validado |
| **Q2** | *Quais discentes pertencem a determinado curso?* | [`consulta02.rq`](consultas/consulta02.rq) | Discente $\rightarrow$ Curso | ✅ Validado |
| **Q3** | *Quais docentes atuam em determinada área de pesquisa?* | [`consulta03.rq`](consultas/consulta03.rq) | Docente $\rightarrow$ Área (SKOS) | ✅ Validado |
| **Q4** | *Quais docentes e discentes participam do mesmo projeto?* | [`consulta04.rq`](consultas/consulta04.rq) | Docente $\times$ Discente $\times$ Projeto | ✅ Validado |
| **Q5** | *Quais publicações estão associadas a docente e quem são os coautores?* | [`consulta05.rq`](consultas/consulta05.rq) | Docente $\times$ Publicação $\times$ Coautor | ✅ Validado |
| **Q6** | *Quais pessoas estão vinculadas a uma unidade específica?* | [`consulta06.rq`](consultas/consulta06.rq) | Pessoa (Docente/Discente) $\times$ Instituto | ✅ Validado |

Consulte o documento [`consultas/resultados_consolidados.md`](consultas/resultados_consolidados.md) para conferir todas as tabelas detalhadas e explicações semânticas.

---

## 5. Integração com a Web de Dados Abertos (Linked Open Data - LOD)

O grafo conecta-se a bases globais canônicas com justificativas semânticas explícitas:

1. **UFRRJ (Instituição):**
   * URI: `http://dados.ufrrj.br/recurso/UFRRJ`
   * `rdfs:seeAlso <https://www.wikidata.org/wiki/Q3550293>` (Wikidata)
   * `owl:sameAs <http://dbpedia.org/resource/Federal_Rural_University_of_Rio_de_Janeiro>` (DBpedia)
2. **Seropédica (Localização institucional):**
   * URI: `http://dados.ufrrj.br/recurso/Seropedica`
   * `owl:sameAs <https://www.wikidata.org/wiki/Q1002058>` (Wikidata)
   * `rdfs:seeAlso <http://dbpedia.org/resource/Serop%C3%A9dica>` (DBpedia)
3. **Áreas Temáticas de Conhecimento (SKOS):**
   * Web Semântica: `skos:exactMatch <https://www.wikidata.org/wiki/Q54837>`
   * Inteligência Artificial: `skos:exactMatch <https://www.wikidata.org/wiki/Q11660>`
   * Dados Abertos: `skos:exactMatch <https://www.wikidata.org/wiki/Q309903>`
4. **Desambiguação de Autoria dos Pesquisadores:**
   * Profa. Dra. Ana Silva: `schema:sameAs <https://orcid.org/0000-0002-1825-0097>`
   * Profa. Dra. Mariana Almeida: `schema:sameAs <https://orcid.org/0000-0001-5000-0000>`

---

## 6. Publicação no GitHub Pages
O conteúdo do diretório `site/` está pronto para publicação estática gratuita no **GitHub Pages**:
1. Criar repositório público no GitHub.
2. Fazer push de todos os arquivos.
3. Em *Settings > Pages*, selecionar a branch `main` e a pasta `/site` (ou renomear `site/` para `docs/`).
4. O portal ficará online publicamente no endereço `https://<usuario>.github.io/<repositorio>/`.

---

## 7. Licenciamento e Direitos
* **Licença dos Dados:** [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
* **Data da Versão:** 21 de Novembro de 2026.
* **Uso de IA:** Totalmente discriminado e auditado em [`declaracao-ia.md`](declaracao-ia.md).
