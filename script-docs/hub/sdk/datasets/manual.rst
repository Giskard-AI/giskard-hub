:og:title: Giskard Hub SDK - Manual Test Case Creation
:og:description: Create manual test cases programmatically using the Python SDK. Build custom datasets with precise control over test scenarios and evaluation criteria.

Create manual tests
===================

This section will guide you through creating your own test datasets programmatically.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub.datasets`` and ``hub.chat_test_cases`` clients to control the Giskard Hub!

Create a dataset
________________

You can create a dataset manually using the ``hub.datasets.create()`` method. Example:

.. code-block:: python

    dataset = hub.datasets.create(
        # The ID of the project where the dataset will be created
        project_id="<PROJECT_ID>",
        name="Production Data",
        description="This dataset contains chats that " \
        "are automatically sampled from the production environment.",
    )

    print(dataset.id)
    # "666030a0d41f357fd061374c"

For detailed information about creating datasets, see the :doc:`/hub/sdk/reference/resources/index` section.

Create a chat test case
_______________________

After creating the dataset, you can add chat test cases to it using the ``hub.chat_test_cases.create()`` method. Example:

**A chat test case (conversation)** is a collection of messages together with evaluation checks (e.g., the expected answer, or rules that the agent must follow when responding).


The parameters for creating a chat test case are:

- **dataset_id** (required): The ID of the dataset where the chat test case will be created.
- **messages** (required): A list of messages, without the last assistant answer.  Each message is a dictionary with keys ``role`` and ``content``.
- **demo_output** (optional): A dictionary with the last assistant answer
- **tags** (optional): A list of tags you can use to categorize and organize the chat test cases
- **checks** (optional): A list of checks. For more information on checks, see the :doc:`/hub/sdk/annotate/index` section.

.. tip:: **Do not include last assistant answer in the list of messages.** In fact, during evaluation, we will pass
    the chat test case to your agent and expect it to generate an assistant answer. The newly generated answer will
    be evaluated against the checks.

    If you want to show the last assistant answer to the user, you can include it in the chat test case as ``demo_output``.
    In this way, it will be shown in the dataset, but not used in the evaluation.

.. code-block:: python

    hub.chat_test_cases.create(
        dataset_id=dataset.id,

        # A list of messages, without the last assistant answer
        messages=[
            {"role": "user", "content": "Hi, I have problems the laptop I bought from you."},
            {"role": "assistant", "content": "I'm sorry to hear that. What seems to be the problem?"},
            {"role": "user", "content": "The battery is not charging."},
        ],

        # We can place a recorded answer as `demo_output` (optional)
        demo_output={
            "role": "assistant",
            "content": "I see. Have you tried to restart the laptop?",
            "metadata": {"category": "laptop", "subcategory": "battery", "resolved": False},
        },

        # Tags (optional)
        tags=["customer-support"],

        # Evaluation checks (optional)
        checks=[
            {"identifier": "correctness", "params": {"reference": "I see, could you please give me the model number of the laptop?"}},
            {"identifier": "conformity", "params": {"rules": ["The assistant should employ a polite and friendly tone."]}},
            {"identifier": "metadata", "params": {"json_path_rules": [{"json_path": "$.category", "expected_value": "laptop", "expected_value_type": "string"}, {"json_path": "$.subcategory", "expected_value": "battery", "expected_value_type": "string"}, {"json_path": "$.resolved", "expected_value": False, "expected_value_type": "boolean"}]}},
            {"identifier": "semantic_similarity", "params": {"reference": "I see, could you please give me the model number of the laptop?", "threshold": 0.8}},
        ]
    )

For detailed information about creating manual datasets, see the :doc:`/hub/sdk/reference/resources/index` section.

Next steps
__________

* **Agentic vulnerability detection** - Try :doc:`/hub/sdk/scan/index`
* **Generate test cases** - Try :doc:`/hub/sdk/datasets/business` or :doc:`/hub/sdk/datasets/security`
* **Review test case and assign checks** - Make sure to :doc:`/hub/ui/annotate/index`
