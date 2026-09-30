import json
import dash
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

from dash import dcc, html, Input, Output, State
from lilypond.basin import Basin
from utils.figure_style import style_figure
from registry import registry

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
            "CACHE_DEFAULT_TIMEOUT": 480,
        }
    )


cfg, app = get_app()
cache = setup_cache(app)


def create_plot_config():
    plot_config = dict(
        view="topology",
        rhizome_layer_active=False,
        rhizome_layer_violationonly_active=False,
        pad_layer_active=True,
        pad_layer_nogap_active=True,
        petal_layer_active=False,
    )
    return plot_config


layout = lambda: html.Div(
    className="d-flex flex-column h-100 overflow-hidden", style={"margin": "-4.5rem 0 0 -9rem"},
    children=[
        dcc.Store(id="plot_config", data=create_plot_config()),
        html.Div(
            id="observer-container",
            children=[
                html.Div(
                    className="d-flex flex-column",
                    style={"flex": "1 1 0", "minWidth": "0", "gap": "2rem"},
                    children=[
                        html.Div(
                            className="d-flex gap-3 rounded rounded-lg text-white mt-3",
                            style={"flex-grow": "0", "background": "#2b263a", "padding": "1rem .9rem",
                                   "width": "max-content", "position": "relative",
                                   "box-shadow": "inset 0 -5px 15px 1px #1d1a27"},
                            children=[
                                html.Span(
                                    "View & Layers",
                                    className="text-white-50 p-3 rounded small",
                                    style={"z-index": "0", "cursor": "default", "position": "absolute", "top": "-25px",
                                           "left": "0", "right": "0", "margin": "auto", "width": "fit-content",
                                           "background": "#2b263a"}
                                ),
                                html.Div(
                                    className="d-flex gap-1",
                                    style={"z-index": "1"},
                                    children=[
                                        dbc.Button(
                                            id="btn-view-topology",
                                            className="d-flex gap-1 align-items-center p-3 py-2 rounded-4 border-0",
                                            n_clicks=0,
                                            color=None,
                                            size="sm",
                                            children=[html.I(className="bi bi-map fs-5 me-1"), "Topology"],
                                        ),
                                        dbc.Button(
                                            id="btn-view-projections",
                                            className="d-flex gap-1 align-items-center p-3 py-2 rounded-4 border-0",
                                            n_clicks=0,
                                            color=None,
                                            size="sm",
                                            children=[html.I(className="bi bi-clock-history fs-5 me-1"),
                                                      "Historical Patterns"],
                                        )
                                    ] + registry.extra_view_buttons()
                                ),
                                html.Div(style={"height": "100%", "width": "2px", "background": "#37334a",
                                                "marginLeft": "10px"}),
                                dbc.Button(
                                    id="btn-layer-rhizome",
                                    n_clicks=0,
                                    className="d-flex align-items-center text-white rounded border-0",
                                    style={"padding": ".5rem", "--bs-text-opacity": ".3"},
                                    color=None,
                                    size="sm",
                                    children=[html.I(className="bi bi-bezier2 fs-5")],
                                ),
                                dbc.Tooltip(
                                    "Topological connections",
                                    target="btn-layer-rhizome",
                                    placement="bottom",
                                ),
                                dbc.Button(
                                    id="btn-layer-pad",
                                    n_clicks=0,
                                    className="d-flex align-items-center text-white rounded border-0",
                                    style={"padding": ".5rem", "--bs-text-opacity": ".3"},
                                    color=None,
                                    size="sm",
                                    children=[html.I(className="bi bi-leaf-fill fs-5")],
                                ),
                                dbc.Tooltip(
                                    "Neighbor distances",
                                    target="btn-layer-pad",
                                    placement="bottom",
                                ),
                                dbc.Button(
                                    id="btn-layer-petal",
                                    n_clicks=0,
                                    className="d-flex align-items-center text-white rounded border-0",
                                    style={"padding": ".5rem", "--bs-text-opacity": ".3"},
                                    color=None,
                                    size="sm",
                                    children=[html.I(className="bi bi-flower1 fs-5")],
                                ),
                                dbc.Tooltip(
                                    "Node activations",
                                    target="btn-layer-petal",
                                    placement="bottom",
                                ),
                            ]
                        ),
                        html.Div(
                            className="d-flex flex-grow-1 gap-3",
                            children=[
                                html.Div(
                                    id="observer-toolbar",
                                    className="d-flex flex-column gap-2 alig-items-center rounded",
                                    style={"box-shadow": "inset 0 -5px 10px 1px #1d1a27"},
                                    children=[
                                        dbc.Button(
                                            id="btn-layer-pad-nogap",
                                            n_clicks=0,
                                            className="text-white rounded border-0",
                                            style={"--bs-text-opacity": ".5"},
                                            size="sm",
                                            color=None,
                                            children=[html.I(className="bi bi-arrows-angle-contract")],
                                        ),
                                        dbc.Tooltip(
                                            "Minimize gaps",
                                            target="btn-layer-pad-nogap",
                                            placement="right",
                                        ),
                                        dbc.Button(
                                            id="btn-layer-rhizome-violationonly",
                                            n_clicks=0,
                                            className="text-white rounded border-0",
                                            style={"--bs-text-opacity": ".5"},
                                            size="sm",
                                            color=None,
                                            children=[html.I(className="bi bi-exclamation-triangle-fill")],
                                        ),
                                        dbc.Tooltip(
                                            "Topology violations",
                                            target="btn-layer-rhizome-violationonly",
                                            placement="right",
                                        ),
                                    ]
                                ),
                                html.Div(id='observer-plot-container', style={"flex": "1 1 0", "minWidth": "0", "height": "100%"}),
                            ]
                        )
                    ]
                ),
                html.Div(
                    id='observer-table-container',
                    style={"display": "none"},
                    children=[
                        html.H6(id="observer-table-title", children="Detections", className="mb-3 text-white fw-semibold"),
                        dag.AgGrid(
                            id="observer-table",
                            rowData=[],
                            columnDefs=[],
                            dashGridOptions={
                                "pagination": True,
                                "paginationPageSize": 25,
                                "paginationPageSizeSelector": [10, 25, 50, 100],
                                "rowSelection": "multiple",
                                "suppressRowClickSelection": False,
                                "animateRows": True,
                                "headerHeight": 44,
                                "rowHeight": 40,
                            },
                            defaultColDef={
                                "sortable": True,
                                "filter": True,
                                "resizable": True,
                                "minWidth": 130,
                                "flex": 1,
                                "cellStyle": {"color": "#F1F5F9"},
                            },
                            className="ag-theme-alpine-dark",
                            style={"width": "100%", "height": "100%"},
                        )
                    ]
                )
            ]
        )
    ]
)


