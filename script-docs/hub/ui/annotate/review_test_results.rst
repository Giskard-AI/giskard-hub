:og:title: Giskard Hub UI - Review Test Results
:og:description: Review evaluation results and understand test failures. Follow the business workflow to analyze check results, understand reasons, and take appropriate actions.

====================================================
Review test results
====================================================

This section guides you through the business workflow for reviewing test results. This workflow is designed for business users who need to review evaluation results, understand failures, and determine the appropriate actions to take.

Starting reviews
----------------

After reviewing the test results, understanding the reasons for failure, and reviewing the conversation flow, you need to decide on the appropriate action.

.. include:: workflow.rst.inc

From an evaluation run
______________________

When reviewing a failure directly from a test execution (not from a task), follow these steps:

1. **Review the failure** - After a test execution, review the failure details
2. **Determine the appropriate action** - Based on your review, decide which of the following scenarios applies:

.. note::

   To review evaluation runs, you first need to run an evaluation. For information on running evaluations, see :doc:`/hub/ui/evaluations/create`. For information on viewing evaluation results, see :doc:`/hub/ui/evaluations/index`.

If the agent is incorrect, the test is well written
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the agent is incorrect and the test is correctly identifying the issue:

- **Open a task** and assign it to the bot developer or the KB manager
- Navigate to the "Distribute tasks" workflow :doc:`/hub/ui/annotate/distribute_tasks`
- Create a task with a clear description of what needs to be fixed in the test

If the agent is correct, the test should be rewritten
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the bot's answer is actually correct and the test should be modified:

**Option 1: Rewrite the test immediately**

- **Go to the linked test case** in the dataset
- **Change the test requirements** - Rewrite checks, modify validation rules, or adjust other test criteria as needed
- **Retest multiple times** - Regenerate the bot answer and retest until the result is always PASS
- **Save the changes** - If the test case was in draft, undraft it
- **Close the task** (if applicable) - You can also set the task as closed

**Option 2: Handle it later**

- **Draft the test case** - Mark the test case as draft to prevent it from being used in evaluations
- **Open a task** - Create a task to track that this test case needs to be modified
- **Determine the test case value:**
  
  * **If the test case has no value** - Remove it from the dataset
  
  * **If the test case has value** - Complete the modification workflow:
    
    - Go to the linked test case in the dataset
    - Change the test requirements (rewrite checks, etc.)
    - Retest multiple times until the result is always PASS (regenerate a bot answer, and retest)
    - Save the changes and if the test case was in draft, undraft it
    - You can also set the task as closed

.. note::

   For detailed information about modifying test cases, see :doc:`/hub/ui/annotate/modify_test_cases`.

If you don't know
^^^^^^^^^^^^^^^^^

If you're uncertain whether the bot's answer is correct:

- **Put the test case in draft** - Mark the test case as draft to prevent it from being used in evaluations
- **Open a task** and assign it to the domain expert
- Navigate to the "Distribute tasks" workflow :doc:`/hub/ui/annotate/distribute_tasks`
- Create a task with your questions and concerns, then assign it to the domain expert who can make this determination

From an assigned task
_____________________

When reviewing a task that has been assigned to you, follow these steps:

1. **Open the task** - Open the task that has been assigned to you
2. **Read the failure details** - Review the description, result, and explanation for the failure
3. **Determine the appropriate action** - Based on your review, decide which of the following scenarios applies:

.. note::

   For information on creating tasks, see :doc:`/hub/ui/annotate/distribute_tasks`.

If the agent is incorrect, the test is well written
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Assign the task to the developer** who should correct the test
- Navigate to the "Distribute tasks" workflow :doc:`/hub/ui/annotate/distribute_tasks`
- Reassign the task to the appropriate developer with a clear description of what needs to be fixed

If the agent is correct, the test should be rewritten
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the test is correct and the test should be rewritten:

- **Provide the reason** why the test should be rewritten in the description of the task
- **Assign the task to the product owner** so that he or she can rewrite the test
- Navigate to the "Distribute tasks" workflow :doc:`/hub/ui/annotate/distribute_tasks`
- Update the task description with your findings and reassign it to the product owner

If you don't know
^^^^^^^^^^^^^^^^^

If you're uncertain whether the test is correct and need a discussion:

- **Provide the reason** why you don't know and why it needs to be discussed in the task description
- **Assign the task to the right person** with the knowledge to make this determination, or reassign it to the product owner
- Navigate to the "Distribute tasks" workflow :doc:`/hub/ui/annotate/distribute_tasks`
- Update the task with your questions and concerns, then reassign it to the appropriate person

Review the check result 
-----------------------

When reviewing a test case, the first thing to check is whether the test passed or failed. By opening the test case, you can see the metrics along with the failure category and tags on the right side of the screen.

.. image:: /_static/images/hub/review-test-metrics.png
   :align: center
   :alt: "Review test metrics"
   :width: 800

**PASS:**

- The test case met all the evaluation criteria
- All checks that were enabled on the test case passed
- The agent's response was acceptable according to the validation rules

