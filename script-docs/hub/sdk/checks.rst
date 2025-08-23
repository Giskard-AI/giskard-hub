:og:description: Custom Checks (SDK) - Build and deploy validation rules, metrics, and testing logic programmatically. Create specialized testing logic for your specific use cases using the Giskard Hub Python SDK.

====================
Manage Checks
====================

In this section, we will show how to define checks programmatically using the SDK.

- A **check** is a reusable evaluation criteria or metric that you can define for your project.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to create, update, and delete checks.

Built-in checks
---------------

Giskard provides a set of built-in checks that you can use to evaluate your agents. These checks form the foundation of :ref:`custom-checks` but they can also be used independently as shown in :ref:`add-checks-to-conversations`.

.. tip::

    For more background information on the built-in checks, see the :doc:`/hub/ui/annotate` section.

.. _custom-checks:

Custom checks
-------------

Custom checks are reusable evaluation criteria that you can define for your project. Built on top of built-in checks (like ``correctness``, ``conformity``, etc.), custom checks allow you to store and reuse your own evaluation logic.

Custom checks can be used in the following ways:

- Applied to conversations in your datasets
- Used during agent evaluations
- Shared across your team **within the same project**
- Modified or updated as your requirements evolve

Create a check
______________

You can create a check using the ``hub.checks.create()`` method. Here's a basic example:

.. code-block:: python

    # Create a custom conformity check
    custom_check = hub.checks.create(
        project_id="your_project_id",
        identifier="answer_english",
        name="Answer in English",
        description="Validates if the agent output is in English",
        params={
            "type": "conformity",
            "rules": ["The answer should be in English"]
        }
    )

The parameters for creating a custom check are:

- **project_id** (required): The ID of the project where the check will be created
- **identifier** (required): A unique identifier for your check (e.g., "answer_english")
- **name** (required): A human-readable name for your check
- **description** (optional): A description explaining what your check does
- **params** (required): A dictionary containing the parameters for your check logic which depends on the check type as described below.

.. tabs::

    .. tab:: Correctness Check

        **Parameter**: ``reference`` (type: ``str``)

        The expected output that the agent's response should match. The correctness check validates whether all information from the reference answer is present in the agent answer without contradiction.

        .. code-block:: python

            params={
                "type": "correctness",
                "reference": "Paris is the capital of France, founded around 200 BC."
            }

    .. tab:: Conformity Check

        **Parameter**: ``rules`` (type: ``list[str]``)

        A list of rules that the agent should follow in its response. Each rule should check a unique and unambiguous behavior.

        .. code-block:: python

            params={
                "type": "conformity",
                "rules": [
                    "The agent should only answer in English",
                    "The agent should maintain a professional tone"
                ]
            }

    .. tab:: Groundedness Check

        **Parameter**: ``context`` (type: ``str``)

        The context in which the agent should ground its output. This check validates that all information in the agent's response is present in the given context without contradiction.

        .. code-block:: python

            params={
                "type": "groundedness",
                "context": (
                    "Sir Edmund Hillary, a New Zealand mountaineer, "
                    "became famous for being one of the first people "
                    "to reach the summit of Mount Everest with Tenzing Norgay "
                    "on May 29, 1953."
                )
            }

    .. tab:: String Match Check

        **Parameter**: ``keyword`` (type: ``str``)

        The string that the agent's output should contain. This check validates that the specified keyword appears in the agent's response.

        .. code-block:: python

            params={
                "type": "string_match",
                "keyword": "Hello"
            }

    .. tab:: Metadata Check

        **Parameter**: ``json_path_rules`` (type: ``list[dict]``)

        A list of dictionaries with the following keys:

        - ``json_path``: The JSON path to the value that the agent's output should contain
        - ``expected_value``: The expected value at the JSON path
        - ``expected_value_type``: The expected type of the value (``string``, ``number``, or ``boolean``)

        .. code-block:: python

            params={
                "type": "metadata",
                "json_path_rules": [
                    {
                        "json_path": "$.user.name",
                        "expected_value": "John",
                        "expected_value_type": "string"
                    },
                    {
                        "json_path": "$.output.success",
                        "expected_value": True,
                        "expected_value_type": "boolean"
                    }
                ]
            }

.. tip::

    - Choose descriptive identifiers for your checks. This makes them easier to find and use later. For example, use ``"financial_accuracy_check"`` instead of ``"check1"``.
    - Custom checks are project-specific. If you need the same check logic across multiple projects, you'll need to create it separately in each project.


Retrieve a check
________________

