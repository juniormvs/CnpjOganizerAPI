import argparse
import pandas as pd
from pathlib import Path

# ---------------------------
# Funções de filtro
# ---------------------------

def filter_by_uf(df, uf):
    if uf:
        df = df[df["uf"].str.contains(uf, na=False)]
    return df


def filter_by_cnae(df, cnae):
    if cnae:
        df = df[df["cnae_fiscal"].str.contains(cnae, na=False)]
    return df


def filter_contact(df):
    return df[
        (df["telefone"].notna() & (df["telefone"] != "")) |
        (df["email"].notna() & (df["email"] != ""))
    ]


# ---------------------------
# Execução principal
# ---------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Filtro avançado de leads B2B a partir de CNPJs"
    )

    parser.add_argument(
        "--input",
        default="data_processed/leads_b2b_final.csv",
        help="CSV de entrada"
    )

    parser.add_argument(
        "--uf",
        help="Filtrar por UF (ex: SC, SP, RJ)"
    )

    parser.add_argument(
        "--cnae",
        help="Filtrar por CNAE (ex: 1412)"
    )

    parser.add_argument(
        "--only-contact",
        action="store_true",
        help="Apenas empresas com telefone ou email"
    )

    parser.add_argument(
        "--output",
        default="data_processed/leads_filtrados.csv",
        help="CSV de saída"
    )

    args = parser.parse_args()

    print("🔹 Lendo CSV...")
    df = pd.read_csv(args.input)
    print(f"🔹 Registros iniciais: {len(df)}")

    df = filter_by_uf(df, args.uf)
    df = filter_by_cnae(df, args.cnae)

    if args.only_contact:
        df = filter_contact(df)

    print(f"✅ Registros após filtros: {len(df)}")

    output_path = Path(args.output)
    df.to_csv(output_path, index=False)

    print(f"📁 Arquivo gerado: {output_path}")


if __name__ == "__main__":
    main()
