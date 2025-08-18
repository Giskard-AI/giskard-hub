====================
Custom checks
====================

In this section, we will show how to create custom checks programmatically using the SDK. Custom checks allow you to define reusable evaluation logic that can be applied to conversations and models across your project.

Let's start by initializing the Hub client.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

.. note:: 
    
    If you didn't set up the environment variables, you will need to provide the API key and the Hub URL explicitly:

    .. code-block:: python

        hub = HubClient(api_key=..., hub_url=...)


What are custom checks?
-----------------------

Custom checks are reusable evaluation criteria that you can define for your project. Built on top of built-in checks (like ``correctness``, ``conformity``, etc.), custom checks allow you to store and reuse your own evaluation logic.

Once created, custom checks can be:

- Applied to conversations in your datasets
- Used during model evaluations
- Shared across your team within the same project
- Modified or updated as your requirements evolve


Create a custom check
---------------------

You can create a custom check using the ``hub.checks.create()`` method. Here's a basic example:

.. code-block:: python

    # Create a custom conformity check
    custom_check = hub.checks.create(
        project_id="your_project_id",
        identifier="answer_english",
        name="Answer in English",
        description="Validates if the model output is in English",
        params={
            "type": "conformity",
            "rules": ["The answer should be in English"]
        }
    )

The parameters for creating a custom check are:

- **project_id** (required): The ID of the project where the check will be created
- **identifier** (required): A unique identifier for your check (e.g., "answer_english")
- **name** (required): A human-readable name for your check
- **params** (required): A dictionary containing the parameters for your check logic. The parameters should include the ``type`` of the check and the specific parameters for that check type.
    - For the ``correctness`` check, the parameter is ``reference`` (type: ``str``), which is the expected output.
    - For the ``conformity`` check, the parameter is ``rules`` (type: ``list[str]``), which is a list of rules that the model should follow in its response.
    - For the ``groundedness`` check, the parameter is ``context`` (type: ``str``), which is the context in which the model should ground its output.
    - For the ``string_match`` check, the parameter is ``keyword`` (type: ``str``), which is the string that the model's output should contain.
    - For the ``metadata`` check, the parameter is ``json_path_rules`` (type: ``list[dict]``), which is a list of dictionaries with the following keys:
        - ``json_path``: The JSON path to the value that the model's output should contain.
        - ``expected_value``: The expected value at the JSON path.
        - ``expected_value_type``: The expected type of the value at the JSON path, one of ``string``, ``number``, ``boolean``.
- **description** (optional): A description explaining what your check does

.. tip::

    Choose descriptive identifiers for your checks. This makes them easier to find and use later. For example, use ``"financial_accuracy_check"`` instead of ``"check1"``.

.. tip::

    Custom checks are project-specific. If you need the same check logic across multiple projects, you'll need to create it separately in each project. 


Examples of custom checks
-------------------------

Here are some practical examples of custom checks you might create:

**1. Domain-specific correctness check**

.. code-block:: python

    # For a financial chatbot
    financial_check = hub.checks.create(
        project_id=project.id,
        identifier="financial_accuracy",
        name="Financial Accuracy Check",
        description="Ensures financial calculations and advice are accurate",
        params={
            "type": "groundedness", # The type of the check
            "context": "The compound interest formula is A = P(1 + r/n)^(nt)" # The context in which the model should ground its output
        }
    )

**2. Tone and style check**

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

**3. Content safety check**

.. code-block:: python

    # For content moderation
    safety_check = hub.checks.create(
        project_id=project.id,
        identifier="content_safety",
        name="Content Safety Check",
        description="Ensures the bot refuses to answer questions that are not related to the domain",
        params={
            "type": "correctness",
            "reference": "I'm sorry, I can't answer that question"
        }
    )


Using custom checks in conversations
------------------------------------

Once you've created a custom check, you can use it in your conversations by referencing its identifier:

.. code-block:: python

    # Add a conversation that uses your custom check
    hub.conversations.create(
        dataset_id=dataset.id,
        messages=[
            {"role": "user", "content": "What's the formula for compound interest?"},
        ],
        checks=[
            # Use your custom check
            {"identifier": "financial_accuracy", "enabled": True},
            # You can also combine with built-in checks
            {"identifier": "conformity", "enabled": True, "params": {"rules": ["Be clear and educational"]}}
        ]
    )


Managing custom checks
----------------------

**List all checks in a project**

.. code-block:: python

    # Get all custom checks for a project
    checks = hub.checks.list(project_id=project.id)
    
    for check in checks:
        print(f"Check: {check.name} (ID: {check.id})")
        print(f"Identifier: {check.identifier}")
        print(f"Description: {check.description}")
        print("---")

**Retrieve a specific check**

.. code-block:: python

    # Get a specific check by ID
    check = hub.checks.retrieve(check_id="your_check_id")
    print(f"Check name: {check.name}")
    print(f"Parameters: {check.params}")

**Update a custom check**

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

**Delete a custom check**

.. code-block:: python

    # Delete a check (this will remove it permanently)
    hub.checks.delete(check_id="your_check_id")
    
    # Or delete multiple checks at once
    hub.checks.delete(check_id=["check_id_1", "check_id_2"])

.. warning::

    Deleting a check is permanent and cannot be undone. Make sure you're not using the check in any active conversations or evaluations before deleting it.
