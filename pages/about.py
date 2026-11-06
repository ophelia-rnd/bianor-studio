import dash
import dash_bootstrap_components as dbc
from dash import html

from registry import registry

dash.register_page(__name__, path="/about", title="About Bianor")

def layout():
    ver = registry.version() if callable(registry.version) else registry.version

    return html.Div(
        children=[
            html.Div(
                className="p-4 rounded shadow-sm",
                style={
                    "backgroundColor": "#1a1d23",
                    "border": "1px solid #2d3139",
                    "maxWidth": "500px",
                },
                children=[
                    html.Div(
                        className="d-flex align-items-center justify-content-between mb-3",
                        children=[
                            html.Img(src="assets/bianor_branding_dark.png", height="24px"),
                            dbc.Badge(
                                f"{registry.edition_name} v{ver}",
                                color=None,
                                className="shadow-sm",
                                style={
                                    "color": "#94a3b8",
                                    "backgroundColor": "rgba(148, 163, 184, 0.12)",
                                    "border": "1px solid rgba(148, 163, 184, 0.2)",
                                    "padding": ".25rem .55rem",
                                    "fontSize": ".7rem",
                                    "fontWeight": "600",
                                    "letterSpacing": ".5px",
                                    "borderRadius": "4px",
                                },
                            ),
                        ],
                    ),
                    html.P(
                        "Interactive visual exploration and contextualization of high-dimensional datasets via Self-Organizing Maps.",
                        className="text-white-50 small mb-3",
                        style={"lineHeight": "1.5"},
                    ),
                    html.Hr(style={"borderColor": "#2d3139", "margin": "1rem 0"}),
                    html.Div(
                        className="d-flex align-items-center justify-content-between",
                        children=[
                            html.Small(
                                "© 2026 Bianor",
                                style={"color": "#64748b", "fontSize": ".75rem"},
                            ),
                            html.Div(
                                className="d-flex gap-3 align-items-center",
                                children=[
                                    html.A(
                                        [html.I(className="bi bi-github me-1"), "GitHub"],
                                        href="https://github.com/ophelia-rnd/bianor-studio",
                                        target="_blank",
                                        className="text-decoration-none small",
                                        style={"color": "#94a3b8", "fontSize": ".75rem"},
                                    ),
                                    html.A(
                                        [html.I(className="bi bi-book me-1"), "Docs"],
                                        href="https://bianor-documentation.onrender.com",
                                        target="_blank",
                                        className="text-decoration-none small",
                                        style={"color": "#94a3b8", "fontSize": ".75rem"},
                                    ),
                                    dbc.Button(
                                        [html.I(className="bi bi-envelope me-1"), "Contact"],
                                        id={"type": "open-premium-modal", "index": "about"},
                                        n_clicks=0,
                                        color="link",
                                        className="text-decoration-none p-0 small",
                                        style={"color": "#5eead4", "fontSize": ".75rem"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
