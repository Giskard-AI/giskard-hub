:og:title: Giskard Hub SDK - Setup Projects
:og:description: Create, manage, and organize projects programmatically. Set up workspaces, configure access controls, and manage team collaboration through the comprehensive Python SDK.

Setup projects
--------------

Projects are the top-level organizational units in Giskard Hub. They provide a workspace for your team to collaborate on LLM agent testing and evaluation.

Each project can contain:

* **Agents**: The AI systems you want to test and evaluate
* **Datasets**: Collections of chat test cases (conversations)
* **Checks**: Validation rules and metrics for your tests
* **Knowledge bases**: Domain-specific information sources
* **Evaluations**: Test runs and their results
* **Users and groups**: Team members with different access levels

In this section, we will walk you through how to setup projects using the SDK.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

Create a project
________________

You can create a project using the ``hub.projects.create()`` method. Example:

.. code-block:: python

    project = hub.projects.create(
        name="My first project",
        description="This is a test project to get started with the Giskard Hub client library",
    )

For detailed information about creating, updating, and deleting projects, see the :doc:`/hub/sdk/reference/resources/index` section.


Next steps
__________

Now that you have created a project, you can start setting up your agents and knowledge bases.

* **Setup agents** - :doc:`/hub/sdk/setup/agents`
* **Setup knowledge bases** - :doc:`/hub/sdk/setup/knowledge_bases`