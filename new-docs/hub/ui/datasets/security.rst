=============================================================
Detect Security Vulnerabilities by Generating Synthetic Tests
=============================================================

Since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don’t have any test conversations to import. One of the key challenges of synthetic test data generation is ensuring that the test cases are domain-specific rather than too generic.

In this section, we will walk you through how to generate synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

What are AI security failures?
------------------------------

Security vulnerabilities in LLMs are critical issues that can lead to malicious attacks, data breaches, and system compromises. Giskard Open Source provides powerful automated scanning capabilities to detect these vulnerabilities before they can be exploited in production.

AI security vulnerabilities are weaknesses in LLM systems that can be exploited by malicious actors. Common types include:

* **Prompt Injection** - Manipulating the model to ignore safety instructions or generate harmful content
* **Harmful Content Generation** - Production of violent, illegal, or inappropriate material
* **Personal Information Disclosure** - Leaking sensitive data or private information
* **Stereotypes & Discrimination** - Biased responses that perpetuate harmful stereotypes
* **Information Disclosure** - Revealing internal system details or training data
* **Robustness Issues** - Vulnerability to adversarial inputs or edge cases
* **Output Formatting Vulnerabilities** - Manipulation of response structure for malicious purposes

.. note::

   Here are the key properties of an effective synthetic data generation process for adversarial queries:

   - **Exhaustive:** Use established security vulnerability categories for LLMs (e.g., `OWASP Top 10 <https://owasp.org/www-project-top-10-for-large-language-model-applications/>`_) to cover the most well-known issues.
   - **Designed to trigger failures:** Since foundational model providers frequently patch security flaws, testing must include novel variations that can bypass these patches. For example, for most prompt injection techniques (e.g., DAN), generating variants increases the likelihood of failures.
   - **Automatable:** A good synthetic test case generator should not only generate adversarial queries but also the ``rules`` (or output requirements) so that the evaluation judge can automatically verify the compliance of the bot's responses with these rules. This is essential for the LLM-as-a-judge setup.
   - **Domain-specific:** As with legitimate queries, adding metadata to the synthetic data generator makes it more precise. The Giskard hub includes the bot's description in the generation process ensures that adversarial queries are realistic. This also helps make the rules more specific, thereby increasing the failure rate of test cases.

.. tip::

   Security vulnerabilities are different from business failures. While business issues focus on accuracy and reliability, security vulnerabilities focus on malicious exploitation and system integrity.
   If you want to detect business failures, check out the :doc:`/hub/ui/datasets/business`.

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
