:og:title: Giskard Hub - Enterprise Agent Testing - Detect Business Failures
:og:description: Generate and manage business logic test cases programmatically. Test compliance, domain-specific scenarios, and business requirements in your LLM agents.

======================================================
Detect business failures by generating synthetic tests
======================================================

Generative AI agents can face an endless variety of real-world scenarios, making it impossible to manually enumerate all possible test cases. Automated, synthetic test case generation is therefore essential—especially when you lack real user conversations to import as tests. However, a major challenge is to ensure that these synthetic cases are tailored to your business context, rather than being overly generic.

By generating domain-specific synthetic tests, you can proactively identify and address these types of failures before they impact your users or business operations.

In this section, we will walk you through how to generate synthetic test cases to detect business failures, such as *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

What are AI business failures?
------------------------------

AI business failures are failures that are related to the business of the AI system. To detect them, we need to generate tests that are designed to trigger failures.

For more context and practical examples of business failures, you can explore our :doc:`/hub/ui/datasets/business` or `realperformance.giskard.ai <https://realperformance.giskard.ai>`_.

The Giskard Hub provides an interface for the synthetic generation of legitimate queries **with expected outputs**. It automatically clusters the documents from the internal knowledge base into key topics and generates test cases for each topic by applying a set of perturbations.
These clusters and topics are then used to generate dedicated test that challenge the agent to answer questions about the specific topic in a way that might not align with the business rules of your organization.

.. tip::

   Business failures are different from security failures. While security failures focus on malicious exploitation and system integrity, business failures focus on the agent's ability to provide accurate, reliable, and appropriate responses in normal usage scenarios.
   If you want to detect security failures, check out the :doc:`/hub/sdk/datasets/security`.

Document-based tests generation
-------------------------------

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub.datasets`` client to control the Giskard Hub!

Create a knowledge base
_______________________

Before we can generate a dataset that is based on a knowledge base, we need to create a knowledge base.
You can do this by creating a JSONL file with a required ``text`` key and an optional ``topic`` key. If you don't provide a ``topic``, the Hub will automatically generate one for you.

.. code-block:: python

   import json

   knowledge_base = [
      {
         "text": "The text of the document",
         "topic": "The topic of the document",
      },
      {
         "text": "The text of the document",
         "topic": "The topic of the document",
      },
   ]
   with open("knowledge_base.jsonl", "w") as f:
      for item in knowledge_base:
         f.write(json.dumps(item) + "\n")

At this point, you manually upload the file to the Hub using the Hub UI as shown in the :doc:`/hub/ui/index` section.

.. code-block:: python

   kb = hub.knowledge_bases.create(
      project_id="<PROJECT_ID>",
      name="Knowledge Base",
      filename="knowledge_base.jsonl",
   )

This will return a :class:`~giskard_hub.data.KnowledgeBase` object, but this object might not be fully populated yet, as the knowledge base is processed asynchronously.
To get an up-to-date version of the knowledge base, we recommend visiting the Hub UI and checking the knowledge base page.

Generate a synthetic test dataset
_________________________________

After creating the knowledge base, we can generate a dataset that is based on the knowledge base we just created.
We can do this by using the ``hub.datasets.generate_knowledge()`` method. Once again, we need to provide an agent ID.
We can get the agent ID and the knowledge base ID by listing all agents using the ``hub.models.list("<PROJECT_ID>")`` and ``hub.knowledge_bases.list("<PROJECT_ID>")`` methods or retrieve the IDs from the Hub UI.

.. code-block:: python

   dataset = hub.datasets.generate_knowledge(
      model_id="<MODEL_ID>",
      knowledge_base_id=kb.id,
      dataset_name="Knowledge Base Dataset",
      description="<MODEL_DESCRIPTION>",
      nb_questions=10,
      # filter the topics to use for the dataset
      topic_ids=[topic["id"] for topic in kb.topics],
   )

This will return a :class:`~giskard_hub.data.Dataset` object, but this object might not be fully populated yet, as the dataset is generated asynchronously.
To get an up-to-date version of the dataset and the generation, we recommend visiting the Hub UI and checking the dataset page.

Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Generate security vulnerabilities** - Try :doc:`/hub/sdk/datasets/security`
* **Set-up continuous red teaming** - Understand exhaustive and proactive detection with :doc:`/hub/ui/continuous-red-teaming`