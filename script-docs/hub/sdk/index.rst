:og:title: Giskard Hub - Enterprise Agent Testing - SDK Quickstart
:og:description: Get started with the Giskard Hub Python SDK for programmatic LLM agent testing. Install, authenticate, and begin building automated testing workflows.

Quickstart & setup
==================

The Giskard Hub SDK provides a Python interface to interact with the Giskard Hub programmatically. This allows you to automate your testing workflows, integrate with your CI/CD pipelines, and build custom tools on top of the Hub.

.. grid:: 1 1 2 2

   .. grid-item-card:: Manage projects, agents and knowledge bases
      :link: projects
      :link-type: doc

      Create, update, and organize projects, agents and knowledge bases

   .. grid-item-card:: Manage datasets and chat test cases
      :link: datasets/index
      :link-type: doc

      Create, update, and organize test datasets and chat test cases manually or using synthetic data generation

   .. grid-item-card:: Manage checks
      :link: checks
      :link-type: doc

      Build and deploy validation rules and metrics for your tests

   .. grid-item-card:: Run and Schedule Evaluations
      :link: evaluations
      :link-type: doc

      Execute tests programmatically in the Hub or locally

   .. grid-item-card:: API Reference
      :link: reference/index
      :link-type: doc

      Complete SDK documentation for the Hub entities and resources

Install the client library
--------------------------

The library is compatible with Python 3.9 to 3.12.

.. code-block:: bash

    pip install giskard-hub

Authentication
--------------

To use the SDK, you need to authenticate with the Hub. You can do this by setting the following environment variables:

.. code-block:: bash

    export GISKARD_HUB_URL="https://your-hub-url"
    export GISKARD_HUB_TOKEN="your-token"

Alternatively, you can pass these values directly to the client:

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient(
        url="https://your-hub-url",
        token="your-token"
    )

.. tip::

   Make sure you are using the correct URL for your Giskard Hub instance. The URL should end with ``/_api``.

You can now use the client to interact with the Hub. You will be able to control the Hub programmatically, independently

Running your first evaluation
-----------------------------

You can now use the client to interact with the Hub. You will be able to control the Hub programmatically, independently
of the UI. Let's start by initializing a client instance:

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

    # List all projects
    projects = hub.projects.list()
    print(f"Found {len(projects)} projects")

    # Get a specific project
    project = hub.projects.get("project-id")
    print(f"Project: {project.name}")

    # List all datasets in the project
    datasets = hub.datasets.list(project.id)
    print(f"Found {len(datasets)} datasets")


Create a project
________________

.. code-block:: python

   from giskard_hub import HubClient

   hub = HubClient()

   project = hub.projects.create(
      name="My first project",
      description="This is a test project to get started with the Giskard Hub client library",
   )

That's it! You have created a project.

.. tip::

   If you have an already existing project, you can easily retrieve it. Either use ``hub.projects.list()`` to get a
   list of all projects, or use ``hub.projects.retrieve("YOUR_PROJECT_ID")`` to get a specific project.

Import a dataset
________________

Let's now create a dataset and add a chat test case example.

.. code-block:: python

    # Let's create a dataset
    dataset = hub.datasets.create(
        project_id=project.id,
        name="My first dataset",
        description="This is a test dataset",
    )


We can now add a chat test case example to the dataset. This will be used for the model evaluation.

.. code-block:: python

   import random

   # Add a chat test case example
   hub.chat_test_cases.create(
      dataset_id=dataset.id,
      messages=[
         dict(role="user", content="What is the capital of France?"),
         dict(role="assistant", content="Paris"),
         dict(role="user", content="What is the capital of Germany?"),
      ],
      demo_output=dict(
         role="assistant",
         content="I don't know that!",
         metadata=dict(
               response_time=random.random(),
               test_metadata="No matter which kind of metadata",
         ),
      ),
      checks=[
         dict(identifier="correctness", params={"reference": "Berlin"}),
         dict(identifier="conformity", params={"rules": ["The agent should always provide short and concise answers."]}),
         dict(identifier="metadata", params={"json_path_rules": [{"json_path": "$.tool", "expected_value": "calculator", "expected_value_type": "string"}]}),
         dict(identifier="semantic_similarity", params={"reference": "Berlin", "threshold": 0.8}),
      ]
   )

These are the attributes you can set for a chat test case (the only required attribute is ``messages``):

