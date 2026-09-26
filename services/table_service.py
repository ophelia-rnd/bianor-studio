from services.data_service import DataService

class TableService(DataService):

    @classmethod
    def list(cls, cfg, table_name, limit:int = 50, offset:int = 0):
        sqls = f"SELECT * FROM IDENTIFIER(:table) LIMIT {limit} OFFSET {offset}"
        params = {"table": table_name}
        return super().execute(cfg, sqls, params=params)
