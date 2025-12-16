import pandas as pd


def enrich_from_receita(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece dados de CNPJ usando mock da Receita Federal.
    """

    receita_df = pd.read_csv("data_raw/receita_mock.csv")

    # Normaliza CNPJ (14 dígitos)
    df["cnpj"] = (
        df["cnpj"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
        .str.zfill(14)
    )

    receita_df["cnpj"] = (
        receita_df["cnpj"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
        .str.zfill(14)
    )

    print(f"🔎 Registros antes do merge: {len(df)}")

    df = df.merge(
        receita_df,
        on="cnpj",
        how="left"
    )

    print(f"📊 Registros enriquecidos:")
    print(df[["cnpj", "situacao", "porte_empresa"]].head())

    return df
