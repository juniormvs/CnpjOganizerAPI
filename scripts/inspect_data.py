#!/usr/bin/env python3
"""
scripts/inspect.py

Inspeciona os arquivos gerados pelo pipeline:
- data_processed/empresas_api.csv        (com raw_json)
- data_processed/empresas_api_clean.csv  (CSV enxuto)
- data_processed/empresas_api_raw.jsonl  (JSONL com brutos)

Gera um resumo (KPIs) e alguns extratos úteis: top UFs, top municípios, top CNAEs,
contagem de erros, proporção encontradas vs não encontradas, amostra de sócios, etc.

Uso:
    cd PythonDev/projetos/cnpj_organizer_api
    python -m venv venv          # se ainda não tiver venv
    source venv/bin/activate
    pip install -r requirements.txt
    python scripts/inspect.py --folder data_processed --top 10
"""

import os
import argparse
import json
from collections import Counter
import pandas as pd

def load_data(folder):
    csv_all = os.path.join(folder, "empresas_api.csv")
    csv_clean = os.path.join(folder, "empresas_api_clean.csv")
    jsonl = os.path.join(folder, "empresas_api_raw.jsonl")

    df_all = pd.read_csv(csv_all, dtype=str) if os.path.exists(csv_all) else pd.DataFrame()
    df_clean = pd.read_csv(csv_clean, dtype=str) if os.path.exists(csv_clean) else pd.DataFrame()

    jsonl_objs = []
    if os.path.exists(jsonl):
        with open(jsonl, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    jsonl_objs.append(json.loads(line))
                except Exception:
                    # skip malformed lines but keep count
                    jsonl_objs.append({"_raw": line})
    return df_all, df_clean, jsonl_objs

def kpis(df_all, df_clean, jsonl_objs):
    total_queries = len(df_all)
    valid_format = df_all["valid_format"].fillna("").astype(str).str.lower().isin(["true","1","yes"]).sum() if "valid_format" in df_all else 0
    errors = df_all["error"].fillna("no_error").value_counts().to_dict() if "error" in df_all else {}
    found = df_all["error"].fillna("").apply(lambda x: 0 if x in ("not_found","invalid_format","http_404","") and x in ("not_found","invalid_format","") else 1).sum() if "error" in df_all else 0
    # better: count where raw_json is not null
    found2 = df_all["raw_json"].notna().sum() if "raw_json" in df_all else 0

    print("=== KPIs ===")
    print("Total queries:", total_queries)
    print("Valid format (local validator):", valid_format)
    print("Found (raw_json present):", found2)
    try:
        pct_found = found2 / total_queries * 100 if total_queries > 0 else 0
    except Exception:
        pct_found = 0
    print(f"Percentual encontrado: {pct_found:.2f}%")
    print("Erros (top):")
    for k,v in list(errors.items())[:10]:
        print(f"  {k}: {v}")
    print()

def top_values(df_clean, column, top=10):
    if column not in df_clean.columns:
        print(f"Coluna '{column}' não existe no CSV enxuto.")
        return
    vc = df_clean[column].fillna("N/A").value_counts().head(top)
    print(f"Top {top} — {column}:")
    for idx, val in enumerate(vc.items(), start=1):
        k, v = val
        print(f"  {idx}. {k} — {v}")
    print()

def extract_socios_from_jsonl(jsonl_objs, max_samples=5):
    """
    Procura pela chave 'socios' ou 'sócios' ou 'socios' em objetos e imprime os primeiros nomes encontrados.
    """
    encontrados = []
    for obj in jsonl_objs:
        if not isinstance(obj, dict):
            continue
        # procura chaves possíveis
        socios = None
        for key in ("socios","sócios","socio","sócio"):
            if key in obj and isinstance(obj[key], list):
                socios = obj[key]
                break
        # procura em sub-objeto estabelecimento
        if socios is None and isinstance(obj.get("estabelecimento"), dict):
            est = obj.get("estabelecimento")
            if est is not None:
                for key in ("socios","sócios","socios"):
                    if key in est and isinstance(est[key], list):
                        socios = est[key]
                        break
        if socios:
            for s in socios:
                nome = s.get("nome") or s.get("nome_socio") or s.get("nome_representante") or s.get("nome_completo")
                cpf = s.get("cpf_cnpj_socio") or s.get("cpf") or s.get("cpf_cnpj")
                encontrados.append({"nome": nome, "cpf_cnpj": cpf})
        if len(encontrados) >= max_samples:
            break
    if not encontrados:
        print("Nenhum sócio identificado nos JSONs (ou estrutura diferente).")
        return
    print("Amostra de sócios extraídos (até max_samples):")
    for i, s in enumerate(encontrados[:max_samples], start=1):
        print(f"  {i}. {s.get('nome')} — {s.get('cpf_cnpj')}")
    print()

def summary_by_cnae(df_clean, top=10):
    if "cnae_fiscal" not in df_clean.columns:
        print("Coluna cnae_fiscal não encontrada no CSV enxuto.")
        return
    vc = df_clean["cnae_fiscal"].fillna("N/A").value_counts().head(top)
    print(f"Top {top} — CNAE fiscal:")
    for i, (k,v) in enumerate(vc.items(), start=1):
        print(f"  {i}. {k} — {v}")
    print()

def run(folder, top):
    df_all, df_clean, jsonl_objs = load_data(folder)
    if df_all.empty:
        print("Arquivo empresas_api.csv não encontrado ou vazio em", folder)
        return
    print(f"Arquivos carregados. Registros totais: {len(df_all)}")
    print()
    kpis(df_all, df_clean, jsonl_objs)

    # top UFs / Municípios / CNAE
    if not df_clean.empty:
        top_values(df_clean, "uf", top=top)
        top_values(df_clean, "municipio", top=top)
        summary_by_cnae(df_clean, top=top)
    else:
        print("CSV enxuto não encontrado — pulei top UFs/municípios/CNAE.")
        print()

    # erros e situações
    if "situacao" in df_all.columns:
        print("Distribuição de 'situacao':")
        print(df_all["situacao"].fillna("N/A").value_counts().head(top))
        print()

    # extrair sócios (amostra)
    extract_socios_from_jsonl(jsonl_objs, max_samples=10)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--folder", "-f", default="data_processed", help="Pasta com os arquivos gerados")
    p.add_argument("--top", type=int, default=10, help="Quantos top itens mostrar")
    args = p.parse_args()
    run(args.folder, args.top)
