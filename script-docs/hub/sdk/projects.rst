:og:title: Giskard Hub - Enterprise Agent Testing - Projects Management
:og:description: Create, manage, and organize projects programmatically. Set up workspaces, configure access controls, and manage team collaboration through the Python SDK.

================================================
Manage your projects, agents and knowledge bases
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

You can also update the project description and failure categories:

.. code-block:: python

    from giskard_hub.data.project import FailureCategory
    
    # Define failure categories for your project
    failure_categories = [
        FailureCategory(
            identifier="hallucination",
            title="Hallucination",
            description="Model generated false or misleading information"
        ),
        FailureCategory(
            identifier="bias",
            title="Bias", 
            description="Model response shows unfair bias"
        )
    ]
    
    # Update project with failure categories
    project = hub.projects.update(
        "<PROJECT_ID>",
        name="My updated project",
        description="Updated project description",
        failure_categories=failure_categories
    )

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

Working with Failure Categories
_______________________________

Failure categories help you organize and classify different types of AI failures that occur during evaluations. They provide structured categorization of issues like hallucinations, bias, or other business logic failures.

.. code-block:: python

    from giskard_hub.data.project import FailureCategory
    
    # Access failure categories from a project
    project = hub.projects.retrieve("<PROJECT_ID>")
    
    for category in project.failure_categories:
        print(f"Category: {category.title}")
        print(f"Identifier: {category.identifier}")
        print(f"Description: {category.description}")

When you run evaluations, failed test cases can be automatically or manually assigned to these failure categories, helping you track and analyze patterns in your AI system's failures.

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

Knowledge bases
---------------

The `hub.knowledge_bases` resource allows you to create, retrieve, update, delete, and list knowledge bases, as well as list topics and documents within a knowledge base.

Create a knowledge base
_______________________

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

Retrieve a knowledge base
_________________________

You can retrieve a knowledge base by ID:

.. code-block:: python

    kb = hub.knowledge_bases.retrieve("<KNOWLEDGE_BASE_ID>")

Update a knowledge base
_______________________

You can update a knowledge base:

.. code-block:: python

    kb_updated = hub.knowledge_bases.update(
        "<KNOWLEDGE_BASE_ID>",
        name="Updated KB name",
        description="Updated description"
    )

Delete a knowledge base
_______________________

You can delete a knowledge base by ID (or a list of IDs):

.. code-block:: python

    hub.knowledge_bases.delete("<KNOWLEDGE_BASE_ID>")

List knowledge bases
____________________

You can list all knowledge bases in a project:

.. code-block:: python

    kbs = hub.knowledge_bases.list(project_id=project.id)
    for kb in kbs:
        print(f"{kb.name} - Topics: {[topic['name'] for topic in kb.topics]}")


List documents in a knowledge base
__________________________________

You can list documents for a knowledge base, optionally filtered by topic:

.. code-block:: python

    documents = hub.knowledge_bases.list_documents("<KNOWLEDGE_BASE_ID>")
    for doc in documents:
        print(doc.content)

    # To filter by topic:
    documents = hub.knowledge_bases.list_documents("<KNOWLEDGE_BASE_ID>", topic_id="<TOPIC_ID>")
    for doc in documents:
        print(doc.content)