@cache.memoize()
def fetch_projection_layer_configs(representation_id):
    from services.map_service import BianorProjectionLayerService
    return BianorProjectionLayerService.list_by_representation(cfg, representation_id)

@cache.memoize()
def fetch_predictions(table, limit:int = 100, offset:int = 0):
    from services.table_service import TableService
    return TableService.list(cfg, table, limit=limit, offset=offset)

@cache.memoize()
def fetch_features(table, ids):
    from services.feature_service import FeatureService
    return FeatureService.list_by_ids(cfg, table, pks=ids)

@cache.memoize()
def fetch_features_by_join(table, join_table):
    from services.feature_service import FeatureService
    return FeatureService.list_by_join(cfg, table, join_table)

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

def create_basin(som_rep):
    return Basin.from_som_representation(som_rep, random_seed=42, verbose=False)

def create_base_pond(basin):
    from lilypond.pond_base_style import PondBaseStyle
    pond_style = PondBaseStyle(
        water_colorscale=[
            [0.0, "#040a14"],
            [1.0, "#164e63"]
        ],
        rhizome_colorscale=[
            [0.0, "#f59e0b"],
            [1.0, "#facc15"]
        ],
        pad_colorscale=[
            [0.0, "#180633"],
            [0.35, "#5b0e8c"],
            [0.65, "#a81b9a"],
            [0.85, "#e13d6a"],
            [1.0, "#f97316"]
        ],
        petal_colorscale=[
            [0.0, "#38bdf8"],
            [1.0, "#bae6fd"]
        ],
        petal_marker=dict(symbol="asterisk", opacity=1, size=15),
        petal_marker_line=dict(width=2),
        petal_halo_marker=dict(symbol="asterisk", color="black", opacity=.6, line=dict(width=6, color="black"))
    )
    return basin.pond(base_style=pond_style)


@dash.callback(
    Output("btn-view-topology", "style"),
    Output("btn-view-projections", "style"),
    Input("plot_config", "data"),
)
def __update_btn_view_style(current_config):
    view = current_config.get("view", None)
    active_states = [view == v for v in ["topology", "projections"]]
    styles = [{"background": "rebeccapurple", "color": "white"} if s else {"background": "none", "color": "grey"} for s
              in active_states]
    return tuple(styles)

@dash.callback(
    Output("btn-layer-rhizome", "style"),
    Output("btn-layer-rhizome-violationonly", "style"),
    Output("btn-layer-pad", "style"),
    Output("btn-layer-petal", "style"),
    Output("btn-layer-pad-nogap", "style"),
    Input("plot_config", "data"),
)
def __update_btn_layer_style(current_config):
    active_states = [current_config.get(f"{k}_active") for k in
                     ["rhizome_layer", "rhizome_layer_violationonly", "pad_layer", "petal_layer", "pad_layer_nogap"]]
    styles = [{"--bs-text-opacity": "1"} if s else {"--bs-text-opacity": ".3"} for s in active_states]
    return tuple(styles)


