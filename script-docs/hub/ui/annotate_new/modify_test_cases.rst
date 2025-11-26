:og:title: Giskard Hub UI - Modify Test Cases
:og:description: Refine test cases and validation rules. Follow the product owner workflow to draft/undraft test cases, enable/disable checks, and structure your dataset.

====================================================
Modify the test cases
====================================================

This section guides you through the product owner workflow for modifying test cases. This workflow is designed for product owners and technical team members who need to refine test cases, adjust validation rules, and structure datasets based on review feedback.

.. note::

   Test cases (conversations) are part of datasets. For information on creating and managing datasets, see :doc:`/hub/ui/datasets/index`.

.. tip::

   **💡 When to modify test cases**

   Modify test cases when:
   
   * Review feedback indicates that test cases need adjustment (see :doc:`/hub/ui/annotate_new/review_test_results`)
   * Test cases are not accurately representing the intended scenarios
   * Checks need to be adjusted to better match evaluation criteria
   * Test cases need to be organized with tags and descriptions
   
   This workflow is typically triggered after a business user reviews test results and identifies issues that need modification.

Draft/Undraft your test case
-----------------------------

Drafting and undrafting test cases allows you to control which test cases are included in evaluation runs.

Draft your test case
____________________

Setting a test case to draft status:

* **Excludes it from evaluation runs** - Draft test cases are not used in evaluations until they are undrafted
* **Indicates work in progress** - Shows that the test case is being reviewed or modified
* **Prevents biased metrics** - Ensures that incomplete or problematic test cases don't affect your evaluation results

To draft a test case:

1. Open the test case (conversation) you want to draft
2. Set it to draft status using the draft toggle or option
3. The test case will be excluded from future evaluation runs until it is undrafted

You can also set a test case to draft when creating a task from an evaluation run. This ensures that failed test cases are automatically excluded from subsequent evaluations until they are reviewed and fixed.

.. note::

   For more information about creating tasks and setting test cases to draft, see :doc:`/hub/ui/annotate_new/distribute_tasks`.

Undraft your test case
______________________

Undrafting a test case makes it available for evaluation runs again:

* **Includes it in evaluations** - The test case will be used in future evaluation runs
* **Indicates completion** - Shows that the test case has been reviewed and is ready
* **Requires resolved tasks** - All associated tasks should be resolved before undrafting

To undraft a test case:

1. Ensure all associated tasks are resolved
2. Open the test case you want to undraft
3. Remove the draft status using the draft toggle or option
4. The test case will be included in future evaluation runs

Hide/Unhide
___________

In addition to drafting, you can hide test cases to organize your dataset:

* **Hide** - Makes the test case less visible in lists and filters (but it may still be included in evaluations if not drafted)
* **Unhide** - Makes the test case visible again in lists and filters

Use hiding to organize large datasets without affecting evaluation runs. Use drafting to control which test cases are actually evaluated.

Rerun the test case?
--------------------

After modifying a test case or its checks, you should rerun the test to validate your changes.

**When to rerun:**

* After modifying the conversation structure
* After updating the answer example
* After enabling or disabling checks
* After modifying check requirements
* After making any changes that could affect the test result

**How to rerun:**

1. Make your modifications to the test case
2. Use the "Rerun" or "Test" option to run the test case in isolation
3. Review the results to see if your changes had the intended effect
4. Continue iterating if needed

Rerunning helps you:

* Validate that your modifications work as expected
* Catch issues before including the test case in a full evaluation run
* Iterate quickly on test case improvements
* Ensure that your changes don't introduce new problems

.. tip::

   **💡 Rerun before full evaluation**

   Always rerun test cases after modifications to validate changes before including them in a full evaluation run. This saves time and ensures your modifications work as intended.

Remove test case
-----------------

If a test case is not relevant to your use case or doesn't test meaningful behavior, you can remove it.

**When to remove a test case:**

* The test case is not relevant to your use case
* The scenario is too ambiguous or difficult to evaluate consistently
* You have duplicate or redundant test cases
* The test case concept is fundamentally flawed and cannot be fixed

**How to remove:**

1. Open the test case you want to remove
2. Use the delete or remove option
3. Confirm the removal

