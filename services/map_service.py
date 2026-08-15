import os

from services.data_service import DataService

class BianorRepresentationConfigService(DataService):

    TABLE = os.getenv('BIANOR_REPRESENTATION_CONFIG_DATABRICKS_TABLE_LOCATION')

    @classmethod
    def list(cls, cfg):
        sqls = """
        SELECT ID, NAME, SOM_MODEL_LOCATION, FEATURE_TABLE_LOCATION FROM IDENTIFIER(:table);
        """
        params = {"table": cls.TABLE}
        return DataService.execute(cfg, sqls, params=params)

class BianorPredictionConfigService(DataService):

    TABLE = os.getenv('BIANOR_PREDICTION_CONFIG_DATABRICKS_TABLE_LOCATION')
    TABLE_MAP = os.getenv('BIANOR_MAP_REPRESENTATION_PREDICTION_CONFIG_DATABRICKS_TABLE_LOCATION')

    @classmethod
    def list_by_representation(cls, cfg, representation_id):
        sqls = """
        SELECT ID, NAME, PREDICTION_TABLE_LOCATION FROM IDENTIFIER(:table) t
            INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PREDICTIONC_ID
            WHERE REPRESENTATIONC_ID = :representation_id;
        """
        params = {"table": cls.TABLE, "table_map": cls.TABLE_MAP, "representation_id": representation_id}
        return DataService.execute(cfg, sqls, params=params)
