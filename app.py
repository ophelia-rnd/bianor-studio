import os
import dash
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, State, ALL
from registry import registry
from constants.demo import (
    DEMO_DATASET_OPTIONS,
    DEMO_DEFAULT_DATASET,
    DEMO_MIN_EPOCHS,
    DEMO_MAX_EPOCHS,
    DEMO_DEFAULT_EPOCHS,
    DEMO_MAP_SIZE_OPTIONS,
    DEMO_DEFAULT_MAP_SIZE,
)
from utils.demo import (
    is_demo_id,
    get_cached_demo_maps,
    get_cached_demo_map,
    train_and_cache_demo,
)

def load_verify_env():
    import os
    from services.backend import catalog_path, is_local, local_root
    if is_local():
        root = local_root()
        assert root.is_dir(), f"BIANOR_LOCAL_CATALOG_ROOT does not exist or is not a directory: {root}"
        path = catalog_path()
        assert path.is_file(), f"catalog.yaml not found under BIANOR_LOCAL_CATALOG_ROOT: {path}"
        return
    assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in environment."
    assert os.getenv('BIANOR_DATABRICKS_CATALOG'), "BIANOR_DATABRICKS_CATALOG must be set in environment."
    assert os.getenv('BIANOR_DATABRICKS_SCHEMA'), "BIANOR_DATABRICKS_SCHEMA must be set in environment."

def setup_app():
    from services.backend import get_databricks_config
    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.PULSE, (
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/"
            "font/bootstrap-icons.min.css"
        )],
        suppress_callback_exceptions=True
    )
    cfg = get_databricks_config()
    return "Bianor", cfg, app

from cache import cache, clear_cache


load_verify_env()
APP_NAME, cfg, app = setup_app()
server = app.server
cache.init_app(server)


