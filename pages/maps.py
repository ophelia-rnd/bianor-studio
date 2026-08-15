import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output
from services.map_service import BianorRepresentationConfigService

dash.register_page(
    __name__,
    path="/maps",
    name="Maps",
    icon="bi-collection"
)

def get_app():
    from dash import get_app
    from databricks.sdk.core import Config
    return Config(), get_app()

def setup_cache(app):
    from flask_caching import Cache
    return Cache(
        app.server,
        config={
            "CACHE_TYPE": "FileSystemCache",
            "CACHE_DIR": ".bianor_cache",
            "CACHE_DEFAULT_TIMEOUT": 1200,
        }
    )

cfg, app = get_app()
cache = setup_cache(app)

layout = html.Div(
    children=[
        html.H3("Maps", className="mb-4"),
        dcc.Markdown(
            f"Browse previously created map configurations. Map configurations are loaded from and can be managed in the `{BianorRepresentationConfigService.TABLE}` database table."
        ),
        html.Div(
            id="map-table-container",
            style={"marginTop": "2rem"}
        )
    ]
)

@cache.memoize()
def fetch_map_configs():
    from services.map_service import BianorRepresentationConfigService
    return BianorRepresentationConfigService.list(cfg)

@dash.callback(Output("map-table-container", "children"),
    Input("map-table-container", "id"),
)
def __populate_table(_):
    map_df = fetch_map_configs()
    map_df_display = map_df.copy()
    map_df_display.columns = ["Id", "Name", "SOM Model Location", "Feature Table Location"]

    def get_tooltip_el(text, cell_id):
        return html.Div(
            children=[
                html.Span(text, id=cell_id, className="text-truncate d-inline-block mw-100"),
                dbc.Tooltip(text, target=cell_id, placement="top"),
            ]
        )

    for colid in map_df_display.columns:
        map_df_display[colid] = [
            get_tooltip_el(str(val), f"cell-{rowid}-{colid}")
            for rowid, val in zip(map_df_display.index, map_df_display[colid])
        ]

    return dbc.Table.from_dataframe(
        map_df_display,
        size="sm",
        striped=False,
        bordered=False,
        color="dark",
        hover=True,
        responsive=True,
        className="truncated-table text-light",
    )
