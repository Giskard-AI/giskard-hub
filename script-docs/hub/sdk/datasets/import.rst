:og:title: Giskard Hub - Enterprise Agent Testing - Import Datasets
:og:description: Import your existing test data into Giskard Hub. Bring chat test cases, CSV files, and other data formats to build comprehensive test datasets.

=============================
Import existing datasets
=============================

You can import existing test datasets from a file. This is particularly useful when you already have a dataset that you want to use for evaluation.

In this section, we will walk you through how to import existing datasets from a JSONL or CSV file, obtained from another tool, like Giskard Open Source.

Importing datasets
------------------

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub.datasets`` and ``hub.chat_test_cases`` clients to import datasets and chat_test_cases!

Create a dataset
________________

As we have seen in the :doc:`/hub/sdk/datasets/index` section, we can create a dataset using the ``hub.datasets.create()`` method.

.. code-block:: python

   dataset = hub.datasets.create(
      project_id="<PROJECT_ID>",
      name="Production Data",
      description="This dataset contains chats that " \
      "are automatically sampled from the production environment.",
   )

After having created the dataset, we can import chat test cases (conversations) into it.

Import chat test cases
____________________

We can import the chats into the dataset using the ``hub.chat_test_cases.create()`` method.

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
            {"identifier": "metadata", "params": {"json_path_rules": [{"json_path": "$.category", "expected_value": "laptop", "expected_value_type": "string"}]}},
            {"identifier": "semantic_similarity", "params": {"reference": "I see, could you please give me the model number of the laptop?", "threshold": 0.8}},
        ]
    )

Import datasets from other tools
--------------------------------

We can also import datasets from other tools, like Giskard Open Source.

Import a dataset from RAGET
___________________________

We can import a dataset from RAGET but we need to do some post-processing to get the dataset in the correct format.
We still start by loading the testset we got from :doc:`/oss/sdk/business`.

.. code-block:: python

    from giskard.rag.testset import QATestset

    testset = QATestset.load("my_testset.jsonl")

We can then format the testset to the correct format and create the dataset using the ``hub.datasets.create()`` method.

.. code-block:: python

    dataset = hub.datasets.create(
        project_id="<PROJECT_ID>",
        name="RAGET Dataset",
        description="This dataset contains chats that are used to evaluate the RAGET model.",
    )

    for sample in testset.samples:
        if sample.metadata["question_type"] == "conversational":
            messages = [
                (
                    m
                    if m["role"] == "user"
                    else {"role": "assistant", "content": "I'm here to help you."}
                )
                for m in sample.conversation_history[:2]
            ]
            messages.append({"role": "user", "content": sample.question})
        else:
            messages = [
                {"role": "user", "content": sample.question},
            ]

        tags = [sample.metadata["question_type"], sample.metadata["topic"]]
        checks = []

        # Add correctness check
        if getattr(sample, "reference_answer", None):
            checks.append(
                {
                    "identifier": "correctness",
                    "enabled": True,
                    "params": {"reference": sample.reference_answer},
                }
            )

        # Add groundedness check
        if getattr(sample, "reference_context", None):
            checks.append(
                {
                    "identifier": "groundedness",
                    "enabled": True,
                    "params": {
                        "context": sample.reference_context,
                    },
                }
            )

        # Add semantic similarity check example
        if getattr(sample, "reference_answer", None):
            checks.append(
                {
                    "identifier": "semantic_similarity",
                    "enabled": True,
                    "params": {
                        "reference": sample.reference_answer,
                        "threshold": 0.8,
                    },
                }
            )

        hub.chat_test_cases.create(
            dataset_id=dataset.id,
            messages=messages,
            checks=checks,
            tags=tags,
        )

Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Generate test cases** - Try :doc:`/hub/sdk/datasets/business` or :doc:`/hub/sdk/datasets/security`