#!/usr/bin/env python3
"""
Script para execução e validação das 6 Consultas SPARQL
Trabalho de Web Semântica e Linked Open Data - UFRRJ
Autor: David Barros da Rosa Filho
"""

import os
import csv
import rdflib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONTOLOGIA_PATH = os.path.join(BASE_DIR, "ontologia", "ontologia.owl")
DADOS_PATH = os.path.join(BASE_DIR, "ontologia", "dados.ttl")
CONSULTAS_DIR = os.path.join(BASE_DIR, "consultas")
RESULTADOS_DIR = os.path.join(CONSULTAS_DIR, "resultados")

os.makedirs(RESULTADOS_DIR, exist_ok=True)

EXPLACOES = {
    1: """* **`:Docente` (Classe):** Subclasse de `:Pessoa` que restringe o escopo aos professores universitários.
* **`:lotadoEm` (Object Property):** Subpropriedade de `:pertenceA`. Liga cada docente ao seu departamento acadêmico de lotação.
* **`:nomeCompleto` (Datatype Property):** Retorna o nome civil e titulação do docente.
* **`rdfs:label` (Annotation Property):** Recupera a identificação legível do departamento.""",
    2: """* **`:Discente` (Classe):** Instâncias de alunos com vínculo de matrícula na universidade.
* **`:Curso` (Classe):** Especialização de `schema:Course` que modela a graduação ofertada.
* **`:matriculadoEm` (Object Property):** Subpropriedade de `:pertenceA`. Conecta o aluno ao curso.
* **`:anoIngresso` e `:periodoAtual` (Datatype Properties):** Literais que indicam o tempo e a fase acadêmica.
* **Cláusula `VALUES`:** Parametriza a consulta para filtrar qualquer curso desejado.""",
    3: """* **`:AreaPesquisa` / `skos:Concept` (Classe):** Modela áreas do conhecimento como conceitos de vocabulário controlado SKOS.
* **`:atuaEmArea` (Object Property):** Relaciona a pessoa às suas linhas de pesquisa ou interesses científicos.
* **`skos:prefLabel` (Annotation Property):** Rótulo preferencial em português (`FILTER (LANG(?nomeArea) = "pt")`).""",
    4: """* **Relação Tripartida de Entidades:** Conecta três classes distintas: `:Docente`, `:Discente` e `:Projeto`.
* **`:participaDeProjeto` (Object Property):** Propriedade que converge a atuação de docentes e alunos na mesma iniciativa científica. Como `:coordenaProjeto` é subpropriedade de `:participaDeProjeto`, a coordenação é inferida como participação direta.""",
    5: """* **`:Publicacao` (Classe):** Alinhada a `dcterms:BibliographicResource` e `schema:ScholarlyArticle`.
* **`:temAutor` (Object Property):** Relaciona o artefato científico a todas as pessoas autoras.
* **`FILTER (?coautor != ?docente)`:** Operador de negação de igualdade por URI para impedir auto-associação de coautoria.""",
    6: """* **Polimorfismo de `:Pessoa`:** Trata instâncias de `:Docente` e `:Discente` sob o mesmo padrão de grafo.
* **`:pertenceA` (Object Property):** Propriedade ancestral compartilhada na taxonomia institucional.
* **`FILTER (?tipoPessoa IN (:Docente, :Discente))`:** Filtra a instanciação direta para categorizar explicitamente o papel de cada pessoa encontrada no Instituto de Ciências Exatas (ICE)."""
}

def carregar_grafo():
    g = rdflib.Graph()
    print("[1/3] Carregando ontologia OWL...")
    g.parse(ONTOLOGIA_PATH, format="turtle")
    print(f"      Ontologia carregada: {len(g)} triplas.")
    print("[2/3] Carregando dados RDF/Turtle...")
    g.parse(DADOS_PATH, format="turtle")
    print(f"      Total de triplas no grafo integrado: {len(g)}.")
    return g

