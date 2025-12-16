print("🚀 Iniciando pipeline OrganizadorCNPJs...\n")

from src.clean_final_csv import clean_final_csv
from src.validate_structural import validate_structural
from src.normalize_cnae import normalize_cnae

import pandas as pd



# ETAPA 1 — LIMPEZA ESTRUTURAL
print("🧹 Etapa 1: Limpeza estrutural")
clean_final_csv()
print("✅ Limpeza concluída\n")

# ENRIQUECIMENTO DE DADOS
from src.enrich_from_receita import enrich_from_receita

print("🧬 Etapa 2.5: Enriquecimento com dados da Receita Federal (mock)")

df = pd.read_csv("data_processed/leads_b2b_clean.csv")
df = enrich_from_receita(df)
df.to_csv("data_processed/leads_b2b_enriched.csv", index=False)


print("✅ Enriquecimento concluído\n")


# ETAPA 2 — VALIDAÇÃO ESTRUTURAL
print("🧪 Etapa 2: Validação estrutural")

INPUT = "data_processed/leads_b2b_enriched.csv"
OUTPUT = "data_processed/leads_b2b_structural_validated.csv"


df = pd.read_csv(INPUT)
df = validate_structural(df)
df.to_csv(OUTPUT, index=False)

from src.quality_metrics import generate_quality_metrics

#STRUCTURAL SCORE - PONTUAÇÃO ESTRUTUAL
from src.structural_score import apply_structural_score

print("📈 Etapa 4.1: Score estrutural")

df = apply_structural_score(df)

df.to_csv("data_processed/leads_b2b_scored.csv", index=False)

print("✅ Score estrutural aplicado\n")

#CLASSIFICAÇÃO DE LEAD - LEAD CLASSIFICATION
from src.lead_classification import classify_leads

print("🏷️ Etapa 4.2: Classificação do lead")

df = classify_leads(df)

df.to_csv("data_processed/leads_b2b_classified.csv", index=False)

print("✅ Leads classificados\n")


# MÉTRICAS DE QUALIDADE

print("📊 Etapa 2.3: Métricas de qualidade")

generate_quality_metrics(df)

valid_df = df[df["is_valid_structural"] == True]
invalid_df = df[df["is_valid_structural"] == False]

valid_df.to_csv("data_processed/leads_b2b_validos.csv", index=False)
invalid_df.to_csv("data_processed/leads_b2b_invalidos.csv", index=False)

print("📁 Arquivos válidos e inválidos gerados\n")


print("✅ Validação estrutural concluída\n")

from src.business_rules import apply_business_rules


# REGRAS DE NEGÓCIO
print("🏷️ Etapa 2.4: Regras de negócio")

df = apply_business_rules(df)

df[df["is_valid_business"] == True].to_csv(
    "data_processed/leads_b2b_business_valid.csv", index=False
)

print("✅ Regras de negócio aplicadas\n")


# ETAPA 3 — NORMALIZAÇÃO DE CNAE
print("🧩 Etapa 3: Normalização de CNAE")
normalize_cnae()
print("✅ Normalização concluída\n")

print("🎉 Pipeline finalizado com sucesso!")
