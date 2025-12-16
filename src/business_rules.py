import pandas as pd


def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica regras simples de negócio para leads B2B.
    """

    def is_commercially_valid(row):
        has_contact = (
            pd.notna(row.get("telefone")) and str(row.get("telefone")).strip() != ""
        ) or (
            pd.notna(row.get("email")) and str(row.get("email")).strip() != ""
        )

        is_active = str(row.get("situacao")).upper() == "ATIVA"

        return has_contact and is_active

    df["is_valid_business"] = df.apply(is_commercially_valid, axis=1)

    return df
