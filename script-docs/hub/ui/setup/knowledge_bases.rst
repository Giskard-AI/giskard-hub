:og:title: Giskard Hub UI - Setup Knowledge Bases
:og:description: Create, manage, and organize projects, agents and knowledge bases through the user interface. Set up workspaces, configure access controls, and manage team collaboration.

Setup knowledge bases
=====================

In this section, we will walk you through how to setup knowledge bases using the Hub interface.

.. tip::

    A **Knowledge Base** is a domain-specific collection of information. You can have several knowledge bases for different areas of your business.

Add a knowledge base
--------------------

On the Knowledge Bases, click on "Add Knowledge Base" button.

.. image:: /_static/images/hub/import-kb-list.png
   :align: center
   :alt: "List of knowledge bases"
   :width: 800

Knowledge base fields
---------------------

The interface below displays the knowledge base details that need to be filled out.

.. image:: /_static/images/hub/import-kb-detail.png
   :align: center
   :alt: "Import a knowledge base"
   :width: 800

- ``Name``: The name of the knowledge base.
- ``File``: The document to upload, containing the knowledge base content. Supported formats are:
    - **JSON**: A JSON file containing an array of objects
    - **JSONL**: A JSON Lines file with one object per line

File formats
------------

**JSON/JSONL format requirements:**

Each object in your JSON or JSONL file should have the following structure:

.. code-block:: json

    {
        "text": "Your document content here",
        "topic": "Optional topic classification"
    }

- ``text`` (required): The document content
- ``topic`` (optional): The topic classification for the document

Validation rules
----------------

**General rules for all formats:**
    - If the ``text`` has a value but the ``topic`` is blank, the ``topic`` will be set to 'Others'. However, if all topics are blank, the ``topic`` will be automatically generated.
    - If both the ``text`` and ``topic`` are blank, or if the ``text`` is blank but the ``topic`` has a value, the entry will not be imported.

The interface below displays information about the knowledge base and its content with corresponding topics. As mentioned above, if no topics were uploaded with the knowledge base, Giskard Hub will also identify and generate them for you. In the example below, the knowledge base is ready to be used with over 1200 documents and 7 topics.

.. image:: /_static/images/hub/import-kb-success.png
   :align: center
   :alt: "Knowledge base successfully imported"
   :width: 800

Next steps
----------

Now that you have created a project, you can start setting up your agents and knowledge bases.

* **Setup agents** - :doc:`/hub/ui/setup/agents`
* **Manage users and groups** - :doc:`/hub/ui/access-rights`
* **Create test cases and datasets** - :doc:`/hub/ui/datasets/index`
* **Launch vulnerability scans** - :doc:`/hub/ui/scan/index`