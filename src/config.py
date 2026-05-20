from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = PROJECT_ROOT / "logs"

DEFAULT_INPUT_FILE = RAW_DATA_DIR / "vendas_exemplo.csv"
DEFAULT_OUTPUT_FILE = PROCESSED_DATA_DIR / "vendas_processadas.parquet"
DEFAULT_LOG_FILE = LOG_DIR / "etl_vendas.log"
