from prefect.deployments import run_deployment
from prefect.client.orchestration import PrefectClient


def deploy_main_pipeline_flow():
    """
    Deploys the main_pipeline_flow from source.
    """
    deployment = (
        __import__("main_flow", fromlist=["main_pipeline_flow"])
        .main_pipeline_flow.from_source(
            source="file:///app",
            entrypoint="main_flow.py:main_pipeline_flow",
        )
        .deploy(
            name="main-pipeline-flow-deployment",
            work_pool_name="flow-pool",  # using the work pool designated for main flows
            parameters={},
        )
    )
    print(f"[✓] Deployed main_pipeline_flow with deployment id: {deployment}")
    return deployment


if __name__ == "__main__":
    deploy_main_pipeline_flow()
