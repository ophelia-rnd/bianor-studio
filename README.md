<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/bianor_branding_dark.png">
    <img alt="Bianor" src="assets/bianor_branding_light.png" width=45%>
  </picture>
</p>

<h3 align="center">
High-dimensional data,<br>
brought into focus in 2D
</h3>

______________________________________________________________________

<p align="center">
    <a href="https://bianor.ophelia-rnd.dev"><b>About Bianor</b></a>
    &nbsp;•&nbsp; <a href="https://demo.bianor.ophelia-rnd.dev"><b>Demo</b></a>
    &nbsp;•&nbsp; <a href="https://www.linkedin.com/company/ophelia-rnd"><b>The Team behind Bianor</b></a>
</p>

______________________________________________________________________

## Overview

**Bianor** is an installable **Databricks App** designed to run natively inside your workspace for interactive data exploration and contextualization.


## Getting Started

To get started with Bianor, the overall process involves the following steps:

1. **Environment Setup:** Preparing your Bianor environment in Databricks.
2. **Application Deployment:** Deploy your Bianor app (natively as a Databricks App or locally).
3. **Model Training & Registration:** Training and registering your models to be viewed in the app.

### 1. Environment Setup

The `bianor-databricks-kit` library is used to set up the Bianor app environment and manage the connection to representation models, projection layers, and predictions in your Databricks workspace.

> [!TIP]
> For instructions refer to the [bianor-databricks-kit repository](https://github.com/ophelia-rnd/bianor-databricks-kit).


### 2. Application Deployment

You can deploy the Bianor application directly in your Databricks workspace or run it locally.

#### Option A: Databricks App (Recommended)

1. **Clone the repository**  
   In your Databricks workspace, clone this repository.

2. **Configure `app.yaml`**  
   Copy the example configuration:
   ```bash
   cp app.yaml.example app.yaml
   ```
   Set your SQL Warehouse ID and target Catalog / Schema:
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


#### Option B: Local Run

1. **Clone & install dependencies**
   ```bash
   git clone https://github.com/org-ophelia-rnd/bianor-databricks.git
   cd bianor-databricks
   pip install -r requirements.txt
   ```

2. **Configure `.env`**  
   Copy the template:
   ```bash
   cp .env.example .env
   ```
   Fill in your Databricks connection details:
   ```ini
   DATABRICKS_HOST=<workspace-url>
   DATABRICKS_CLIENT_ID=<client-id>
   DATABRICKS_CLIENT_SECRET=<client-secret>
   DATABRICKS_WAREHOUSE_ID=<sql-warehouse-id>

   BIANOR_DATABRICKS_CATALOG=<my_catalog>
   BIANOR_DATABRICKS_SCHEMA=<my_schema>
   ```

3. **Start the server**
   ```bash
   python app.py
   ```
   Open `http://localhost:8050` in your browser.


### 3. Model Training & Registration

Once your environment and app are set up, you can integrate your models. Train a `SomRepresentation` model using the `minisom-representation` library and register it in your Databricks workspace via MLflow. Finally, use the `bianor-databricks-kit` to link the registered model to your Bianor catalog so it can be accessed and visualized in the app.

> [!TIP]
> For instructions refer to the [minisom-representation](https://github.com/ophelia-rnd/minisom-representation) and [bianor-databricks-kit](https://github.com/ophelia-rnd/bianor-databricks-kit) repositories.

> [!NOTE]
> The trained and registered models are completely independent of the Bianor application itself. They are trained and managed through your standard MLflow lifecycle and are simply linked to the app for interactive exploration.

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
