Manage tests
=====================

.. image:: /_static/images/hub/annotation-studio.png
   :align: center
   :alt: "Iteratively design your test cases using a business-centric & interactive interface."
   :width: 800

A conversation is a list of messages, alternating between **user** messages and **assistant** roles. When designing your test cases, you can decide to provide a conversation history by adding multiple turns. Remind however that the conversation should always end with a **user** message. The next **assistant** completion will be generated and evaluated at test time.

Simple conversation
-------------------

In the simplest case, a conversation is composed by a single message by the user. Here's an example:

For example, if you want to test the ability of the agent to handle a multi-turn conversation, you could write the following conversation:

   **User:** Hello, which language is your open-source library written in?


Multi-turn conversation
-----------------------

If you want to test the ability of the agent to handle a multi-turn conversation, you can write provide a conversation history with previous **assistant** messages:


   **User:** Hello, I wanted to have more information about your open-source library.

   **Assistant:** Hello! I'm happy to help you learn more about our library. What would you like to know?

   **User:** Which language is it written in?

You can provide as many turns as you want. Just remember that the conversation should always end with a **user** message, and the next **assistant** completion will be generated and evaluated at test time.

Answer examples
---------------

You can also provide an "answer example" for each test. The answer example will not be used at test time, but it can be useful while annotating the dataset with your evaluation criteria. In fact, you can test your evaluation criteria against the answer example to make sure they are working as expected.

There are multiple ways to provide an answer example:
  1. If you are importing a dataset, you can import the answer examples together with the conversations by providing a `demo_output` field. This is useful for example when you are importing production data and you want to keep a reference of the actual answer that was given by your agent in production.
  2. You can generate the agent's answer by clicking on the three-dot button and selecting "Replace the assistant message".
  3. You can also write your own answer example from scratch. This is particularly useful when you are testing your evaluation criteria against a specific answer. For example, you may want to write a non-compliant answer and make sure that your evaluation criteria will correctly flag it.

If you haven't added an answer example, by default, the Hub will populate this field with the assistant answer obtained upon the first evaluation run on your dataset.

