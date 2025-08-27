:og:title: Giskard Hub - Enterprise Agent Testing - Dataset Management
:og:description: Create, manage, and organize test datasets for LLM agent evaluations. Import conversations, generate synthetic data, and build comprehensive test cases.

===============================================
Create test datasets
===============================================

A **dataset** is a collection of conversations used to evaluate your agents. We allow manual test creation for fine-grained control,
but since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don't have any test conversations to import.

This section will guide you through creating your own test datasets. In general, we cover five different ways to create datasets:

.. grid:: 1 1 2 2

   .. grid-item-card:: Manual test creation for fine-grained control
      :link: manual
      :link-type: doc

      Design your own test cases using a full control over the test case creation process and explore them in the playground.

   .. grid-item-card:: Import existing datasets
      :link: import
      :link-type: doc

      Import existing test datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.

   .. grid-item-card:: Detect security vulnerabilities by generating synthetic tests
      :link: security
      :link-type: doc

      Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

   .. grid-item-card:: Detect business failures by generating synthetic tests
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
