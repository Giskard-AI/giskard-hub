=============================================================
Detect Security Vulnerabilities by Generating Synthetic Tests
=============================================================

Since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don’t have any test conversations to import. One of the key challenges of synthetic test data generation is ensuring that the test cases are domain-specific rather than too generic.

In this section, we will walk you through how to generate synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

What are AI Security Vulnerabilities?
------------------------------------

Security vulnerabilities in LLMs are critical issues that can lead to malicious attacks, data breaches, and system compromises.

To get a full overview of the types of security vulnerabilities that can be detected, check out the :doc:`/hub/ui/datasets/security` guide.

.. tip::

   Security vulnerabilities are different from business failures. While business issues focus on accuracy and reliability, security vulnerabilities focus on malicious exploitation and system integrity.
   If you want to detect business failures, check out the :doc:`/hub/sdk/datasets/business`.

Adversarial tests generation
----------------------------

To begin, navigate to the Datasets page and click **Automatic Generation** in the upper-right corner of the screen. This will open a modal with two options: Adversarial or Document-Based. Select the Adversarial option.

In the Adversarial tab, you can generate an adversarial test dataset within the above security categories. Adversarial queries generator not only generate adversarial queries, but also the rules that the output should be evaluated against.

.. image:: /_static/images/hub/generate-dataset-adversarial.png
   :align: center
   :alt: "Generate adversarial dataset"
   :width: 800

- ``Dataset name``: Provide a name for the dataset.

- ``Agent``: Select the agent you want to use for evaluating this dataset.

- ``Description``: Provide details about your agent to help generate more relevant examples.

- ``Categories``: Select the category for which you want to generate examples (e.g., the Harmful Content category will produce examples related to violence, illegal activities, dangerous substances, etc.).

- ``Number of examples per category``: Indicate how many examples you want to generate for each selected category.
