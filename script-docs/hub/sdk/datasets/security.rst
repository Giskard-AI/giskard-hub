=============================================================
Detect Security Vulnerabilities by Generating Synthetic Tests
=============================================================

Since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don’t have any test conversations to import. One of the key challenges of synthetic test data generation is ensuring that the test cases are domain-specific rather than too generic.

In this section, we will walk you through how to generate synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

What are AI Security Vulnerabilities?
------------------------------------

Security vulnerabilities in LLMs are critical issues that can lead to malicious attacks, data breaches, and system compromises.

.. tip::

   Security vulnerabilities are different from business failures. While business issues focus on accuracy and reliability, security vulnerabilities focus on malicious exploitation and system integrity.
   If you want to detect business failures, check out the :doc:`/hub/sdk/datasets/business`.

Adversarial Tests Generation
----------------------------

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub.datasets`` client to control the Giskard Hub!

To generate a dataset, we can use the ``hub.datasets.generate()`` method.

Define Adversarial Issue Categories
___________________________________

First, we need to define adversarial issue categories.
We can do this by creating a list of dictionaries, where each dictionary contains the name and description of the category.
Keep in mind that the categories are used to generate adversarial queries, so they need to be explicit and detailed.
To get a full overview of the types of security vulnerabilities that can be detected, check out the :doc:`/hub/ui/datasets/security` guide.
Underneath, we have a list of categories that we can use to generate a dataset.

.. code-block:: python

   categories = [
      {
         "name": "Harmful Content",
         "desc": "Harmful content is content that is harmful to the user or the model.",
      },
      {
         "name": "Stereotypes & Discrimination",
         "desc": "Stereotypes & Discrimination is content that is harmful to the user or the model.",
      },
      {
         "name": "Misinformation",
         "desc": "Misinformation is content that is false or misleading.",
      }
   ]

Generate a Synthetic Test Dataset
_________________________________

We can get the model ID by listing all models using the ``hub.models.list("<PROJECT_ID>")`` method or retrieve the model ID from the Hub UI.

.. code-block:: python

   dataset_name = "Adversarial Dataset"
   dataset = hub.datasets.generate(
      model_id="<MODEL_ID>",
      dataset_name=dataset_name,
      categories=categories,
      description="<MODEL_DESCRIPTION>",
      nb_examples=10,
   )

This will return a :class:`~giskard_hub.data.Dataset` object, but this object might not be fully populated yet, as the dataset is generated asynchronously.
To get an up-to-date version of the dataset and the generation, we recommend visiting the Hub UI and checking the dataset page.