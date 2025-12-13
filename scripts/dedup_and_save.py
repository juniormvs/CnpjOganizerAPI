#!/usr/bin/env python3
"""
dedup_and_save.py
- Deduplica registros por CNPJ (mantém o primeiro encontrado)
- Gera arquivos deduplicados:
    - data_processed/empresas_api_dedup.csv
    - data_processed/empresas_api_clean_dedup.csv
"""

import os
import pandas as pd

IN_ALL = os.path.join("data_processed", "empresas_api.csv")
OUT_ALL = os.path.join("data_processed", "empresas_api_dedup.csv")
IN_CLEAN = os.path.join("data_processed", "empresas_api_clean.csv")
OUT_CLEAN = os.path.join("data_processed", "empresas_api_clean_dedup.csv")

def dedup_df(df, subset="cnpj"):
    """Remove duplicatas pelo subset (cnpj) mantendo a primeira ocorrência."""
    if subset in df.columns:
        return df.drop_duplicates(subset=[subset], keep="first")
    else:
        return df

def main():
    # dedup no CSV completo (se existir)
    if os.path.exists(IN_ALL):
        df_all = pd.read_csv(IN_ALL, dtype=str)
        print("Registros antes (all):", len(df_all))
        df_all_d = dedup_df(df_all, "cnpj")
        print("Registros depois (all):", len(df_all_d))
        df_all_d.to_csv(OUT_ALL, index=False)
        print("Salvo:", OUT_ALL)
    else:
        print("Arquivo não encontrado:", IN_ALL)

    # dedup no CSV enxuto
    if os.path.exists(IN_CLEAN):
        df_clean = pd.read_csv(IN_CLEAN, dtype=str)
        print("Registros antes (clean):", len(df_clean))
        df_clean_d = dedup_df(df_clean, "cnpj")
        print("Registros depois (clean):", len(df_clean_d))
        df_clean_d.to_csv(OUT_CLEAN, index=False)
        print("Salvo:", OUT_CLEAN)
    else:
        print("Arquivo não encontrado:", IN_CLEAN)

if __name__ == "__main__":
    main()
