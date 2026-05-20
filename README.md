# etl-vendas-python

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2.3-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/status-concluido-2E8B57?style=for-the-badge)
![License](https://img.shields.io/badge/licen%C3%A7a-MIT-blue?style=for-the-badge)

Projeto de portfolio que implementa um pipeline ETL de vendas em Python. O pipeline le um arquivo CSV bruto, limpa e transforma os dados com pandas, calcula metricas de venda, registra logs de execucao e salva o resultado em formato Parquet.

## Objetivo

Demonstrar uma arquitetura simples e profissional para processamento de dados de vendas, cobrindo as principais etapas de um ETL:

- extracao de dados a partir de CSV;
- limpeza e padronizacao dos dados;
- tratamento de nulos e duplicatas;
- conversao de datas;
- criacao de colunas derivadas;
- carga dos dados processados em Parquet;
- registro de logs para auditoria da execucao.

## Arquitetura

```text
etl-vendas-python/
|-- data/
|   |-- raw/
|   |   |-- vendas_exemplo.csv
|   |-- processed/
|       |-- .gitkeep
|-- logs/
|   |-- .gitkeep
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- etl.py
|   |-- logger.py
|-- .gitignore
|-- README.md
|-- requirements.txt
```

## Diagrama Do Pipeline

```mermaid
flowchart LR
    A["CSV bruto<br/>data/raw/vendas_exemplo.csv"] --> B["Pipeline ETL<br/>src/etl.py"]
    B --> C["Limpeza e transformacao<br/>pandas"]
    C --> D["Parquet processado<br/>data/processed/vendas_processadas.parquet"]
    B --> E["Logs de execucao<br/>logs/etl_vendas.log"]
```

## Tecnologias Usadas

- Python 3.10+
- pandas
- pyarrow
- pathlib
- logging

## Skills Demonstradas

- ETL
- Data Cleaning
- Pandas
- Parquet
- Logging
- Estruturacao de Projeto
- Manipulacao de Dados
- Pipeline de Dados

## Como Instalar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependencias:

```bash
python -m pip install -r requirements.txt
```

## Como Rodar O ETL

Execute com os caminhos padrao:

```bash
python -m src.etl
```

No Windows, se o comando `python` nao estiver disponivel, use o launcher:

```bash
py -m src.etl
```

Ou informe entrada, saida e log explicitamente:

```bash
python -m src.etl --input data/raw/vendas_exemplo.csv --output data/processed/vendas_processadas.parquet --log-file logs/etl_vendas.log
```

Tambem e possivel executar o arquivo diretamente:

```bash
python src/etl.py
```

## Exemplo De Entrada

Arquivo: `data/raw/vendas_exemplo.csv`

```csv
ID Venda,Data Venda,Cliente,Produto,Quantidade,Preco Unitario,Desconto
1001,01/05/2026,Ana Silva,Notebook,1,3500.00,150.00
1002,02/05/2026,Bruno Costa,Mouse,2,80.50,0
1003,03/05/2026,Carla Lima,Teclado,1,230.90,10.90
```

## Exemplo De Saida

Arquivo: `data/processed/vendas_processadas.parquet`

Colunas esperadas apos o processamento:

```text
id_venda
data_venda
cliente
produto
quantidade
preco_unitario
desconto
valor_total
data_processamento
```

Exemplo de regra aplicada:

```text
valor_total = quantidade * preco_unitario - desconto
```

## Logs

Os logs sao gerados em:

```text
logs/etl_vendas.log
```

Eles registram inicio e fim do pipeline, quantidade de linhas lidas, colunas padronizadas, duplicatas removidas, datas invalidas descartadas e exportacao do Parquet.

## Proximos Passos

- Adicionar testes automatizados com pytest.
- Criar validacoes de qualidade de dados.
- Separar transformacoes em modulos menores.
- Adicionar suporte a multiplos arquivos CSV.
- Criar uma camada de metricas agregadas por produto, cliente e periodo.
- Orquestrar o pipeline com Airflow ou Prefect.
