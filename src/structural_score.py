import pandas as pd


def apply_structural_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica score estrutural baseado no completeness_score.
    """

    def score_rule(completeness):
        if completeness >= 0.9:
            return 100
        elif completeness >= 0.75:
            return 80
        elif completeness >= 0.6:
            return 60
        else:
            return 20

    df["structural_score"] = df["completeness_score"].apply(score_rule)

    return df
