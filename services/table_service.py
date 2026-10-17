from services.backend import is_local
from services.data_service import DataService

class TableService(DataService):

    @classmethod
    def list(cls, cfg, table_name, limit:int = 50, offset:int = 0):
        if is_local():
            return super().read_local_table(table_name).iloc[offset:offset + limit].copy()
        sqls = f"SELECT * FROM IDENTIFIER(:table) LIMIT {limit} OFFSET {offset}"
        params = {"table": table_name}
        return super().execute(cfg, sqls, params=params)
