# Community Edition &mdash; Prerequisites

The **Community Edition** is tailored for individual **researchers, data scientists, and curious minds** seeking to visually contextualize high-dimensional data.

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
    | **Toolkit** | [`bianor-databricks-kit`](https://github.com/ophelia-rnd/bianor-databricks-kit) | Python library to initialize metadata tables and link models. |
    | **Training Library** | [`minisom-representation`](https://github.com/ophelia-rnd/minisom-representation) | Python library to train `SomRepresentation` models on your data. |

=== ":material-laptop: Local Run"

    !!! warning "Work in Progress"
        Local execution documentation and workflows are currently under active development.

---

## Next Steps

Once you are ready, proceed to **[Launch Bianor](run.md)** to configure and launch your app.
