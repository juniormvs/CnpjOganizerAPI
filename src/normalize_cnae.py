import pandas as pd
import ast
import os

INPUT = "data_processed/leads_b2b_clean.csv"
OUTPUT = "data_processed/leads_b2b_final.csv"


print("🔹 Lendo CSV...")
df = pd.read_csv(INPUT)

print("Colunas encontradas:")
print(df.columns.tolist())

print(f"🔹 Registros: {len(df)}")

# Colunas desejadas (ideal)
cols = [
    "cnpj",
    "razao_social",
    "nome_fantasia",
    "municipio",
    "uf",
    "situacao",      # pode não existir
    "telefone",
    "email",
    "cnae_fiscal"
]

# 🔑 FILTRO INTELIGENTE (só pega o que existe)
cols_existentes = [c for c in cols if c in df.columns]

print("Colunas usadas no processamento:")
print(cols_existentes)

df = df[cols_existentes]


# Salva CSV final
os.makedirs("data_processed", exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("✅ Arquivo final gerado:", OUTPUT)