def serve_layout():
    navbar = dbc.Navbar(
        id="navbar",
        color=None,
        style={"marginBottom": "1rem"},
        children=html.Div(
            className="d-flex align-items-center w-100",
            children=[
                html.Div(
                    id="branding-container",
                    className="d-flex align-items-center",
                    children=[
                        dbc.Button(
                            html.I(className="bi bi-layout-sidebar text-white"),
                            id="btn-sidebar-toggle",
                            style={"marginTop": ".4rem"},
                            color="link",
                            className="border-0 text-decoration-none me-1",
                            n_clicks=0,
                        ),
                        html.Div(
                            className="d-flex flex-column align-items-end",
                            style={"marginRight": "20px"},
                            children=[
                                html.A(html.Img(src="assets/bianor_branding_dark.png", height="25px")),
                                html.Div(
                                    registry.edition_badge_func(),
                                    style={"height": "0px", "marginTop": "-.5rem"} 
                                )
                            ]
                        )
                    ],
                ),
                html.Div(
                    className="d-flex align-items-center flex-grow-1",
                    style={"marginTop": ".9rem"},
                    children=[
                        html.Div(
                            className="d-flex align-items-center gap-2",
                            children=[
                                html.Span("/", className="text-white-50", style={"fontSize": ".8rem"}),
                                dcc.Dropdown(
                                    id="drp-map",
                                    className="dropdown",
                                    searchable=False,
                                    options=[],
                                    placeholder="Select Representation...",
                                    optionHeight = 40,
                                    style={"fontSize": ".8rem", "cursor": "pointer", "border": "none"},
                                ),
                                html.Span("/", className="text-white-50", style={"fontSize": ".8rem"}),
                                dcc.Dropdown(
                                    id="drp-prediction",
                                    className="dropdown",
                                    searchable=False,
                                    placeholder="Select Predictions...",
                                    optionHeight = 40,
                                    style={"fontSize": ".8rem", "cursor": "pointer", "border": "none"},
                                    disabled=True
                                )
                            ]
                        ),
                        html.A(
                            [
                                html.I(className="bi bi-book me-1"),
                                html.Span("Documentation", className="ms-1"),
                            ],
                            href="https://bianor-documentation.onrender.com",
                            target="_blank",
                            className="ms-auto me-2 d-flex align-items-center text-decoration-none navbar-doc-btn",
                        ),
                        registry.navbar_cta()
                    ]
                )
            ]
        )
    )

    sidebar = html.Div(
        id="sidebar",
        style={},
        children=[
            dbc.Button(
                id="btn-create",
                className="text-start d-flex align-items-center text-white",
                n_clicks=0,
                color=None,
                size="sm",
                children=[html.I(className="bi bi-plus-lg fs-5 me-1", style={"color": "#a855f7"}), "New"],
            ),
            dbc.Button(
                id="btn-quick-demo",
                className="text-start d-flex align-items-center text-white",
                n_clicks=0,
                color=None,
                size="sm",
                children=[html.I(className="bi bi-magic fs-5 me-1", style={"color": "#d946ef"}), "Quick Demo"],
            ),
            dbc.Modal(
                id="mdl-create",
                is_open=False,
                children=[
                    dbc.ModalHeader(dbc.ModalTitle("New Representation")),
                    dbc.ModalBody([
                        "In order to populate your Bianor application with additional models and layers, refer to the ",
                        html.A("Documentation", href="https://bianor-documentation.onrender.com", target="_blank"),
                        "."
                    ]),
                    dbc.ModalFooter([
                        html.Span(
                            html.A("More about Bianor", href="https://bianor.ophelia-rnd.dev", target="_blank"),
                            className="me-auto small text-muted"
                        ),
                        dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
                    ])
                ]
            ),
            dbc.Modal(
                id="mdl-quick-demo",
                is_open=False,
                children=[
                    dbc.ModalHeader(dbc.ModalTitle("Quick Demo")),
                    dbc.ModalBody([
                        html.P("Select a toy dataset to instantly map it into a 2D representation to be explored.", className="text-muted small"),
                        dcc.Dropdown(
                            id="drp-demo-dataset",
                            options=DEMO_DATASET_OPTIONS,
                            value=DEMO_DEFAULT_DATASET,
                            clearable=False,
                            searchable=False,
                            className="mb-3"
                        ),
                        html.P(f"Number of epochs ({DEMO_MIN_EPOCHS}-{DEMO_MAX_EPOCHS}):", className="text-muted small mb-1"),
                        dbc.Input(
                            id="inp-demo-epoch",
                            type="number",
                            min=DEMO_MIN_EPOCHS,
                            max=DEMO_MAX_EPOCHS,
                            step=1,
                            value=DEMO_DEFAULT_EPOCHS,
                            className="mb-3"
                        ),
                        html.P("Map Size:", className="text-muted small mb-1"),
                        dbc.RadioItems(
                            id="rad-demo-map-size",
                            options=DEMO_MAP_SIZE_OPTIONS,
                            value=DEMO_DEFAULT_MAP_SIZE,
                            inline=True,
                            className="mb-3"
                        ),
                    ]),
                    dbc.ModalFooter([
                        dbc.Button("Cancel", id="btn-demo-cancel", color="light", n_clicks=0, className="me-2"),
                        dbc.Button("Map & Explore", id="btn-demo-run", color="primary", n_clicks=0)
                    ])
                ]
            ),
            registry.premium_modal(),
            dbc.Nav(
                vertical=True,
                className="small mb-3",
                children=[
                    dbc.NavLink([html.I(className="bi bi-house-door me-2"), "Home"], href="/", id="nav-home", active="exact", className="text-white"),
                    dbc.NavLink([html.I(className="bi bi-map me-2"), "Explorer"], href="/explorer", id="nav-explorer", active="exact", className="text-white"),
                    dbc.NavLink([html.I(className="bi bi-collection me-2"), "Catalog"], href="/catalog", id="nav-maps", active="exact", className="text-white"),
                    dbc.NavLink([html.I(className="bi bi-info-circle me-2"), "About"], href="/about", id="nav-about", active="exact", className="text-white"),
                ]
            )
        ]
    )

    return html.Div(
        id="main-container",
        className="d-flex flex-column min-vh-100",
        children=[
            dcc.Store(id="selected_map"),
            dcc.Store(id="selected_prediction"),
            dcc.Store(id="trigger-training"),
            navbar,
            html.Div(
                id="body-container",
                className="d-flex flex-grow-1",
                children=[sidebar, dash.page_container],
            ),
            dbc.Modal(
                id="mdl-training-progress",
                is_open=False,
                backdrop="static",
                keyboard=False,
                centered=True,
                contentClassName="bg-transparent border-0 shadow-none",
                children=[
                    dbc.ModalBody(
                        className="d-flex flex-column align-items-center justify-content-center p-5",
                        children=[
                            dbc.Spinner(color="primary", spinner_style={"width": "4rem", "height": "4rem", "borderWidth": "0.4em"}),
                            html.H4("Mapping Data...", className="mt-4 fw-bold text-white shadow-sm"),
                            html.P("Please wait while the map is being generated.", className="text-white-50 mb-0")
                        ]
                    )
                ]
            )
        ]
    )

