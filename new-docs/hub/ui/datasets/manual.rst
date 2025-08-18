====================================================
Manual Test Creation for Fine-Grained Control
====================================================

You can create test datasets manually for fine-grained control. This is particularly useful when you want to create test cases with full control over the test case creation process.

In this section, we will walk you through how to create a dataset manually.

Create a new dataset
--------------------

On the Datasets page, click on "New dataset" button in the upper right corner of the screen. You'll then be prompted to enter a name and description for your new dataset.

.. image:: /_static/images/hub/create-dataset.png
   :align: center
   :alt: "Create a dataset"
   :width: 800

After creating the dataset, you can add individual conversations to it.

Add a conversation
------------------

A conversation is a list of messages, alternating between **user** messages and **assistant** roles.
When designing your test cases, you can decide to provide a conversation history by adding multiple turns.
Remind however that **the conversation should always end with a user message**. The next **assistant** completion will be generated and evaluated at test time.

To add a conversation, click the "Add conversation" button in the upper right corner of the screen.

.. image:: /_static/images/hub/add-conversation.png
   :align: center
   :alt: "Add a conversation"
   :width: 800

A conversation consists of the following components:

- ``Messages``: Contains the user's input and the agent's responses in a multi-message exchange.
- ``Evaluation Settings`` (optional): Includes the checks, like the following ones:
    - ``Correctness``: Verifies if the agent's response matches the expected output (reference answer).
    - ``Conformity``: Ensures the agent's response adheres to the rules, such as "The agent must be polite."
    - ``Groundedness``: Ensures the agent's response is grounded in the conversation.
    - ``String matching``: Checks if the agent's response contains a specific string, keyword, or sentence.
    - And any custom checks you may have defined.
- ``Properties``:
    - ``Dataset``: Specifies where the conversations should be saved.
    - ``Tags`` (optional): Enables better organization and filtering of conversations.

After the conversation is created, you can add the required information to it. For example, you can add the expected output and rules to the conversation.

.. image:: /_static/images/hub/annotation-studio.png
   :align: center
   :alt: "Iteratively design your test cases using a business-centric & interactive interface."
   :width: 800

.. tip::

    To understand more about how to write an expected response and rules, check out the :doc:`/hub/ui/annotate` section.