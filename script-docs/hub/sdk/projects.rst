:og:title: Giskard Hub - Enterprise Agent Testing - Projects Management
:og:description: Create, manage, and organize projects programmatically. Set up workspaces, configure access controls, and manage team collaboration through the Python SDK.

================================================
Manage your projects and agents
================================================

Projects are the top-level organizational units in Giskard Hub. They provide a workspace for your team to collaborate on LLM agent testing and evaluation.

Each project can contain:

* **Agents**: The AI systems you want to test and evaluate
* **Datasets**: Collections of test cases and conversations
* **Knowledge bases**: Domain-specific information sources
* **Evaluations**: Test runs and their results
* **Users and groups**: Team members with different access levels

In this section, we will walk you through how to manage projects using the SDK.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to create, update, and delete projects and agents.

Projects
--------

Create a project
________________

You can create a project using the ``hub.projects.create()`` method. Example:

.. code-block:: python

    project = hub.projects.create(
        name="My first project",
        description="This is a test project to get started with the Giskard Hub client library",
    )

Retrieve a project
__________________

You can retrieve a project using the ``hub.projects.retrieve()`` method:

.. code-block:: python

    project = hub.projects.retrieve("<PROJECT_ID>")

Update a project
________________

You can update a project using the ``hub.projects.update()`` method:

.. code-block:: python

    project = hub.projects.update("<PROJECT_ID>", name="My updated project")

Delete a project
________________

You can delete a project using the ``hub.projects.delete()`` method:

.. code-block:: python

    hub.projects.delete("<PROJECT_ID>")

List projects
_____________

You can list all projects using the ``hub.projects.list()`` method:

.. code-block:: python

    projects = hub.projects.list()
    for project in projects:
        print(project.name)

Agents
------

Create an agent
_______________

You can create an agent using the ``hub.models.create()`` method. Example:

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

After creating the agent, you can test it by running a chat:

.. code-block:: python

    response = model.chat(
        messages=[
            dict(role="user", content="What is the capital of France?"),
            dict(role="assistant", content="Paris"),
            dict(role="user", content="What is the capital of Germany?"),
        ],
    )
    print(response)

If all is working well, this will return something like:

.. code-block:: python

    ModelOutput(
        message=ChatMessage(
            role='assistant',
            content='The capital of Germany is Berlin.'
        ),
        metadata={}
    )

Retrieve an agent
_________________

You can retrieve an agent using the ``hub.models.retrieve()`` method:

.. code-block:: python

    model = hub.models.retrieve("<MODEL_ID>")

Update an agent
_______________

You can update an agent using the ``hub.models.update()`` method:

.. code-block:: python

    model = hub.models.update("<MODEL_ID>", name="My updated agent")

Delete an agent
_______________

You can delete an agent using the ``hub.models.delete()`` method:

.. code-block:: python

    hub.models.delete("<MODEL_ID>")

List agents
___________

You can list all agents in a project using the ``hub.models.list()`` method:

.. code-block:: python

    models = hub.models.list("<PROJECT_ID>")
    for model in models:
        print(model.name)