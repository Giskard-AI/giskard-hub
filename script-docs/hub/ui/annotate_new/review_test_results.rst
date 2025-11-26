:og:title: Giskard Hub UI - Review Test Results
:og:description: Review evaluation results and understand test failures. Follow the business workflow to analyze check results, understand reasons, and take appropriate actions.

====================================================
Review test results
====================================================

This section guides you through the business workflow for reviewing test results. This workflow is designed for business users who need to review evaluation results, understand failures, and determine the appropriate actions to take.

Starting point
--------------

You can start reviewing test results from two entry points:

**From a task (redirection to the assign page):**

- Open a task that has been assigned to you
- Navigate to the linked test case or evaluation run
- Review the test results to understand what needs to be reviewed

.. note::

   Tasks are created from evaluation runs or scan results. For information on creating tasks, see :doc:`/hub/ui/annotate_new/distribute_tasks`.

**From an evaluation run (redirect to overall):**

- Open an evaluation run directly
- Navigate through the test cases to find ones that need review
- Review the overall results and individual test case results

.. note::

   To review evaluation runs, you first need to run an evaluation. For information on running evaluations, see :doc:`/hub/ui/evaluations/create`. For information on viewing evaluation results, see :doc:`/hub/ui/evaluations/index`.

The goal of the review: if you agree with the result, close the task. If you don't agree, modify the test case (redirect to the "Modify test cases" section).

.. tip::

   **💡 Review workflow best practices**

   When reviewing test results:
   
   * Start by understanding the overall evaluation context
   * Review check results systematically (PASS/FAIL)
   * Read explanations carefully to understand failure reasons
   * Review conversation flow to assess test case structure
   * Make informed decisions about whether to close tasks or request modifications

Review the check result of the test case
----------------------------------------

When reviewing a test case, the first thing to check is whether the test passed or failed.

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

   For detailed information about checks and how they work, see :doc:`/hub/ui/annotate/checks`. For information on enabling/disabling checks, see the "Enable/Disable checks" section in :doc:`/hub/ui/annotate_new/modify_test_cases`.

.. note::

   The "navigation" button allows you to navigate between different test cases in an evaluation run or between different evaluation runs. Use it to efficiently review multiple test results.

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

For more information about checks and how to enable/disable them, see the "Enable/Disable checks" section in :doc:`/hub/ui/annotate_new/modify_test_cases`. For comprehensive information about all check types, see :doc:`/hub/ui/annotate/checks`.

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

   You can change the categories used for classification. The system uses AI to automatically classify failures, but you can adjust these categories to better match your business needs.

Review the flow of the conversation
-----------------------------------

Understanding the conversation flow helps you assess whether the test case structure is appropriate and whether the agent's response makes sense in context.

Conversation structure and answer examples
__________________________________________

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

**Answer examples**

You can also provide an "answer example" for each test case. This answer example is not used during evaluation runs, but helps when annotating the dataset or validating your evaluation criteria. For example, you might want to:

1. Import answer examples together with conversations by providing a `demo_output` field in your dataset.
2. Generate the agent's answer by replacing the assistant message directly in the interface.
3. Write your own answer example to check specific behaviors or validation rules.

If you do not provide an answer example, the Hub will automatically use the assistant reply generated during the first evaluation run as the default example.

.. note::

   For more detailed information about creating and managing conversations, see :doc:`/hub/ui/annotate/conversations`.

When reviewing the conversation flow, consider:

* Whether the conversation structure makes sense
* Whether the user messages are clear and unambiguous
* Whether the conversation history provides necessary context
* Whether the test case accurately represents the scenario you want to test

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

For more information about metadata checks and other check types, see :doc:`/hub/ui/annotate/checks`.

Take the right action
---------------------

After reviewing the test results, understanding the reasons for failure, and reviewing the conversation flow, you need to decide on the appropriate action.

If you agree, close the task
_________________________________________________

If you agree that the test result is correct (either a pass or a legitimate failure):

1. **Review the task** - Make sure you've thoroughly reviewed all aspects
2. **Add any final comments** - Document your review findings
3. **Close the task** - Mark the task as completed

This indicates that the test case is working as intended and no further action is needed.

If you disagree, modify the test case
_______________________________________________________________________________________

If you don't agree with the test result, you have two options:

**Option 1: Modify the test case yourself**

- If you have the necessary permissions and knowledge
- Navigate to the "Modify test cases" workflow :doc:`/hub/ui/annotate_new/modify_test_cases`
- Make the necessary changes to the test case or checks
- Validate the changes and rerun the test

**Option 2: Assign the task to the product owner**

- If you don't have the necessary permissions or technical knowledge
- Navigate to the "Distribute tasks" workflow :doc:`/hub/ui/annotate_new/distribute_tasks`
- Create or update a task assigned to the product owner
- Provide a clear description of what needs to be modified
- Include your review findings and recommendations

The product owner can then:
- Modify the test case structure
- Adjust the checks or validation rules
- Remove the test case if it's not relevant
- Draft/undraft the test case as needed

Decision workflow
-----------------

.. mermaid::
   :align: center

   graph TD
       A[Review Test Result] --> B{Agree with Result?}
       B -->|Yes| C[Close Task]
       B -->|No| D{Have Permissions?}
       D -->|Yes| E[Modify Test Case]
       D -->|No| F[Assign to Product Owner]
       E --> G[Validate Changes]
       F --> H[Product Owner Modifies]
       G --> I[Task Complete]
       H --> I

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

* **Modify test cases** - Learn how to refine test cases and checks :doc:`/hub/ui/annotate_new/modify_test_cases`
* **Distribute tasks** - Create and manage tasks to organize review work :doc:`/hub/ui/annotate_new/distribute_tasks`

