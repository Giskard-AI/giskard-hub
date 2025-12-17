:og:title: Giskard Hub SDK - Security Test Generation
:og:description: Generate and manage security-focused test cases programmatically. Test for vulnerabilities, prompt injection attacks, and security failures using the comprehensive Python SDK.

=============================================================
Generate security tests
=============================================================

This section will guide you through generating security-focused test cases using the Hub interface.

Security testing is a critical component of LLM agent evaluation. It focuses on identifying vulnerabilities that could be exploited by malicious actors or lead to unintended behavior.

Adversarial Security Testing
----------------------------

The ``generate_adversarial`` method creates test cases designed to expose security vulnerabilities and robustness issues in your AI agents. This is particularly useful for:

.. code-block:: python

    # Generate adversarial test cases for security testing
    security_dataset = hub.datasets.generate_adversarial(
        model_id=model.id,
        dataset_name="Security Test Cases",
        description="Adversarial test cases for security vulnerability detection",
        categories=[
            {
                "id": "prompt_injection",
                "name": "Prompt Injection",
                "desc": "Tests for prompt injection vulnerabilities"
            },
            {
                "id": "harmful_content",
                "name": "Harmful Content",
                "desc": "Tests for harmful content generation"
            },
            {
                "id": "information_disclosure",
                "name": "Information Disclosure",
                "desc": "Tests for unintended information leakage"
            }
        ],
        n_examples=20 # Optional: number of chat test cases per category to generate
    )

    # Wait for the dataset to be created
    security_dataset.wait_for_completion()

    # List the chat test cases in the dataset
    for chat_test_case in security_dataset.chat_test_cases:
        print(chat_test_case.messages[0].content)

.. tip::

   You can also use the `Giskard Hub UI </hub/ui/scan/index>`_ to generate security test cases if you prefer a visual interface.

Next steps
----------

* **Agentic vulnerability detection** - Try :doc:`/hub/sdk/scan/index`
* **Generate knowledge base tests** - Try :doc:`/hub/sdk/datasets/knowledge_base`
* **Review test case** - Make sure to :doc:`/hub/ui/annotate/index`