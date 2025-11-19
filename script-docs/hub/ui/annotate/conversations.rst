:og:title: Giskard Hub UI - Conversation Management and Test Cases
:og:description: Manage and create conversation test cases with intuitive visual tools. Design multi-turn dialogues, add answer examples, and build comprehensive test scenarios for LLM agent evaluation.

Evaluate test cases
===================

.. image:: /_static/images/hub/annotation-studio.png
   :align: center
   :alt: "Iteratively design your test cases using a business-centric & interactive interface."
   :width: 800

A conversation or test case is a list of messages, alternating between **user** messages and **assistant** roles. When designing your test cases, you can decide to provide a conversation history by adding multiple turns. Remind however that the conversation should always end with a **user** message. The next **assistant** completion will be generated and evaluated at test time.

.. note::

  Except for very specific cases, conversations should always end with a user message. The next agent response will be generated and evaluated at runtime.

Types of conversations
_______________________

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
________________

You can also provide an "answer example" for each test. The answer example will not be used at test time, but it can be useful while annotating the dataset with your evaluation criteria. In fact, you can test your evaluation criteria against the answer example to make sure they are working as expected.

There are multiple ways to provide an answer example:
  1. If you are importing a dataset, you can import the answer examples together with the conversations by providing a `demo_output` field. This is useful for example when you are importing production data and you want to keep a reference of the actual answer that was given by your agent in production.
  2. You can generate the agent's answer by clicking on the three-dot button and selecting "Replace the assistant message".
  3. You can also write your own answer example from scratch. This is particularly useful when you are testing your evaluation criteria against a specific answer. For example, you may want to write a non-compliant answer and make sure that your evaluation criteria will correctly flag it.

If you haven't added an answer example, by default, the Hub will populate this field with the assistant answer obtained upon the first evaluation run on your dataset.

How to iterate on test cases?
______________________________

Test cases (conversations) are the foundation of your evaluation dataset. Iterating on test cases involves analyzing evaluation results, understanding failures, and refining your test cases to better capture the behaviors you want to test.

Analyze the evaluation results
------------------------------

When reviewing evaluation results, start by analyzing failed test cases:

1. **Review the Results** - Understand what the agent output was and how it differs from expectations
2. **Review the Explanation** - See why the test failed according to the checks
3. **Review the Checks** - Understand what evaluation criteria were applied and whether they're appropriate
4. **Review the Conversation** - Examine the test case structure, user messages, and conversation flow

Understanding the root cause
------------------------------

Based on your analysis, determine the root cause of the failure:

**If the test case is correctly identifying a real issue (true positive):**

* The agent's response has a genuine problem (hallucination, incorrect information, policy violation, etc.)
* The test case and checks are working as intended
* You may need to fix the agent, update the knowledge base, or address the underlying issue

**If the test case is incorrectly flagging a valid response (false positive):**

* The agent's response is actually correct or acceptable
* The test case or checks need adjustment
* You should iterate on the test case or checks to better capture your requirements

**If the test case structure is unclear or incomplete:**

* The conversation messages may be ambiguous or missing context
* The answer example may not reflect the expected behavior
* The test case needs refinement to better express the intended scenario

Iterate on the test case
------------------------------

When you need to improve a test case, consider the following approaches:

**Modify the conversation:**

* **Clarify user messages** - Make the user's intent clearer or add necessary context
* **Add conversation history** - Include previous turns if they're needed to understand the scenario
* **Adjust the conversation flow** - Restructure multi-turn conversations to better test the intended behavior

**Update the answer example:**

* **Replace with actual agent output** - Use the agent's response from an evaluation run if it better represents the scenario
* **Write a specific example** - Create an answer example that clearly demonstrates the expected or problematic behavior
* **Test against the example** - Verify that your checks correctly evaluate the answer example

**Adjust the checks:**

* **Modify check parameters** - Refine thresholds, rules, or expected values
* **Add or remove checks** - Include additional checks or remove checks that aren't relevant
* **Create new checks** - If existing checks don't capture your requirements, create custom checks

**Remove the test case:**

* If the test case isn't relevant to your use case or doesn't test meaningful behavior
* If the scenario is too ambiguous or difficult to evaluate consistently
* If you have duplicate or redundant test cases

.. mermaid::
   :align: center

   graph TD
       A[Evaluation Results] --> B[Analyze Failed Test Case]
       B --> C{Is it a true positive?}
       C -->|Yes| D[Fix Agent/Knowledge Base]
       C -->|No| E{What's the issue?}
       E -->|Test Case Unclear| F[Modify Conversation]
       E -->|Answer Example Wrong| G[Update Answer Example]
       E -->|Checks Inappropriate| H[Adjust Checks]
       E -->|Not Relevant| I[Remove Test Case]
       F --> J[Test Changes]
       G --> J
       H --> J
       J --> K{Test Case Valid?}
       K -->|No| E
       K -->|Yes| L[Test Case Ready]
       D --> M[Re-run Evaluation]

Test and validate changes
------------------------------

After modifying a test case:

1. **Review the updated test case** - Ensure the conversation structure and answer example are clear
2. **Test against checks** - Verify that your checks correctly evaluate the answer example
3. **Run a focused evaluation** - Test the updated test case in isolation or with a small subset
4. **Compare results** - Check if the test case now behaves as expected
5. **Validate across datasets** - If the test case is part of a broader evaluation, ensure it works well with other test cases

If the test case still doesn't work as expected:
* Continue iterating on the conversation, answer example, or checks
* Consider whether the test case concept is valid or needs to be rethought
* Evaluate if you need to create a new test case instead of modifying the existing one

Best practices for iterating on test cases
------------------------------------------

* **Start with clear intent** - Know what behavior or scenario you want to test before creating or modifying a test case
* **Keep test cases focused** - Each test case should test one specific behavior or scenario
* **Use answer examples effectively** - Answer examples help validate that your checks work correctly
* **Test incrementally** - Make small changes and test them before making larger modifications
* **Document your intent** - Use tags or descriptions to document what each test case is testing
* **Review regularly** - Periodically review test cases to ensure they remain relevant and effective
* **Remove obsolete test cases** - Clean up test cases that are no longer relevant or have been superseded

Next steps
__________

Now that you have created a conversation, you can assign checks and tags to it, or create tasks to manage review workflows.

* **Assign checks to tests** - :doc:`/hub/ui/annotate/checks`
* **Assign tags to tests** - :doc:`/hub/ui/annotate/tags`
* **Manage tasks** - :doc:`/hub/ui/annotate/tasks`
* **Run evaluations** - :doc:`/hub/ui/evaluations/create`