import pandas as pd

REQUIRED_FIELDS = [
    "cnpj",
    "razao_social",
    "municipio",
    "uf",
    "telefone",
    "email",
    "cnae_fiscal",
    "situacao",
    "porte_empresa",
    "data_inicio_atividade",
    "natureza_juridica"
    
]


def validate_structural(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica validação estrutural e gera métricas de qualidade.
    """

    validation_errors = []
    completeness_scores = []
    is_valid_list = []

    total_fields = len(REQUIRED_FIELDS)

    for _, row in df.iterrows():
        missing_fields = []

        for field in REQUIRED_FIELDS:
            if field not in df.columns or pd.isna(row.get(field)) or str(row.get(field)).strip() == "":
                missing_fields.append(field)

        valid_fields = total_fields - len(missing_fields)
        completeness = round(valid_fields / total_fields, 2)

        error_str = ", ".join(missing_fields) if missing_fields else "OK"
        validation_errors.append(error_str)

        completeness_scores.append(completeness)
        is_valid_list.append(completeness >= 0.7)

    df["validation_errors"] = validation_errors
    df["completeness_score"] = completeness_scores
    df["is_valid_structural"] = is_valid_list

    return df
