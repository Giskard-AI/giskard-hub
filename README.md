# Quick Start

## Evaluating from your Jupyter notebook

Start by initializing a client.

```python
from giskard_hub.client import HubClient

# Note: API key and Hub URL can also be provided by setting env variables GSK_API_KEY and GSK_HUB_URL
client = HubClient(
    api_key="GSK_API_KEY",
    hub_url="GSK_HUB_URL",
)
```


Next, retrieve relevant objects from the server (project, model & dataset).

```python
from giskard_hub.data import Dataset, Model, Project

project: Project = client.get_projects()[0]
model: Model = client.get_models(project.id)[0]
dataset: Dataset = client.get_datasets(project.id)[0]
```

You can then launch an evaluation, which downloads the dataset to be sent to your LLM agent for completion.

```python
from typing import List
from giskard_hub.data import Evaluation

# This will contain the messages, expected outputs, policies, IDs, tags, notes, etc
to_complete: List[Evaluation] = client.evaluate(
    model_id=model.id,
    dataset_id=dataset.id,
)
```

You can then send this to your LLM agent for output completion.

```python
# Dummy LLM agent
def dummy_model(all_data: Evaluation):
    # Simulated call to an agent and updating the evaluation
    all_data.set_output("Sorry, I can't answer your question.")
    # Alternatively, could be done like this
    # all_data.output = ModelOutput(response=LLMMessage(role="assistant", content="Sorry, I can't answer your question."), metadata={})

for elt in to_complete:
    dummy_model(elt)
```

You can then push the completed elements to the Hub. This will start the evaluation process on the Hub.

```python
updates = client.update_evaluations(to_complete)
```

Next, either head to the Hub to inspect the evaluation results in details, or get summarized results directly in your
development environment.

```python
# Extract the execution_id
execution_id = to_complete[0].execution_id

# Extract the results from the Hub
results = client.get_results(execution_id=execution_id)
results
```

## Evaluating using a Python script

```python
from typing import List
from giskard_hub.client import HubClient
from giskard_hub.data import Dataset, Evaluation, Model, Project


# Dummy LLM agent
def dummy_model(all_data: Evaluation):
    # Simulated call to an agent and updating the evaluation
    all_data.set_output("Sorry, I can't answer your question.")
    # Alternatively, could be done like this
    # all_data.output = ModelOutput(response=LLMMessage(role="assistant", content="Sorry, I can't answer your question."), metadata={})

if __name__ == "__main__":
    # Note: API key and Hub URL can also be provided by setting env variables GSK_API_KEY and GSK_HUB_URL
    client = HubClient(
        api_key="GSK_API_KEY",
        hub_url="GSK_HUB_URL",
    )
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
```

## Evaluating using CLI

```bash
#!/bin/bash
set -eu
# Set env variable to avoid giving this info everytime
export GSK_API_KEY=GSK_API_KEY
export GSK_HUB_URL=GSK_HUB_URL
folder_path=./test-folder

rm -rf $folder_path
mkdir -p $folder_path

project_id=$(python -m giskard_hub.cli projects | jq --raw-output .[0].id)
model_id=$(python -m giskard_hub.cli models --project-id $project_id | jq --raw-output .[0].id)
dataset_id=$(python -m giskard_hub.cli datasets --project-id $project_id | jq --raw-output .[0].id)

python -m giskard_hub.cli evaluate --folder-path $folder_path --dataset-id $dataset_id --model-id $model_id --local-mode
execution_id=$(find $folder_path -type f | grep ".json$" | head -n1 | xargs -I {} jq --raw-output .execution_id {})

# Following line is faking a dummy LLM agent changing data in the json
find $folder_path -type f | grep ".json$" | xargs -I {} sed -i 's|"output": null|"output": "Sorry, I cant answer your question."|g' {} | sh
python -m giskard_hub.cli update-evaluations --evaluation-path $folder_path

python -m giskard_hub.cli results --execution-id $execution_id
```

## Evaluating a single dataset entry

```python
if __name__ == "__main__":
    # Initialise client
    client = HubClient(
        api_key="2b437295-dabe-4084-ba03-cdb259e3e678",
        hub_url="http://backend.llm.localhost/",
    )

    results = client.single_eval(
        TransientEvaluation(
            messages=[LLMMessage(role="user", content="What color is an orange ?")],
            model_output=ModelOutput(
                response=LLMMessage(role="assistant", content="An orange is green.")
            ),
            model_description="You are an agent that give informations about fruits",
            policies=[
                "Agent must never say the word 'orange'",
                "Agent must be polite",
            ],
            expected_output="Orange.",
        )
    )
    print("Got results")
    print(results)
```