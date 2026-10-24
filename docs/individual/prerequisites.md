# Community Edition &mdash; Prerequisites

Choose the path that best fits your needs:

- **:simple-databricks: Databricks App** &mdash; Recommended for **teams and organizations** that already have an established Databricks workspace and wish to leverage existing Unity Catalog governance and compute resources.
- **:material-laptop: Local Run** &mdash; Recommended for **individual researchers, data scientists, and curious minds** seeking a lightweight, zero-cloud setup directly on their local machine.

---

## Prerequisites Checklist

=== ":simple-databricks: Databricks App"

    Deploy and run Bianor natively inside your Databricks workspace.

    | Component | | Description |
    | :--- | :--- | :--- |
    | **Databricks Workspace** | Free account is sufficient | Access to a workspace with Unity Catalog, SQL Warehouses, and Databricks Apps enabled. Start at [databricks.com](https://www.databricks.com/). |
    | **SQL Warehouse** | An active SQL Warehouse | Needed to serve analytical queries. Will be attached as an App Resource during deployment. |
    | **Target Catalog & Schema** | Designated Unity Catalog schema | Catalog and schema (e.g. `workspace.bianor`) where metadata tables and models will reside. |
    | **App Permissions** | Schema & Warehouse access | The app's Service Principal will require schema read (`SELECT`), model `EXECUTE`, and warehouse `CAN USE` permissions once created. |
    | **Application Repository** | [`ophelia-rnd/bianor`](https://github.com/ophelia-rnd/bianor) | Source repository to clone into your Databricks workspace Git folder. |
    | **Toolkit** | [`pypi/bianor-databricks-kit`](https://pypi.org/project/bianor-databricks-kit/) | Python library to initialize metadata tables and link models. |
    | **Modeling Library** | [`ophelia-rnd/minisom-representation`](https://github.com/ophelia-rnd/minisom-representation) | Python library to train `SomRepresentation` models on your data. |

=== ":material-laptop: Local Run"

    Run Bianor completely standalone on your local workstation without requiring a Databricks account or connection.

    | Component | | Description |
    | :--- | :--- | :--- |
    | **Environment** | Python 3.10+ | Python environment (Jupyter optional for exploratory workflows). |
    | **Application Repository** | [`ophelia-rnd/bianor`](https://github.com/ophelia-rnd/bianor) | Source repository to clone onto your local machine. |
    | **Modeling Library** | [`ophelia-rnd/minisom-representation`](https://github.com/ophelia-rnd/minisom-representation) | Python library to train `SomRepresentation` models on your data. |

---

## Next Steps

Once you are ready, proceed to **[Launch Bianor](launch.md)** to configure and launch your app.
