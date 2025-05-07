=================
Manage datasets
=================

In this section, we will show how to import datasets and conversations programmatically. This allows for full control
over the import process and is especially useful when you have to import datasets or conversations in bulk (for example,
if you want to import production data).

Let's start by initializing the Hub client.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

.. note:: 
    
    If you didn't set up the environment variables, you will need to provide the API key and the Hub URL explicitly:

    .. code-block:: python

        hub = HubClient(api_key=..., hub_url=...)


You can now use the ``hub`` client to control the LLM Hub! Let's start by creating a fresh project.


Prepare the dataset
-------------------

If you don't have a dataset already, you can create one. A dataset is a collection of conversations that are used to
evaluate your agents.

.. code-block:: python

    dataset = hub.datasets.create(
        project_id="5f5e2b3b7b3f9b001f3f3b3d",  # The ID of the project where the dataset will be created
        name="Production Data",
        description="This dataset contains conversations that " \
        "are automatically sampled from the production environment.",
    )

If you already have a dataset, you can retrieve it by its ID:

.. code-block:: python

    dataset = hub.datasets.retrieve("666030a0d41f357fd061374c")


Import conversations
--------------------

You can now add conversations to the dataset. Conversations are a collection of messages together with evaluation checks (e.g., the expected answer, or rules that the agent must follow when responding).

The list of **messages** is the only required parameter. Each message is a dictionary with keys ``role`` and ``content``.

.. note:: **Do not include last assistant answer in the list of messages.** In fact, during evaluation, we will pass
    the conversation to your agent and expect it to generate an assistant answer. The newly generated answer will
    be evaluated against the checks.

    If you want to show the last assistant answer to the user, you can include it in the conversation as ``demo_output``.
    In this way, it will be shown in the dataset, but not used in the evaluation.

You can also pass two types of evaluation annotations:

- **checks** A list of checks that the agent must pass when generating the answer. It can be a built-in or custom check. For example, the built-in checks are:
    - **correctness**  A reference answer that will be used to determine the correctness of the agent's response
    - **conformity**  A list of rules that the agent must follow when generating the answer.
    - **groundedness**  A context in which the agent must ground its response.
    - **string_match**  A keyword that the agent's response must contain.
    - **metadata**  A list of JSON path rules that the agent's response must match.

For better organization, you can also assign tags to the conversation.

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
        ]
    )

You can add as many conversations as you want to the dataset.



Retrieving and editing conversations
------------------------------------

You can also retrieve existing conversation for editing or deletion.

For example, in certain cases you may want programmatically assign certain annotations to the conversation, or update
the conversation with the new data.

Let's say we want to add the tag "tech" to all conversations containing the word "laptop" in the user message:

.. code-block:: python
    
    # Retrieve all conversations
    conversations = hub.conversations.list(dataset_id=dataset.id)
    
    # Or simply
    conversations = dataset.conversations

    # Update the conversations
    for conversation in conversations:
        if "laptop" in conversation.messages[0].content:
            # This will only update the tags, without changing the other fields
            hub.conversations.update(
                conversation.id,
                tags=conversation.tags + ["tech"]
            )


Finally, you can delete conversations that you no longer need. For example:

.. code-block:: python
    
    conversation_to_delete = dataset.conversations[0]

    hub.conversations.delete(conversation_to_delete.id)


This will definitively remove the conversation from the Hub.

