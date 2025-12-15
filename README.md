# 📊 OrganizadorCNPJs — Data Pipeline em Python para Validação de CNPJs

Pipeline em Python para **validação estrutural e qualidade de dados cadastrais de empresas (CNPJs)** em larga escala, baseado em regras determinísticas inspiradas em cenários corporativos reais.

O projeto faz a **coleta, limpeza, normalização e organização** de dados públicos de CNPJs, preparando-os para uso analítico, comercial ou integração com outros sistemas.

Projeto focado em **engenharia de dados aplicada**, análise de sistemas e boas práticas em Python.

---

## 🎯 Escopo atual

O projeto encontra-se na fase de **validação estrutural de dados**, com foco em garantir que os registros estejam corretamente formatados **antes da aplicação de regras de negócio mais complexas**.

Nesta etapa, são aplicadas validações como:
- Formato do CNPJ (14 dígitos numéricos)
- Presença de campos obrigatórios
- Validação e padronização de datas
- Normalização de campos textuais
- Estrutura mínima para processamento em escala

---

## 🧠 Por que validar dados antes?

Em ambientes corporativos (bancos, ERPs, telecom, marketplaces B2B), dados inconsistentes geram:
- falhas de integração
- retrabalho operacional
- análises imprecisas
- riscos técnicos e de negócio

Este projeto simula a **primeira camada de qualidade de dados**, fundamental antes do consumo por sistemas críticos ou analíticos.

---

## 🧭 Roadmap

- [x] Estrutura inicial do projeto
- [x] Definição das regras estruturais
- [ ] Implementação completa das validações estruturais
- [ ] Regras cadastrais e de negócio
- [ ] Cruzamento e enriquecimento de dados
- [ ] Automação e relatórios
- [ ] (Futuro) Camada de IA generativa aplicada

---

## 🧠 O que este projeto demonstra

- Consumo de APIs públicas
- Validação e qualidade de dados
- Manipulação de JSON estruturado
- Limpeza e normalização com Pandas
- Organização de pipelines de dados
- Boas práticas em projetos Python

---

## 📁 Estrutura do Projeto



---

## 🗂️ Estrutura do Repositório

```text
OrganizadorCNPJs/
├── data_raw/ # Dados de entrada (ignorado no Git)
├── data_processed/ # Dados processados (ignorado no Git)
├── src/ # Módulos do pipeline
│ ├── clean_final_csv.py
│ └── normalize_cnae.py
├── run.py # Script principal de execução
├── requirements.txt
├── README.md
└── .gitignore
```

---


---

## 🔧 Tecnologias Utilizadas

- Python 3.11
- Pandas
- Requests
- APIs públicas de CNPJ
- Git & GitHub

---

## ▶️ Como executar (forma simplificada)

### 1️⃣ Criar e ativar ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

### 3. Executar Scripts - Old

```bash
python src/fetch_api.py          # coleta dados da API
python src/clean_final_csv.py    # gera leads_b2b.csv
python src/normalize_cnae.py     # gera leads_b2b_final.csv
```
### 4. Executar o pipeline completo

```bash
python run.py

```
O script run.py orquestra as etapas do pipeline e gera os arquivos processados no diretório data_processed/.

---

## 📌 Observações

Dados sensíveis não são versionados
Arquivos CSV servem apenas como exemplo local
Projeto com foco educacional, técnico e demonstrativo
Ideal para demonstrar fundamentos de engenharia de dados em Python

---

## 👤 Autor

**Mário Júnior**

Desenvolvedor Python | Engenharia de Dados | IA

Email: juniormvs@hotmail.com

Telefone: (+5518998037038)

LinkedIn: https://www.linkedin.com/in/juniormvs


---

## 📄 Licença / Aviso

Projeto para fins educacionais. Recomenda-se atender às leis de privacidade e LGPD ao usar dados sensíveis.
