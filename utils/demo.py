from constants.demo import DEMO_ID_PREFIX, DEMO_MODEL_PREFIX, DEMO_MARKER_STYLES

def is_demo_id(val) -> bool:
    return bool(val and str(val).startswith(DEMO_ID_PREFIX))

def is_demo_model(val) -> bool:
    return bool(val and str(val).startswith(DEMO_MODEL_PREFIX))


def build_demo_projections(data, dataset_name: str = ""):
    """Extracts labeled target classes as projection layer definitions."""
    X = data.data
    y = data.target
    target_names = getattr(data, "target_names", None)

    projections = []
    unique_classes = sorted(y.unique()) if hasattr(y, "unique") else sorted(set(y))

    for idx, cls_val in enumerate(unique_classes):
        if target_names is not None and idx < len(target_names):
            raw_name = str(target_names[idx])
            if dataset_name == "digits":
                name = f"Digit {raw_name}"
            elif "_" in raw_name:
                name = raw_name.replace("_", " ").title()
            else:
                name = raw_name.capitalize()
        else:
            name = f"Class {cls_val}"

        marker = DEMO_MARKER_STYLES[idx % len(DEMO_MARKER_STYLES)]
        X_cls = X[y == cls_val]

        projections.append({
            "name": name,
            "data": X_cls,
            "marker": marker,
        })

    return projections


def apply_demo_projections(pond, demo_model, scaler):
    """Applies demo class projections onto the given pond."""
    for proj in getattr(demo_model, "projections", None) or []:
        pond.attraction_layer(
            scaler.transform(proj["data"]),
            name=proj["name"],
            marker=proj["marker"]
        )
