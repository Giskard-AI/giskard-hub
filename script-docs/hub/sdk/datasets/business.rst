:og:title: Giskard Hub - Enterprise Agent Testing - Detect Business Failures
:og:description: Generate and manage business logic test cases programmatically. Test compliance, domain-specific scenarios, and business requirements in your LLM agents.

======================================================
Detect business failures by generating synthetic tests
======================================================

Generative AI agents can face an endless variety of real-world scenarios, making it impossible to manually enumerate all possible scenarios. Automated, synthetic test case generation is therefore essential—especially when you lack real user chats to import as tests. However, a major challenge is to ensure that these synthetic cases are tailored to your business context, rather than being overly generic.

By generating domain-specific synthetic tests, you can proactively identify and address these types of failures before they impact your users or business operations.

Document-Based Testing
----------------------

The ``generate_document_based`` method creates test cases from your knowledge base, making it ideal for testing business logic and accuracy.

Before generating test cases, you need to `create a knowledge base </hub/sdk/projects>`_.

.. code-block:: python

    # Generate document-based test cases for business testing
    business_dataset = hub.datasets.generate_document_based(
        model_id=model.id,
        knowledge_base_id=knowledge_base.id,
        dataset_name="Business Logic Tests",
        description="Test cases based on company knowledge base",
        n_questions=15, # total number of questions to generate
        topic_ids=["topic-uuid-1", "topic-uuid-2"]  # Optional: filter by specific topics
    )

    # Wait for the dataset to be created
    business_dataset.wait_for_completion()

    # List the chat test cases in the dataset
    for chat_test_case in business_dataset.chat_test_cases:
        print(chat_test_case.messages[0].content)

.. note::

   You can also use the `Giskard Hub UI </hub/ui/datasets/business>`_ to generate business test cases if you prefer a visual interface.

Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Generate security vulnerabilities** - Try :doc:`/hub/sdk/datasets/security`
* **Set-up continuous red teaming** - Understand exhaustive and proactive detection with :doc:`/hub/ui/continuous-red-teaming`