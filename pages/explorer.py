import json
import dash
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

from dash import dcc, html, Input, Output, State
from lilypond.basin import Basin
from utils.figure_style import style_figure
from registry import registry
from functools import lru_cache

dash.register_page(
    __name__,
    path="/explorer",
    name="Map Explorer",
    icon="bi-map"
)

from cache import cache
from services.backend import get_databricks_config
from utils.demo import is_demo_id, is_demo_model

cfg = get_databricks_config()

def create_plot_config():
    plot_config = dict(
        view="topology",
        rhizome_layer_active=False,
        rhizome_layer_violationonly_active=False,
        pad_layer_active=True,
        pad_layer_nogap_active=True,
        petal_layer_active=False,
        projection_qe_color_active=False,
    )
    return plot_config


layout = lambda: html.Div(
    className="d-flex flex-column h-100 overflow-hidden explorer-page", style={"margin": "-4.7rem 0 0 -8.4rem"},
    children=[
        dcc.Store(id="plot_config", data=create_plot_config()),
        html.Div(
            id="observer-container",
            children=[
                html.Div(
                    className="d-flex flex-column",
                    style={"flex": "1 1 0", "minWidth": "0", "gap": "1.25rem", "paddingTop": "0.65rem"},
                    children=[
                        html.Div(
                            className="observer-chrome observer-view-bar d-flex gap-3 rounded-3 text-white",
                            children=[
                                html.Span(
                                    "View & Layers",
                                    className="observer-chrome-label text-white-50 px-2 py-0 rounded small",
                                ),
                                html.Div(
                                    className="view-controls",
                                    children=[
                                        html.Div(
                                            id="view-switcher",
                                            className="view-switcher view-topology",
                                            children=[
                                                html.Div(className="view-switcher-slider"),
                                                dbc.Button(
                                                    id="btn-view-topology",
                                                    className="d-flex gap-1 align-items-center px-3 py-2 border-0",
                                                    n_clicks=0,
                                                    color=None,
                                                    size="sm",
                                                    children=[html.I(className="bi bi-map me-1"), "Data Landscape"],
                                                ),
                                                dbc.Button(
                                                    id="btn-view-projections",
                                                    className="d-flex gap-1 align-items-center px-3 py-2 border-0",
                                                    n_clicks=0,
                                                    color=None,
                                                    size="sm",
                                                    children=[html.I(className="bi bi-clock-history me-1"),
                                                              "Historical Projections"],
                                                ),
                                                dbc.Button(
                                                    id="btn-view-components",
                                                    className="d-flex gap-1 align-items-center px-3 py-2 border-0",
                                                    n_clicks=0,
                                                    color=None,
                                                    size="sm",
                                                    children=[html.I(className="bi bi-stack me-1"), "Components"],
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            id="components-selector-container",
                                            className="components-selector d-none",
                                            style={"display": "none"},
                                            children=[
                                                dcc.Dropdown(
                                                    id="drp-component-idx",
                                                    className="components-selector-dropdown",
                                                    clearable=False,
                                                    searchable=False,
                                                    placeholder="Feature...",
                                                    optionHeight=32,
                                                    style={"minWidth": "200px", "fontSize": ".8rem", "color": "#1b1824", "cursor": "pointer"},
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ] + registry.extra_view_buttons() + [
                                html.Div(className="observer-view-bar-divider"),
                                dbc.Button(
                                    id="btn-layer-rhizome",
                                    n_clicks=0,
                                    className="d-flex align-items-center text-white rounded border-0",
                                    style={"padding": ".35rem", "--bs-text-opacity": ".3"},
                                    color=None,
                                    size="sm",
                                    children=[html.I(className="bi bi-bezier2")],
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
                                    style={"padding": ".35rem", "--bs-text-opacity": ".3"},
                                    color=None,
                                    size="sm",
                                    children=[html.I(className="bi bi-leaf-fill")],
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
                                    style={"padding": ".35rem", "--bs-text-opacity": ".3"},
                                    color=None,
                                    size="sm",
                                    children=[html.I(className="bi bi-flower1")],
                                ),
                                dbc.Tooltip(
                                    "Training activations",
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
                                    className="observer-chrome d-flex flex-column gap-2 align-items-center rounded-3",
                                    children=[
                                        dbc.Button(
                                            id="btn-projection-qe-color",
                                            n_clicks=0,
                                            className="text-white rounded border-0",
                                            style={"--bs-text-opacity": ".5"},
                                            size="sm",
                                            color=None,
                                            children=[html.I(className="bi bi-rulers")],
                                        ),
                                        dbc.Tooltip(
                                            "Show distances from map",
                                            target="btn-projection-qe-color",
                                            placement="right",
                                        ),
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
                                        html.Div(
                                            id="btn-layer-rhizome-violationonly-wrap",
                                            style={"display": "none"},
                                            children=[
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
                                                    "Focus on violating connections",
                                                    target="btn-layer-rhizome-violationonly",
                                                    placement="right",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(id='observer-plot-container', className="observer-plot-container"),
                            ]
                        )
                    ]
                ),
                html.Div(
                    id='observer-table-container',
                    style={"display": "none"},
                    children=[
                        html.Div(
                            className="d-flex align-items-center justify-content-between mb-2",
                            children=[
                                html.Span(
                                    id="observer-table-title",
                                    children="Points of Interest",
                                    className="text-white-50 fw-semibold text-uppercase",
                                    style={
                                        "fontSize": "0.75rem",
                                        "letterSpacing": "0.06em",
                                        "whiteSpace": "nowrap",
                                        "overflow": "hidden",
                                        "textOverflow": "ellipsis",
                                    },
                                ),
                            ],
                        ),
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
                                "headerHeight": 32,
                                "rowHeight": 30,
                            },
                            defaultColDef={
                                "sortable": True,
                                "filter": True,
                                "resizable": True,
                                "minWidth": 120,
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
    if not representation_id or is_demo_id(representation_id):
        import pandas as pd
        return pd.DataFrame()
    from services.map_service import BianorProjectionLayerService
    return BianorProjectionLayerService.list_by_representation(cfg, representation_id)

@cache.memoize()
def fetch_predictions(table, limit:int = 100, offset:int = 0):
    if not table or is_demo_model(table):
        import pandas as pd
        return pd.DataFrame(columns=["id"])
    from services.table_service import TableService
    return TableService.list(cfg, table, limit=limit, offset=offset)

@cache.memoize()
def fetch_features(table, ids):
    if not table or is_demo_model(table):
        import pandas as pd
        return pd.DataFrame()
    from services.feature_service import FeatureService
    return FeatureService.list_by_ids(cfg, table, pks=ids)

@cache.memoize()
def fetch_features_by_join(table, join_table):
    from services.feature_service import FeatureService
    return FeatureService.list_by_join(cfg, table, join_table)

@lru_cache(maxsize=3)
def load_model(model_loc):
    from services.model_service import ModelService
    return ModelService.load(model_loc)

@lru_cache(maxsize=3)
def load_representation(model_loc):
    model = load_model(model_loc)
    som_rep = model.model
    return som_rep

@lru_cache(maxsize=3)
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
            [0.0, "#1d2127"],
            [1.0, "#10141a"],
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
    Output("view-switcher", "className"),
    Input("plot_config", "data"),
)
def __update_btn_view_style(current_config):
    view = (current_config or {}).get("view", "topology")
    if view not in ("topology", "projections", "components"):
        view = "topology"
    return f"view-switcher view-{view}"

@dash.callback(
    Output("btn-layer-rhizome", "style"),
    Output("btn-layer-rhizome-violationonly", "style"),
    Output("btn-layer-pad", "style"),
    Output("btn-layer-petal", "style"),
    Output("btn-layer-pad-nogap", "style"),
    Output("btn-projection-qe-color", "style"),
    Output("btn-layer-rhizome-violationonly-wrap", "style"),
    Input("plot_config", "data"),
)
def __update_btn_layer_style(current_config):
    current_config = current_config or {}
    active_states = [current_config.get(f"{k}_active") for k in
                     ["rhizome_layer", "rhizome_layer_violationonly", "pad_layer", "petal_layer", "pad_layer_nogap", "projection_qe_color"]]
    styles = [{"--bs-text-opacity": "1"} if s else {"--bs-text-opacity": ".3"} for s in active_states]
    rhizome_wrap = {} if current_config.get("rhizome_layer_active") else {"display": "none"}
    return (*styles, rhizome_wrap)


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
    Input("btn-view-components", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_view(plot_config, _):
    view = "components"
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

@dash.callback(
    Output("plot_config", "data", allow_duplicate=True),
    State("plot_config", "data"),
    Input("btn-projection-qe-color", "n_clicks"),
    prevent_initial_call=True
)
def __handle_btn_projection_qe_color(plot_config, _):
    is_active = plot_config.get("projection_qe_color_active", False)
    plot_config.update({"projection_qe_color_active": not is_active})
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
    if is_active:
        plot_config.update({"rhizome_layer_violationonly_active": False})
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
    Output("drp-component-idx", "options"),
    Output("drp-component-idx", "value"),
    Output("components-selector-container", "style"),
    Output("components-selector-container", "className"),
    Input("selected_map", "data"),
    Input("plot_config", "data"),
    State("drp-component-idx", "value"),
)
def __update_component_selector(selected_map, plot_config, current_component_idx):
    view = (plot_config or {}).get("view")
    if not selected_map or view != "components":
        return [], current_component_idx, {"display": "none"}, "components-selector d-none"

    som_rep_model_loc = selected_map.get("SOM_MODEL_LOCATION")
    som_rep_model = load_representation(som_rep_model_loc)
    basin = create_basin(som_rep_model)

    n_components = getattr(basin.som_representation, "component_size_", None)
    
    if n_components is None:
        n_components = 0

    scaler = load_scaler(som_rep_model_loc)
    feat_names = getattr(scaler, "feature_names_in_", None)

    options = [
        {
            "label": f"Feature {i + 1}" + (f": {feat_names[i]}" if feat_names is not None and i < len(feat_names) else ""),
            "value": i
        }
        for i in range(n_components)
    ]

    val = current_component_idx if (current_component_idx is not None and current_component_idx < n_components) else 0
    return options, val, {"display": "flex"}, "components-selector d-flex"

@dash.callback(
    Output('observer-plot-container', 'children'),
    Input("selected_map", "data"),
    Input("selected_prediction", "data"),
    Input("plot_config", "data"),
    Input("drp-component-idx", "value"),
    Input("observer-table", "selectedRows")
)
def __update_plot(selected_map, selected_prediction, plot_config, selected_component_idx, selected_rows):
    if not selected_map:
        return html.Div(
            className="observer-empty",
            children=[
                html.I(className="bi bi-map observer-empty-icon"),
                html.Span("Select a representation", className="observer-empty-title"),
                html.Span("Choose one from the dropdown to visualize it here", className="observer-empty-hint"),
            ],
        )

    view = plot_config.get("view", None)
    comp_idx = selected_component_idx if selected_component_idx is not None else 0
    qe_based_coloring = bool(plot_config.get("projection_qe_color_active", False))

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
            if view == "components":
                pond.pad_layer(gap=("nogap" if nogap else "auto"), colorscale="RdYlGn", color_by=dict(feature_idx=comp_idx))
            else:
                pond.pad_layer(gap=("nogap" if nogap else "auto"))
        if plot_config.get("petal_layer_active"):
            pond.petal_layer()
    else:
        if view == "components":
            pond.rhizome_layer().pad_layer(gap="nogap", colorscale="RdYlGn", color_by=dict(feature_idx=comp_idx)).petal_layer()
        else:
            pond.rhizome_layer().pad_layer(gap="nogap").petal_layer()

    if view == "projections":
        scaler = load_scaler(som_rep_model_loc)
        projections = []
        if is_demo_id(selected_map.get("ID")):
            for proj in getattr(load_model(som_rep_model_loc), "projections", None) or []:
                projections.append({
                    "X": scaler.transform(proj["data"]),
                    "name": proj["name"],
                    "marker": proj["marker"],
                })
        else:
            projection_configs = fetch_projection_layer_configs(selected_map.get("ID"))
            for _, config_record in projection_configs.iterrows():
                X_numeric = fetch_features_by_join(table=selected_map["FEATURES_LOCATION"],
                                           join_table=config_record["SAMPLES_LOCATION"])
                X_numeric.set_index("id", drop=True, inplace=True)
                X_numeric = X_numeric.copy()

                meta_cols_raw = config_record.get("META_COLUMNS")
                if pd.notna(meta_cols_raw):
                    meta_cols = [c.strip() for c in meta_cols_raw.split(",") if c.strip()]
                    drop_cols = [c for c in meta_cols if c in X_numeric.columns]
                    if drop_cols:
                        X_numeric.drop(columns=drop_cols, inplace=True)
                
                scaler = load_scaler(som_rep_model_loc)
                projections.append({
                    "X": scaler.transform(X_numeric),
                    "name": config_record["NAME"],
                    "marker": json.loads(config_record["MARKER_DICT"]),
                })
        
        if qe_based_coloring:
            if projections:
                X_merged = np.vstack([proj["X"] for proj in projections])
                marker = dict(size=15, line=dict(width=2.5, color="black"))
                pond.attraction_layer(X_merged, name="Projections", marker=marker, color_by_quantization_error=True)
        else:
            for proj in projections:
                pond.attraction_layer(proj["X"], name=proj["name"], marker=proj.get("marker"))

    selected_ids = [row.get("id") for row in (selected_rows or []) if row.get("id") is not None]
    if selected_prediction and selected_ids:
        X_numeric = fetch_features(table=selected_map["FEATURES_LOCATION"], ids=selected_ids)
        X_numeric.set_index("id", drop=True, inplace=True)
        scaler = load_scaler(som_rep_model_loc)
        marker = dict(size=22, symbol="bowtie", line=dict(width=2.5, color="black")) if qe_based_coloring else dict(color="white", size=22, symbol="bowtie")
        pond.attraction_layer(scaler.transform(X_numeric), marker=marker, color_by_quantization_error=qe_based_coloring, colorbar_title="Quantization Error (⋈)")

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
        return {"display": "none"}, "Points of Interest"
    pred_name = selected_prediction.get("NAME", "")
    title = f"Points of Interest: {pred_name}" if pred_name else "Points of Interest"
    return {
        "display": "flex",
        "flexDirection": "column",
        "flex": "0 0 480px",
        "minWidth": "380px",
        "maxWidth": "380px",
        "height": "100%",
        "paddingTop": "0.65rem",
    }, title
