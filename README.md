# 🏢 CnpjOrganizerAPI

Pipeline em Python para **coleta, organização, limpeza, normalização e geração de leads B2B** a partir de dados de CNPJ.

Projeto focado em **engenharia de dados**, **tratamento de JSON**, **uso de APIs**, **Pandas** e **produtização de dados**, ideal para portfólio profissional.



## 🎯 Objetivo do Projeto

Construir um fluxo completo que:

- Consulta dados de empresas via API pública
- Processa respostas complexas em JSON
- Organiza dados em CSV
- Normaliza informações estratégicas (CNAE)
- Gera um **arquivo final pronto para prospecção B2B**


## 🧱 Estrutura do Projeto

```
CnpjOrganizerAPI/
├── data_raw/
│   └── (arquivos de entrada com CNPJs)
│
├── data_processed/
│   ├── empresas_api.csv
│   ├── empresas_api_clean.csv
│   ├── empresas_api_raw.jsonl
│   ├── leads_b2b.csv
│   └── leads_b2b_final.csv
│
├── scripts/
│   ├── inspect.py
│   └── plots.py
│
├── src/
│   ├── fetch_api.py
│   ├── clean_final_csv.py
│   └── normalize_cnae.py
│
├── requirements.txt
├── README.md
└── .gitignore
```


## ⚙️ Tecnologias Utilizadas



- Python 3.11
- Pandas
- Requests
- Matplotlib
- CSV / JSONL
- Git e GitHub

##  🔄 Pipeline de Dados
### 1️⃣ Coleta de Dados via API


```
thon src/fetch_api.py

```
O script:

- Lê CNPJs da pasta data_raw
- Consulta uma API pública
- Salva os dados em:
  - CSV estruturado
  - JSONL bruto para auditoria

### 2️⃣ Inspeção e Análise Rápida
```
thon scripts/inspect.py

```
Gera:

- KPIs básicos
- Contagem de erros
- Distribuição por UF e município
- Amostra de sócios (quando disponível)

### 3️⃣ Limpeza e Geração de Leads
```
python src/clean_final_csv.py

```

Resultados:

- Padronização de telefone e email
- Remoção de registros inválidos
- Geração do arquivo leads_b2b.csv

### 4️⃣ Normalização de CNAE

```
python src/normalize_cnae.py

```

Transforma o campo cnae_fiscal (JSON) em colunas separadas:

- Código CNAE
- Descrição CNAE

Arquivo final gerado:

```
data_processed/leads_b2b_final.csv
```
## 📊 Exemplo de Colunas do Arquivo Final

```
cnpj
razao_social
nome_fantasia
municipio
uf
telefone
email
cnae_codigo
cnae_descricao

```
## 🧪 Como Abrir os Arquivos CSV
Recomendado:

- LibreOffice Calc
- Abrir pelo próprio programa (Arquivo → Abrir)
- Codificação: UTF-8
- Separador: vírgula (,)

## 🚀 Próximos Passos (Roadmap)

- Validação automática de e-mails
- Score de qualidade de leads
- Filtros por CNAE estratégico
- Exportação para CRM
- Interface Web (Streamlit)

## 👨‍💻 Autor

**Mário Junior**

Projeto desenvolvido como parte de evolução prática em:
- Engenharia de Dados
- Automação
- Inteligência Artificial aplicada a negócios

---

## Contato

Mario Junior  
Email: juniormvs@hotmail.com  
Telefone: (adicione aqui seu telefone)

LinkedIn: https://www.linkedin.com/in/juniormvs

---

## ⚠️ Aviso Legal

Projeto educacional e demonstrativo.
Os dados utilizados devem respeitar a legislacao vigente (LGPD).
