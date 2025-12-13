import pandas as pd
import ast
import re

INPUT = "data_processed/leads_b2b.csv"
OUTPUT = "data_processed/leads_b2b_clean.csv"

# ===============================
# 1. Carregar dados
# ===============================
df = pd.read_csv(INPUT)

print(f"Registros iniciais: {len(df)}")
print("Colunas:", df.columns.tolist())

# ===============================
# 2. Funções auxiliares
# ===============================

def extract_nome(value):
    """
    Extrai o campo 'nome' de strings que representam dicionários.
    Ex: "{'id': 19, 'nome': 'Rio de Janeiro'}" -> "Rio de Janeiro"
    """
    if pd.isna(value):
        return ""
    if isinstance(value, str) and value.startswith("{"):
        try:
            d = ast.literal_eval(value)
            return d.get("nome", "")
        except:
            return ""
    return value


def only_digits(value):
    """Remove tudo que não for número"""
    if pd.isna(value):
        return ""
    return re.sub(r"\D", "", str(value))


# ===============================
# 3. Limpezas por coluna
# ===============================

if "municipio" in df.columns:
    df["municipio"] = df["municipio"].apply(extract_nome)

if "uf" in df.columns:
    df["uf"] = df["uf"].apply(extract_nome)

if "telefone" in df.columns:
    df["telefone"] = df["telefone"].apply(only_digits)

if "cnpj" in df.columns:
    df["cnpj"] = df["cnpj"].apply(only_digits)

# ===============================
# 4. Regras de negócio
# ===============================

if "situacao" in df.columns:
    df = df[df["situacao"] == "Ativa"]

# ===============================
# 5. Remover duplicados
# ===============================

if "cnpj" in df.columns:
    df = df.drop_duplicates(subset=["cnpj"])

print(f"Registros finais: {len(df)}")

# ===============================
# 6. Seleção final de colunas
# ===============================

final_columns = [
    "cnpj",
    "razao_social",
    "nome_fantasia",
    "municipio",
    "uf",
    "telefone",
    "email",
    "cnae_fiscal"
]

df = df[final_columns]

# ===============================
# 7. Salvar CSV limpo
# ===============================

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
print(f"CSV FINAL GERADO: {OUTPUT}")
