:og:title: Giskard Hub UI - Modify Test Cases
:og:description: Refine test cases and validation rules. Follow the product owner workflow to draft/undraft test cases, enable/disable checks, and structure your dataset.

====================================================
Modify the test cases
====================================================

This section guides you through the product owner workflow for modifying test cases. This workflow is designed for product owners and technical team members who need to refine test cases, adjust validation rules, and structure datasets based on review feedback.

.. tip::

   Test cases (conversations) are part of datasets. For information on creating and managing datasets, see :doc:`/hub/ui/datasets/index`.

.. tip::

   **💡 When to modify test cases**
   
   * Review feedback indicates that test cases need adjustment (see :doc:`/hub/ui/annotate/review_test_results`)
   * Test cases are not accurately representing the intended scenarios
   * Checks need to be adjusted to better match evaluation criteria
   * Test cases need to be organized with tags and descriptions
   
   This workflow is typically triggered after a business user reviews test results and identifies issues that need modification.

Modify test cases
^^^^^^^^^^^^^^^^^

Draft/Undraft your test case
-----------------------------

Drafting and undrafting test cases allows you to control which test cases are included in evaluation runs.

Setting a test case to draft status:

* **Excludes it from evaluation runs** - Draft test cases are not used in evaluations until they are undrafted
* **Indicates work in progress** - Shows that the test case is being reviewed or modified
* **Prevents biased metrics** - Ensures that incomplete or problematic test cases don't affect your evaluation results

To draft a test case:

1. Open the test case (conversation) you want to draft
2. Set it to draft status using the draft toggle or option
3. The test case will be excluded from future evaluation runs until it is undrafted

You can also set a test case to draft when creating a task from an evaluation run. This ensures that failed test cases are automatically excluded from subsequent evaluations until they are reviewed and fixed.

.. tip::

   For more information about creating tasks and setting test cases to draft, see :doc:`/hub/ui/annotate/task_management`.

Hide/Unhide
___________

In addition to drafting, you can hide false positive results to organize your evaluation overview:

* **Hide** - Makes the false positive result less visible in the evaluation overview and for the metrics computations in the dashboard
* **Unhide** - Makes the false positive result visible again in the evaluation overview

.. tip::

   You can look at understanding the overview of evaluations in :doc:`/hub/ui/evaluations/create`.

Rerun the test case
-------------------

After modifying a test case or its checks, you should rerun the test to validate your changes.

**When to rerun:**

* After modifying the conversation structure
* After updating the answer example
* After enabling or disabling checks
* After modifying check requirements
* After making any changes that could affect the test result

**How to rerun:**

1. Make your modifications to the test case
2. Use the "Test" option to run the test case in isolation
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

Modify checks
^^^^^^^^^^^^^

Checks are evaluation criteria that measure the quality of your agent's responses. You can enable or disable checks on individual test cases to control what is being evaluated.

It is important to understand any changes you make to the checks and how they will affect the evaluation results.

- **Enable/Disable checks** - Enable or disable checks on a test case to control what is being evaluated
- **Modify check requirement** - Modify the requirements of a check to better match your evaluation criteria
- **Validate the check** - Validate the check to ensure it works correctly

.. tip::

   For an overview of the different checks and how to choose the right one, see :doc:`/hub/ui/annotate/overview`.

Enable/Disable checks
---------------------

You can enable multiple checks on a single test case to evaluate different aspects of the agent's response. 

Disabling a check removes it from the evaluation for that specific test case, but the check definition remains available for use on other test cases.

Modify check requirements
--------------------------

You can adjust the parameters of most built-in checks (like context or reference answer) specifically for the current test case by editing them directly within the test case view. These changes only impact the selected test case. 

If you want to change the requirements of a custom check (such as its overall rules or similarity threshold), you must edit the custom check itself from the Checks page. Modifying a custom check will affect all test cases using that check. For major or experimental changes, it's recommended to create a new custom check instead—then enable it only on the test cases where you want the new behavior.

.. tip::

   To get a full overview of the different checks and the parameters to configure them, see :doc:`/hub/ui/annotate/overview`.

Validate the check
------------------

After modifying a check, you should validate it to ensure it works correctly.

Rerunning the agent answer
________________________

To validate that your check modifications work correctly:

1. **Rerun the test case** - Execute the test case with the modified check
2. **Review the result** - Check if the test passes or fails as expected
3. **Review the explanation** - Understand why the check passed or failed
4. **Compare with expectations** - Verify that the result matches what you intended

Rerunning the agent answer helps you:

* Verify that the check correctly evaluates the agent's response in different scenarios
* Ensure that your modifications don't break the check
* Catch issues before using the check in full evaluation runs

Rerunning the check evaluation
______________________________

You may also need to validate the check evaluation by rerunning it multiples for each of the regenereated answers.

1. **Review check explanations** - Understand how the check evaluated the response
2. **Check for consistency** - Ensure the check provides consistent evaluations
3. **Validate against examples** - Test the check against known good and bad examples
4. **Adjust if needed** - Modify the check prompt or configuration if results are inconsistent

For more information about iterating on checks, see :doc:`/hub/ui/annotate/overview`.

Structure your test cases with tags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tags are optional but highly recommended labels that help you organize and filter your test cases. Tags help you analyze evaluation results by allowing you to:

* **Filter results** - Focus on specific test cases or scenarios
* **Compare performance** - See how your agent performs across different test categories
* **Identify weak areas** - Discover which types of tests have higher failure rates
* **Organize reviews** - Review test cases by category or domain

.. tip::

   For more information about tags, see :doc:`/hub/ui/annotate/overview`.

Next steps
^^^^^^^^^^

Now that you understand how to modify test cases, you can:

* **Review test results** - Understand how test results are reviewed :doc:`/hub/ui/annotate/review_test_results`
* **Distribute tasks** - Learn how tasks are created and managed :doc:`/hub/ui/annotate/task_management`
* **Learn about checks** - Get detailed information about check types :doc:`/hub/ui/annotate/overview`
* **Learn about tags** - Understand how to organize with tags :doc:`/hub/ui/annotate/overview`

