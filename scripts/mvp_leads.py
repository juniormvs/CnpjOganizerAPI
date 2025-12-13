import pandas as pd
import os

# Caminhos
INPUT = "data_processed/empresas_api_clean.csv"
OUTPUT = "data_processed/leads_b2b.csv"

print("📥 Lendo base limpa...")
df = pd.read_csv(INPUT)

print("🔎 Filtrando empresas ATIVAS...")
df = df[df["situacao"] == "Ativa"]

print("📞 Mantendo empresas com telefone ou email...")
df = df[
    (df["telefone"].notna() & (df["telefone"] != "")) |
    (df["email"].notna() & (df["email"] != ""))
]

print("🧱 Selecionando colunas comerciais...")
cols = [
    "cnpj",
    "razao_social",
    "nome_fantasia",
    "municipio",
    "uf",
    "telefone",
    "email",
    "situacao",
    "cnae_fiscal"
]

df_final = df[cols]

print("💾 Salvando leads comerciais...")
df_final.to_csv(OUTPUT, index=False)

print(f"✅ MVP GERADO: {OUTPUT}")
print(f"📊 Total de leads: {len(df_final)}")
