<<<<<<< HEAD
# 📊 CNPJ Organizer API — Data Pipeline para Leads B2B

Pipeline em Python para **coleta, limpeza, normalização e geração de leads B2B** a partir de CNPJs públicos.

Projeto focado em **engenharia de dados aplicada**, automação e preparação de dados para uso comercial e analítico.

---

## 🚀 Objetivo do Projeto

Transformar dados brutos de CNPJ em **listas limpas e segmentadas de empresas**, prontas para:

- Prospecção B2B
- Análise de mercado
- Segmentação por CNAE
- Integração com CRM
- Produtos de dados

---

## 🧠 O que este projeto demonstra

- Consumo de API pública
- Validação de dados
- Manipulação de JSON complexo
- Limpeza e normalização de dados
- Engenharia de dados com Pandas
- Boas práticas de projeto Python

---

## 📁 Estrutura do Projeto

CnpjOganizerAPI/
├── data_raw/ # Dados de entrada (ignorado no Git)
├── data_processed/ # Dados gerados (ignorado no Git)
├── src/ # Código principal
│ ├── clean_final_csv.py
│ └── normalize_cnae.py
├── scripts/ # Scripts auxiliares
├── README.md
├── requirements.txt
└── .gitignore


---

## 🔧 Tecnologias Utilizadas

- Python 3.11
- Pandas
- Requests
- APIs públicas de CNPJ
- Git & GitHub

---

## ▶️ Como executar

1️⃣ Criar ambiente virtual
bash
python -m venv .venv
source .venv/bin/activate

2️⃣ Instalar dependências
pip install -r requirements.txt

3️⃣ Executar o pipeline
python src/clean_final_csv.py
python src/normalize_cnae.py


Os arquivos finais serão gerados localmente no diretório data_processed/.

📌 Observações Importantes

Dados sensíveis não são versionados

Os CSVs gerados servem apenas como exemplo local

Projeto com foco educacional, técnico e demonstrativo

Ideal para mostrar domínio em engenharia de dados Python

👤 Autor

Mário Júnior
Desenvolvedor Python | IA | Engenharia de Dados

🔗 LinkedIn:
https://www.linkedin.com/in/juniormvs
=======
# CnpjOganizerAPI
>>>>>>> 89cecc73b4470943b64884ed71983fcd19fa7a41
