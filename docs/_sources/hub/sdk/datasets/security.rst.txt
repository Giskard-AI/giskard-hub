:og:title: Giskard Hub - Enterprise Agent Testing - Security Testing
:og:description: Generate and manage security-focused test cases programmatically. Test for vulnerabilities, prompt injection attacks, and security failures using the Python SDK.

============================================================
Detect security vulnerabilities by generating synthetic tests
============================================================

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

.. note::

   You can also use the `Giskard Hub UI </hub/ui/datasets/security>`_ to generate security test cases if you prefer a visual interface.

Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Generate business failures** - Try :doc:`/hub/sdk/datasets/business`
* **Set-up continuous red teaming** - Understand exhaustive and proactive detection with :doc:`/hub/ui/continuous-red-teaming`