# Getting Started

## 1. Environment Setup

Use the `bianor-databricks-kit` library to set up the Bianor app environment in your Databricks workspace.

> [!TIP]
> For instructions refer to the [bianor-databricks-kit repository](https://github.com/ophelia-rnd/bianor-databricks-kit).

## 2. Application Deployment

You can deploy the Bianor application directly in your Databricks workspace or run it locally.

### Databricks App (Recommended)

1. **Clone the repository**  
   In your Databricks workspace, clone this repository.

   ```bash
   https://github.com/ophelia-rnd/bianor-databricks.git
   ```

2. **Configure `app.yaml`**  
   Copy the example configuration.
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


### Local Run

1. **Clone & install dependencies**
   ```bash
   git clone https://github.com/ophelia-rnd/bianor-databricks.git
   ```
   ```bash
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


## 3. Model Training & Registration

Train a `SomRepresentation` model using the `minisom-representation` library and register it in your Databricks workspace via MLflow.

Finally, use the `bianor-databricks-kit` to link a registered model to your Bianor instance, so it can be inspected in the app.

> [!TIP]
> For instructions refer to the [minisom-representation](https://github.com/ophelia-rnd/minisom-representation) and [bianor-databricks-kit](https://github.com/ophelia-rnd/bianor-databricks-kit) repositories.

> [!NOTE]
> The trained and registered models are completely independent of the Bianor application itself. They are trained and managed through your standard MLflow / Databricks lifecycle and are simply linked to the app for interactive exploration.