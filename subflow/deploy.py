from prefect.deployments import run_deployment
from prefect.client.orchestration import PrefectClient


def deploy_subflow_deployment():
    """
    Deploys the subflow_deployment from source.
    """
    deployment = (
        __import__("subflow", fromlist=["subflow_deployment"])
        .subflow_deployment.from_source(
            source="file:///app",
            entrypoint="subflow.py:subflow_deployment",
        )
        .deploy(
            name="subflow-deployment",
            work_pool_name="subflow-pool",  # using the work pool designated for subflows
            parameters={},
        )
    )
    print(f"[✓] Deployed subflow_deployment with deployment id: {deployment}")
    return deployment


if __name__ == "__main__":
    deploy_subflow_deployment()
