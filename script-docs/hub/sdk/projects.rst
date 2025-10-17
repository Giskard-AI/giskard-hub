:og:title: Giskard Hub - Enterprise Agent Testing - Projects Management
:og:description: Create, manage, and organize projects programmatically. Set up workspaces, configure access controls, and manage team collaboration through the Python SDK.

================================================
Manage projects, agents and knowledge bases
================================================

Projects are the top-level organizational units in Giskard Hub. They provide a workspace for your team to collaborate on LLM agent testing and evaluation.

Each project can contain:

* **Agents**: The AI systems you want to test and evaluate
* **Datasets**: Collections of chat test cases (conversations)
* **Knowledge bases**: Domain-specific information sources
* **Evaluations**: Test runs and their results
* **Users and groups**: Team members with different access levels

In this section, we will walk you through how to manage projects using the SDK.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to create, update, and delete projects, agents, and knowledge bases.

Manage projects
--------

You can create a project using the ``hub.projects.create()`` method. Example:

.. code-block:: python

    project = hub.projects.create(
        name="My first project",
        description="This is a test project to get started with the Giskard Hub client library",
    )

For detailed information about Creating, updating, and deleting projects, see the :doc:`/hub/sdk/reference/resources/index` section.

Manage agents
-------------

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

For detailed information about agent management methods, see the :doc:`/hub/sdk/reference/resources/index` section.

Manage knowledge bases
---------------

The `hub.knowledge_bases` resource allows you to create, retrieve, update, delete, and list knowledge bases, as well as list topics and documents within a knowledge base.

You can create a knowledge base using the ``hub.knowledge_bases.create()`` method. The `data` parameter can be a path (relative or absolute) to a JSON/JSONL file or a list of dicts containing a `text` key and an optional `topic` key.

.. code-block:: python

    # Create a kb from a file
    kb_from_file = hub.knowledge_bases.create(
        project_id="<PROJECT_ID>",
        name="My knowledge base",
        data="my_kb.json",  # could also be a JSONL file 
        description="A knowledge base for finance domain",
    )

    kb_from_list = hub.knowledge_bases.create(
        project_id="<PROJECT_ID>",
        name="My knowledge base",
        data=[
            {"text": "The capital of France is Paris", topic="europe"}, 
            {"text": "The capital of Germany is Berlin", topic="europe"}
        ],
        description="A knowledge base for geography domain",
    )

After creating the knowledge base, we need to wait for it to be ready because we need to process documents and topics server-side:

.. code-block:: python

    kb.wait_for_completion()

For detailed information about knowledge base management methods, see the :doc:`/hub/sdk/reference/resources/index` section.