**FAIL:**

- The test case did not meet one or more evaluation criteria
- At least one check that was enabled on the test case failed
- The agent's response did not comply with the validation rules

To understand why a test failed, you need to review the specific checks that were applied. 

.. note::

   For detailed information about checks and how they work, see :doc:`/hub/ui/annotate/overview`. For information on enabling/disabling checks, see the "Enable/Disable checks" section in :doc:`/hub/ui/annotate/modify_test_cases`.

Understand the reason
---------------------

To understand why a test passed or failed, you need to review the explanation for each check and understand the failure categories.

Read the explanation for each check
____________________________________

Each check provides an explanation of why it passed or failed. This explanation helps you understand:

* What the check was evaluating
* What criteria were applied
* Why the test passed or failed
* What specific aspects of the agent's response caused the result

.. note::

   For more information about checks and how to enable/disable them, see the "Enable/Disable checks" section in :doc:`/hub/ui/annotate/modify_test_cases`. For comprehensive information about all check types, see :doc:`/hub/ui/annotate/overview`.

Review the category of fail (if it's a fail)
_____________________________________________

When a test fails, it is categorized based on the type of failure. Understanding these categories helps you:

* Identify patterns in failures
* Prioritize which issues to address first
* Assign tasks to the right team members

**Common failure categories:**

* **Hallucination** - The agent generated information not present in the context
* **Omission** - The agent failed to include required information
* **Conformity violation** - The agent did not follow business rules or constraints
* **Groundedness issue** - The agent's answer contains information not grounded in the provided context
* **Metadata mismatch** - The agent's metadata does not match expected values
* **String matching failure** - Required keywords or phrases are missing

.. note::

   You can change the categories used for classification but before doing so, we recommend you to read about the best practices for modifying test cases in :doc:`/hub/ui/annotate/modify_test_cases`.

Review the flow of the conversation
-----------------------------------

Understanding the conversation flow helps you assess whether the test case structure is appropriate and whether the agent's response makes sense in context.

When reviewing the conversation flow, consider:

* Whether the conversation structure makes sense
* Whether the user messages are clear and unambiguous
* Whether the conversation history provides necessary context
* Whether the test case accurately represents the scenario you want to test

Conversation structure 
______________________

A conversation, or test case, is composed of a sequence of messages between the **user** and the **assistant**, alternating between each role. When designing your test cases, you can provide conversation history by adding multiple turns (multi-turn), but the conversation should always end with a **user** message. The agent's next **assistant** completion will be generated and evaluated at test time.

Simple conversation
___________________

In the simplest scenario, a conversation consists of a single message from the user. For example:

   **User:** Hello, which language is your open-source library written in?

Multi-turn conversation
_______________________

To test multi-turn capabilities or provide more context, you can add several alternating messages. For instance:

   **User:** Hello, I wanted to have more information about your open-source library.

   **Assistant:** Hello! I'm happy to help you learn more about our library. What would you like to know?

   **User:** Which language is it written in?

You can add as many turns as needed, but always ensure the conversation ends with a user message, since the assistant’s reply will be evaluated at runtime.

Conversation Answer Examples
____________________________

You can also provide an "answer example" for each test case. This answer example is not used during evaluation runs, but helps when annotating the dataset or validating your evaluation criteria. For example, you might want to:

1. Import answer examples together with conversations by providing a `demo_output` field in your dataset.
2. Generate the agent's answer by replacing the assistant message directly in the interface.
3. Write your own answer example to check specific behaviors or validation rules.

If you do not provide an answer example, the Hub will automatically use the assistant reply generated during the first evaluation run as the default example.

.. note::

   For more detailed information about creating and managing conversations, see :doc:`/hub/ui/annotate/review_test_results`.

Conversation metadata
_____________________

The conversation metadata provides additional information about the agent's response, which a developer decided to pass along with the answer, such as:

* Tool calls that were made
* System flags or status indicators
* Additional context or structured data
* Any other information the agent includes in its response

Reviewing metadata helps you understand:

* What actions the agent took during the conversation
* Whether the agent followed expected workflows
* Whether system-level requirements were met
* Whether the response structure matches expectations

For more information about metadata checks and other check types, see :doc:`/hub/ui/annotate/overview`.

Best practices
--------------

* **Review thoroughly** - Take time to understand all aspects of the test result before making a decision
* **Document your findings** - Add comments to tasks to help others understand your review
* **Use appropriate actions** - Close tasks when results are correct, assign modification work when changes are needed
* **Collaborate effectively** - Work with product owners and other team members to ensure test cases are accurate
* **Maintain quality** - Only close tasks when you're confident the test results are correct

Next steps
----------

Now that you understand how to review test results, you can:

* **Modify test cases** - Learn how to refine test cases and checks :doc:`/hub/ui/annotate/modify_test_cases`
* **Distribute tasks** - Create and manage tasks to organize review work :doc:`/hub/ui/annotate/distribute_tasks`

