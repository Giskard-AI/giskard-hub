:og:title: Giskard Hub - Enterprise Agent Testing - Dataset Management
:og:description: Create, manage, and organize test datasets into Giskard Hub. Import chat test cases, generate synthetic data, and build comprehensive test datasets.

===================================
Manage datasets and chat test cases
===================================


This section will guide you through creating your own test datasets programmatically.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub.datasets`` client to control the Giskard Hub!

Datasets
============

A **dataset** is a collection of chat test cases (conversations) used to evaluate your agents. We allow manual test creation for fine-grained control,
but since generative AI agents can encounter an infinite number of scenarios, automated test case generation is often necessary, especially when you don't have any chat transcripts to import.

Create a dataset
________________

Manual creation
~~~~~~~~~~~~~~~

If you don't have a dataset already, you can create one manually.

.. code-block:: python

    dataset = hub.datasets.create(
        # The ID of the project where the dataset will be created
        project_id="<PROJECT_ID>",
        name="Production Data",
        description="This dataset contains chats that " \
        "are automatically sampled from the production environment.",
    )

    print(dataset.id)
    # "666030a0d41f357fd061374c"

Automated generation
~~~~~~~~~~~~~~~~~~~~

Alternatively, you can generate a dataset automatically using the following methods:

.. grid:: 1 1 2 2

    .. grid-item-card:: Detect Security Vulnerabilities by Generating Synthetic Tests
        :link: security
        :link-type: doc

        Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

    .. grid-item-card:: Detect Business Failures by Generating Synthetic Tests
        :link: business
        :link-type: doc

        Detect business failures, by generating synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

    .. grid-item-card:: Import Existing Datasets
        :link: import
        :link-type: doc

        Import existing test datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.


API Reference
==============

For detailed information about dataset and chat test case management methods, see the :doc:`/hub/sdk/reference` section.

.. toctree::
   :hidden:
   :maxdepth: 1

   security
   business
   import
