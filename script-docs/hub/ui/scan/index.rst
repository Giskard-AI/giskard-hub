:og:title: Giskard Hub UI - AI Vulnerability Scanning and Red Teaming
:og:description: Scan your AI agent for safety and security failures, including prompt injection, harmful content, excessive agency and other OWASP top 10 vulnerabilities with automated red teaming.


==========================
Launch vulnerability scans
==========================

Test your AI agent for safety and security vulnerabilities with automated red teaming attacks.

.. raw:: html

   <iframe width="100%" height="400" src="https://www.youtube.com/embed/uiyWEcVJgvc?si=ViEyFCdxwNkJtZ_1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

The vulnerability scan helps you identify weaknesses in your AI agent by testing it against common attack patterns. This includes:

* Prompt injection attempts
* Harmful content generation
* Data extraction attacks
* Other OWASP GenAI Top 10 risks

**How it works:**
The scan runs dozens of specialized red teaming probes that adapt to your agent's capabilities and use case. Each probe tests for specific vulnerabilities and provides detailed results.

**What you get:**

* A security grade (A-D) based on detected vulnerabilities
* Detailed breakdown by attack category and severity
* Conversation logs showing exactly how attacks were performed
* Actionable insights to improve your agent's defenses

.. image:: /_static/images/hub/scan/scan-results.png
   :align: center
   :alt: "Example of vulnerability scan results"
   :width: 800

Quick start
-----------

.. grid:: 1 1 2 2
   
   .. grid-item-card:: Launch a scan
      :link: launch-scan
      :link-type: doc

      Select your agent and **Launch Scan** to start the red teaming process

   .. grid-item-card:: Review scan results
      :link: review-scan-results
      :link-type: doc

      Review results and take action on detected vulnerabilities

High-level workflow
-------------------

.. mermaid::
   :align: center

   graph LR
       A([<a href="launch-scan.html" target="_self">Launch Scan</a>]) --> C([<a href="review-scan-results.html" target="_self">Review Vulnerabilities</a>])
       C --> D{Take Action}
       D -->|Convert to Test| E[Send to Dataset]
       D -->|Create Task| F[<a href="../annotate/distribute_tasks.html" target="_self">Distribute Task</a>]
       E --> H[<a href="../annotate/modify_test_cases.html" target="_self">Iterate on Test Cases</a>]
       F --> H
       H --> A

Vulnerability categories
------------------------

The scan tests for these common AI security risks:

.. grid:: 1

  .. grid-item-card:: 📚 Vulnerability Categories
    :link: vulnerability-categories/index
    :link-type: doc

    Detailed information about the vulnerability categories tested by the scan

    * **55 specialized probes** across 11 vulnerability categories
    * **Detailed attack patterns** and detection indicators  
    * **Risk-level classifications** to prioritize remediation
    * **Comprehensive mitigation strategies** with practical guidance

Key probes
----------

The scan includes specialized probes that test for advanced attack scenarios:

* **Harmful Misguidance** - Tests whether an AI agent validates or encourages dangerous behaviors when users implicitly seek affirmation for harmful actions. The probe generates domain-specific scenarios where users frame risky intentions positively or indirectly, like a banking customer asking about investing retirement savings in volatile assets, or someone asking about quitting their job while carrying substantial debt. The probe automatically adapts attack scenarios to agent's use case, testing whether it can detect and respond appropriately when vulnerable users frame dangerous decisions as normal choices.

* **Agentic Tool Extraction** - Implements an agentic reconnaissance workflow that systematically queries the agent to discover and enumerate available tools, functions, and capabilities, exposing the agent's internal configuration and expanding the attack surface for targeted exploitation.

.. toctree::
   :maxdepth: 3
   :hidden:

   launch-scan
   review-scan-results
   vulnerability-categories/index