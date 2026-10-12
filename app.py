import os
import dash
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, State, ALL
from registry import registry

def load_verify_env():
    from dotenv import load_dotenv
    load_dotenv()
    assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in environment."
    assert os.getenv('BIANOR_DATABRICKS_CATALOG'), "BIANOR_DATABRICKS_CATALOG must be set in environment."
    assert os.getenv('BIANOR_DATABRICKS_SCHEMA'), "BIANOR_DATABRICKS_SCHEMA must be set in environment."

def setup_app():
    from databricks.sdk.core import Config
    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.PULSE, (
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/"
            "font/bootstrap-icons.min.css"
        )],
        suppress_callback_exceptions=True
    )
    return "Bianor", Config(), app

def setup_cache(app):
    from flask_caching import Cache
    timeout = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))
    return Cache(
        app.server,
        config={
            "CACHE_TYPE": "FileSystemCache",
            "CACHE_DIR": ".bianor_cache",
            "CACHE_DEFAULT_TIMEOUT": timeout,
        }
    )

load_verify_env()
APP_NAME, cfg, app = setup_app()
server = app.server
cache = setup_cache(app)


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
            dbc.Modal(
                id="mdl-create",
                is_open=False,
                children=[
                    dbc.ModalHeader(dbc.ModalTitle("New Representation")),
                    dbc.ModalBody([
                        "In order to populate your Bianor application with additional models and layers, use the ",
                        html.A("bianor-databricks-kit", href="https://github.com/ophelia-rnd/bianor-databricks-kit", target="_blank"),
                        " toolkit."
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
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="selected_map"),
            dcc.Store(id="selected_prediction"),
            navbar,
            html.Div(
                id="body-container",
                className="d-flex flex-grow-1",
                children=[sidebar, dash.page_container],
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

@app.callback(Output("drp-map", "options"),
    Input("drp-map", "id"),
)
def __update_drp_map_options(_):
    map_df = fetch_map_configs()
    options = [{"label": item["NAME"], "value": item["ID"]} for idx, item in map_df.iterrows()]
    return options

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
    if not selected_map_id: return None
    maps_df = fetch_map_configs()
    selected_map = maps_df.loc[maps_df["ID"] == selected_map_id].iloc[0].to_dict()
    return selected_map

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

if __name__ == "__main__":
    debug = os.getenv("DEBUG_MODE", "false").lower() in ("true", "1")
    app.run(debug=debug)
