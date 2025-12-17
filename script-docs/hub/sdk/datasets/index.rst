:og:title: Giskard Hub SDK - Dataset and Test Case Management
:og:description: Create, manage, and organize test datasets programmatically. Import chat test cases, generate synthetic data, and build comprehensive test datasets using the Python SDK.

===================================
Create test cases and datasets
===================================

This section will guide you through creating your own test datasets programmatically.

A **dataset** is a collection of chat test cases (conversations) used to evaluate your agents. We allow manual test creation for fine-grained control,
but since generative AI agents can encounter an infinite number of scenarios, automated test case generation is often necessary, especially when you don't have any chat transcripts to import.

.. grid:: 1 1 2 2

    .. grid-item-card:: Create manual tests
        :link: manual
        :link-type: doc

        Create manual test cases using the ``hub.datasets.create()`` and ``hub.chat_test_cases.create()`` methods.

    .. grid-item-card:: Generate security tests
        :link: security
        :link-type: doc

        Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

    .. grid-item-card:: Generate knowledge base tests
        :link: knowledge_base
        :link-type: doc

        Detect business failures, by generating synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

    .. grid-item-card:: Import tests
        :link: import
        :link-type: doc

        Import existing test datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.

.. tip::
   
   For advanced automated discovery of weaknesses such as prompt injection or hallucinations, check out our :doc:`Vulnerability Scanner </hub/sdk/scan/index>`, which uses automated agents to generate tests for common security and robustness issues.

High-level workflow
-------------------

.. include:: ../../ui/datasets/graph.rst.inc

.. toctree::
   :hidden:
   :maxdepth: 1

   manual
   security
   knowledge_base
   import