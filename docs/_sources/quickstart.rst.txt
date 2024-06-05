===========
Quick start
===========

Install the client library
==========================

The library is compatible with Python 3.9 to 3.12.

.. code-block:: bash
   :caption: Shell

   pip install giskard-hub


Get your API key
================

Head over to your Giskard Hub instance and click on the user icon in the top right corner. You will find your personal
API key, click on the button to copy it.

.. image:: /_static/quickstart/api_key.png
   :width: 779px
   :scale: 50%
   :align: center
   :alt: ""

.. note::

   If you don't see your API key in the UI, it means your administrator has not enabled API keys. Please contact them to get one. 


Configure your environment
==========================

You can set the following environment variables to avoid passing them as arguments to the client:

.. code-block:: bash
   :caption: Shell

   export GSK_API_KEY=your_api_key
   export GSK_HUB_URL=https://your-giskard-hub-instance.com/_api



Create a project and run an evaluation
======================================

You can now use the client to interact with the Hub. You will be able to control the Hub programmatically, independently
of the UI. Let's start by initializing a client instance:

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

If you didn't set up the environment variables, you can provide the API key and
Hub URL as arguments:

.. code-block:: python

    hub = HubClient(
        api_key="YOUR_GSK_API_KEY",
        hub_url="THE_GSK_HUB_URL",
    )


You can now use the ``hub`` client to control the LLM Hub! Let's start by creating a fresh project.


Create a project
----------------

.. code-block:: python

    project = hub.projects.create(
        name="My first project",
        description="This is a test project to get started with the Giskard Hub client library",
    )

That's it! You have created a project. You will now see it in the Hub UI project selector:

.. image:: /_static/quickstart/new_project.png
   :scale: 50%
   :align: center
   :alt: ""

.. tip::

   If you have an already existing project, you can easily retrieve it. Either use ``hub.projects.list()`` to get a
   list of all projects, or use ``hub.projects.retrieve("YOUR_PROJECT_ID")`` to get a specific project.



Import a dataset
----------------

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
        policies=[
            "The agent should always provide short and concise answers.",
        ],
    )

These are the attributes you can set for a conversation (the only required attribute is ``messages``):

- ``messages``: A list of messages in the conversation. Each message is a dictionary with the following keys:
    - ``role``: The role of the message, either "user" or "assistant".
    - ``content``: The content of the message.
- ``expected_output``: The expected output of the conversation. This is used for evaluation.
- ``policies``: A list of policies that the conversation should follow. This is used for evaluation.
- ``demo_output``: A demonstration of a (possibly wrong) output from the model. This is just for demonstration purposes.

You can add as many conversations as you want to the dataset.


Again, you'll find your newly created dataset in the Hub UI:

.. image:: /_static/quickstart/dataset_conversation.png
   :align: center
   :alt: ""


Configure a model
-----------------

.. note:: In this section we will run evaluation against models configured in
    the Hub. If you want to evaluate a local model that is not yet exposed with
    an API, check the :doc:`/guide/local-evaluation`.

Before running our first evaluation, we'll need to set up a model. You'll need an API endpoint ready to serve the model.
Then, you can configure the model API in the Hub:

.. code-block:: python

    model = hub.models.create(
        project_id=project.id,
        name="My Bot",
        description="A chatbot for demo purposes",
        url="https://my-model-endpoint.example.com/bot_v1",
        supported_languages=["en", "fr"],
        # if your model endpoint needs special headers:
        headers={"X-API-Key": "MY_TOKEN"},
    )


We can test that everything is working well by running a chat with the model:

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
-----------------------

We can now lunch a remote evaluation of our model!

.. code-block:: python

    eval_run = hub.evaluate(
        model=model,
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

.. image:: /_static/quickstart/metrics_output.png
   :align: center
   :alt: ""


.. tip:: 

    You can directly pass IDs to the evaluate function, e.g. ``model=model_id``
    and ``dataset=dataset_id``, without having to retrieve the objects first.

