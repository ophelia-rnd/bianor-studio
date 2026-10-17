import os
from pathlib import Path

import pandas as pd

from services.backend import local_root

class DataService:

    CATALOG = os.getenv('BIANOR_DATABRICKS_CATALOG')
    SCHEMA = os.getenv('BIANOR_DATABRICKS_SCHEMA')

    @classmethod
    def get_table_path(cls, table_name):
        return f"{cls.CATALOG}.{cls.SCHEMA}.{table_name}"

    @classmethod
    def resolve_local_table_path(cls, table_name):
        path = Path(table_name).expanduser()
        if not path.is_absolute():
            path = local_root() / path
        return path.resolve()

    @classmethod
    def read_local_table(cls, table_name):
        path = cls.resolve_local_table_path(table_name)
        assert path.is_file(), f"Local table not found: {path}"
        suffix = path.suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(path)
        elif suffix in (".parquet", ".pq"):
            df = pd.read_parquet(path)
        else:
            raise ValueError(f"Unsupported table format '{suffix}' for {path}. Use .csv or .parquet.")
        df.columns = [c.lower() for c in df.columns]
        return df

    @classmethod
    def execute(cls, cfg, sqls, params=None):
        data = pd.DataFrame([])

        try:
            from databricks import sql
            with sql.connect(
                    server_hostname=cfg.host,
                    http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
                    credentials_provider=lambda: cfg.authenticate
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sqls, parameters=params)
                    columns = [desc[0] for desc in cursor.description]
                    data = pd.DataFrame(cursor.fetchall(), columns=columns)

        except Exception as e:
            print(f"An error occurred in querying data: {str(e)}")

        return data