.. warning::

   Removing a test case is permanent. Make sure you want to remove it before confirming. Consider drafting it instead if you might need it later.

Enable/Disable checks
---------------------

Checks are evaluation criteria that measure the quality of your agent's responses. You can enable or disable checks on individual test cases to control what is being evaluated.

What is a check?
________________

A check is a validation rule that evaluates whether the agent's response meets specific criteria. Various types of checks are available:

* **Correctness Check** - Verifies that all information from the reference answer is present without contradiction
* **Conformity Check** - Verifies that the agent follows business rules and constraints
* **Groundedness Check** - Verifies that all information is present in the given context
* **String Matching Check** - Verifies that specific keywords or sentences are present
* **Metadata Check** - Verifies that metadata matches expected values at JSON paths
* **Semantic Similarity Check** - Verifies that the response is semantically similar to a reference

For detailed information about each check type, including examples and best practices, see :doc:`/hub/ui/annotate/checks`.

.. tip::

   **💡 Choosing the right check**

   The choice of check depends on what you want to evaluate:
   
   * Use **Correctness Check** to ensure all required information is present
   * Use **Groundedness Check** to detect hallucinations
   * Use **Conformity Check** to verify business rules are followed
   * Use **Metadata Check** to verify tool calls and system behavior
   * Use **String Matching Check** for specific keywords or phrases
   * Use **Semantic Similarity Check** when you need to allow variation in wording
   
   For guidance on choosing checks, see :doc:`/hub/ui/annotate/checks`.

Enable checks
_____________

To enable a check on a test case:

1. Open the test case
2. Navigate to the checks section
3. Select the check you want to enable
4. Configure the check parameters if needed
5. Save the changes

You can enable multiple checks on a single test case to evaluate different aspects of the agent's response.

Disable checks
______________

To disable a check on a test case:

1. Open the test case
2. Navigate to the checks section
3. Disable the check you want to remove
4. Save the changes

Disabling a check removes it from the evaluation for that specific test case, but the check definition remains available for use on other test cases.

Modify check requirement
--------------------------

You can modify the requirements of a check to better match your evaluation criteria.

Reference/Context/Rules
________________________

Depending on the check type, you can modify:

**For Correctness Check:**
* **Reference Answer** - The expected answer that the agent should match

**For Groundedness Check:**
* **Reference Context** - The context that the agent's answer should be grounded in

**For Conformity Check:**
* **Rules** - The business rules or constraints that the agent should follow
* You can add, remove, or modify individual rules

**For String Matching Check:**
* **Keyword or Sentence** - The specific string that should be present in the response

**For Metadata Check:**
* **JSON Path Rules** - The expected values at specific JSON paths in the metadata

**For Semantic Similarity Check:**
* **Reference Answer** - The reference that the response should be similar to
* **Threshold** - The minimum similarity score required

To modify check requirements:

1. Open the test case with the check you want to modify
2. Navigate to the checks section
3. Edit the check parameters
4. Save the changes
5. Rerun the test to validate the changes

For more detailed information about each check type and its parameters, including examples and configuration options, see :doc:`/hub/ui/annotate/checks`.

.. note::

   When modifying check requirements, make sure to rerun the test case to validate that your changes work correctly. See the "Validate the check" section below.

Validate the check
------------------

After modifying a check, you should validate it to ensure it works correctly.

Rerunning the bot answer
________________________

To validate that your check modifications work correctly:

1. **Rerun the test case** - Execute the test case with the modified check
2. **Review the result** - Check if the test passes or fails as expected
3. **Review the explanation** - Understand why the check passed or failed
4. **Compare with expectations** - Verify that the result matches what you intended

Rerunning the bot answer helps you:

* Verify that the check correctly evaluates the agent's response
* Ensure that your modifications don't break the check
* Catch issues before using the check in full evaluation runs

Rerunning the judge
___________________

If your check uses an LLM-as-a-judge approach, you may also need to validate the judge's evaluation:

1. **Review judge explanations** - Understand how the judge evaluated the response
2. **Check for consistency** - Ensure the judge provides consistent evaluations
3. **Validate against examples** - Test the judge against known good and bad examples
4. **Adjust if needed** - Modify the judge prompt or configuration if results are inconsistent

