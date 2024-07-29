# Giskard Hub Client Library

The Giskard Hub is a platform that centralizes the validation process of LLM
applications, empowering product teams to ensure all functional, business &
legal requirements are met, and keeping them in close contact with the
development team to avoid delayed deployment timelines.

The ``giskard_hub`` Python library provides a simple way for developers and data
scientists to manage and evaluate LLM applications in their development workflow
during the prototyping phase and for continuous integration testing.

Read the quick start guide to get up and running with the `giskard_hub` library.
You will learn how to execute local evaluations from a notebook, script or CLI, and
synchronize them to the Giskard Hub platform.

Access the full docs at: https://docs-hub.giskard.ai/

## Install the client library

The library is compatible with Python 3.9 to 3.12.

``` bash
pip install giskard-hub
```

## Create a project and run an evaluation

You can now use the client to interact with the Hub. You will be able to
control the Hub programmatically, independently of the UI. Let's start
by initializing a client instance:

``` python
from giskard_hub import HubClient

hub = HubClient()
```

You can provide the API key and Hub URL as arguments. Head over to your Giskard Hub instance and click on the user 
icon in the top right corner. You will find your personal API key, click on the
button to copy it.

``` python
hub = HubClient(
    api_key="YOUR_GSK_API_KEY",
    hub_url="THE_GSK_HUB_URL",
)
```

You can now use the `hub` client to control the LLM Hub! Let's start by
creating a fresh project.

### Create a project

``` python
project = hub.projects.create(
    name="My first project",
    description="This is a test project to get started with the Giskard Hub client library",
)
```

That's it! You have created a project. You will now see it in the Hub UI
project selector.

**Tip**

If you have an already existing project, you can easily retrieve it.
Either use `hub.projects.list()` to get a list of all projects, or use
`hub.projects.retrieve("YOUR_PROJECT_ID")` to get a specific project.


### Import a dataset

Let's now create a dataset and add a conversation example.

``` python
# Let's create a dataset
dataset = hub.datasets.create(
    project_id=project.id,
    name="My first dataset",
    description="This is a test dataset",
)
```

We can now add a conversation example to the dataset. This will be used
for the model evaluation.

``` python
# Add a conversation example
hub.conversations.create(
    dataset_id=dataset.id,
        messages=[
        dict(role="user", content="What is the capital of France?"),
        dict(role="assistant", content="Paris"),
        dict(role="user", content="What is the capital of Germany?"),
    ],
    expected_output="Berlin",
    demo_output=dict(role="assistant", content="I don't know that!"),
    rules=[
        "The agent should always provide short and concise answers.",
    ],
)
```

These are the attributes you can set for a conversation (the only
required attribute is `messages`):

-   `messages`: A list of messages in the conversation. Each message is a dictionary with the following keys:  
    -   `role`: The role of the message, either "user" or "assistant".
    -   `content`: The content of the message.

-   `expected_output`: The expected output of the conversation. This is
    used for evaluation.

-   `rules`: A list of rules that the conversation should follow.
    This is used for evaluation.

-   `demo_output`: A demonstration of a (possibly wrong) output from the
    model. This is just for demonstration purposes.

You can add as many conversations as you want to the dataset.

Again, you'll find your newly created dataset in the Hub UI.

### Configure a model

Before running our first evaluation, we'll need to set up a model.
You'll need an API endpoint ready to serve the model. Then, you can
configure the model API in the Hub:

``` python
model = hub.models.create(
    project_id=project.id,
    name="My Bot",
    description="A chatbot for demo purposes",
    url="https://my-model-endpoint.example.com/bot_v1",
    supported_languages=["en", "fr"],
    # if your model endpoint needs special headers:
    headers={"X-API-Key": "MY_TOKEN"},
)
```

We can test that everything is working well by running a chat with the
model:

``` python
response = model.chat(
    messages=[
        dict(role="user", content="What is the capital of France?"),
        dict(role="assistant", content="Paris"),
        dict(role="user", content="What is the capital of Germany?"),
    ],
)

print(response)
```

If all is working well, this will return something like

``` python
ModelOutput(
    message=ChatMessage(
        role='assistant',
        content='The capital of Germany is Berlin.'
    ),
    metadata={}
)
```

### Run a remote evaluation

We can now launch a remote evaluation of our model!

``` python
eval_run = client.evaluate(
    model=model,
    dataset=dataset,
    name="test-run",  # optional
)
```

The evaluation will run asynchronously on the Hub. To retrieve the
results once the run is complete, you can use the following:

``` python

# This will block until the evaluation status is "finished"
eval_run.wait_for_completion()

# Print the evaluation metrics
eval_run.print_metrics()
```


**Tip**

You can directly pass IDs to the evaluate function, e.g.
`model=model_id` and `dataset=dataset_id`, without having to retrieve
the objects first.
