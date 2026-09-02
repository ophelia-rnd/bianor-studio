import dash
import constants.table as table_const

from dash import dcc, html, Input, Output, dash_table

dash.register_page(
    __name__,
    path="/configuration",
    name="Configuration",
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

def create_datatable(elem_id:str):
    return dash_table.DataTable(
        id=elem_id,
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
        row_selectable=False, column_selectable=False, cell_selectable=False, tooltip_delay=0, tooltip_duration=None,
    )

layout = html.Div(
    children=[
        html.H3("Configuration", className="mb-4"),
        dcc.Markdown(f"Browse previously created map configurations.", style={"marginBottom": "2rem"}),

        html.H4("Representations", className="mb-3"),
        dcc.Markdown(f"Representation configurations are loaded from and can be managed "
                     f"in the `{table_const.TABLE_REPRESENTATION}` database table."),
        create_datatable("tbl-representation"),

        html.H4("Projection Layers", className="mb-3", style={"marginTop": "2rem"}),
        dcc.Markdown(
            f"Projection layer configurations are loaded from and can be managed "
            f"in the `{table_const.TABLE_PROJECTION_LAYER}` "
            f"and `{table_const.TABLE_MAP_REPRESENTATION_PROJECTION_LAYER}` database tables."),
        create_datatable("tbl-projection"),

        html.H4("Predictions", className="mb-3", style={"marginTop": "2rem"}),
        dcc.Markdown(f"Prediction configurations are loaded from and can be managed "
             f"in the `{table_const.TABLE_PREDICTION}` "
             f"and `{table_const.TABLE_MAP_REPRESENTATION_PREDICTION}` database tables."),
        create_datatable("tbl-prediction"),
    ]
)

@cache.memoize()
def fetch_map_configs():
    from services.map_service import BianorRepresentationService
    return BianorRepresentationService.list(cfg)

@cache.memoize()
def fetch_projection_layer_configs():
    from services.map_service import BianorProjectionLayerService
    return BianorProjectionLayerService.list_mappings(cfg)

@cache.memoize()
def fetch_prediction_configs():
    from services.map_service import BianorPredictionService
    return BianorPredictionService.list_mappings(cfg)

def __create_table_content(df):
    table_columns = [{"name": c, "id": c} for c in df.columns]
    table_rows = df.to_dict('records')
    tooltip_data = [{
        column: {'value': str(value)}
        for column, value in row.items()
    } for row in table_rows]
    return table_rows, table_columns, tooltip_data

@dash.callback(
    Output("tbl-representation", "data"),
    Output("tbl-representation", "columns"),
    Output("tbl-representation", "tooltip_data"),
    Input("tbl-representation", "id"),
)
def __populate_representation_table(_):
    map_df = fetch_map_configs().copy()
    if map_df.empty: return [], [], []
    map_df.columns = ["Id", "Name", "SOM Model Location", "Features Location"]
    return __create_table_content(map_df)

@dash.callback(
    Output("tbl-projection", "data"),
    Output("tbl-projection", "columns"),
    Output("tbl-projection", "tooltip_data"),
    Input("tbl-projection", "id"),
)
def __populate_projection_table(_):
    map_df = fetch_projection_layer_configs().copy()
    if map_df.empty: return [], [], []
    map_df.columns = ["Representation Name", "Projection Name", "Samples Location", "Marker"]
    return __create_table_content(map_df)

@dash.callback(
    Output("tbl-prediction", "data"),
    Output("tbl-prediction", "columns"),
    Output("tbl-prediction", "tooltip_data"),
    Input("tbl-prediction", "id"),
)
def __populate_prediction_table(_):
    map_df = fetch_prediction_configs().copy()
    if map_df.empty: return [], [], []
    map_df.columns = ["Representation Name", "Prediction Name", "Prediction Location"]
    return __create_table_content(map_df)
