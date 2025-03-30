from prefect import flow, task, get_run_logger
from prefect.deployments import run_deployment
from prefect.client import get_client
from prefect.variables import Variable


@task
def fetch_data(source: str = "default_source", limit: int = 3):
    logger = get_run_logger()
    logger.info(f"Fetching data from {source} with limit {limit}")
    data = "abstract_data"
    logger.debug(f"Fetched data: {data}")
    return data


@task
def store_output(output: str, filename: str = "output.txt"):
    logger = get_run_logger()
    logger.info(f"Storing output to {filename}")
    logger.debug(f"Output content: {output}")
    return filename


@flow(name="Main Pipeline")
async def main_pipeline_flow():
    logger = get_run_logger()
    logger.info("Starting Main Pipeline flow")

    # Fetch the required data
    data = fetch_data()
    logger.info(f"Data received: {data}")

    # Run the subflow deployment asynchronously and obtain the result
    logger.info("Running subflow deployment")
    subflow_run = await run_deployment(
        "Subflow/subflow-deployment",
        parameters={"data": data},
    )
    logger.info(f"Subflow run details: {subflow_run}")
    logger.info(f"Subflow run type: {type(subflow_run)}")

    # Retrieve the state of the subflow run
    client = get_client()
    subflow_state = await client.read_flow_run(subflow_run.id)

    # Extract the result from the subflow state
    if subflow_state.state.is_completed():
        result = await Variable.get(name="latest_output", default="No output found")
        logger.info(f"Retrieved output: {result}")
    else:
        logger.error(
            f"Subflow did not complete successfully. State: {subflow_state.state}"
        )
        result = "Error: Subflow failed"

    # Optionally store the output
    stored_filename = store_output(result)
    logger.info(f"Output stored in: {stored_filename}")
    return result


if __name__ == "__main__":
    main_pipeline_flow()
