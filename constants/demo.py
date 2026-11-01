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
    {"symbol": "circle", "color": "#ffffff", "size": 11, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "diamond", "color": "#38bdf8", "size": 11, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "square", "color": "#34d399", "size": 11, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "cross", "color": "#fde047", "size": 12, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "triangle-up", "color": "#3b82f6", "size": 11, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "star", "color": "#e9d5ff", "size": 12, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "hexagon", "color": "#00f5d4", "size": 11, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "hourglass", "color": "#a3e635", "size": 11, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "bowtie", "color": "#fed7aa", "size": 12, "line": {"width": 1.2, "color": "#000000"}},
    {"symbol": "x", "color": "#818cf8", "size": 12, "line": {"width": 1.2, "color": "#000000"}},
]
