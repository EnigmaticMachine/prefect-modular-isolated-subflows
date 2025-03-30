from prefect.deployments import run_deployment
from prefect import flow
from prefect.client.orchestration import PrefectClient


def deploy_main_pipeline_flow():
    """
    Deploys the main_pipeline_flow from source.
    """
    deployment = (
        __import__("main_pipeline_flow", fromlist=["main_pipeline_flow"])
        .main_pipeline_flow.from_source(
            source="file:///app",
            entrypoint="main_pipeline_flow.py:main_pipeline_flow",
        )
        .deploy(
            name="main-pipeline-flow-deployment",
            work_pool_name="flow-pool",  # using the default work pool for main flows
            parameters={},
        )
    )
    print(f"[✓] Deployed main_pipeline_flow with deployment id: {deployment}")
    return deployment


if __name__ == "__main__":
    deploy_main_pipeline_flow()
