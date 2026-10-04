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
    &nbsp;•&nbsp; <a href="https://www.linkedin.com/company/ophelia-rnd"><b>Team behind Bianor</b></a>
</p>

______________________________________________________________________

## About

**Bianor** is an installable **Databricks App** designed for interactive exploration and contextualization of the data and models residing in your workspace.

## Overview

Setting up your Bianor application involves the following steps:

1. **Environment Setup:** Preparing your Bianor environment in Databricks.
2. **Application Deployment:** Deploy your Bianor app.
3. **Model Training & Registration:** Training and registering your models to be inspected in Bianor.

> [!NOTE]
> The trained and registered models are completely independent of the Bianor application itself. They are trained and managed through your standard MLflow / Databricks lifecycle and are simply linked to the app for interactive exploration.

> [!TIP]
> You may run Bianor locally while still accessing your data in your Databricks workspace.
> To do so, refer to the [documentation](/docs/get_started.md).

## Getting Started

### 1. Environment Setup

Use the [`bianor-databricks-kit`](https://github.com/ophelia-rnd/bianor-databricks-kit) library to set up the Bianor app environment in your Databricks workspace.

### 2. Application Deployment

1. **Clone the repository**  
   In your Databricks workspace, clone this repository.

   ```bash
   https://github.com/ophelia-rnd/bianor-databricks.git
   ```

2. **Configure `app.yaml`**  
   Copy the example configuration (`app.yaml.example` $\rightarrow$ `app.yaml`).
   Set your SQL Warehouse ID and target catalog / schema:
   ```yaml
   command: [
     "python",
     "app.py"
   ]

   env:
     - name: "DATABRICKS_WAREHOUSE_ID"
       valueFrom: "<sql-warehouse-id>"

     - name: "BIANOR_DATABRICKS_CATALOG"
       value: "<my_catalog>"

     - name: "BIANOR_DATABRICKS_SCHEMA"
       value: "<my_schema>"
   ```

3. **Deploy the app**  
   Navigate to **Databricks Apps**, create a new app from the cloned repository, and deploy it.



### 3. Model Training & Registration

Train a `SomRepresentation` model using the [`minisom-representation`](https://github.com/ophelia-rnd/minisom-representation) library and register it in your Databricks workspace via MLflow.
Finally, use the [`bianor-databricks-kit`](https://github.com/ophelia-rnd/bianor-databricks-kit) to link a registered model to your Bianor instance, so it can be inspected in the app.

## Contact

For questions, feedback, or enterprise inquiries:
- **Partnerships:** Reach out at [hello@ophelia-rnd.dev](mailto:hello@ophelia-rnd.dev)
- **Issues & Feature Requests:** Open an issue [here](https://github.com/ophelia-rnd/bianor-databricks/issues)
- Learn more about the [team and mission](https://bianor.ophelia-rnd.dev) behind Bianor or connect on [LinkedIn](https://www.linkedin.com/company/ophelia-rnd)

______________________________________________________________________

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
