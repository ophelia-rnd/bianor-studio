<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/bianor_branding_dark.png">
    <img alt="Bianor" src="assets/bianor_branding_light.png" width=45%>
  </picture>
</p>

<h3 align="center">
High-dimensional observations mapped to visual contexts in 2D
</h3>

______________________________________________________________________

<p align="center">
    <a href="https://bianor.ophelia-rnd.dev"><b>About Bianor</b></a>
    &nbsp;•&nbsp; <a href="https://demo.bianor.ophelia-rnd.dev"><b>Demo</b></a>
    &nbsp;•&nbsp; <a href="https://bianor-documentation.onrender.com"><b>Documentation</b></a>
    &nbsp;•&nbsp; <a href="https://www.linkedin.com/company/bianor-insights"><b>Contact Us</b></a>
</p>


## About

**Bianor** is an **interactive app** for exploring and contextualizing high-dimensional data via Self-Organizing Map (SOM) representations.

## Getting Started

Deploy and run Bianor directly on your local workstation.


### 1. Clone the Repository

```bash
git clone https://github.com/ophelia-rnd/bianor.git
cd bianor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`
```bash
cp .env.local.example .env
```

### 4. Prepare the Demo Setup (Optional)

The repository comes with a notebook that sets up local data and a representation model for the Iris dataset, along with a configured `catalog.yaml` manifest. Execute all cells in [`bianor_local_catalog/notebooks/demo_iris.ipynb`](https://github.com/ophelia-rnd/bianor/blob/main/bianor_local_catalog/notebooks/demo_iris.ipynb).

### 5. Launch Bianor

Start the application and navigate to `http://localhost:8050`.

```bash
python app.py
```

### 6. Explore Bianor

1. **Select a Representation**: Choose *Iris Representation* from the top navigation selector.
2. **Inspect Topology**: Toggle between `Neighbor Distances`, `Training Activations`, and `Topological Connections` to inspect cluster structure and node density in 2D.
3. **Analyze Components**: Use the `Component View` to visualize individual feature distributions across the map.
4. **Overlay Projections & Predictions**: Display labeled historical samples and ground-truth classification of holdout observations.

> [!TIP]
> To learn more, refer to the [Documentation](https://bianor-documentation.onrender.com).

## License

This project is licensed under the [Apache License 2.0](LICENSE).

The Apache 2.0 license grants permissions for the source code, but does not grant rights to use the project's trademarks, logos, or brand names.

## Contact

For questions, feedback, or enterprise inquiries:
- **Partnerships:** Reach out at [hello@ophelia-rnd.dev](mailto:hello@ophelia-rnd.dev)
- **Issues & Feature Requests:** Open an issue [here](https://github.com/ophelia-rnd/bianor/issues)
- Learn more about the [Team and Mission](https://bianor.ophelia-rnd.dev) behind Bianor or connect on [LinkedIn](https://www.linkedin.com/company/bianor-insights)


<br>
<br>

<div align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/footer/bianor_branding_dark.png">
      <img height="25px" alt="Bianor logo" src="assets/footer/bianor_branding_light.png">
    </picture>
    &nbsp;&nbsp;&nbsp;
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/footer/ophelia_rnd_logo_dark.png">
      <img height="25px" alt="Ophelia R&D logo" src="assets/footer/ophelia_rnd_logo_light.png">
    </picture>
</div>
