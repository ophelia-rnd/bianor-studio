import os
import pandas as pd

from databricks import sql

class DataService:

    @classmethod
    def execute(cls, cfg, sqls, params=None):
        data = pd.DataFrame([])

        try:
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
