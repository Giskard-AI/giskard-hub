:og:title: Giskard Hub SDK - Setup Agents
:og:description: Create, manage, and organize agents programmatically. Set up workspaces, configure access controls, and manage team collaboration through the comprehensive Python SDK.

Setup agents
------------

Agents are the AI systems, LLMs or agents you want to test and evaluate. They are configured through an API endpoint.

In this section, we will walk you through how to setup agents using the SDK.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

Create an agent
________________

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

Next steps
__________

Now that you have created an agent, you can continue by setting up your knowledge base or creating test cases and datasets.

* **Setup knowledge bases** - :doc:`/hub/sdk/setup/knowledge_bases`
* **Create test cases and datasets** - :doc:`/hub/sdk/datasets/index`