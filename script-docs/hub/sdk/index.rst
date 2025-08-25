:og:title: Giskard Hub - Enterprise Agent Testing - SDK Quickstart
:og:description: Build enterprise LLM agent testing with our Python SDK. Automate testing, manage projects, datasets, and run evaluations.

Quickstart & Setup
==================

**Giskard Hub is our enterprise platform for LLM agent testing with team collaboration and continuous red teaming.**

The Giskard Hub Python SDK provides technical users with programmatic access to all enterprise features, enabling automation of agent testing, project and dataset management.

.. grid:: 1 1 2 2

   .. grid-item-card:: Manage Projects
      :link: projects
      :link-type: doc

      Create, update, and organize projects

   .. grid-item-card:: Manage Datasets and Conversations
      :link: datasets/index
      :link-type: doc

      Create, update, and organize test datasets and conversations manually or using synthetic data generation

   .. grid-item-card:: Manage Checks
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
   :caption: Shell

   pip install giskard-hub

Configure your environment
--------------------------

Get your API key
________________

Head over to your Giskard Hub instance and click on the user icon in the bottom left corner. You will find your personal
API key, click on the button to copy it.

.. note::

   If you don't see your API key in the UI, it means your administrator has not enabled API keys. Please contact them to get one.


Connect to the Hub
__________________

You can set the following environment variables to avoid passing them as arguments to the client:

.. code-block:: bash
   :caption: Shell

   export GSK_API_KEY=your_api_key
   export GSK_HUB_URL=https://your-giskard-hub-instance.com/_api

.. tip::
   Make sure you are using the correct URL for your Giskard Hub instance. The URL should end with ``/_api``.

Running your first evaluation
-----------------------------

You can now use the client to interact with the Hub. You will be able to control the Hub programmatically, independently
of the UI. Let's start by initializing a client instance:

.. code-block:: python

   from giskard_hub import HubClient

   hub = HubClient()

If you didn't set up the environment variables, you can provide the API key and
Hub URL as arguments:

.. code-block:: python

   from giskard_hub import HubClient

   hub = HubClient(
      api_key="YOUR_GSK_API_KEY",
      hub_url="THE_GSK_HUB_URL",
   )

You can now use the ``hub`` client to control the Giskard Hub! Let's start by creating a fresh project.


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

Let's now create a dataset and add a conversation example.

.. code-block:: python

    # Let's create a dataset
    dataset = hub.datasets.create(
        project_id=project.id,
        name="My first dataset",
        description="This is a test dataset",
    )


We can now add a conversation example to the dataset. This will be used for the model evaluation.

.. code-block:: python

   from giskard_hub import HubClient
   import random

   # Add a conversation example
   hub.conversations.create(
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
      ]
   )

These are the attributes you can set for a conversation (the only required attribute is ``messages``):

- ``messages``: A list of messages in the conversation. Each message is a dictionary with the following keys:
    - ``role``: The role of the message, either "user" or "assistant".
    - ``content``: The content of the message.
- ``demo_output``: A demonstration of a (possibly wrong) output from the model with an optional metadata. This is just for demonstration purposes.
- ``checks``: A list of checks that the conversation should pass. This is used for evaluation. Each check is a dictionary with the following keys:
    - ``identifier``: The identifier of the check. If it's a built-in check, you will also need to provide the ``params`` dictionary. The built-in checks are:
        - ``correctness``: The output of the model should match the reference.
        - ``conformity``: The conversation should follow a set of rules.
        - ``groundedness``: The output of the model should be grounded in the conversation.
        - ``string_match``: The output of the model should contain a specific string (keyword or sentence).
        - ``metadata``: The metadata output of the model should match a list of JSON path rules.
    - ``params``: A dictionary of parameters for the check. The parameters depend on the check type:
        - For the ``correctness`` check, the parameter is ``reference`` (type: ``str``), which is the expected output.
        - For the ``conformity`` check, the parameter is ``rules`` (type: ``list[str]``), which is a list of rules that the conversation should follow.
        - For the ``groundedness`` check, the parameter is ``context`` (type: ``str``), which is the context in which the model should ground its output.
        - For the ``string_match`` check, the parameter is ``keyword`` (type: ``str``), which is the string that the model's output should contain.
        - For the ``metadata`` check, the parameter is ``json_path_rules`` (type: ``list[dict]``), which is a list of dictionaries with the following keys:
            - ``json_path``: The JSON path to the value that the model's output should contain.
            - ``expected_value``: The expected value at the JSON path.
            - ``expected_value_type``: The expected type of the value at the JSON path, one of ``string``, ``number``, ``boolean``.

.. note::

   For detailed information about these checks, including examples and how they work, see :doc:`/hub/ui/annotate`.

You can add as many conversations as you want to the dataset.

Configure an Agent
___________________

.. note:: In this section we will run evaluation against agents configured in
    the Hub. If you want to evaluate a local agent that is not yet exposed with
    an API, check the :doc:`/hub/sdk/evaluations`.

Before running our first evaluation, we'll need to set up an agent. You'll need an API endpoint ready to serve the agent.
Then, you can configure the agent API in the Hub:

.. code-block:: python

    agent = hub.agents.create(
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

    response = agent.chat(
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
        model=agent,  # Note: parameter is still named 'model' for backward compatibility
        dataset=dataset,
        name="test-run",  # optional
    )

The evaluation will run asynchronously on the Hub. For this reason, the
:class:`giskard_hub.dat.EvaluationRun` object returned by the ``evaluate``
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
