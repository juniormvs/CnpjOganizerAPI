#!/usr/bin/env python3
"""
plots.py
- Gera gráficos simples a partir de data_processed/empresas_api_clean_norm.csv
- Produz:
    - data_processed/top_ufs.png
    - data_processed/situacao_pie.png
    - data_processed/top_cnaes.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

IN_PATH = os.path.join("data_processed", "empresas_api_clean_norm.csv")
OUT_DIR = "data_processed"

def safe_plot_bar(series, title, out_file, xlabel=None, ylabel="count"):
    ax = series.plot.bar(figsize=(8,4))
    ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.figure.tight_layout()
    ax.figure.savefig(out_file)
    print("Salvo:", out_file)
    plt.close(ax.figure)

def main():
    if not os.path.exists(IN_PATH):
        raise SystemExit(f"Arquivo não encontrado: {IN_PATH}")

    df = pd.read_csv(IN_PATH, dtype=str)

    # Top UFs
    if "uf_norm" in df.columns:
        top_ufs = df["uf_norm"].fillna("N/A").value_counts().head(20)
        safe_plot_bar(top_ufs, "Top UFs", os.path.join(OUT_DIR, "top_ufs.png"), xlabel="UF")

    # Situação (pie)
    if "situacao" in df.columns:
        situ = df["situacao"].fillna("N/A").value_counts()
        ax = situ.plot.pie(autopct="%1.1f%%", figsize=(6,6), title="Distribuição por situação")
        ax.figure.tight_layout()
        ax.figure.savefig(os.path.join(OUT_DIR, "situacao_pie.png"))
        print("Salvo:", os.path.join(OUT_DIR, "situacao_pie.png"))
        plt.close(ax.figure)

    # Top CNAEs
    if "cnae_fiscal" in df.columns:
        top_cnaes = df["cnae_fiscal"].fillna("N/A").value_counts().head(20)
        safe_plot_bar(top_cnaes, "Top CNAEs", os.path.join(OUT_DIR, "top_cnaes.png"), xlabel="CNAE")
    else:
        print("Coluna cnae_fiscal não encontrada - pulando gráfico de CNAE.")

if __name__ == "__main__":
    main()
