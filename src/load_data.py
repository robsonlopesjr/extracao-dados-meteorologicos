import logging
import os
import pandas as pd

from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(env_path)

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")


def get_engine():
    logging.info(f"→ Conectando em {host}:{port}/{database}")

    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )


engine = get_engine()


def load_weather_data(table_name: str, df: pd.DataFrame):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info("\n✓ Dados carregados com sucesso")

    df_check = pd.read_sql(f"SELECT * from {table_name}", con=engine)

    logging.info(f"\nTotal de registros na tabela: {len(df_check)}")
