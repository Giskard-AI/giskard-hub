:og:title: Giskard Hub UI - Enterprise Agent Testing Platform
:og:description: Launch enterprise LLM agent testing with team collaboration, continuous red teaming, and comprehensive evaluation workflows. Perfect for business users managing AI safety in production environments.

====================
Quickstart & setup
====================

**Giskard Hub is our enterprise platform for LLM agent testing with team collaboration and continuous red teaming.** The Hub provides a comprehensive user interface for performing LLM evaluations in production environments with enterprise-grade security and collaboration features.

The Hub is the user interface from which you can perform LLM evaluations. It implements the following 4-step workflow:

.. image:: /_static/images/hub/hub-workflow.png
   :align: center
   :alt: "The hub workflow"
   :width: 800


.. grid:: 1 1 2 2

   .. grid-item-card:: Setup projects, agents and knowledge bases
      :link: setup/index
      :link-type: doc

      Set up projects, agents and knowledge bases.
   
   .. grid-item-card:: Launch vulnerability scans
      :link: scan/index
      :link-type: doc

      Automatically scan your agent for safety and security failures.

   .. grid-item-card:: Create test cases and datasets
      :link: datasets/index
      :link-type: doc

      Create test cases and datasets manually or using synthetic data generation.

   .. grid-item-card:: Evaluate tests and assign validation rules
      :link: annotate/index
      :link-type: doc

      Use domain knowledge to review and refine test cases through humans in the loop.

   .. grid-item-card:: Run, schedule and compare evaluations
      :link: evaluations/index
      :link-type: doc

      Run evaluations and schedule them to run automatically.

   .. grid-item-card:: Release notes
      :link: release_notes/index
      :link-type: doc

      View the latest features and changes.

High-level workflow
-------------------

.. mermaid::
   :align: center

   graph LR
       B[Red Team Scan] -->  D[Create Test Cases]
       D --> F[Annotate & Assign Checks]
       F --> G[Run Evaluations]
       G --> H[Review Results]
       H --> F
       H --> B

.. note::

    Throughout this user guide, we'll use a banking app called Zephyr Bank, designed by data scientists. The app's agent provides customer service support on their website, offering knowledge about the bank's products, services, and more.

The dashboard
================

The Dashboard is the first page you'll see upon logging in. It provides an overview of your project, displaying the number of agents, datasets, evaluations, and knowledge bases.

It also features a graph showing the agent's performance over time, measured by the average success rate of the evaluations. The success rate is calculated based on some evaluation metrics, such as Conformity, Correctness, Groundedness, String Matching, Metadata, Semantic Similarity, and more. We'll delve into these metrics in more detail in the Evaluations section.

.. note::

   For detailed information about evaluation metrics and checks, including examples and how they work, see :doc:`/hub/ui/annotate/index`.

Additionally, the dashboard lists your most recent evaluations and datasets for quick access.

.. image:: /_static/images/hub/dashboard.png
   :align: center
   :alt: "Dashboard"
   :width: 800


Create a project
=================

In this section, you will learn how to create a project.

First, click on the "Settings" icon on the left panel, this page allows you to manage your projects and users (if you have the proper access rights).

In the Projects tab, click on "Create project" button. A modal will appear where you can enter your project's name and description.

.. image:: /_static/images/hub/create-project.png
   :align: center
   :alt: "Create a project"
   :width: 800

Once the project is created, you can access its dashboard by clicking on it in the list. Alternatively, use the dropdown menu in the upper left corner of the screen to select the project you want to work on.


Setup an agent
================

This section guides you through creating a new agent.

.. note::

    Agents are configured through an API endpoint. They can be evaluated against datasets.

On the Agents page, click on the "New agent" button.

.. image:: /_static/images/hub/setup-agent-list.png
   :align: center
   :alt: "List of agents"
   :width: 800

The interface below displays the agent details that need to be filled out.

.. image:: /_static/images/hub/setup-agent-detail.png
   :align: center
   :alt: "Setup an agent"
   :width: 800

- ``Name``: The name of the agent.
- ``Description``: Used to refine automatic evaluation and generation for better accuracy in your specific use case.
- ``Supported Languages``: Add the languages your agent can handle. Note that this affects data generation.
- ``Connection Settings``:
    - ``Agent API Endpoint``: The URL of your agent's API endpoint. This is where requests are sent to interact with your agent.
    - ``Headers``: These are useful for authentication and other custom headers


The endpoint should expect an object with the following structure:

.. code-block:: python

    {
        "messages": [
            {
            "role": "user",
            "content": "Hello!"
            },
            {
            "role": "assistant",
            "content": "Hello! How can I help you?"
            },
            {
            "role": "user",
            "content": "What color is an orange?"
            }
        ]
    }

The endpoint's response should have the following structure:

.. code-block:: python

    {
        "response": {
            "role": "assistant",
            "content": "An orange is green"
        },
        "metadata": {
            "some_key": "whatever value"
        }
    }

Import a knowledge base
========================

This section guides you through importing your custom knowledge base.

.. note::

    A **Knowledge Base** is a domain-specific collection of information. You can have several knowledge bases for different areas of your business.

On the Knowledge Bases, click on "Add Knowledge Base" button.

.. image:: /_static/images/hub/import-kb-list.png
   :align: center
   :alt: "List of knowledge bases"
   :width: 800

The interface below displays the knowledge base details that need to be filled out.

.. image:: /_static/images/hub/import-kb-detail.png
   :align: center
   :alt: "Import a knowledge base"
   :width: 800

- ``Name``: The name of the knowledge base.
- ``File``: The document to upload, containing the knowledge base content. Supported formats are:
    - **JSON**: A JSON file containing an array of objects
    - **JSONL**: A JSON Lines file with one object per line


**JSON/JSONL format requirements:**

Each object in your JSON or JSONL file should have the following structure:

.. code-block:: json

    {
        "text": "Your document content here",
        "topic": "Optional topic classification"
    }

- ``text`` (required): The document content
- ``topic`` (optional): The topic classification for the document

**General rules for all formats:**
    - If the ``text`` has a value but the ``topic`` is blank, the ``topic`` will be set to 'Others'. However, if all topics are blank, the ``topic`` will be automatically generated.
    - If both the ``text`` and ``topic`` are blank, or if the ``text`` is blank but the ``topic`` has a value, the entry will not be imported.

The interface below displays information about the knowledge base and its content with corresponding topics. As mentioned above, if no topics were uploaded with the knowledge base, Giskard Hub will also identify and generate them for you. In the example below, the knowledge base is ready to be used with over 1200 documents and 7 topics.

.. image:: /_static/images/hub/import-kb-success.png
   :align: center
   :alt: "Knowledge base successfully imported"
   :width: 800
