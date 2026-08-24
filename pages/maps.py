import dash

from dash import dcc, html, Input, Output, dash_table
from services.map_service import BianorRepresentationConfigService, BianorPredictionConfigService

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
        dcc.Markdown(f"Browse previously created map configurations.", style={"marginBottom": "2rem"}),
        html.H4("Representation Configurations", className="mb-3"),
        dcc.Markdown(f"Representation configurations are loaded from and can be managed in the `{BianorRepresentationConfigService.TABLE}` database table."),
        dash_table.DataTable(
            id="map-representation-table",
            style_as_list_view=True,
            style_header={
                'backgroundColor': '#2b263a',
                'border': 'none',
                'padding': '1rem .75rem',
            },
            style_cell={
                'background': 'none',
                'color': 'white',
                'border': 'none',
                'padding': '.75rem',
                'fontSize': '.8rem',
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Id'},
                    'textAlign': 'center',
                    'width': '50px',
                    'max-width': '50px',
                    'box-sizing': 'border-box'
                }
            ],
            style_table={
                'backgroundColor': '#332e49',
                'cursor': 'default'
            },
            row_selectable=False,
            column_selectable=False,
            cell_selectable=False,
            tooltip_delay=0,
            tooltip_duration=None,
        ),
        html.H4("Representation-Prediction Configurations", className="mb-3", style={"marginTop": "2rem"}),
        dcc.Markdown(f"Representation-Prediction configurations are loaded from and can be managed in the `{BianorPredictionConfigService.TABLE}` and `{BianorPredictionConfigService.TABLE_MAP}` database tables."),
        dash_table.DataTable(
            id="map-representation-prediction-table",
            style_as_list_view=True,
            style_header={
                'backgroundColor': '#2b263a',
                'border': 'none',
                'padding': '1rem .75rem',
            },
            style_cell={
                'background': 'none',
                'color': 'white',
                'border': 'none',
                'padding': '.75rem',
                'fontSize': '.8rem',
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Id'},
                    'textAlign': 'center',
                    'width': '50px',
                    'max-width': '50px',
                    'box-sizing': 'border-box'
                }
            ],
            style_table={
                'backgroundColor': '#332e49',
                'cursor': 'default'
            },
            row_selectable=False,
            column_selectable=False,
            cell_selectable=False,
            tooltip_delay=0,
            tooltip_duration=None,
        ),
    ]
)

@cache.memoize()
def fetch_map_configs():
    from services.map_service import BianorRepresentationConfigService
    return BianorRepresentationConfigService.list(cfg)

@cache.memoize()
def fetch_prediction_mapping_configs():
    from services.map_service import BianorPredictionConfigService
    return BianorPredictionConfigService.list_maps(cfg)

@dash.callback(
    Output("map-representation-table", "data"),
    Output("map-representation-table", "columns"),
    Output("map-representation-table", "tooltip_data"),
    Input("map-representation-table", "id"),
)
def __populate_representation_table(_):
    map_df = fetch_map_configs().copy()
    map_df.columns = ["Id", "Name", "SOM Model Location", "Feature Table Location"]
    table_columns = [{"name": c, "id": c} for c in map_df.columns]
    table_rows = map_df.to_dict('records')
    tooltip_data = [{
        column: {'value': str(value)}
        for column, value in row.items()
    } for row in table_rows]
    return table_rows, table_columns, tooltip_data

@dash.callback(
    Output("map-representation-prediction-table", "data"),
    Output("map-representation-prediction-table", "columns"),
    Output("map-representation-prediction-table", "tooltip_data"),
    Input("map-representation-prediction-table", "id"),
)
def __populate_representation_prediction_table(_):
    map_df = fetch_prediction_mapping_configs().copy()
    map_df.columns = ["Representation Name", "Prediction Table Location"]
    table_columns = [{"name": c, "id": c} for c in map_df.columns]
    table_rows = map_df.to_dict('records')
    tooltip_data = [{
        column: {'value': str(value)}
        for column, value in row.items()
    } for row in table_rows]
    return table_rows, table_columns, tooltip_data
