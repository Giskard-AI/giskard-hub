:og:title: Giskard Hub - Enterprise Agent Testing - Detect Security Vulnerabilities
:og:description: Generate and manage security test cases programmatically. Test for vulnerabilities, prompt injection, and data leakage in your LLM agents.

=============================================================
Detect Security Vulnerabilities by Generating Synthetic Tests
=============================================================

Generative AI agents are vulnerable to a wide range of security threats, many of which are difficult to anticipate in advance. Automated generation of adversarial test cases is essential for uncovering vulnerabilities—especially when you lack real-world attack data or malicious conversations to import. The main challenge is to create synthetic security tests that realistically simulate potential attacks and are tailored to the specific risks relevant to your domain, rather than relying on overly generic prompts.

In this section, we will walk you through how to generate synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

What are AI Security Vulnerabilities?
-------------------------------------

Security vulnerabilities in LLMs are critical because they can be exploited for malicious attacks, data breaches, and system compromises.
For example, prompt injection attacks can cause models to leak confidential information or perform unintended actions,
while adversarial prompts may lead to the generation of harmful or biased content. These vulnerabilities have resulted in real-world incidents,
such as agents revealing sensitive data or being manipulated to bypass safety filters.
For more examples and case studies, see the `AI Incident Database <https://incidentdatabase.ai/>`_ and `Realharm <https://realharm.giskard.ai/>`_.

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

We can get the agent ID by listing all agents using the ``hub.agents.list("<PROJECT_ID>")`` method or retrieve the agent ID from the Hub UI.

.. code-block:: python

   dataset_name = "Adversarial Dataset"
   dataset = hub.datasets.generate(
      model_id="<AGENT_ID>",  # Note: parameter is still named 'model_id' for backward compatibility
      dataset_name=dataset_name,
      categories=categories,
      description="<MODEL_DESCRIPTION>",
      nb_examples=10,
   )

This will return a :class:`~giskard_hub.data.Dataset` object, but this object might not be fully populated yet, as the dataset is generated asynchronously.
To get an up-to-date version of the dataset and the generation, we recommend visiting the Hub UI and checking the dataset page.

Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Generate business failures** - Try :doc:`/hub/sdk/datasets/business`
* **Set-up continuous red teaming** - Understand exhaustive and proactive detection with :doc:`/hub/ui/continuous-red-teaming`