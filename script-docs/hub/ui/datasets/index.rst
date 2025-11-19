:og:title: Giskard Hub UI - Dataset Management and Test Creation
:og:description: Create, manage, and organize test datasets for LLM agent evaluations. Import conversations, generate synthetic data, and build comprehensive test cases with intuitive visual tools.

===============================================
Create test cases and datasets
===============================================

A **dataset** is a collection of conversations used to evaluate your agents. We allow manual test creation for fine-grained control,
but since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don't have any test conversations to import.

In this section, we will walk you through how to create test cases and datasets using the Hub interface. In general, we cover five different ways to create datasets:

.. grid:: 1 1 2 2

   .. grid-item-card:: Create manual tests
      :link: manual
      :link-type: doc

      Design your own test cases using a full control over the test case creation process and explore them in the playground.

   .. grid-item-card:: Import tests
      :link: import
      :link-type: doc

      Import existing test datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.

   .. grid-item-card:: Generate security tests
      :link: security
      :link-type: doc

      Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

   .. grid-item-card:: Generate business tests
      :link-type: doc
      :link: business


      Detect business failures, by generating synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

High-level workflow
-------------------

.. mermaid::
   :align: center

   graph LR
       A[Create Dataset] --> B{Source}
       B -->|Manual| C[Create Manually]
       B -->|Import| D[Import Existing]
       B -->|Generate| E[Generate Tests]
       B -->|Scan Results| F[From Scan]
       C --> G[Test Cases]
       D --> G
       E --> G
       F --> G
       G --> H[Iterate on Test Cases]

.. tip::
   
   For advanced automated discovery of weaknesses such as prompt injection or hallucinations, check out our :doc:`Vulnerability Scanner </hub/ui/scan/index>`, which uses automated agents to generate tests for common security and robustness issues.

.. toctree::
   :maxdepth: 2
   :hidden:

   manual
   import
   security
   business
