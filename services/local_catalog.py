import pandas as pd
import yaml

from services.backend import catalog_path

_CACHE = None

_REPRESENTATION_COLUMNS = ["ID", "NAME", "SOM_MODEL_LOCATION", "FEATURES_LOCATION"]
_PROJECTION_COLUMNS = ["NAME", "SAMPLES_LOCATION", "MARKER_DICT"]
_PROJECTION_MAPPING_COLUMNS = ["REPRESENTATION_NAME", "NAME", "SAMPLES_LOCATION", "MARKER_DICT"]
_PREDICTION_COLUMNS = ["ID", "NAME", "PREDICTION_LOCATION"]
_PREDICTION_MAPPING_COLUMNS = ["REPRESENTATION_NAME", "NAME", "PREDICTION_LOCATION"]


def load_catalog():
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    path = catalog_path()
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    _CACHE = {
        "representations": raw.get("representations") or [],
        "projection_layers": raw.get("projection_layers") or [],
        "predictions": raw.get("predictions") or [],
    }
    return _CACHE


def _empty(columns):
    return pd.DataFrame(columns=columns)


def _sorted_records(records):
    return sorted(records, key=lambda row: row.get("id", 0))


def _same_id(left, right):
    if left is None or right is None:
        return False
    return str(left) == str(right)


def _rep_name_by_id():
    return {row.get("id"): row.get("name") for row in load_catalog()["representations"]}


def representations():
    records = _sorted_records(load_catalog()["representations"])
    if not records:
        return _empty(_REPRESENTATION_COLUMNS)
    rows = [
        {
            "ID": row.get("id"),
            "NAME": row.get("name"),
            "SOM_MODEL_LOCATION": row.get("som_model_location"),
            "FEATURES_LOCATION": row.get("features_location"),
        }
        for row in records
    ]
    return pd.DataFrame(rows, columns=_REPRESENTATION_COLUMNS)


def projection_mappings():
    name_by_id = _rep_name_by_id()
    records = _sorted_records(load_catalog()["projection_layers"])
    if not records:
        return _empty(_PROJECTION_MAPPING_COLUMNS)
    rows = [
        {
            "REPRESENTATION_NAME": name_by_id.get(row.get("representation_id"), ""),
            "NAME": row.get("name"),
            "SAMPLES_LOCATION": row.get("samples_location"),
            "MARKER_DICT": row.get("marker_dict"),
        }
        for row in records
    ]
    return pd.DataFrame(rows, columns=_PROJECTION_MAPPING_COLUMNS)


def projection_layers_by_representation(representation_id):
    records = [
        row for row in _sorted_records(load_catalog()["projection_layers"])
        if _same_id(row.get("representation_id"), representation_id)
    ]
    if not records:
        return _empty(_PROJECTION_COLUMNS)
    rows = [
        {
            "NAME": row.get("name"),
            "SAMPLES_LOCATION": row.get("samples_location"),
            "MARKER_DICT": row.get("marker_dict"),
        }
        for row in records
    ]
    return pd.DataFrame(rows, columns=_PROJECTION_COLUMNS)


def prediction_mappings():
    name_by_id = _rep_name_by_id()
    records = _sorted_records(load_catalog()["predictions"])
    if not records:
        return _empty(_PREDICTION_MAPPING_COLUMNS)
    rows = [
        {
            "REPRESENTATION_NAME": name_by_id.get(row.get("representation_id"), ""),
            "NAME": row.get("name"),
            "PREDICTION_LOCATION": row.get("prediction_location"),
        }
        for row in records
    ]
    return pd.DataFrame(rows, columns=_PREDICTION_MAPPING_COLUMNS)


def predictions_by_representation(representation_id):
    records = [
        row for row in _sorted_records(load_catalog()["predictions"])
        if _same_id(row.get("representation_id"), representation_id)
    ]
    if not records:
        return _empty(_PREDICTION_COLUMNS)
    rows = [
        {
            "ID": row.get("id"),
            "NAME": row.get("name"),
            "PREDICTION_LOCATION": row.get("prediction_location"),
        }
        for row in records
    ]
    return pd.DataFrame(rows, columns=_PREDICTION_COLUMNS)
