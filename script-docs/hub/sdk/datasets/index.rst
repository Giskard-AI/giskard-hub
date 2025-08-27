:og:title: Giskard Hub - Enterprise Agent Testing - Dataset Management
:og:description: Create, manage, and organize test datasets programmatically. Import conversations, generate synthetic data, and build comprehensive test cases using the Python SDK.

================================
Create test datasets
================================

A **dataset** is a collection of conversations used to evaluate your agents. We allow manual test creation for fine-grained control,
but since generative AI agents can encounter an infinite number of test cases, automated test case generation is often necessary, especially when you don't have any test conversations to import.

This section will guide you through creating your own test datasets programmatically.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub.datasets`` client to control the Giskard Hub!

Datasets
--------

A dataset is a collection of conversations that are used to evaluate your agents.

Create a dataset
________________

Manual creation
~~~~~~~~~~~~~~~

If you don't have a dataset already, you can create one manually.

.. code-block:: python

    dataset = hub.datasets.create(
        # The ID of the project where the dataset will be created
        project_id="<PROJECT_ID>",
        name="Production Data",
        description="This dataset contains conversations that " \
        "are automatically sampled from the production environment.",
    )

    print(dataset.id)
    # "666030a0d41f357fd061374c"

Automated generation
~~~~~~~~~~~~~~~~~~~~

Alternatively, you can generate a dataset automatically using the following methods:

.. grid:: 1 1 2 2

    .. grid-item-card:: Detect Security Vulnerabilities by Generating Synthetic Tests
        :link: security
        :link-type: doc

        Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

    .. grid-item-card:: Detect Business Failures by Generating Synthetic Tests
        :link: business
        :link-type: doc

        Detect business failures, by generating synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

    .. grid-item-card:: Import Existing Datasets
        :link: import
        :link-type: doc

        Import existing test datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.


Retrieve a dataset
__________________

If you already have a dataset, you can retrieve it by its ID:

.. code-block:: python

    dataset = hub.datasets.retrieve("<DATASET_ID>")

Update a dataset
________________

You can update a dataset using the ``hub.datasets.update()`` method. Here's a basic example:

.. code-block:: python

    dataset = hub.datasets.update("<DATASET_ID>", name="My updated dataset")

Alternatively, you can update a dataset by managing its :ref:`conversations <conversations>`.

Delete a dataset
________________

You can delete a dataset using the ``hub.datasets.delete()`` method. Here's a basic example:

.. code-block:: python

    hub.datasets.delete("<DATASET_ID>")


.. _conversations:

Conversations
-------------

A conversation is a collection of messages together with evaluation checks (e.g., the expected answer, or rules that the agent must follow when responding).

Create a conversation
_____________________

You can now add conversations to the dataset. Conversations are a collection of messages together with evaluation checks (e.g., the expected answer, or rules that the agent must follow when responding).

The parameters for creating a conversation are:

- **dataset_id** (required): The ID of the dataset where the conversation will be created.
- **messages** (required): A list of messages, without the last assistant answer.  Each message is a dictionary with keys ``role`` and ``content``.
- **demo_output** (optional): A dictionary with the last assistant answer
- **tags** (optional): A list of tags you can use to categorize and organize the conversations
- **checks** (optional): A list of checks. For more information on checks, see the :doc:`/hub/sdk/checks` section.

.. note:: **Do not include last assistant answer in the list of messages.** In fact, during evaluation, we will pass
    the conversation to your agent and expect it to generate an assistant answer. The newly generated answer will
    be evaluated against the checks.

    If you want to show the last assistant answer to the user, you can include it in the conversation as ``demo_output``.
    In this way, it will be shown in the dataset, but not used in the evaluation.

.. code-block:: python

    hub.conversations.create(
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

Retrieve conversations
______________________

You can also retrieve existing conversations for editing or deletion.

For example, in certain cases you may want programmatically assign certain annotations to the conversation, or update
the conversation with the new data.

.. code-block:: python

    # Retrieve all conversations
    conversations = hub.conversations.list(dataset_id=dataset.id)

    # Or simply
    conversations = dataset.conversations

Update a conversation
_____________________

After retrieving the conversations, we can update them.
For example, let's say we want to add the tag "tech" to all conversations containing the word "laptop" in the user message:

.. code-block:: python

    # Update the conversations
    for conversation in conversations:
        if "laptop" in conversation.messages[0].content:
            # This will only update the tags, without changing the other fields
            hub.conversations.update(
                conversation.id,
                tags=conversation.tags + ["tech"]
            )

Delete a conversation
_____________________

Finally, you can delete conversations that you no longer need. For example:

.. code-block:: python

    conversation_to_delete = dataset.conversations[0]

    hub.conversations.delete(conversation_to_delete.id)


.. warning::

    Deleting a conversation is permanent and cannot be undone. Make sure you're not using the conversation in any active evaluations before deleting it.

.. toctree::
   :hidden:
   :maxdepth: 1

   security
   business
   import
