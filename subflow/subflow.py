from prefect import flow, task, get_run_logger
from prefect.variables import Variable


@task
def process_data(input_data: str) -> str:
    logger = get_run_logger()
    logger.info(f"Processing input data: {input_data}")
    # Simulate data processing
    processed_output = f"Processed Data: {input_data.upper()}"
    logger.debug(f"Processed output: {processed_output}")
    return processed_output


@flow(name="Subflow", persist_result=True)
def subflow_deployment(input_data: str) -> str:
    logger = get_run_logger()
    logger.info(f"Starting subflow with input data: {input_data}")
    result = process_data(input_data)
    # Persist the result in a Prefect variable for retrieval by the parent flow
    Variable.set(name="latest_output", value=result, overwrite=True)
    return result


if __name__ == "__main__":
    sample_input = "example_data"
    print(subflow_deployment(sample_input))
