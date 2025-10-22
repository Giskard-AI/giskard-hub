:og:title: Giskard Hub SDK - Setup Knowledge Bases
:og:description: Create, manage, and organize knowledge bases programmatically. Set up workspaces, configure access controls, and manage team collaboration through the comprehensive Python SDK.

Setup knowledge bases
---------------------

Knowledge bases are domain-specific information sources we can use to test your agents. They are used to generate synthetic test cases for business and security tests.

In this section, we will walk you through how to setup knowledge bases using the SDK.

First, let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

Create a knowledge base
_______________________

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

Next steps
__________

Now that you have created a knowledge base, you can continue by setting up your agent or creating test cases and datasets.

* **Setup agents** - :doc:`/hub/sdk/setup/agents`
* **Create test cases and datasets** - :doc:`/hub/sdk/datasets/index`