import json
from dataclasses import asdict
from pathlib import Path
from typing import Annotated, Optional

import typer

from giskard_hub.client import HubClient
from giskard_hub.data import Evaluation

app = typer.Typer()


@app.command()
def evaluate(
    dataset_id: Annotated[
        str,
        typer.Option(help="Id of the dataset"),
    ],
    model_id: Annotated[
        str,
        typer.Option(help="Id of the model"),
    ],
    tags: Annotated[
        Optional[list[str]],
        typer.Option(help="Tags to filter only a subset of the datasets"),
    ] = None,
    local_mode: Annotated[
        bool,
        typer.Option(
            help="Whether agent output will be provided from local execution or not"
        ),
    ] = True,
    folder_path: Annotated[
        Path,
        typer.Option(help="Folder to download the dataset into"),
    ] = None,
    api_key: Annotated[
        str,
        typer.Option(
            envvar="GSK_API_KEY", help="API Key to use to interact with the hub"
        ),
    ] = None,
    hub_url: Annotated[
        str,
        typer.Option(envvar="GSK_HUB_URL", help="Base url of Hub backend"),
    ] = None,
):
    """Start the evaluation of a dataset on the hub.
    If local mode is chosen, then model output needs to be computed manually before pushing it to the hub.
    """
    client = HubClient(hub_url=hub_url, api_key=api_key)
    client.evaluate(
        model_id=model_id,
        dataset_id=dataset_id,
        tags=tags,
        local_mode=local_mode,
        use_file=True,
        folder=folder_path,
    )


@app.command()
def update_evaluations(
    evaluation_path: Annotated[
        Path,
        typer.Option(help="Folder containing json evaluations or single json file"),
    ],
    api_key: Annotated[
        str,
        typer.Option(
            envvar="GSK_API_KEY", help="API Key to use to interact with the hub"
        ),
    ] = None,
    hub_url: Annotated[
        str,
        typer.Option(envvar="GSK_HUB_URL", help="Base url of Hub backend"),
    ] = None,
):
    """Update a started evaluation, to provide agent output to the hub"""
    client = HubClient(hub_url=hub_url, api_key=api_key)
    evaluation_path = evaluation_path.resolve()
    if evaluation_path.is_dir():
        print(f"Updating all evaluation in folder {evaluation_path}")
        to_update = [
            Evaluation.from_dict(json.loads(file.read_text()))
            for file in evaluation_path.glob("*.json")
            if file.is_file()
        ]
        client.update_evaluations(to_update)
    else:
        print(f"Updating single evaluation {evaluation_path}")
        client.update_evaluation(json.loads(evaluation_path.read_text()))


@app.command()
def results(
    execution_id: Annotated[
        str,
        typer.Option(help="Id of the execution to get the result"),
    ],
    max_interval: Annotated[
        int,
        typer.Option(help="Number of time we check for evaluation completion"),
    ] = 20,
    interval_time: Annotated[
        int,
        typer.Option(help="Interval in seconds to wait before checking again"),
    ] = 10,
    api_key: Annotated[
        str,
        typer.Option(
            envvar="GSK_API_KEY", help="API Key to use to interact with the hub"
        ),
    ] = None,
    hub_url: Annotated[
        str,
        typer.Option(envvar="GSK_HUB_URL", help="Base url of Hub backend"),
    ] = None,
):
    """Wait for the results of an execution and output them"""
    client = HubClient(hub_url=hub_url, api_key=api_key)
    print(
        json.dumps(
            [
                asdict(elt)
                for elt in client.get_results(
                    execution_id, max_interval=max_interval, interval_time=interval_time
                )
            ]
        )
    )


@app.command()
def projects(
    api_key: Annotated[
        str,
        typer.Option(
            envvar="GSK_API_KEY", help="API Key to use to interact with the hub"
        ),
    ] = None,
    hub_url: Annotated[
        str,
        typer.Option(envvar="GSK_HUB_URL", help="Base url of Hub backend"),
    ] = None,
):
    """List the projects on the hub"""
    client = HubClient(hub_url=hub_url, api_key=api_key)
    print(json.dumps([asdict(elt) for elt in client.get_projects()]))


@app.command()
def datasets(
    project_id: Annotated[
        str,
        typer.Option(help="Project id to use"),
    ] = None,
    api_key: Annotated[
        str,
        typer.Option(
            envvar="GSK_API_KEY", help="API Key to use to interact with the hub"
        ),
    ] = None,
    hub_url: Annotated[
        str,
        typer.Option(envvar="GSK_HUB_URL", help="Base url of Hub backend"),
    ] = None,
):
    """List the projects in given project on the hub"""
    client = HubClient(hub_url=hub_url, api_key=api_key)
    print(
        json.dumps([asdict(elt) for elt in client.get_datasets(project_id=project_id)])
    )


@app.command()
def models(
    project_id: Annotated[
        str,
        typer.Option(help="Project id to use"),
    ] = None,
    api_key: Annotated[
        str,
        typer.Option(
            envvar="GSK_API_KEY", help="API Key to use to interact with the hub"
        ),
    ] = None,
    hub_url: Annotated[
        str,
        typer.Option(envvar="GSK_HUB_URL", help="Base url of Hub backend"),
    ] = None,
):
    """List the models in given project on the hub"""
    client = HubClient(hub_url=hub_url, api_key=api_key)
    print(json.dumps([asdict(elt) for elt in client.get_models(project_id=project_id)]))


typer_click_object = typer.main.get_group(app)

if __name__ == "__main__":
    typer_click_object()