app.layout = serve_layout

@cache.memoize()
def fetch_map_configs():
    from services.map_service import BianorRepresentationService
    return BianorRepresentationService.list(cfg)

@cache.memoize()
def fetch_prediction_configs(selected_map_id):
    if not selected_map_id or is_demo_id(selected_map_id):
        import pandas as pd
        return pd.DataFrame()
    from services.map_service import BianorPredictionService
    return BianorPredictionService.list_by_representation(cfg, representation_id=selected_map_id)

@app.callback(
    Output("mdl-create", "is_open"),
    [Input("btn-create", "n_clicks"), Input("close", "n_clicks")],
    [State("mdl-create", "is_open")],
) # FIXME
def __open_create_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("btn-demo-run", "disabled"),
    Input("inp-demo-epoch", "value"),
)
def __validate_demo_epoch(epoch):
    if epoch is None:
        return True
    try:
        epoch = int(epoch)
        return not (DEMO_MIN_EPOCHS <= epoch <= DEMO_MAX_EPOCHS)
    except ValueError:
        return True

@app.callback(
    Output("mdl-quick-demo", "is_open"),
    [Input("btn-quick-demo", "n_clicks"), Input("btn-demo-cancel", "n_clicks"), Input("btn-demo-run", "n_clicks")],
    [State("mdl-quick-demo", "is_open")],
)
def __toggle_demo_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open

@app.callback(
    Output("mdl-premium", "is_open"),
    [
        Input({"type": "open-premium-modal", "index": ALL}, "n_clicks"),
    ],
    [State("mdl-premium", "is_open")],
    prevent_initial_call=True,
)
def __toggle_premium_modal(cta_clicks, is_open):
    if not dash.ctx.triggered:
        return is_open
    for trigger in dash.ctx.triggered:
        prop_id = trigger.get("prop_id", "")
        value = trigger.get("value")
        if "open-premium-modal" in prop_id and value:
            return True
    return is_open

@app.callback(Output("sidebar", "style"),
    Input("btn-sidebar-toggle", "n_clicks"),
    State("sidebar", "style")
)
def __toggle_sidebar(n_clicks, current_style):
    if not n_clicks: return current_style
    is_hidden = current_style.get("display") == "none"
    current_style["display"] = "flex" if is_hidden else "none"
    return current_style

def get_map_options():
    map_df = fetch_map_configs()
    options = [{"label": item["NAME"], "value": item["ID"]} for idx, item in map_df.iterrows()]
    for d in get_cached_demo_maps(cache):
        if not any(opt["value"] == d["ID"] for opt in options):
            options.append({"label": d["NAME"], "value": d["ID"]})
    return options


