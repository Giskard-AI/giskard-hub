===============================================
Manage Projects and Models
===============================================

In this section, we will show how to manage projects programmatically using the SDK.

- A **project** is a collection of models, datasets, and evaluations.
- A **model** is a LLM, RAG workflow or Agent that needs to be evaluated.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to create, update, and delete projects and models.

Projects
--------

Create a project
________________

You can create a project using the ``hub.projects.create()`` method. Here's a basic example:

.. code-block:: python

    project = hub.projects.create(
        name="My first project",
        description="This is a test project to get started with the Giskard Hub client library",
    )

Retrieve a project
__________________

You can retrieve a project using the ``hub.projects.retrieve()`` method. Here's a basic example:

.. code-block:: python

    project = hub.projects.retrieve("<PROJECT_ID>")

Update a project
________________

You can update a project using the ``hub.projects.update()`` method. Here's a basic example:

.. code-block:: python

    project = hub.projects.update("<PROJECT_ID>", name="My updated project")

Delete a project
________________

You can delete a project using the ``hub.projects.delete()`` method. Here's a basic example:

.. code-block:: python

    hub.projects.delete("<PROJECT_ID>")

List projects
_____________

You can list all projects using the ``hub.projects.list()`` method. Here's a basic example:

.. code-block:: python

    projects = hub.projects.list()

    for project in projects:
        print(project.name)

Models
------

Create a model
________________

Before running our first evaluation, we’ll need to set up a model. You’ll need an API endpoint ready to serve the model. Then, you can configure the model API in the Hub:

You can create a model using the ``hub.models.create()`` method. Here's a basic example:

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

After creating the model, you can test that everything is working well by running a chat with the model:

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

Retrieve a model
________________

You can retrieve a model using the ``hub.models.retrieve()`` method. Here's a basic example:

.. code-block:: python

    model = hub.models.retrieve("<MODEL_ID>")

Update a model
________________

You can update a model using the ``hub.models.update()`` method. Here's a basic example:

.. code-block:: python

    model = hub.models.update("<MODEL_ID>", name="My updated model")

Delete a model
________________

You can delete a model using the ``hub.models.delete()`` method. Here's a basic example:

.. code-block:: python

    hub.models.delete("<MODEL_ID>")

List models
____________

You can list all models using the ``hub.models.list()`` method. Here's a basic example:

.. code-block:: python

    models = hub.models.list("<PROJECT_ID>")

    for model in models:
        print(model.name)