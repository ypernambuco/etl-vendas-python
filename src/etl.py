import argparse
import logging
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import DEFAULT_INPUT_FILE, DEFAULT_LOG_FILE, DEFAULT_OUTPUT_FILE
from src.logger import setup_logger


REQUIRED_COLUMNS = {
    "id_venda",
    "data_venda",
    "cliente",
    "produto",
    "quantidade",
    "preco_unitario",
}


def normalize_column_name(column: str) -> str:
    """Padroniza nomes de colunas para snake_case sem acentos."""
    normalized = unicodedata.normalize("NFKD", column.strip().lower())
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    return normalized.strip("_")


def read_csv(input_file: Path, logger: logging.Logger) -> pd.DataFrame:
    """Lê o arquivo CSV de vendas e retorna um DataFrame."""
    logger.info("Lendo CSV: %s", input_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {input_file}")

    dataframe = pd.read_csv(input_file)
    logger.info("CSV lido com sucesso: %s linhas, %s colunas", *dataframe.shape)
    return dataframe


def validate_columns(dataframe: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV de vendas sem colunas obrigatórias: {missing}")


def clean_data(dataframe: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """Limpa, transforma e enriquece os dados de vendas."""
    logger.info("Iniciando limpeza e transformação dos dados de vendas")

    cleaned = dataframe.copy()
    cleaned.columns = [normalize_column_name(column) for column in cleaned.columns]
    validate_columns(cleaned)

    before_duplicates = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    duplicates_removed = before_duplicates - len(cleaned)

    text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)

    cleaned["cliente"] = cleaned["cliente"].fillna("Não informado")
    cleaned["produto"] = cleaned["produto"].fillna("Não informado")

    cleaned["data_venda"] = pd.to_datetime(
        cleaned["data_venda"],
        errors="coerce",
        dayfirst=True,
    )

    numeric_columns = ["quantidade", "preco_unitario"]
    if "desconto" in cleaned.columns:
        numeric_columns.append("desconto")
    else:
        cleaned["desconto"] = 0.0

    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").fillna(0)

    invalid_dates = int(cleaned["data_venda"].isna().sum())
    cleaned = cleaned.dropna(subset=["data_venda"])

    cleaned["valor_total"] = (
        (cleaned["quantidade"] * cleaned["preco_unitario"]) - cleaned["desconto"]
    ).clip(lower=0).round(2)

    cleaned = cleaned.dropna(how="all")
    cleaned["data_processamento"] = pd.Timestamp.now().floor("s")

    logger.info("Colunas padronizadas: %s", list(cleaned.columns))
    logger.info("Duplicatas removidas: %s", duplicates_removed)
    logger.info("Linhas removidas por data inválida: %s", invalid_dates)
    logger.info("Limpeza concluída: %s linhas, %s colunas", *cleaned.shape)

    return cleaned


def export_parquet(dataframe: pd.DataFrame, output_file: Path, logger: logging.Logger) -> None:
    """Exporta o DataFrame limpo para Parquet."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Exportando Parquet: %s", output_file)
    try:
        dataframe.to_parquet(output_file, index=False)
    except ImportError:
        raise ImportError(
            "Dependência para exportar Parquet não encontrada. "
            "Instale as dependências com: python -m pip install -r requirements.txt"
        ) from None
    logger.info("Arquivo Parquet exportado com sucesso: %s linhas", len(dataframe))


def run_pipeline(input_file: Path, output_file: Path, log_file: Path) -> None:
    logger = setup_logger(log_file)
    logger.info("Pipeline ETL iniciado")

    try:
        raw_data = read_csv(input_file, logger)
        clean_dataset = clean_data(raw_data, logger)
        export_parquet(clean_dataset, output_file, logger)
    except ImportError as error:
        logger.error("Pipeline ETL falhou: %s", error)
        raise
    except Exception:
        logger.exception("Pipeline ETL falhou")
        raise

    logger.info("Pipeline ETL finalizado")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline ETL de vendas: CSV para Parquet.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help=f"Caminho do CSV de entrada. Padrão: {DEFAULT_INPUT_FILE}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Caminho do Parquet de saída. Padrão: {DEFAULT_OUTPUT_FILE}",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=DEFAULT_LOG_FILE,
        help=f"Caminho do arquivo de log. Padrão: {DEFAULT_LOG_FILE}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run_pipeline(args.input, args.output, args.log_file)
    except Exception as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
