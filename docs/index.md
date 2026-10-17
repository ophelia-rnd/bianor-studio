<p align="left" class="hero-branding">
  <img class="hero-light-only" src="assets/bianor_branding_light.png" alt="Bianor" width="40%" />
  <img class="hero-dark-only" src="assets/bianor_branding_dark.png" alt="Bianor" width="40%" />
</p>

**Bianor** is an interactive app for exploring and contextualizing high-dimensional data via Self-Organizing Map (SOM) representations.

---

## Architecture at a Glance

Bianor integrates with **Databricks**: data in _Unity Catalog_, models in _MLflow_.
A fully **local workflow** is also available when you do not need a Databricks connection.


```mermaid
flowchart TD
    subgraph DBR ["Data & ML Workspace"]
        direction LR
        Data["High-Dimensional Data"] --> Train["Train <code>SomRepresentation</code>"]
        Train --> Register["Register Representation Model in MLflow"]
    end

    subgraph BIANOR ["Bianor Application"]
        direction LR
        Explore["Explore Data Relationships<br/>in 2D Visual Contexts"]
    end

    Register ==>|"Link to Bianor"| Explore

    style DBR fill:#ff362108,stroke:#FF3621,stroke-width:2px,stroke-dasharray: 4 2
    style BIANOR fill:#4f46e508,stroke:#6366f1,stroke-width:2px,stroke-dasharray: 4 2

    classDef databricks fill:#ff362115,stroke:#FF3621,stroke-width:1.5px;
    classDef bianor fill:#4f46e515,stroke:#6366f1,stroke-width:1.5px;

    class Data,Train,Register databricks;
    class Explore bianor;
```

---

## Get Started

<div class="grid cards" markdown>

-   :material-account-school:{ .lg .middle } __Community Edition__

    ---

    Designed for individual **researchers**, **data scientists**, and **curious minds**. Explore high-dimensional representations.

    * [Core Features](features.md)
    * [Prerequisites](individual/prerequisites.md)
    * [Launch Bianor](individual/launch.md)
    * [Modeling & Configuration](individual/modeling.md)

-   :material-domain:{ .lg .middle } __Biome Edition__

    ---

    Designed for **organizations** and **data teams** with established Databricks workspaces.

    * For early access or assistance, reach out at [hello@ophelia-rnd.dev](mailto:hello@ophelia-rnd.dev)

</div>
