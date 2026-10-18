import dash_bootstrap_components as dbc
from dash import html
from version import __version__

class AppRegistry:
    def __init__(self, version=__version__):
        self.version = version
        self.edition_name = "Community Edition"
        self.edition_badge_func = lambda: dbc.Badge("COMMUNITY", color=None, className="shadow-sm", style={"color": "#a855f7", "padding": "0", "fontSize": ".45rem", "fontWeight": "bold", "letterSpacing": ".5px"})
        
        self.navbar_cta = lambda: dbc.Button(
            [
                html.I(className="bi bi-lightning-charge-fill text-warning"),
                html.Span("Contact the Team for More", className="fw-semibold ms-1"),
            ],
            id={"type": "open-premium-modal", "index": "navbar"},
            n_clicks=0,
            className="me-2 d-flex align-items-center text-decoration-none text-warning navbar-cta",
            color=None,
            size="sm",
        )
        
        self.about_page_callout = lambda: html.Div([
            html.I(className="bi bi-lock-fill text-warning me-2"),
            html.Span("Using Community Edition. ", className="text-white-50"),
            dbc.Button([
                "Contact the Team"
            ], id={"type": "open-premium-modal", "index": "about"}, n_clicks=0, color="link", className="text-warning text-decoration-none fw-bold p-0 align-baseline", style={"cursor": "pointer"}),
            html.Span(" to unlock advanced features.", className="text-white-50")
        ], className="mt-3 mb-4 p-3 small rounded", style={"backgroundColor": "rgba(255, 193, 7, 0.1)", "border": "1px solid rgba(255, 193, 7, 0.3)"})

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
                            className="text-warning fw-bold text-decoration-none"
                        )   
                    ], className="p-3 rounded border border-secondary mb-2")
                ]),
            ]
        )

        self.extra_view_buttons = lambda: []

registry = AppRegistry()
