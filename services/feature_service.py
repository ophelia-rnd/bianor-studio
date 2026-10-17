import json

from services.backend import is_local
from services.data_service import DataService

class FeatureService(DataService):

    @classmethod
    def _require_id(cls, df, table_name):
        assert "id" in df.columns, f"Column 'id' is required in local table: {table_name}"
        return df

    @classmethod
    def list_by_ids(cls, cfg, table_name, pks):
        if is_local():
            df = cls._require_id(super().read_local_table(table_name), table_name)
            keys = {str(pk) for pk in pks}
            return df[df["id"].astype(str).isin(keys)].copy()
        sqls = f"SELECT * FROM IDENTIFIER(:table) WHERE array_contains(from_json(:ids, 'ARRAY<INT>'), id)"
        params = {"table": table_name, "ids": json.dumps(pks)}
        return super().execute(cfg, sqls, params=params)

    @classmethod
    def list_by_join(cls, cfg, table_name, join_table_name):
        if is_local():
            left = cls._require_id(super().read_local_table(table_name), table_name)
            right = cls._require_id(super().read_local_table(join_table_name), join_table_name)
            left = left.copy()
            left["_join_id"] = left["id"].astype(str)
            right = right[["id"]].drop_duplicates().copy()
            right["_join_id"] = right["id"].astype(str)
            return left.merge(right[["_join_id"]], on="_join_id").drop(columns=["_join_id"])
        sqls = """
               SELECT t.* FROM IDENTIFIER(:table) t
                 INNER JOIN IDENTIFIER(:join_table) tj ON t.id = tj.id
               """
        params = {"table": table_name, "join_table": join_table_name}
        return super().execute(cfg, sqls, params=params)
