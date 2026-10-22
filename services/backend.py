import os
from pathlib import Path

BACKEND_DATABRICKS = "databricks"
BACKEND_LOCAL = "local"

_DATABRICKS_ENV_VARS = (
    "DATABRICKS_WAREHOUSE_ID",
    "BIANOR_DATABRICKS_CATALOG",
    "BIANOR_DATABRICKS_SCHEMA",
)
_ENV_LOADED = False


def project_root():
    return Path(__file__).resolve().parent.parent


def ensure_env():
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    from dotenv import load_dotenv
    root = project_root()
    load_dotenv(root / ".env")
    load_dotenv(root / ".env.local")
    _ENV_LOADED = True


def _has_databricks_env():
    return all(os.getenv(name) for name in _DATABRICKS_ENV_VARS)


def _default_local_root():
    return project_root() / "bianor_local_catalog"


def backend_name():
    ensure_env()
    name = (os.getenv("BIANOR_BACKEND") or "").strip().lower()
    if name in (BACKEND_LOCAL, BACKEND_DATABRICKS):
        return name
    if os.getenv("BIANOR_LOCAL_CATALOG_ROOT"):
        return BACKEND_LOCAL
    if _has_databricks_env():
        return BACKEND_DATABRICKS
    if (_default_local_root() / "catalog.yaml").is_file():
        return BACKEND_LOCAL
    return BACKEND_DATABRICKS


def is_local():
    return backend_name() == BACKEND_LOCAL


def local_root():
    ensure_env()
    root = os.getenv("BIANOR_LOCAL_CATALOG_ROOT")
    if root:
        return Path(root).expanduser().resolve()
    return _default_local_root().resolve()


def catalog_path():
    return local_root() / "catalog.yaml"


def get_databricks_config():
    """
    Returns Databricks SDK Config if running with the Databricks backend.
    In local mode, returns None without importing databricks-sdk.
    """
    if is_local():
        return None
    try:
        from databricks.sdk.core import Config
        return Config()
    except ImportError as exc:
        raise ImportError(
            "Databricks backend requires 'databricks-sdk'. "
            "Please install it with `pip install databricks-sdk` or switch "
            "to local mode (BIANOR_BACKEND=local)."
        ) from exc
