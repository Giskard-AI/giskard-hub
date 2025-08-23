:og:description: Giskard Hub Datasets (UI) - Create, manage, and organize test datasets for LLM evaluations. Import conversations, generate synthetic data, and build comprehensive test cases for your AI agents.

===============================================
Create Test Datasets
===============================================

A **dataset** is a collection of conversations used to evaluate your agents. We allow for manual test creation for fine-grained control,
but since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don’t have any test conversations to import.

This section will guide you through creating your own test datasets. In general, we cover five different ways to create datasets:

.. grid:: 1 1 2 2

   .. grid-item-card:: Manual Test Creation for Fine-Grained Control
      :link: manual
      :link-type: doc

      Design your own test cases using a full control over the test case creation process and explore them in the playground.

   .. grid-item-card:: Import Existing Datasets
      :link: import
      :link-type: doc

      Import existing test datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.

   .. grid-item-card:: Detect Security Vulnerabilities by Generating Synthetic Tests
      :link: security
      :link-type: doc

      Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

   .. grid-item-card:: Detect Business Failures by Generating Synthetic Tests
      :link: business
      :link-type: doc

      Detect business failures, by generating synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.



.. toctree::
   :maxdepth: 2
   :hidden:

   manual
   import
   security
   business
