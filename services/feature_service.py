import json

from services.data_service import DataService

class FeatureService(DataService):

    @classmethod
    def list_by_ids(cls, cfg, table_name, pks):
        sqls = f"SELECT * FROM IDENTIFIER(:table) WHERE array_contains(from_json(:ids, 'ARRAY<INT>'), id)"
        params = {"table": table_name, "ids": json.dumps(pks)}
        return super().execute(cfg, sqls, params=params)

    @classmethod
    def list_by_join(cls, cfg, table_name, join_table_name):
        sqls = """
               SELECT t.* FROM IDENTIFIER(:table) t
                 INNER JOIN IDENTIFIER(:join_table) tj ON t.id = tj.id
               """
        params = {"table": table_name, "join_table": join_table_name}
        return super().execute(cfg, sqls, params=params)
