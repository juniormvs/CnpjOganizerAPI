import pandas as pd


def classify_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classifica leads com base no structural_score.
    """

    def classify(score):
        if score == 100:
            return "PRIORITÁRIO"
        elif score == 80:
            return "BOM"
        elif score == 60:
            return "MÉDIO"
        elif score == 20:
            return "DESCARTAR"
        else:
            return "INDEFINIDO"

    df["lead_classification"] = df["structural_score"].apply(classify)

    return df
