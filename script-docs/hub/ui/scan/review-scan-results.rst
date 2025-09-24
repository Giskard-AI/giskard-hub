===============================================
Review scan results
===============================================

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

For each detected issue, you can:

**Mark as false positive**
   If the identified issue doesn't represent a real risk in your context, mark it as a false positive. This updates your security grade automatically.

**Convert to test case**
   Click **Send to dataset** to save the attack as a reproducible test case. This helps you:
   
   * Track fixes over time
   * Build regression tests
   * Share examples with your team

