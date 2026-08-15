import json

from services.data_service import DataService

class FeatureService(DataService):

    @classmethod
    def list_by_ids(cls, cfg, table, pks):
        sqls = f"SELECT * FROM IDENTIFIER(:table) WHERE array_contains(from_json(:ids, 'ARRAY<INT>'), id)"
        params = {"table": table, "ids": json.dumps(pks)}
        return DataService.execute(cfg, sqls, params=params)