For more information about iterating on checks, see :doc:`/hub/ui/annotate/checks`.

Structure your test case
----------------------------------------------------------

You can add additional structure and metadata to your test cases to better organize and understand them.

Assigning tags
______________

Tags allow you to organize and categorize test cases. They help you:

* Filter conversations based on categories
* Manage your agent's performance more effectively
* Group similar test cases together
* Track different types of issues or scenarios

**Categories of tags:**

* **Issue-Related Tags** - Categorize types of problems (e.g., "Hallucination", "Misunderstanding")
* **Attack-Oriented Tags** - Relate to adversarial testing (e.g., "SQL Injection Attempt", "Phishing Query")
* **Legitimate Question Tags** - Categorize standard queries (e.g., "Balance Inquiry", "Loan Application")
* **Context-Specific Tags** - Pertain to business contexts (e.g., "Caisse d'Epargne", "Corporate Banking")
* **User Behavior Tags** - Describe user behavior (e.g., "Confused User", "Angry Customer")
* **Temporal Tags** - Track testing phases (e.g., "red teaming phase 1", "red teaming phase 2")

To assign tags:

1. Open the test case
2. Navigate to the tags section
3. Select or create tags that apply to the test case
4. Save the changes

You can assign multiple tags to a single test case to cover all relevant aspects.

For more information about tags, including best practices and naming conventions, see :doc:`/hub/ui/annotate/tags`.

.. tip::

   **💡 Organizing with tags**

   Use tags strategically to:
   
   * Filter test cases by category or issue type
   * Track performance across different scenarios
   * Organize large datasets effectively
   * Identify patterns in failures
   
   You can assign multiple tags to a single test case to cover all relevant aspects.

Update task descriptions
_________________________

You can add a description to a test case to document:

* What the test case is testing
* Why it's important
* What behavior or scenario it represents
* Any special considerations or context

Task descriptions help:

* Team members understand the purpose of each test case
* Maintain context over time
* Document decisions and rationale
* Guide future modifications

To add a description:

1. Open the test case
2. Navigate to the description or metadata section
3. Add or edit the description
4. Save the changes

Add comments
____________

Comments allow you to add notes and insights about a test case:

* Review findings and observations
* Document modifications and their reasons
* Share context with team members
* Track the evolution of a test case

Comments are particularly useful for:

* Documenting why a test case was modified
* Explaining complex scenarios or edge cases
* Sharing insights from review processes
* Maintaining a history of changes and decisions

To add a comment:

1. Open the test case
2. Navigate to the comments section
3. Add your comment
4. Save the changes

Best practices
--------------

* **Iterate incrementally** - Make small changes and test them before making larger modifications
* **Validate changes** - Always rerun tests after modifying test cases or checks
* **Document decisions** - Use descriptions and comments to document why changes were made
* **Organize with tags** - Use tags to maintain structure in large datasets
* **Draft when needed** - Use drafting to prevent incomplete test cases from affecting evaluations
* **Remove obsolete cases** - Clean up test cases that are no longer relevant

Workflow summary
----------------

.. mermaid::
   :align: center

   graph TD
       A[Receive Task/Review Feedback] --> B[Open Test Case]
       B --> C{Action Needed}
       C -->|Draft| D[Set to Draft]
       C -->|Modify| E[Modify Test Case]
       C -->|Remove| F[Remove Test Case]
       C -->|Adjust Checks| G[Enable/Disable/Modify Checks]
       E --> H[Rerun Test]
       G --> H
       H --> I{Result Correct?}
       I -->|No| E
       I -->|Yes| J[Add Tags/Comments]
       J --> K[Undraft if Ready]
       K --> L[Task Complete]

Next steps
----------

Now that you understand how to modify test cases, you can:

* **Review test results** - Understand how test results are reviewed :doc:`/hub/ui/annotate_new/review_test_results`
* **Distribute tasks** - Learn how tasks are created and managed :doc:`/hub/ui/annotate_new/distribute_tasks`
* **Learn about checks** - Get detailed information about check types :doc:`/hub/ui/annotate/checks`
* **Learn about tags** - Understand how to organize with tags :doc:`/hub/ui/annotate/tags`

