from services.data_service import DataService

class TableService(DataService):

    @classmethod
    def list(cls, cfg, table_name, limit:int = 50):
        sqls = f"SELECT * FROM IDENTIFIER(:table) LIMIT {limit}"
        params = {"table": table_name}
        return super().execute(cfg, sqls, params=params)
