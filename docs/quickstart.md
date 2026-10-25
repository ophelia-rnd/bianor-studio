# Quick Start

## Clone the Repository

```bash
git clone https://github.com/ophelia-rnd/bianor.git
cd bianor
```

---

## Option A: Running with Docker

```bash
docker compose up --build
```

Navigate to `http://localhost:8050`.

---

## Option B: Local Python Environment

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare the Demo Setup

The repository comes with a notebook that sets up local data and a representation model for the Iris dataset, along with a configured `catalog.yaml` manifest. Execute all cells in [`bianor_local_catalog/notebooks/demo_iris.ipynb`](https://github.com/ophelia-rnd/bianor/blob/main/bianor_local_catalog/notebooks/demo_iris.ipynb).

### 3. Launch Bianor

Start the application and navigate to `http://localhost:8050`.

```bash
python app.py
```

---

## Explore Bianor

1. **Select a Representation**: Choose *Iris Representation* from the top navigation selector.
2. **Inspect Topology**: Toggle between **Neighbor Distances**, **Training Activations**, and **Topological Connections** to inspect cluster structure and node density in 2D.
3. **Analyze Components**: Use the **Component View** to visualize individual feature distributions across the map.
4. **Overlay Projections & Predictions**: Display labeled historical samples and ground-truth classification of holdout observations.

---

## Next Steps

- **Core Features**: Learn about all the features in [Core Features](features.md).
- **Train Custom Representations**: Train and configure custom models in [Modeling & Configuration](individual/modeling.md).
- **Deploy on Databricks**: Follow the [Databricks Launch Guide](individual/launch.md) to run inside a Databricks workspace.
