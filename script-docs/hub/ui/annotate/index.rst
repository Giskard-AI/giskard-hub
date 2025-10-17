:og:title: Giskard Hub UI - Human-in-the-Loop Annotation and Review
:og:description: Review and refine test cases with domain expertise. Use collaborative annotation workflows to improve test quality and ensure comprehensive coverage with intuitive visual tools.

================================
Review tests with human feedback
================================

Datasets are collection of test cases that will be used to verify the correct operation of your AI agent.

Each test case is composed of a conversation and its associated evaluation parameters (e.g. an expected answer, rules that the agent must respect, etc.).

A conversation is a list of messages. In the simplest case, a conversation is composed by a single message by the user. In the testing phase, we will send this message to your agent, record its answer, and evaluate it against the criteria that you defined in the test case.

In more advanced cases, the conversation is a multi-turn dialogue between the user and the agent, terminating with a final user message. When testing, we will pass the conversation history to your agent to generate the response that will be evaluated.

The Datasets section of the Giskard Hub provides an interface for reviewing and assigning evaluation criteria (checks) to conversations.

.. note::

  Except for very specific cases, conversations should always end with a user message. The next agent response will be generated and evaluated at runtime.

.. grid:: 1 1 2 2
   .. grid-item-card:: Create a conversation
      :link: conversations
      :link-type: doc

      Learn about conversation in test cases and how to manage and create them.

   .. grid-item-card:: Create and assign checks
      :link: checks
      :link-type: doc

      Create and assign checks to conversations to evaluate the correctness, conformity, and other evaluation metrics.

   .. grid-item-card:: Create and assign tags
      :link: tags
      :link-type: doc

      Learn about tags and how to use them to organize your conversations.

.. toctree::
   :hidden:
   :maxdepth: 3

   conversations
   checks
   tags