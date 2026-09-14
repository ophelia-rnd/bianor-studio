from services.data_service import DataService
import constants.table as table_const

class BianorRepresentationService(DataService):

    @classmethod
    def list(cls, cfg):
        sqls = """
            SELECT ID, NAME, SOM_MODEL_LOCATION, FEATURES_LOCATION
            FROM IDENTIFIER(:table)
            ORDER BY ID;
            """
        params = {"table": super().get_table_path(table_const.TABLE_REPRESENTATION)}
        return super().execute(cfg, sqls, params=params)

class BianorProjectionLayerService(DataService):

    @classmethod
    def list_mappings(cls, cfg):
        sqls = """
            SELECT tr.NAME AS REPRESENTATION_NAME, t.NAME, t.SAMPLES_LOCATION, t.MARKER_DICT
            FROM IDENTIFIER(:table) t
                INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PROJECTION_LAYER_ID
                INNER JOIN IDENTIFIER(:table_representation) tr ON tr.ID = tm.REPRESENTATION_ID
            ORDER BY t.ID;
            """
        params = {
            "table": super().get_table_path(table_const.TABLE_PROJECTION_LAYER),
            "table_map": super().get_table_path(table_const.TABLE_MAP_REPRESENTATION_PROJECTION_LAYER),
            "table_representation": super().get_table_path(table_const.TABLE_REPRESENTATION)
        }
        return super().execute(cfg, sqls, params=params)

    @classmethod
    def list_by_representation(cls, cfg, representation_id):
        sqls = """
            SELECT t.NAME, t.SAMPLES_LOCATION, t.MARKER_DICT
            FROM IDENTIFIER(:table) t
                INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PROJECTION_LAYER_ID
            WHERE tm.REPRESENTATION_ID = :representation_id
            ORDER BY t.ID;
            """
        params = {
            "table": super().get_table_path(table_const.TABLE_PROJECTION_LAYER),
            "table_map": super().get_table_path(table_const.TABLE_MAP_REPRESENTATION_PROJECTION_LAYER),
            "representation_id": representation_id
        }
        return super().execute(cfg, sqls, params=params)

class BianorPredictionService(DataService):

    @classmethod
    def list_mappings(cls, cfg):
        sqls = """
            SELECT tr.NAME AS REPRESENTATION_NAME, t.NAME, t.PREDICTION_LOCATION
            FROM IDENTIFIER(:table) t
                INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PREDICTION_ID
                INNER JOIN IDENTIFIER(:table_representation) tr ON tr.ID = tm.REPRESENTATION_ID
            ORDER BY t.ID;
            """
        params = {
            "table": super().get_table_path(table_const.TABLE_PREDICTION),
            "table_map": super().get_table_path(table_const.TABLE_MAP_REPRESENTATION_PREDICTION),
            "table_representation": super().get_table_path(table_const.TABLE_REPRESENTATION)
        }
        return super().execute(cfg, sqls, params=params)

    @classmethod
    def list_by_representation(cls, cfg, representation_id):
        sqls = """
        SELECT t.ID, t.NAME, t.PREDICTION_LOCATION
        FROM IDENTIFIER(:table) t
            INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PREDICTION_ID
        WHERE tm.REPRESENTATION_ID = :representation_id
        ORDER BY t.ID;
        """
        params = {
            "table": super().get_table_path(table_const.TABLE_PREDICTION),
            "table_map": super().get_table_path(table_const.TABLE_MAP_REPRESENTATION_PREDICTION),
            "representation_id": representation_id
        }
        return super().execute(cfg, sqls, params=params)
