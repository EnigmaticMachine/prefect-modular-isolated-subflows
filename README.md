# prefect-modular-isolated-subflows
This repository demonstrates a modular architecture using Prefect 3, where each flow component is deployed as an isolated container. This design enables independent updates and redeployments of each component without affecting the entire pipeline.


## Overview

In this system:
- **Main Flow:** Orchestrates the overall pipeline, fetches data, and triggers subflows.
- **Subflow:** Handles specific processing tasks (e.g., data transformation or report generation) in an isolated environment.
- **Prefect Server:** Manages orchestration, logging, and state tracking.
- **Workers:** Separate containers execute the main flow and subflow based on dedicated work pools.


This separation ensures that if you update the code for the subflow, you only need to redeploy its container without impacting the main pipeline.



## How the System Works

1. **Modular Isolation:**
   - Each flow (main and subflow) is packaged in its own directory with its dedicated Dockerfile and dependencies.
   - This modularity allows independent updates and redeployment for each flow component.

2. **Prefect Orchestration:**
   - The Prefect server runs in its own container and manages the flow deployments and worker registrations.
   - Main flow and subflow workers are set up in separate containers connected to specific work pools (`flow-pool` for main flows and `subflow-pool` for subflows).

3. **Deployment Process:**
   - Each flow has a corresponding deploy script (`deploy.py`) that registers the flow with the Prefect server.



## Setup & Deployment

### 1. Build and Start Containers

Use Docker Compose to build and start all required containers:

`docker-compose up --build`


### 2. Deploy Flows

Once the containers are running, you need to register your flows with the Prefect server:

- **Deploy Main Flow:**
    Execute the deploy script inside the main flow worker container:

    `docker-compose exec prefect-worker-flow python deploy.py`

- **Deploy Subflow:**
    Execute the deploy script inside the subflow worker container:

    `docker-compose exec prefect-worker-subflow python deploy.py`


These commands load your flow definitions from the respective directories and register them as deployments with the Prefect server. Check the output to verify that deployments are successful.

### 3. Triggering Flow Runs

After deployment, you can trigger flow runs via the Prefect UI. The main flow will call the subflow deployment dynamically during its execution.



## How It Works Internally

- **Main Flow (`main_flow.py`):**
    Fetches required data and triggers the subflow by calling `run_deployment()`. It then waits for the subflow’s result and proceeds with further processing (e.g., storing output).

- **Subflow (`subflow.py`):**
    Processes the data passed from the main flow. Once completed, it stores its output in a Prefect variable so that the main flow can retrieve it.
