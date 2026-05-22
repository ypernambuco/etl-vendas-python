# etl-vendas-python

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2.3-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20evolu%C3%A7%C3%A3o-2E8B57?style=for-the-badge)
![License](https://img.shields.io/badge/licen%C3%A7a-MIT-blue?style=for-the-badge)

Projeto simples de ETL de vendas feito para praticar Python, pandas e organização básica de um pipeline de dados.

A ideia é partir de um arquivo CSV pequeno, aplicar algumas regras de limpeza e salvar uma versão processada em Parquet. O projeto não tenta simular uma arquitetura de produção; ele serve como estudo prático e como registro da minha evolução com dados.

## Objetivo

Praticar as etapas principais de um ETL em um cenário fácil de explicar:

- ler dados de vendas a partir de um CSV;
- padronizar nomes de colunas;
- tratar duplicatas, campos vazios e datas inválidas;
- converter colunas numéricas;
- criar a coluna `valor_total`;
- salvar o resultado em Parquet;
- registrar logs simples da execução.

## Estrutura Do Projeto

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

## Fluxo Do Pipeline

```mermaid
flowchart LR
    A["CSV bruto<br/>data/raw/vendas_exemplo.csv"] --> B["Pipeline ETL<br/>src/etl.py"]
    B --> C["Limpeza e transformação<br/>pandas"]
    C --> D["Parquet processado<br/>data/processed/vendas_processadas.parquet"]
    B --> E["Logs de execução<br/>logs/etl_vendas.log"]
```

## Tecnologias Usadas

- Python 3.10+
- pandas
- pyarrow
- pathlib
- logging

## O Que Pratiquei

- leitura de arquivos CSV com pandas;
- limpeza e padronização de dados;
- tratamento de valores ausentes e duplicados;
- conversão de datas e números;
- criação de colunas derivadas;
- exportação para Parquet;
- uso de logs para acompanhar a execução;
- organização simples de um projeto Python.

## Aprendizados

Durante este projeto, pratiquei principalmente a separação entre entrada, transformação e saída dos dados. Também foi útil perceber alguns detalhes comuns em dados reais, como nomes de colunas inconsistentes, datas inválidas, campos vazios e linhas duplicadas.

Outro aprendizado foi deixar os caminhos principais em um arquivo de configuração simples e permitir que o ETL também receba caminhos pela linha de comando. Isso facilita testar o pipeline com outros arquivos sem mudar o código.

## Limitações

Este projeto ainda é pequeno e tem algumas limitações importantes:

- o dataset é fictício e bem reduzido;
- a validação dos dados ainda é simples;
- não existe carga em banco de dados;
- não há testes automatizados específicos para este projeto ainda;
- os indicadores analíticos ainda não foram separados em uma camada própria;
- não existe orquestração do pipeline.

Essas limitações fazem parte do escopo atual. A intenção é evoluir o projeto aos poucos, mantendo as mudanças fáceis de entender.

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

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Como Rodar O ETL

Execute com os caminhos padrão:

```bash
python -m src.etl
```

No Windows, se o comando `python` não estiver disponível, use o launcher:

```bash
py -m src.etl
```

Ou informe entrada, saída e log explicitamente:

```bash
python -m src.etl --input data/raw/vendas_exemplo.csv --output data/processed/vendas_processadas.parquet --log-file logs/etl_vendas.log
```

Também é possível executar o arquivo diretamente:

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

## Exemplo De Saída

Arquivo: `data/processed/vendas_processadas.parquet`

Colunas esperadas após o processamento:

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

Os logs são gerados em:

```text
logs/etl_vendas.log
```

Eles registram início e fim do pipeline, quantidade de linhas lidas, colunas padronizadas, duplicatas removidas, datas inválidas descartadas e exportação do Parquet.

## Próximos Passos

- Adicionar testes automatizados para as transformações principais.
- Criar validações simples de qualidade dos dados.
- Gerar métricas agregadas por produto e período.
- Criar consultas SQL usando SQLite.
- Montar um dashboard simples com os indicadores gerados.
