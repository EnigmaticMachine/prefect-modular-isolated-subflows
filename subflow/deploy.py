from prefect.deployments import run_deployment
from prefect import flow
from prefect.client.orchestration import PrefectClient


def deploy_subflow_deployment():
    """
    Deploys the subflow_deployment from source.
    """
    deployment = (
        __import__("subflow_deployment", fromlist=["subflow_deployment"])
        .subflow_deployment.from_source(
            source="file:///app",
            entrypoint="subflow_deployment.py:subflow_deployment",
        )
        .deploy(
            name="subflow-deployment",
            work_pool_name="subflow-pool",  # specify the work pool for subflows
            parameters={},
        )
    )
    print(f"[✓] Deployed subflow_deployment with deployment id: {deployment}")
    return deployment


if __name__ == "__main__":
    deploy_subflow_deployment()
