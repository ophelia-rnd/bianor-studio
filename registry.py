import dash_bootstrap_components as dbc
from dash import html
from version import __version__

class AppRegistry:
    def __init__(self, version=__version__):
        self.version = version
        self.edition_name = "Studio"
        self.edition_badge_func = lambda: dbc.Badge("STUDIO", color=None, className="shadow-sm", style={"color": "#94a3b8", "backgroundColor": "rgba(148, 163, 184, 0.12)", "padding": ".15rem .5rem", "fontSize": ".42rem", "fontWeight": "600", "letterSpacing": "1px", "borderRadius": "4px"})
        
        self.navbar_cta = lambda: dbc.Button(
            html.I(className="bi bi-cup-hot"),
            id={"type": "open-premium-modal", "index": "navbar"},
            n_clicks=0,
            className="d-flex align-items-center justify-content-center text-decoration-none navbar-cta",
            color=None,
            size="sm",
        )
        
        self.about_page_callout = lambda: None

        self.premium_modal = lambda: dbc.Modal(
            id="mdl-premium",
            is_open=False,
            children=[
                dbc.ModalHeader(dbc.ModalTitle([
                    "Contact the Team"
                ])),
                dbc.ModalBody([
                    html.P(
                        "Contact the Team to unlock advanced features and custom solutions.",
                    ),
                    html.Div([
                        html.A(
                            [html.I(className="bi bi-envelope-fill me-1"), "hello@ophelia-rnd.dev"],
                            href="mailto:hello@ophelia-rnd.dev?subject=Inquiry%20About%20Bianor%20Solutions",
                            className="fw-bold text-decoration-none",
                            style={"color": "#00a088"},
                        )   
                    ], className="p-3 rounded border border-secondary mb-2")
                ]),
            ]
        )

        self.extra_view_buttons = lambda: []

registry = AppRegistry()