def get_map_by_id(selected_map_id):
    if not selected_map_id:
        return None
    if is_demo_id(selected_map_id):
        return get_cached_demo_map(selected_map_id, cache)
    maps_df = fetch_map_configs()
    matches = maps_df.loc[maps_df["ID"] == selected_map_id]
    if not matches.empty:
        return matches.iloc[0].to_dict()
    return None


@app.callback(
    Output("drp-map", "options"),
    Input("drp-map", "id"),
)
def __update_drp_map_options(_):
    return get_map_options()


@app.callback(
    Output("drp-prediction", "options"),
    Output("drp-prediction", "value"),
    Output("drp-prediction", "disabled"),
    Output("drp-prediction", "style"),
    Input("drp-map", "value"),
    State("drp-prediction", "style")
)
def __update_drp_prediction_options(selected_map_id, current_style):
    pred_df = fetch_prediction_configs(selected_map_id)
    options = [{"label": item["NAME"], "value": item["ID"]} for idx, item in pred_df.iterrows()]
    is_disabled = len(options) == 0
    current_style["visibility"] = "visible" if not is_disabled else "hidden"
    return options, None, is_disabled, current_style


@app.callback(
    Output("selected_map", "data"),
    Input("drp-map", "value"),
)
def __store_selected_map(selected_map_id):
    return get_map_by_id(selected_map_id)


@app.callback(
    Output("selected_prediction", "data"),
    State("selected_map", "data"),
    Input("drp-prediction", "value"),
)
def __store_selected_prediction(selected_map, selected_pred_id):
    if not selected_map or not selected_pred_id: return None
    pred_df = fetch_prediction_configs(selected_map_id=selected_map["ID"])
    selected_pred = pred_df.loc[pred_df["ID"] == selected_pred_id].iloc[0].to_dict()
    return selected_pred


@app.callback(
    Output("trigger-training", "data"),
    Output("mdl-training-progress", "is_open"),
    Input("btn-demo-run", "n_clicks"),
    State("drp-demo-dataset", "value"),
    State("inp-demo-epoch", "value"),
    State("rad-demo-map-size", "value"),
    prevent_initial_call=True
)
def __start_training(n_clicks, dataset, epoch, map_size_factor):
    if not n_clicks:
        return dash.no_update, dash.no_update
    return (
        {"dataset": dataset, "epoch": epoch, "map_size_factor": map_size_factor},
        True
    )


@app.callback(
    Output("drp-map", "options", allow_duplicate=True),
    Output("drp-map", "value", allow_duplicate=True),
    Output("selected_map", "data", allow_duplicate=True),
    Output("_pages_location", "pathname", allow_duplicate=True),
    Output("mdl-training-progress", "is_open", allow_duplicate=True),
    Output("selected_prediction", "data", allow_duplicate=True),
    Output("drp-prediction", "value", allow_duplicate=True),
    Input("trigger-training", "data"),
    prevent_initial_call=True
)
def __run_quick_demo(training_data):
    if not training_data:
        return (
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update, dash.no_update
        )

    import time
    start_time = time.time()

    dataset_name = training_data["dataset"]
    epoch = training_data["epoch"]
    map_size_factor = training_data.get("map_size_factor", 1.0)

    demo_map = train_and_cache_demo(dataset_name, epoch, map_size_factor, cache)

    elapsed = time.time() - start_time
    if elapsed < 3.0:
        time.sleep(3.0 - elapsed)

    updated_options = get_map_options()

    return (
        updated_options,
        demo_map["ID"],
        demo_map,
        "/explorer",
        False,
        None,
        None,
    )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Bianor Dash application.")
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the configured CACHE_DIR before starting the application.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        dest="debug_mode",
        default=os.getenv("DEBUG_MODE", "false").lower() in ("true", "1"),
        help="Run Dash in debug mode.",
    )
    cli_args, _ = parser.parse_known_args()
    if cli_args.clear_cache and os.getenv("WERKZEUG_RUN_MAIN") != "true":
        clear_cache()

    debug_mode = cli_args.debug_mode
    port=os.getenv("SERVER_PORT", None)
    app.run(debug=debug_mode, port=port)