You can retrieve a check using the ``hub.checks.retrieve()`` method. Here's a basic example:

.. code-block:: python

    # Get a specific check by ID
    check = hub.checks.retrieve(check_id="your_check_id")
    print(f"Check name: {check.name}")
    print(f"Parameters: {check.params}")

Update a check
______________

You can update a check using the ``hub.checks.update()`` method. Here's a basic example:

.. code-block:: python

    # Update an existing check
    updated_check = hub.checks.update(
        check_id="your_check_id",
        identifier="updated_check",
        name="Updated Check Name",
        description="Updated description",
        params={
            "type": "correctness",
            "reference": "Updated reference answer"
        }
    )

    # Partial update
    hub.checks.update(
        check_id="your_check_id",
        params={
            "type": "conformity",
            "rules": ["Be clear and educational"]
        }
    )

Delete a check
______________

You can delete a check using the ``hub.checks.delete()`` method. Here's a basic example:

.. code-block:: python

    # Delete a check (this will remove it permanently)
    hub.checks.delete(check_id="your_check_id")

    # Or delete multiple checks at once
    hub.checks.delete(check_id=["check_id_1", "check_id_2"])

.. warning::

    Deleting a check is permanent and cannot be undone. Make sure you're not using the check in any active conversations or evaluations before deleting it.

List checks
___________

You can list all checks for a project using the ``hub.checks.list()`` method. Here's a basic example:

.. code-block:: python

    # Get all custom checks for a project
    checks = hub.checks.list(project_id=project.id)

    for check in checks:
        print(f"Check: {check.name} (ID: {check.id})")
        print(f"Identifier: {check.identifier}")
        print(f"Description: {check.description}")
        print("---")

.. _add-checks-to-conversations:

Add checks to conversations
---------------------------

Once you've created a check, you can use it in your conversations by referencing its identifier:

.. code-block:: python

    # Add a conversation that uses your check
    hub.conversations.create(
        dataset_id=dataset.id,
        messages=[
            {"role": "user", "content": "What's the formula for compound interest?"},
        ],
        checks=[
            # Use your check
            {"identifier": "financial_accuracy", "enabled": True},
            # You can also combine them with built-in checks
            {
                "identifier": "conformity",
                "enabled": True,
                "params": {"rules": ["Be clear and educational"]}
            }
        ]
    )

Examples of checks
------------------

Here are some practical examples of custom checks you might create:

Domain-specific correctness
___________________________

Sometimes, you might want to ensure that the agent's output is grounded in a specific context. For example, if you're building a financial agent, you might want to ensure that the agent's output is grounded in the financial context.

.. code-block:: python

    # For a financial agent
    financial_check = hub.checks.create(
        project_id=project.id,
        identifier="financial_accuracy",
        name="Financial Accuracy Check",
        description="Ensures financial calculations and advice are accurate",
        params={
            # The type of the check
            "type": "groundedness",
            # The context in which the agent should ground its output
            "context": "The compound interest formula is A = P(1 + r/n)^(nt)"
        }
    )

Tone and style checks
_____________________

We can use a conformity check to ensure that the agent maintains a professional and helpful tone.

.. code-block:: python

    # For customer service scenarios
    tone_check = hub.checks.create(
        project_id=project.id,
        identifier="professional_tone",
        name="Professional Tone Check",
        description="Validates that responses maintain a professional and helpful tone",
        params={
            "type": "conformity",
            "rules": [
                "Response should be polite and professional",
                "Avoid casual language or slang"
            ]
        }
    )

Content safety checks
_____________________

A major use case for checks is to ensure that the agent does not answer questions that are not related to the domain.

.. code-block:: python

    # For content moderation
    safety_check = hub.checks.create(
        project_id=project.id,
        identifier="content_safety",
        name="Content Safety Check",
        description="Ensures the agent refuses to answer questions that are not related to the domain",
        params={
            "type": "correctness",
            "reference": "I'm sorry, I can't answer that question"
        }
    )

Verify tool calls
_________________

You can use a metadata check to verify that the agent calls the correct tool or calls any tool at all. For example, to ensure your agent always uses the latest information, you can use a metadata check to verify that the agent calls the correct tool.

.. code-block:: python

    # For tool calling
    tool_check = hub.checks.create(
        project_id=project.id,
        identifier="tool_calling",
        name="Tool Calling Check",
        description="Ensures the agent calls the correct tool",
        params={
            "type": "metadata",
            "json_path_rules": [
                {"json_path": "$.tool", "expected_value": "calculator", "expected_value_type": "string"}
            ]
        }
    )