- ``messages``: A list of messages in the chat. Each message is a dictionary with the following keys:
    - ``role``: The role of the message, either "user" or "assistant".
    - ``content``: The content of the message.
- ``demo_output``: A demonstration of a (possibly wrong) output from the model with an optional metadata. This is just for demonstration purposes.
- ``checks``: A list of checks that the chat should pass. This is used for evaluation. Each check is a dictionary with the following keys:
    - ``identifier``: The identifier of the check. If it's a built-in check, you will also need to provide the ``params`` dictionary. The built-in checks are:
        - ``correctness``: The output of the model should match the reference.
        - ``conformity``: The chat test case should follow a set of rules.
        - ``groundedness``: The output of the model should be grounded to a specific context.
        - ``string_match``: The output of the model should contain a specific string (keyword or sentence).
        - ``metadata``: The metadata output of the model should match a list of JSON path rules.
    - ``semantic_similarity``: The output of the model should be semantically similar to the reference.
    - ``params``: A dictionary of parameters for the check. The parameters depend on the check type:
        - For the ``correctness`` check, the parameter is ``reference`` (type: ``str``), which is the expected output.
        - For the ``conformity`` check, the parameter is ``rules`` (type: ``list[str]``), which is a list of rules that the chat should follow.
        - For the ``groundedness`` check, the parameter is ``context`` (type: ``str``), which is the context in which the model should ground its output.
        - For the ``string_match`` check, the parameter is ``keyword`` (type: ``str``), which is the string that the model's output should contain.
        - For the ``metadata`` check, the parameter is ``json_path_rules`` (type: ``list[dict]``), which is a list of dictionaries with the following keys:
            - ``json_path``: The JSON path to the value that the model's output should contain.
            - ``expected_value``: The expected value at the JSON path.
            - ``expected_value_type``: The expected type of the value at the JSON path, one of ``string``, ``number``, ``boolean``.
        - For the ``semantic_similarity`` check, the parameters are ``reference`` (type: ``str``) and ``threshold`` (type: ``float``), where ``reference`` is the expected output and ``threshold`` is the similarity score below which the check will fail.

.. note::

   For detailed information about these checks, including examples and how they work, see :doc:`/hub/ui/annotate`.

You can add as many chat test cases as you want to the dataset.

Configure an Agent
___________________

.. note:: In this section we will run evaluation against agents configured in
    the Hub. If you want to evaluate a local agent that is not yet exposed with
    an API, check the :doc:`/hub/sdk/evaluations`.

Before running our first evaluation, we'll need to set up an agent. You'll need an API endpoint ready to serve the agent.
Then, you can configure the agent API in the Hub:

.. code-block:: python

    model = hub.models.create(
        project_id=project.id,
        name="My Agent",
        description="An agent for demo purposes",
        url="https://my-agent-endpoint.example.com/agent_v1",
        supported_languages=["en", "fr"],
        # if your agent endpoint needs special headers:
        headers={"X-API-Key": "MY_TOKEN"},
    )


We can test that everything is working well by running a chat with the agent:

.. code-block:: python

    response = model.chat(
        messages=[
            dict(role="user", content="What is the capital of France?"),
            dict(role="assistant", content="Paris"),
            dict(role="user", content="What is the capital of Germany?"),
        ],
    )

    print(response)

If all is working well, this will return something like

.. code-block:: python

    ModelOutput(
        message=ChatMessage(
            role='assistant',
            content='The capital of Germany is Berlin.'
        ),
        metadata={}
    )

Run a remote evaluation
_______________________

We can now launch a remote evaluation of our agent!

.. code-block:: python

    eval_run = hub.evaluate(
        model=model,
        dataset=dataset,
        name="test-run",  # optional
    )

The evaluation will run asynchronously on the Hub. For this reason, the
:class:`giskard_hub.data.evaluation.EvaluationRun` object returned by the ``evaluate``
method may miss some attributes (e.g. ``eval_run.metrics`` may be empty) until
the evaluation is complete.

To wait until the evaluation run has finished running, you can use:

.. code-block:: python

    eval_run.wait_for_completion()


Once ready, you can print the evaluation metrics:

.. code-block:: python

    eval_run.print_metrics()

.. image:: /_static/images/cli/metrics_output.png
   :align: center
   :alt: "Metrics"
   :width: 800

.. tip::

    You can directly pass IDs to the evaluate function, e.g. ``model=model_id``
    and ``dataset=dataset_id``, without having to retrieve the objects first.
