:og:title: Giskard Hub - Enterprise Agent Testing - Project Management
:og:description: Create, update, and organize LLM agent testing projects programmatically. Manage project settings, users, and configurations through code.

===============================================
Manage Projects and Agents
===============================================

In this section, we will show how to manage projects programmatically using the SDK.

- A **project** is a collection of agents, datasets, and evaluations.
- An **agent** is a LLM, RAG workflow or AI Agent that needs to be evaluated.

.. note::
   **Migration Note**: The SDK now uses "agents" terminology instead of "models" to align with the UI.
   The ``hub.models`` attribute is deprecated but still works for backward compatibility.
   Please use ``hub.agents`` for new code.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to create, update, and delete projects and agents.

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

Agents
------

Create an agent
________________

Before running our first evaluation, we'll need to set up an agent. You'll need an API endpoint ready to serve the agent. Then, you can configure the agent API in the Hub:

You can create an agent using the ``hub.agents.create()`` method. Here's a basic example:

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

After creating the agent, you can test that everything is working well by running a chat with the agent:

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

Retrieve an agent
_________________

You can retrieve an agent using the ``hub.agents.retrieve()`` method. Here's a basic example:

.. code-block:: python

    agent = hub.agents.retrieve("<AGENT_ID>")

Update an agent
_______________

You can update an agent using the ``hub.agents.update()`` method. Here's a basic example:

.. code-block:: python

    agent = hub.agents.update("<AGENT_ID>", name="My updated agent")

Delete an agent
_______________

You can delete an agent using the ``hub.agents.delete()`` method. Here's a basic example:

.. code-block:: python

    hub.agents.delete("<AGENT_ID>")

List agents
___________

You can list all agents using the ``hub.agents.list()`` method. Here's a basic example:

.. code-block:: python

    agents = hub.agents.list("<PROJECT_ID>")

    for agent in agents:
        print(agent.name)

Legacy API (Deprecated)
_______________________

.. warning::
   The following methods are deprecated and will be removed in a future version.
   Please use the ``hub.agents`` methods shown above instead.

.. code-block:: python

    # Deprecated - use hub.agents.create() instead
    model = hub.models.create(...)

    # Deprecated - use hub.agents.retrieve() instead
    model = hub.models.retrieve("<MODEL_ID>")

    # Deprecated - use hub.agents.update() instead
    model = hub.models.update("<MODEL_ID>", name="My updated model")

    # Deprecated - use hub.agents.delete() instead
    hub.models.delete("<MODEL_ID>")

    # Deprecated - use hub.agents.list() instead
    models = hub.models.list("<PROJECT_ID>")