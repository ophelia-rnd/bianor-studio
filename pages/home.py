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
    "Bianor fuses **data visualization** and **contextualization** with **anomaly detection**.",
    ("In Bianor, `MiniSom` and `SomRepresentation` models are visualized via `lilypond`, a tool that provides enhanced _Self-Organizing Map (SOM)_ displays. "
     "Additionally, pre-configured historical patterns and points of interest such as **class distributions** and **anomalies** are projected onto the representations. "
     "All representations, historical pattern layers, anomaly detectors source from your _Databricks_ catalog. ")
]

layout = html.Div(
    children=[
        html.H3(title_header, className="mb-4"),
        dcc.Markdown(taglines[0]),
        dcc.Markdown(taglines[1]),
        html.Div(
            className="d-flex gap-3",
            style={"marginTop": "2rem", "flex-wrap": "wrap"},
            children=[
                dbc.Button([html.I(className="bi bi-newspaper me-2"), "About Bianor"], outline=True, color="secondary",
                           size="md", href="https://bianor.ophelia-rnd.dev", target="_blank"),
                dbc.Button([html.I(className="bi bi-flask-fill me-2"), "About Ophelia R&D"], outline=True, color="primary",
                           size="md", href="https://github.com/ophelia-rnd", target="_blank"),
                dbc.Button([html.I(className="bi bi-linkedin")], outline=True, color="info",
                           size="md", href="https://linkedin.com/company/ophelia-rnd", target="_blank"),
                dbc.Button([html.I(className="bi bi-envelope-at")], outline=True, color="info",
                           size="md", href="mailto:matebalogh@ophelia-rnd.dev", target="_blank"),
            ]
        ),
        html.Div(
            className="d-flex gap-3",
            style={"marginTop": "1.25rem", "flex-wrap": "wrap"},
            children=[
                dbc.Button([html.I(className="bi bi-github me-2"), "Bianor"], outline=True, color="secondary",
                           size="md", href="https://github.com/ophelia-rnd/bianor-databricks", target="_blank"),
                dbc.Button([html.I(className="bi bi-github me-2"), "Lilypond"], outline=True, color="success",
                           size="md", href="https://github.com/ophelia-rnd/lilypond", target="_blank"),
                dbc.Button([html.I(className="bi bi-github me-2"), "SomRepresentation"], outline=True, color="light",
                           size="md", href="https://github.com/ophelia-rnd/minisom-representation", target="_blank"),
                dbc.Button([html.I(className="bi bi-github me-2"), "MiniSom"], outline=True, color="light",
                           size="md", href="https://github.com/JustGlowing/minisom", target="_blank"),
            ]
        )
    ]
)
