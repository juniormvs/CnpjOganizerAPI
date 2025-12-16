import pandas as pd


def enrich_with_defaults(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquecimento controlado (temporário) para simulação corporativa.
    """

    if "situacao" not in df.columns:
        df["situacao"] = "ATIVA"

    if "porte_empresa" not in df.columns:
        df["porte_empresa"] = "DESCONHECIDO"

    if "natureza_juridica" not in df.columns:
        df["natureza_juridica"] = "DESCONHECIDA"

    return df
