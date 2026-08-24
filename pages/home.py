import dash
import dash_bootstrap_components as dbc

from dash import html, dcc

dash.register_page(
    __name__,
    path="/",
    name="Home",
    icon="bi-house-door"
)

title_header = "Welcome to Bianor"
taglines = [
    "Bianor is an open-source application that fuses **data visualization** with **anomaly detection** and **contextualization**.",
    ("To do so, `MiniSom` models are used for data representations, `lilypond` for visualization, ",
     "while the anomaly predictions can be produced by any custom model registered in the Databricks catalog.")
]

layout = html.Div(
    children=[
        html.H3(title_header, className="mb-4"),
        dcc.Markdown(taglines[0]),
        dcc.Markdown(taglines[1]),
        html.Div(
            id="home-link-container",
            className="d-flex gap-3",
            style={"marginTop": "2rem"},
            children=[
                dbc.Button([html.I(className="bi bi-flask-fill me-2"), "About Ophelia R&D"], outline=True, color="danger",
                           size="md", href="https://github.com/ophelia-rnd", target="_blank"),
                dbc.Button([html.I(className="bi bi-github me-2"), "Bianor"], outline=True, color="primary",
                           size="md", href="https://github.com/ophelia-rnd/bianor", target="_blank"),
                dbc.Button([html.I(className="bi bi-github me-2"), "Lilypond"], outline=True, color="success",
                           size="md", href="https://github.com/ophelia-rnd/lilypond", target="_blank"),
                dbc.Button([html.I(className="bi bi-github me-2"), "MiniSom"], outline=True, color="secondary",
                           size="md", href="https://github.com/JustGlowing/minisom", target="_blank"),
                dbc.Button([html.I(className="bi bi-stack me-2"), "Databricks"], outline=True, color="secondary",
                           size="md", href="https://www.databricks.com/", target="_blank"),
                dbc.Button([html.I(className="bi bi-linkedin")], outline=True, color="primary",
                           size="md", href="https://linkedin.com/company/ophelia-rnd", target="_blank"),
                dbc.Button([html.I(className="bi bi-envelope-at")], outline=True, color="primary",
                           size="md", href="mailto:matebalogh@ophelia-rnd.dev", target="_blank"),
            ]
        )
    ]
)
