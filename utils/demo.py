from collections import namedtuple
from constants.demo import (
    DEMO_ID_PREFIX,
    DEMO_MODEL_PREFIX,
    DEMO_MARKER_STYLES,
    MAP_SIZE_LABELS,
)

DemoPythonModel = namedtuple(
    "DemoPythonModel",
    ["model", "scaler", "projections"],
    defaults=[None]
)


def is_demo_id(val) -> bool:
    return bool(val and str(val).startswith(DEMO_ID_PREFIX))


def is_demo_model(val) -> bool:
    return bool(val and str(val).startswith(DEMO_MODEL_PREFIX))


def get_cached_demo_maps(cache) -> list:
    """Returns all demo map metadata records from cache."""
    return cache.get("all_demo_maps") or []


def get_cached_demo_map(demo_id: str, cache) -> dict | None:
    """Retrieves a demo map metadata dictionary by ID from cache."""
    demo = cache.get(str(demo_id))
    if demo:
        return demo
    for d in get_cached_demo_maps(cache):
        if d.get("ID") == demo_id:
            return d
    return None


def register_demo_map(demo_map: dict, cache) -> None:
    """Saves demo map metadata into cache and updates all_demo_maps registry."""
    demo_id = demo_map["ID"]
    cache.set(demo_id, demo_map)
    demo_maps = get_cached_demo_maps(cache)
    demo_maps = [d for d in demo_maps if d.get("ID") != demo_id] + [demo_map]
    cache.set("all_demo_maps", demo_maps)


def build_demo_projections(data, dataset_name: str = "") -> list:
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


def apply_demo_projections(pond, demo_model, scaler) -> None:
    """Applies demo class projections onto the given pond."""
    for proj in getattr(demo_model, "projections", None) or []:
        pond.attraction_layer(
            scaler.transform(proj["data"]),
            name=proj["name"],
            marker=proj["marker"]
        )


def load_demo_dataset(dataset_name: str):
    """Loads scikit-learn toy dataset as a frame."""
    from sklearn import datasets

    if dataset_name == "iris":
        return datasets.load_iris(as_frame=True)
    if dataset_name == "wine":
        return datasets.load_wine(as_frame=True)
    if dataset_name == "digits":
        return datasets.load_digits(as_frame=True)
    return datasets.load_breast_cancer(as_frame=True)


def train_and_cache_demo(dataset_name: str, epoch: int, map_size_factor: float, cache) -> dict:
    """Trains SOM on toy dataset, caches model and projections, and returns demo map record."""
    from sklearn.preprocessing import StandardScaler
    from minisom_representation import calc_som_hyparams, SomRepresentation, calc_initial_sigma

    data = load_demo_dataset(dataset_name)
    X = data.data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    RANDOM_SEED = 42
    VERBOSE = False

    recommended_params = calc_som_hyparams(X_scaled, initial_sigma_factor=3.0)
    d1, d2, sigma = map(recommended_params.get, ("d1", "d2", "sigma"))

    if map_size_factor != 1.0:
        d1 = int(round(d1 * map_size_factor))
        d2 = int(round(d2 * map_size_factor))
        sigma = calc_initial_sigma(d1, d2, factor=3.0)

    decay_function = "linear_decay_to_zero"
    epoch = int(epoch) if epoch else 50
    epoch = max(1, min(50, epoch))

    som_rep = SomRepresentation(
        d1=d1,
        d2=d2,
        sigma=sigma,
        random_seed=RANDOM_SEED,
        verbose=VERBOSE,
        decay_function=decay_function
    ).fit_online(X_scaled, num_iteration=epoch)

    demo_projections = build_demo_projections(data, dataset_name)
    demo_model = DemoPythonModel(model=som_rep, scaler=scaler, projections=demo_projections)

    model_loc = f"{DEMO_MODEL_PREFIX}{dataset_name}_e{epoch}_f{map_size_factor}"
    cache.set(model_loc, demo_model)

    dataset_display = dataset_name.replace("_", " ").capitalize()
    size_label = MAP_SIZE_LABELS.get(float(map_size_factor), f"{map_size_factor}x")
    demo_id = f"{DEMO_ID_PREFIX}{dataset_name}_e{epoch}_f{map_size_factor}"
    demo_map = {
        "ID": demo_id,
        "NAME": f"Demo: {dataset_display} ({size_label}, Epochs: {epoch})",
        "SOM_MODEL_LOCATION": model_loc,
        "IS_DEMO": True
    }

    register_demo_map(demo_map, cache)
    return demo_map
