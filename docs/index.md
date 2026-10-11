<p align="left" class="hero-branding">
  <img class="hero-light-only" src="assets/bianor_branding_light.png" alt="Bianor" width="40%" />
  <img class="hero-dark-only" src="assets/bianor_branding_dark.png" alt="Bianor" width="40%" />
</p>

# Bianor Documentation

**Bianor** is an installable **Databricks App** designed for interactive exploration and contextualization of high-dimensional data and Self-Organizing Map (SOM) representations residing in your Databricks workspace.

---

## Architecture at a Glance

Bianor is purpose-built for the Databricks ecosystem. It natively relies on data residing in Unity Catalog and models registered through MLflow. However, the Bianor application itself can be run either deployed as a native Databricks App or executed locally on your workstation.

```mermaid
flowchart TD
    subgraph DBR ["Databricks Workspace"]
        direction LR
        Data["High-Dimensional Data"] --> Train["Train <code>SomRepresentation</code>"]
        Train --> Register["Register & Track Model<br/>in MLflow"]
    end

    subgraph BIANOR ["Bianor Application"]
        direction LR
        Explore["Explore Data Relationships<br/>in 2D Visual Contexts"]
    end

    Register ==>|"Link Registered Model"| Explore

    style DBR fill:#ff362108,stroke:#FF3621,stroke-width:2px,stroke-dasharray: 4 2
    style BIANOR fill:#4f46e508,stroke:#6366f1,stroke-width:2px,stroke-dasharray: 4 2

    classDef databricks fill:#ff362115,stroke:#FF3621,stroke-width:1.5px;
    classDef bianor fill:#4f46e515,stroke:#6366f1,stroke-width:1.5px;

    class Data,Train,Register databricks;
    class Explore bianor;
```

---

## Get Started

Choose the edition that best matches your environment and goals:

<div class="grid cards" markdown>

-   :material-account-school:{ .lg .middle } __Community Edition__

    ---

    Designed for individual **researchers, data scientists, and curious minds**. Explore high-dimensional representations with a free Databricks account.

    * [Prerequisites](individual/setup.md)
    * [Launch Bianor](individual/run.md)

-   :material-domain:{ .lg .middle } __Biome Edition__

    ---

    Designed for **organizations and data teams** with established Databricks workspaces.

    * For early access or assistance, reach out at [hello@ophelia-rnd.dev](mailto:hello@ophelia-rnd.dev).

</div>