def executar_consultas(g):
    print("[3/3] Executando consultas SPARQL e gerando relatórios de resultados...")
    
    perguntas = {
        1: "Quais são os docentes cadastrados e seus respectivos departamentos ou unidades acadêmicas?",
        2: "Quais discentes pertencem a determinado curso?",
        3: "Quais docentes atuam em determinada área de pesquisa?",
        4: "Quais docentes e discentes participam de um mesmo projeto de pesquisa?",
        5: "Quais publicações estão associadas a determinado docente e quem são seus coautores?",
        6: "Quais pessoas estão vinculadas a uma unidade acadêmica específica, independentemente de serem docentes ou discentes?"
    }

    relatorio_geral = ["# Resultados Consolidados das Consultas SPARQL\n"]
    relatorio_geral.append("**Disciplina:** Web Semântica e Linked Open Data (UFRRJ)\n")
    relatorio_geral.append("**Autor:** David Barros da Rosa Filho\n")
    relatorio_geral.append(f"**Total de triplas avaliadas no grafo:** {len(g)}\n\n---\n")

    for i in range(1, 7):
        arquivo_rq = os.path.join(CONSULTAS_DIR, f"consulta0{i}.rq")
        if not os.path.exists(arquivo_rq):
            print(f"Aviso: {arquivo_rq} não encontrado.")
            continue
            
        with open(arquivo_rq, "r", encoding="utf-8") as f:
            sparql_query = f.read()

        resultado = g.query(sparql_query)
        variaveis = [str(v) for v in resultado.vars]
        linhas = []
        for row in resultado:
            linhas.append([str(row[v]) if row[v] is not None else "" for v in resultado.vars])

        # 1. Salvar em CSV
        csv_path = os.path.join(RESULTADOS_DIR, f"resultado0{i}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow(variaveis)
            writer.writerows(linhas)

        # 2. Salvar em TXT formatado
        txt_path = os.path.join(RESULTADOS_DIR, f"resultado0{i}.txt")
        with open(txt_path, "w", encoding="utf-8") as f_txt:
            f_txt.write(f"Consulta 0{i}: {perguntas[i]}\n")
            f_txt.write("=" * 80 + "\n\n")
            f_txt.write(sparql_query.strip() + "\n\n")
            f_txt.write("=" * 80 + "\n")
            f_txt.write(f"Total de registros retornados: {len(linhas)}\n")
            f_txt.write("-" * 80 + "\n")
            if linhas:
                col_widths = [max(len(v), max((len(r[idx]) for r in linhas), default=0)) for idx, v in enumerate(variaveis)]
                header_line = " | ".join(v.ljust(col_widths[idx]) for idx, v in enumerate(variaveis))
                sep_line = "-+-".join("-" * col_widths[idx] for idx in range(len(variaveis)))
                f_txt.write(header_line + "\n")
                f_txt.write(sep_line + "\n")
                for row_data in linhas:
                    f_txt.write(" | ".join(row_data[idx].ljust(col_widths[idx]) for idx in range(len(variaveis))) + "\n")
            else:
                f_txt.write("(Nenhum registro retornado)\n")

        # 3. Adicionar ao relatório consolidado em Markdown
        relatorio_geral.append(f"## Consulta 0{i}: {perguntas[i]}\n")
        relatorio_geral.append(f"**Arquivo da consulta:** [`consulta0{i}.rq`](../consulta0{i}.rq)\n")
        relatorio_geral.append("### Código SPARQL\n```sparql")
        relatorio_geral.append(sparql_query.strip())
        relatorio_geral.append("```\n")
        relatorio_geral.append(f"### Resultado Obtido ({len(linhas)} registros)\n")
        if linhas:
            md_header = "| " + " | ".join(variaveis) + " |"
            md_sep = "| " + " | ".join(["---"] * len(variaveis)) + " |"
            relatorio_geral.append(md_header)
            relatorio_geral.append(md_sep)
            for row_data in linhas:
                relatorio_geral.append("| " + " | ".join(val.replace("|", "/") for val in row_data) + " |")
        else:
            relatorio_geral.append("_Nenhum registro retornado._")
        
        relatorio_geral.append("\n### Explicação das Classes e Propriedades Utilizadas\n")
        relatorio_geral.append(EXPLACOES.get(i, ""))
        relatorio_geral.append("\n\n---\n")

        print(f" -> Consulta 0{i} concluída com sucesso ({len(linhas)} linhas geradas).")

    consolidado_path = os.path.join(CONSULTAS_DIR, "resultados_consolidados.md")
    with open(consolidado_path, "w", encoding="utf-8") as f_cons:
        f_cons.write("\n".join(relatorio_geral))
    print(f"\n[OK] Relatório consolidado gerado em: {consolidado_path}")

if __name__ == "__main__":
    grafo = carregar_grafo()
    executar_consultas(grafo)
