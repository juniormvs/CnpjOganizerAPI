# src/main.py
import os
import sys
import argparse
import json
import pandas as pd
from tqdm import tqdm

# garante imports funcionarem quando executado como script dentro da pasta src/
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from fetch_api import fetch_batch
from utils import only_digits, validate_cnpj

# --------------------------
# Leitura e limpeza da entrada
# --------------------------
def read_input_file(path):
    """
    Lê um arquivo texto com uma query por linha (CNPJ ou texto).
    Faz limpeza mínima: strip, remove aspas e vírgulas no final.
    Retorna lista de strings limpas.
    """
    cleaned = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            # remover aspas envolventes e vírgulas finais acidentais
            if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
                s = s[1:-1].strip()
            # remover vírgula final (ex: "27865757000102,")
            if s.endswith(","):
                s = s[:-1].strip()
            # remover espaços internos desnecessários
            s = s.strip()
            if s:
                cleaned.append(s)
    return cleaned

# --------------------------
# Função utilitária para extrair valores do JSON
# --------------------------
def safe_get(data: dict, *keys, default=None):
    """
    Tenta várias chaves no dicionário 'data'. Retorna o primeiro valor não-None.
    Também busca em sub-objetos comuns (ex: 'estabelecimento', 'empresa').
    """
    if not data:
        return default
    # busca direta
    for k in keys:
        if isinstance(data, dict) and k in data and data[k] not in (None, ""):
            return data[k]
    # busca em sub-objetos comuns
    for sub in ("estabelecimento", "estabelecimentos", "empresa", "data"):
        subobj = data.get(sub) if isinstance(data.get(sub), dict) else None
        if subobj:
            for k in keys:
                if k in subobj and subobj[k] not in (None, ""):
                    return subobj[k]
    return default

# --------------------------
# Transformação dos resultados em DataFrame
# --------------------------
def transform_results_to_df(results):
    """
    Transforma a lista de dicionários retornada por fetch_batch em um DataFrame pandas.
    - Mantém 'raw_json' com o JSON completo (string) para auditoria.
    - Tenta extrair campos comuns para colunas separadas.
    """
    rows = []
    for r in results:
        data = r.get("data") or {}
        base = {
            "query": r.get("query"),
            "cnpj": r.get("cnpj"),
            "valid_format": r.get("valid_format"),
            "error": r.get("error"),
            # salva o JSON original como string (evita perda de dados)
            "raw_json": json.dumps(data, ensure_ascii=False) if data else None,
        }

        # heurística para extrair campos com chaves diferentes dependendo da API
        base.update({
            "razao_social": safe_get(data, "razao_social", "nome", "nome_empresa", "nome_razao"),
            "nome_fantasia": safe_get(data, "nome_fantasia", "fantasia"),
            "municipio": safe_get(data, "municipio", "cidade"),
            "uf": safe_get(data, "uf", "estado"),
            "bairro": safe_get(data, "bairro"),
            "logradouro": safe_get(data, "logradouro", "rua"),
            "numero": safe_get(data, "numero", "nro"),
            "cep": safe_get(data, "cep"),
            "telefone": safe_get(data, "telefone", "telefone1", "telefone_principal"),
            "email": safe_get(data, "email"),
            "situacao": safe_get(data, "situacao", "situacao_cadastral", "status"),
            "cnae_fiscal": safe_get(data, "cnae_fiscal", "atividade_principal")
        })
        rows.append(base)
    df = pd.DataFrame(rows)
    return df

# --------------------------
# Função que cria CSV limpo e JSONL
# --------------------------
def save_clean_and_jsonl(df: pd.DataFrame, output_folder: str):
    """
    Recebe DataFrame (com coluna raw_json) e gera:
    - empresas_api_clean.csv: CSV enxuto com colunas selecionadas
    - empresas_api_raw.jsonl: cada linha é um JSON com o objeto original
    """
    os.makedirs(output_folder, exist_ok=True)
    # colunas úteis para CSV enxuto
    cols = ["query","cnpj","valid_format","error","razao_social","nome_fantasia","municipio","uf","bairro","logradouro","numero","cep","telefone","email","situacao","cnae_fiscal"]
    cols_existing = [c for c in cols if c in df.columns]
    clean_path = os.path.join(output_folder, "empresas_api_clean.csv")
    df[cols_existing].to_csv(clean_path, index=False)
    print("✔ Salvo CSV enxuto:", clean_path)

    # salvar JSONL com os raw_json (um JSON por linha)
    jsonl_path = os.path.join(output_folder, "empresas_api_raw.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as fout:
        for raw in df.get("raw_json", pd.Series()).dropna():
            try:
                # se raw já é string JSON, parse e re-dump para garantir formatação consistente
                obj = json.loads(raw)
                fout.write(json.dumps(obj, ensure_ascii=False))
                fout.write("\n")
            except Exception:
                # se falhar no parse, grava a string bruta para não perder informação
                fout.write(json.dumps({"raw": raw}, ensure_ascii=False))
                fout.write("\n")
    print("✔ Salvo JSONL com brutos:", jsonl_path)

# --------------------------
# MAIN
# --------------------------
def main(input_path, output_folder, max_workers, delay):
    os.makedirs(output_folder, exist_ok=True)
    print("📥 Lendo arquivo de entrada:", input_path)
    queries = read_input_file(input_path)
    if not queries:
        print("⚠️ Arquivo de entrada vazio.")
        return

    print(f"🔎 Iniciando buscas para {len(queries)} queries (max_workers={max_workers})")
    results = fetch_batch(queries, max_workers=max_workers, delay_between_requests=delay)

    print("🧰 Transformando resultados em DataFrame...")
    df = transform_results_to_df(results)

    # garantir cnpj com 14 dígitos (ou string vazia)
    if "cnpj" in df.columns:
        df["cnpj"] = df["cnpj"].fillna("").apply(lambda s: s if s == "" else str(s).zfill(14))

    csv_path = os.path.join(output_folder, "empresas_api.csv")
    parquet_path = os.path.join(output_folder, "empresas_api.parquet")

    print("💾 Salvando CSV e Parquet (com raw_json)...")
    df.to_csv(csv_path, index=False)
    try:
        df.to_parquet(parquet_path, index=False)
    except Exception as e:
        print("⚠️ Erro salvando parquet:", e)

    # salvar CSV enxuto e JSONL com brutos
    save_clean_and_jsonl(df, output_folder)

    print("✅ Pronto.")
    print("CSV completo:", csv_path)
    print("PARQUET:", parquet_path)
    print("CSV enxuto:", os.path.join(output_folder, "empresas_api_clean.csv"))
    print("JSONL bruto:", os.path.join(output_folder, "empresas_api_raw.jsonl"))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Organizador de Empresas via API - fetch CNPJs")
    p.add_argument("--input", "-i", default="../data_raw/sample_cnpjs.txt", help="Arquivo com CNPJs/queries por linha")
    p.add_argument("--output", "-o", default="../data_processed", help="Pasta de saída")
    p.add_argument("--workers", "-w", type=int, default=6, help="Número de threads paralelas")
    p.add_argument("--delay", "-d", type=float, default=0.05, help="Delay entre requisições (s)")
    args = p.parse_args()
    main(args.input, args.output, args.workers, args.delay)
