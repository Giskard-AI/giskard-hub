======================================================
Detect Business Failures by Generating Synthetic Tests
======================================================

Since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don’t have any test conversations to import. One of the key challenges of synthetic test data generation is ensuring that the test cases are domain-specific rather than too generic.

In this section, we will walk you through how to generate synthetic test cases to detect business failures, like *hallucinations* or *deanial to answer questions*, using document-based queries and knowledge bases.

What are AI business failures?
------------------------------

AI business failures are failures that are related to the business of the AI system. To detect them, we need to generate tests that are designed to trigger failures.

The Giskard Hub provides an interface for the synthetic generation of legitimate queries **with expected outputs**. It automatically clusters the documents from the internal knowledge base into key topics and generates test cases for each topic by applying a set of perturbations.
These clusters and topics are then used to generate dedicated test that challenge the bot to answer questions about the specific topic in a way that might not align with the business rules of your organization.

.. tip::

   Business failures are different from security failures. While security failures focus on malicious exploitation and system integrity, business failures focus on the model's ability to provide accurate, reliable, and appropriate responses in normal usage scenarios.
   If you want to detect security failures, check out the :doc:`/hub/sdk/datasets/security`.

Document-based tests generation
-------------------------------

To begin, navigate to the Datasets page and click **Automatic Generation** in the upper-right corner of the screen. This will open a modal with two options: Adversarial or Document-Based. Select the Document-Based option.

The Document Based tab allows you to generate a dataset with examples based on your knowledge base.

.. image:: /_static/images/hub/generate-dataset-document-based.png
   :align: center
   :alt: "Generate document based dataset"
   :width: 800

In this case, dataset generation requires two additional pieces of information:

- ``Knowledge Base``: Choose the knowledge base you want to use as a reference.
- ``Topics``: Select the topics within the chosen knowledge base from which you want to generate examples.

Once you click on "Generate," you receive a dataset where:

- The groundedness check is enabled: the context consists of the knowledge documents relevant to answering the query.
- The correctness check is disabled, but its reference (expected output) is prefilled by the Hub. If you want to execute the dataset with the correctness check, you can either enable it manually or enable it for multiple conversations at once by selecting multiple conversations in the Dataset tab and enabling the correctness check.








