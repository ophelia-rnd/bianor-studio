DEMO_ID_PREFIX = "demo_id_"
DEMO_MODEL_PREFIX = "demo_model_"

DEMO_MIN_EPOCHS = 1
DEMO_MAX_EPOCHS = 50
DEMO_DEFAULT_EPOCHS = 25

DEMO_DATASET_OPTIONS = [
    {"label": "Iris Dataset (150 samples)", "value": "iris"},
    {"label": "Wine Dataset (178 samples)", "value": "wine"},
    {"label": "Breast Cancer Dataset (569 samples)", "value": "breast_cancer"},
    {"label": "Digits Dataset (1,797 samples)", "value": "digits"},
]
DEMO_DEFAULT_DATASET = "iris"

MAP_SIZE_LABELS = {
    1.0: "Regular",
    2.0: "Large",
    3.5: "Super",
}

DEMO_MAP_SIZE_OPTIONS = [
    {"label": label, "value": val}
    for val, label in MAP_SIZE_LABELS.items()
]
DEMO_DEFAULT_MAP_SIZE = 1.0

DEMO_MARKER_STYLES = [
    {"symbol": "circle", "color": "#f43f5e", "size": 10},
    {"symbol": "diamond", "color": "#38bdf8", "size": 10},
    {"symbol": "square", "color": "#34d399", "size": 10},
    {"symbol": "cross", "color": "#fbbf24", "size": 11},
    {"symbol": "triangle-up", "color": "#a855f7", "size": 10},
    {"symbol": "star", "color": "#f472b6", "size": 11},
    {"symbol": "hexagon", "color": "#2dd4bf", "size": 10},
    {"symbol": "hourglass", "color": "#a3e635", "size": 10},
    {"symbol": "bowtie", "color": "#fb923c", "size": 11},
    {"symbol": "x", "color": "#e879f9", "size": 11},
]
