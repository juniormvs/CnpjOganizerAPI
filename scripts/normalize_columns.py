#!/usr/bin/env python3
"""
normalize_columns.py
- Lê data_processed/empresas_api_clean.csv
- Converte colunas que contêm string-repr de dict (ex: "{'id':..., 'sigla':'RJ', ...}")
  em valores mais limpos:
    - uf_norm: sigla (ex: "RJ") ou texto original se falhar
    - municipio_norm: nome (ex: "Rio de Janeiro") ou texto original se falhar
- Salva novo CSV: data_processed/empresas_api_clean_norm.csv
"""

import ast
import json
import os
import pandas as pd

IN_PATH = os.path.join("data_processed", "empresas_api_clean.csv")
OUT_PATH = os.path.join("data_processed", "empresas_api_clean_norm.csv")

def parse_maybe_dict(s):
    """
    Recebe string possivelmente igual a "{'id': 3243, 'nome': 'Rio de Janeiro', ...}"
    ou JSON com aspas duplas.
    Retorna sigla/nome (quando for uf/municipio) ou string original se não conseguir parsear.
    """
    if pd.isna(s):
        return None
    s = str(s).strip()
    if not s:
        return None

    # tenta literal_eval para strings com aspas simples (representação Python)
    if s.startswith("{") and ("'" in s):
        try:
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                return d.get("sigla") or d.get("nome") or d.get("descricao") or str(d)
        except Exception:
            pass

    # tenta json.loads para strings com aspas duplas
    if s.startswith("{") and ('"' in s):
        try:
            d = json.loads(s)
            if isinstance(d, dict):
                return d.get("sigla") or d.get("nome") or d.get("descricao") or str(d)
        except Exception:
            pass

    # se não for dict, retorna a string original (possivelmente já está ok)
    return s

def main():
    if not os.path.exists(IN_PATH):
        raise SystemExit(f"Arquivo não encontrado: {IN_PATH}")

    df = pd.read_csv(IN_PATH, dtype=str)

    # aplica parse_maybe_dict nas colunas, só se existirem
    if "uf" in df.columns:
        df["uf_norm"] = df["uf"].apply(parse_maybe_dict)
    if "municipio" in df.columns:
        df["municipio_norm"] = df["municipio"].apply(parse_maybe_dict)

    # grava resultado
    df.to_csv(OUT_PATH, index=False)
    print("OK — salvo:", OUT_PATH)

if __name__ == "__main__":
    main()