# ----

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-view-topology", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_view(plot_config, _):
    view = "topology"
    plot_config.update({"view": view})
    return plot_config

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-view-projections", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_view(plot_config, _):
    view = "projections"
    plot_config.update({"view": view})
    return plot_config

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-layer-pad-nogap", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_layer(plot_config, _):
    is_active = plot_config.get("pad_layer_nogap_active", False)
    plot_config.update({"pad_layer_nogap_active": not is_active})
    return plot_config

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-layer-rhizome-violationonly", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_layer(plot_config, _):
    is_active = plot_config.get("rhizome_layer_violationonly_active", False)
    plot_config.update({"rhizome_layer_violationonly_active": not is_active})
    return plot_config


# ----

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-layer-rhizome", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_layer(plot_config, _):
    is_active = plot_config.get("rhizome_layer_active", False)
    plot_config.update({"rhizome_layer_active": not is_active})
    return plot_config

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-layer-pad", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_layer(plot_config, _):
    is_active = plot_config.get("pad_layer_active", False)
    plot_config.update({"pad_layer_active": not is_active})
    return plot_config

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-layer-petal", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_layer(plot_config, _):
    is_active = plot_config.get("petal_layer_active", False)
    plot_config.update({"petal_layer_active": not is_active})
    return plot_config

@dash.callback(
    Output('observer-plot-container', 'children'),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
    Input("plot_config", "data"),
    Input("observer-table", "selectedRows")
)
def __update_plot(selected_map, selected_prediction, plot_config, selected_rows):
    if not selected_map: return html.Span("Select a representation to be visualized.", className="text-white-50")

    view = plot_config.get("view", None)

    som_rep_model_loc = selected_map.get("SOM_MODEL_LOCATION")
    som_rep_model = load_representation(som_rep_model_loc)

    basin = create_basin(som_rep_model)
    pond = create_base_pond(basin)

    if plot_config:
        if plot_config.get("rhizome_layer_active"):
            violationonly = plot_config.get("rhizome_layer_violationonly_active", False)
            pond.rhizome_layer(violations_only=violationonly)
        if plot_config.get("pad_layer_active"):
            nogap = plot_config.get("pad_layer_nogap_active", False)
            pond.pad_layer(gap=("nogap" if nogap else "auto"))
        if plot_config.get("petal_layer_active"):
            pond.petal_layer()
    else:
        pond.rhizome_layer().pad_layer(gap="nogap").petal_layer()

    if view == "projections":
        projection_configs = fetch_projection_layer_configs(selected_map.get("ID"))
        for i, config_record in projection_configs.iterrows():
            X = fetch_features_by_join(table=selected_map["FEATURES_LOCATION"],
                                       join_table=config_record["SAMPLES_LOCATION"])
            X.set_index("id", drop=True, inplace=True)
            scaler = load_scaler(som_rep_model_loc)
            pond.attraction_layer(scaler.transform(X), name=config_record["NAME"],
                                  marker=json.loads(config_record["MARKER_DICT"]))

    selected_ids = [row.get("id") for row in (selected_rows or []) if row.get("id") is not None]
    if selected_prediction and selected_ids:
        X = fetch_features(table=selected_map["FEATURES_LOCATION"], ids=selected_ids)
        X.set_index("id", drop=True, inplace=True)
        scaler = load_scaler(som_rep_model_loc)
        marker = dict(color="white", size=22, symbol="bowtie")
        pond.attraction_layer(scaler.transform(X), marker=marker)

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
    Output("observer-table", "rowData"),
    Output("observer-table", "columnDefs"),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
)
def __populate_prediction_table(selected_map, selected_prediction):
    if not selected_map or not selected_prediction: return [], []
    prediction_table_loc = selected_prediction.get("PREDICTION_LOCATION")

    df_predictions = fetch_predictions(prediction_table_loc, limit=5000, offset=0).copy()
    if df_predictions.empty: return [], []

    df_predictions.columns = [c.lower() for c in df_predictions.columns]
    assert "id" in df_predictions.columns, "Id column is required in prediction table."
    column_defs = [
        {
            "headerName": str(c).lower().capitalize(),
            "field": c,
            "checkboxSelection": c == "id",
            "headerCheckboxSelection": c == "id",
            "minWidth": 150 if c == "id" else 130,
            "flex": 1,
        }
        for c in df_predictions.columns
    ]
    row_data = df_predictions.to_dict('records')
    return row_data, column_defs

@dash.callback(
    Output("observer-table", "selectedRows"),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
)
def __reset_selected_rows(selected_map, selected_prediction):
    return []

@dash.callback(
    Output("observer-table-container", "style"),
    Output("observer-table-title", "children"),
    Input("selected_prediction", "data"),
)
def __toggle_table_container(selected_prediction):
    if not selected_prediction:
        return {"display": "none"}, "Detections"
    pred_name = selected_prediction.get("NAME", "")
    title = f"Detections: {pred_name}" if pred_name else "Detections"
    return {
        "display": "flex",
        "flexDirection": "column",
        "flex": "0 0 520px",
        "minWidth": "460px",
        "maxWidth": "650px",
        "height": "100%",
    }, title
