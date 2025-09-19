:og:title: Giskard Hub - Enterprise Agent Testing - Import Datasets
:og:description: Import your existing test data into Giskard Hub. Bring conversations, JSON files, and other data formats to build comprehensive test datasets.

=============================
Import Existing Datasets
=============================

You can import existing test datasets from a file. This is particularly useful when you already have a dataset that you want to use for evaluation.

In this section, we will walk you through how to import existing datasets from a JSONL file, obtained from another tool, like Giskard Open Source.

Create a new dataset
----------------------

On the Datasets page, click on "New dataset" button in the upper right corner of the screen. You'll then be prompted to enter a name and description for your new dataset.

.. image:: /_static/images/hub/create-dataset.png
   :align: center
   :alt: "Create a dataset"
   :width: 800

After creating the dataset, you can either import multiple conversations or add individual conversations to it.

Import a dataset of conversations
---------------------------------

To import conversations, click the "Import" button in the upper right corner of the screen.

.. image:: /_static/images/hub/import-conversations.png
   :align: center
   :alt: "List of conversations"
   :width: 800

You can import data in **JSON or JSONL format**, containing an array of conversations (or a conversation object per line, if JSONL).

Each conversation must be defined as a JSON object with a ``messages`` field containing the chat messages in OpenAI format. You can also specify these optional attributes:

- ``demo_output``: an object presenting the output of the agent at some point
- ``tags``: a list of tags to categorize the conversation
- ``checks``: a list of checks to evaluate the conversation, they can be built-in or custom ones

.. note::

   For detailed information about built-in checks like correctness, conformity, groundedness, string matching, metadata, and semantic similarity, including examples and how they work, see :doc:`/hub/ui/annotate`.

.. image:: /_static/images/hub/import-conversations-detail.png
   :align: center
   :alt: "Import a conversation"
   :width: 800

Here's an example of the structure and content in a dataset:

.. code-block:: python

    [
        {
            "messages": [
                {"role": "assistant", "content": "Hello!"},
                {"role": "user", "content": "Hi Agent!"},
            ],
            "demo_output": {"role": "assistant", "content": "How can I help you ?"},
            "tags": ["greetings"],
            "checks": [
                {"identifier": "correctness", "params": {"reference": "How can I help you?"}},
                {"identifier": "conformity", "params": {"rules": ["The agent should not do X"]}},
                {"identifier": "metadata", "params": {"json_path_rules": [{"json_path": "$.tool", "expected_value": "calculator", "expected_value_type": "string"}]}},
                {"identifier": "semantic_similarity", "params": {"reference": "How can I help you?", "threshold": 0.8}},
            ]
        }
    ]


Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Generate test cases** - Try :doc:`/hub/ui/datasets/business` or :doc:`/hub/ui/datasets/security`
