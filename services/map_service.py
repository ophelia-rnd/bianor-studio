from services.data_service import DataService
import constants.table as table_const

class BianorRepresentationConfigService(DataService):

    TABLE = table_const.TABLE_REPRESENTATION

    @classmethod
    def list(cls, cfg):
        sqls = """
        SELECT ID, NAME, SOM_MODEL_LOCATION, FEATURE_TABLE_LOCATION FROM IDENTIFIER(:table);
        """
        params = {"table": super().get_table_path(cls.TABLE)}
        return super().execute(cfg, sqls, params=params)

class BianorProjectionLayerConfigService(DataService):

    TABLE = table_const.TABLE_PROJECTION_LAYER
    TABLE_MAP = table_const.TABLE_MAP_REPRESENTATION_PROJECTION_LAYER

    @classmethod
    def list_projections(cls, cfg, representation_id):
        sqls = """
               SELECT t.NAME, t.SAMPLES_LOCATION, t.MARKER_CONFIG  \
               FROM IDENTIFIER(:table) t \
                        INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PROJECTIONLAYERC_ID \
                        INNER JOIN IDENTIFIER(:table_representation) tr ON tr.ID = tm.REPRESENTATIONC_ID
               WHERE tr.ID = :representation_id
               ORDER BY t.ID; \
               """
        params = {"table": super().get_table_path(cls.TABLE), "table_map": super().get_table_path(cls.TABLE_MAP),
                  "table_representation": BianorRepresentationConfigService.TABLE, "representation_id": representation_id}
        return super().execute(cfg, sqls, params=params)

class BianorPredictionConfigService(DataService):

    TABLE = table_const.TABLE_PREDICTION
    TABLE_MAP = table_const.TABLE_MAP_REPRESENTATION_PREDICTION

    @classmethod
    def list_maps(cls, cfg):
        sqls = """
       SELECT tr.NAME, t.PREDICTION_TABLE_LOCATION FROM IDENTIFIER(:table) t
            INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PREDICTIONC_ID
            INNER JOIN IDENTIFIER(:table_representation) tr ON tr.ID = tm.REPRESENTATIONC_ID;
       """
        params = {"table": super().get_table_path(cls.TABLE), "table_map": super().get_table_path(cls.TABLE_MAP),
                  "table_representation": BianorRepresentationConfigService.TABLE}
        return super().execute(cfg, sqls, params=params)

    @classmethod
    def list_by_representation(cls, cfg, representation_id):
        sqls = """
        SELECT ID, NAME, PREDICTION_TABLE_LOCATION FROM IDENTIFIER(:table) t
            INNER JOIN IDENTIFIER(:table_map) tm ON t.ID = tm.PREDICTIONC_ID
            WHERE REPRESENTATIONC_ID = :representation_id;
        """
        params = {"table": super().get_table_path(cls.TABLE), "table_map": super().get_table_path(cls.TABLE_MAP),
                  "representation_id": representation_id}
        return super().execute(cfg, sqls, params=params)
