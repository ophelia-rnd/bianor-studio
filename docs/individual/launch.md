# Community Edition &mdash; Launch Bianor

Choose your deployment mode to configure and launch Bianor.

=== ":simple-databricks: Databricks App"

    Deploy and run Bianor directly inside your Databricks workspace.

    ### 1. Clone repository into Workspace
    In Databricks, navigate to **Workspace** and create a new **Git folder** using the following repository:
    ```text
    https://github.com/ophelia-rnd/bianor.git
    ```

    ### 2. Configure `app.yaml`
    In your cloned folder, set your target catalog and schema in `app.yaml`:
    ```yaml
    command: [
      "python",
      "app.py"
    ]

    env:
      - name: "DATABRICKS_WAREHOUSE_ID"
        valueFrom: "sql-warehouse"

      - name: "BIANOR_DATABRICKS_CATALOG"
        value: "workspace"

      - name: "BIANOR_DATABRICKS_SCHEMA"
        value: "bianor"
    ```

    ### 3. Create app with SQL Warehouse resource
    1. Navigate to **Compute** $\rightarrow$ **Apps** $\rightarrow$ click **Create app**.
    2. Enter an app name (e.g. `bianor`).
    3. Under **App resources**, click **+ Add resource** $\rightarrow$ select **SQL Warehouse**:
        - **Resource key:** `sql-warehouse`
        - **SQL warehouse:** Select your active warehouse.

    ### 4. Grant Service Principal access in Catalog Explorer
    Creating the app generates an app-specific **Service Principal**. Grant it permissions via the UI:

    1. Open **Catalog** $\rightarrow$ navigate to your designated catalog and schema (`workspace.bianor`).
    2. Under **Permissions**, click **Grant**:
        - Select your app service principal.
        - Add privileges: **`USE CATALOG`**, **`USE SCHEMA`**, **`SELECT`** (data access), and **`EXECUTE`** (for MLflow model loading).
    3. Ensure the Service Principal also has **`Can use`** permission on your selected SQL Warehouse (**SQL Warehouses** $\rightarrow$ **Permissions**).

    ### 5. Deploy the app from your Workspace folder
    1. On the app details page, set the source directory to your cloned repository folder in **Workspace**.
    2. Click **Deploy**.

    ### 6. Visit the deployed app
    Once deployment completes, click the app URL to open Bianor.

=== ":material-laptop: Local Run"

    Deploy and run Bianor directly on your local workstation.

    ### 1. Clone repository
    ```bash
    git clone https://github.com/ophelia-rnd/bianor.git
    ```

    ### 2. Install dependencies
    ```bash
    cd bianor
    pip install -r requirements.txt
    ```

    ### 3. Configure `.env`
    ```bash
    cp .env.local.example .env
    ```
    ```env
    # .env file
    BIANOR_BACKEND=local
    BIANOR_LOCAL_CATALOG_ROOT=./bianor_local_catalog
    ```

    ### 4. Launch Bianor
    Run the following command and open `http://localhost:8050`.
    ```bash
    python app.py
    ```


---

## Next Steps

Once your application is running, proceed to **[Modeling & Configuration](modeling.md)** to train your first representation and link it to Bianor.
