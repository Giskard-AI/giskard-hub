:og:title: Giskard Hub UI - Review Scan Results and Security Analysis
:og:description: Review comprehensive vulnerability scan results with detailed security analysis. Understand security grades, explore attack details, and take actionable steps to improve AI agent security.

Review scan results
===================

Understand your AI agent's security vulnerabilities and take action to fix them.

Understanding your security grade
----------------------------------

Your scan results include a security grade from A to D:

* **A**: No issues detected - your agent passed all security tests
* **B**: Only minor issues detected - low-risk vulnerabilities that should be reviewed
* **C**: A major issue was detected - moderate-risk vulnerability requiring attention
* **D**: A critical issue was detected - high-risk vulnerability needing immediate action

.. image:: /_static/images/hub/scan/scan-results.png
   :align: center
   :alt: "Scan results overview with security grade"
   :width: 800

Explore attack details
----------------------

Scroll to any vulnerability category to see the specific attacks that were tested:

.. image:: /_static/images/hub/scan/probe-listing.png
   :align: center
   :alt: "List of probes and attack attempts"
   :width: 800

Analyze individual vulnerabilities
----------------------------------

Click **Review** next to any probe to see detailed attack results:

.. image:: /_static/images/hub/scan/attempt-successful.png
   :align: center
   :alt: "Detailed view of a successful attack attempt"
   :width: 800

This shows you:

* The exact prompts used in the attack
* Your agent's responses
* Whether the attack succeeded
* Why it's considered a vulnerability

Take action on findings
-----------------------

For each detected issue, you have two main actions:

- **Mark as false positive:**  
  If the identified issue is not a real risk for your use case (for example, it is expected behavior or not relevant to your deployment), you can mark it as a false positive. This will immediately update your agent's security grade and help you track which findings require action.

- **Convert to test case:**  
  You can save the detected attack as a reproducible test case by clicking **Send to dataset**. This allows you to track fixes over time, build regression tests to make sure the issue doesn't reappear, and share concrete examples with your team for further analysis and improvement.

.. tip:: 

   To learn more about reviewing test cases, see :doc:`/hub/ui/annotate/review_test_results`.

Next steps
----------

Now that you have reviewed the scan results, you can take action on the detected vulnerabilities.

* **Review test cases** - :doc:`/hub/ui/annotate/index`
* **Run and schedule evaluations** - :doc:`/hub/ui/evaluations/index`