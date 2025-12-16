import pandas as pd


def generate_quality_metrics(df: pd.DataFrame):
    total = len(df)
    valid = df["is_valid_structural"].sum()
    invalid = total - valid

    print(f"📊 Total registros: {total}")
    print(f"✅ Válidos: {valid} ({round(valid / total * 100, 2)}%)")
    print(f"❌ Inválidos: {invalid} ({round(invalid / total * 100, 2)}%)\n")

    print("🔎 Top campos mais ausentes:")
    errors = df["validation_errors"].str.split(", ").explode()
    top_missing = errors.value_counts().head(5)

    print(top_missing)
