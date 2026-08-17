import dash

from dash import dcc, html, Input, Output, dash_table
from lilypond.basin import Basin
from utils.figure_style import style_figure

dash.register_page(
    __name__,
    path="/explorer",
    name="Map Explorer",
    icon="bi-map"
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
    className="d-flex flex-column h-100 overflow-hidden",
    children=[
        html.H3("Explorer", className="mb-4"),
        html.Div(
            id="observer-container",
            children=[
                html.Div(id='observer-plot-container'),
                html.Div(
                    id='observer-table-container',
                    children=[
                        html.H6("Detections", className="mb-3"),
                        dash_table.DataTable(
                            id="observer-table",
                            style_as_list_view=True,
                            row_selectable="multi",
                            style_header={
                                'backgroundColor': '#1b1824',
                                'border': 'none',
                                'position': 'sticky',
                                'top': '0',
                                'zIndex': '1000'
                            },
                            style_cell={
                                'background': 'none',
                                'color': 'white',
                                'border': 'none',
                                'padding': '7px',
                                'fontSize': '.8rem',
                            },
                            style_table={
                                'backgroundColor': '#221e2e',
                                'cursor': 'pointer'
                            },
                            cell_selectable=False,
                            column_selectable=False,
                            css=[{"selector": ".dash-spreadsheet", "rule":'max-height: unset;'}],
                        )
                    ]
                )
            ]
        )
    ]
)

@cache.memoize()
def fetch_predictions(table, limit:int = 100):
    from services.prediction_service import PredictionService
    return PredictionService.list(cfg, table, limit=limit)

@cache.memoize()
def fetch_features(table, ids):
    from services.feature_service import FeatureService
    return FeatureService.list_by_ids(cfg, table, pks=ids)

@cache.memoize()
def load_model(model_loc):
    from services.model_service import ModelService
    return ModelService.load(model_loc)

@cache.memoize()
def load_representation(model_loc):
    model = load_model(model_loc)
    som_rep = model.model
    return som_rep

@cache.memoize()
def load_scaler(model_loc):
    model = load_model(model_loc)
    scaler = model.scaler
    return scaler

@cache.memoize()
def create_basin(som_rep):
    return Basin.from_som_representation(som_rep, random_seed=42, verbose=False)

@cache.memoize()
def create_base_pond(basin):
    from lilypond.pond_base_style import PondBaseStyle
    modern_style = PondBaseStyle(
        water_colorscale="Teal",
        rhizome_colorscale=PondBaseStyle.pond().rhizome_colorscale,
        pad_colorscale="Plasma",
        petal_colorscale="Greys",
        petal_marker_line=dict(width=0),
        petal_marker=dict(symbol="star", opacity=1),
        petal_halo_marker=None
    )
    return basin \
        .pond(base_style=modern_style) \
        .rhizome_layer() \
        .pad_layer(gap="nogap") \
        .petal_layer()

@dash.callback(
    Output('observer-plot-container', 'children'),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
    Input("observer-table", "selected_row_ids")
)
def __update_plot(selected_map, selected_prediction, selected_row_ids):
    if not selected_map: return html.Span("Select a representation to be visualized.", className="text-white-50")

    som_rep_model_loc = selected_map.get("SOM_MODEL_LOCATION")
    som_rep_model = load_representation(som_rep_model_loc)

    basin = create_basin(som_rep_model)
    pond = create_base_pond(basin)

    if selected_prediction and selected_row_ids and len(selected_row_ids):
        X = fetch_features(table=selected_map["FEATURE_TABLE_LOCATION"], ids=selected_row_ids)
        X.set_index("id", drop=True, inplace=True)
        scaler = load_scaler(som_rep_model_loc)
        pond.attraction_layer(scaler.transform(X))

    fig = pond.visualize(show_fig=False, title=None)
    fig = style_figure(fig)

    import uuid
    return dcc.Graph(
        id=f"observer-graph-{uuid.uuid4()}",
        figure=fig,
        style={'width': '100%', 'height': '100%'},
        responsive=True
    )

@dash.callback(
    Output("observer-table", "data"),
    Output("observer-table", "columns"),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
)
def __populate_prediction_table(selected_map, selected_prediction):
    if not selected_map or not selected_prediction: return [], []
    prediction_table_loc = selected_prediction.get("PREDICTION_TABLE_LOCATION")
    df_predictions = fetch_predictions(prediction_table_loc).copy()
    df_predictions.columns = [c.lower() for c in df_predictions.columns]
    assert "id" in df_predictions.columns, "Id column is required in prediction table."
    table_columns = [{"name": str(c).lower().capitalize(), "id": c} for c in df_predictions.columns]
    table_rows = df_predictions.to_dict('records')
    return table_rows, table_columns

@dash.callback(
    Output("observer-table", "selected_row_ids"),
    Output("observer-table", "selected_rows"),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
)
def __reset_selected_rows(selected_map, selected_prediction):
    return [], []
