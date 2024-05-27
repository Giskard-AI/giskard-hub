from typing import List

from giskard_hub.client import HubClient
from giskard_hub.data import Dataset, Evaluation, Model, Project


def dummy_model(all_data: Evaluation):
    # Here, all data contains everything
    # - policies
    # - tags
    # - the conversation
    # and so on..
    # Most probably, user will want to take extra care of all_data.conversation.messages

    # Following line is simulated calling a dummy agent and updating the evaluation
    all_data.set_output("Sry, I was not paying attention")

    # Alternaltively, could be done like this
    # all_data.output = ModelOutput(response=LLMMessage(role="assistant", content="Sry, I was not paying attention"), metadata={})


if __name__ == "__main__":
    # Initialise client
    client = HubClient(
        api_key="2b437295-dabe-4084-ba03-cdb259e3e678",
        hub_url="http://backend.llm.localhost/",
    )
    # api_key and hub url can also be provided by setting env variable GSK_API_KEY and GSK_HUB_URL
    project: Project = client.get_projects()[0]
    model: Model = client.get_models(project.id)[0]
    dataset: Dataset = client.get_datasets(project.id)[0]
    to_complete: List[Evaluation] = client.evaluate(
        model_id=model.id,
        dataset_id=dataset.id,
    )
    execution_id = to_complete[0].execution_id
    for elt in to_complete:
        dummy_model(elt)

    updates = client.update_evaluations(to_complete)

    results = client.get_results(execution_id=execution_id)
    print("Got results")
    print(results)
