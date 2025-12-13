# 📊 CnpjOrganizerAPI

Pipeline de Engenharia de Dados em Python para coleta, limpeza, normalização e geração de leads B2B a partir de dados públicos de CNPJ.

Projeto voltado para **engenharia de dados aplicada**, automação, transformação de dados e produção de artefatos para uso comercial e analítico.

---

## 📌 Visão Geral

Este projeto faz o seguinte:

- Consome uma API pública de CNPJ  
- Tratamento e validação de CNPJs  
- Normalização de campos em JSON complexo  
- Geração de CSVs limpos e prontos para análise  
- Geração de **leads B2B** (empresas ativas com telefone/email)  
- Normalização de CNAE (códigos e descrições)

Esse tipo de pipeline demonstra habilidades em Python, Pandas, APIs, transformação de dados e produção de resultados que agregam valor. :contentReference[oaicite:5]{index=5}

---

## 🗂️ Estrutura do Repositório

```text
CnpjOrganizerAPI/
├── data_raw/                # Dados de entrada (CNPJs puros)
├── data_processed/          # Arquivos gerados pelo pipeline
│   ├── empresas_api.csv
│   ├── empresas_api_clean.csv
│   ├── empresas_api_raw.jsonl
│   ├── leads_b2b.csv
│   └── leads_b2b_final.csv
├── scripts/                 # Scripts de inspeção e análise
│   ├── inspect.py
│   └── plots.py
├── src/                     # Código principal do pipeline
│   ├── fetch_api.py
│   ├── clean_final_csv.py
│   └── normalize_cnae.py
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação principal
└── .gitignore
```

---

## 🧰 Tecnologias Utilizadas

Este projeto foi construído com:

- Python 3.11  
- Pandas (manipulação de dados)  
- Requests (consumo de APIs)  
- CSV e JSONL (formatos de dados)  
- (Opcional) Matplotlib (para análise exploratória)  
- Git & GitHub  

---

## ⚡ Como Executar o Pipeline

### 1. Preparar Ambiente

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

### 3. Executar Scripts

```bash
python src/fetch_api.py          # coleta dados da API
python src/clean_final_csv.py    # gera leads_b2b.csv
python src/normalize_cnae.py     # gera leads_b2b_final.csv
```

---

## 📈 O Que Você Gera

Após execução, o arquivo principal de saída fica em:

```
data_processed/leads_b2b_final.csv
```

Esse arquivo contém colunas como:

- `cnpj`  
- `razao_social`  
- `nome_fantasia`  
- `municipio`  
- `uf`  
- `telefone`  
- `email`  
- `cnae_codigo`  
- `cnae_descricao`

Esses dados são úteis para prospecção, análises e integração com CRMs.

---

## 🧠 Competências Demonstradas

Este projeto mostra:

- Engenharia de Dados aplicados  
- Limpeza e transformação de dados reais  
- Integração com APIs públicas  
- Uso avançado de Pandas  
- Produção de artefatos reutilizáveis  
- Pipeline replicável e modular :contentReference[oaicite:6]{index=6}

---

## 🤝 Contato

**Mario Junior**  
Email: juniormvs@hotmail.com  
Telefone: (adicione aqui seu telefone)  
LinkedIn: https://www.linkedin.com/in/juniormvs

---

## 📄 Licença / Aviso

Projeto para fins educacionais. Recomenda-se atender às leis de privacidade e LGPD ao usar dados sensíveis.
