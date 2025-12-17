:og:title: Giskard Hub - Enterprise AI Agent Testing - AI Vulnerability Scan
:og:description: Scan your AI agent for safety and security failures, including prompt injection, harmful content, excessive agency and other OWASP top 10 vulnerabilities.


===============================================
AI Vulnerability Scan
===============================================

Test your AI agent for safety and security vulnerabilities with automated red teaming attacks.

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

1. Go to **Scan** in the left sidebar
2. Click **Launch Scan**
3. Select your agent and vulnerability categories to test
4. Click **Launch Scan** to start the red teaming process
5. Review results and take action on detected vulnerabilities

.. toctree::
   :maxdepth: 2
   :hidden:

   launch-scan
   review-scan-results



Vulnerability categories
------------------------

The scan tests for these common AI security risks:

Security Risks
==============

.. grid:: 2

    .. grid-item-card:: 🔓 Prompt Injection
        :class-card: sd-border-1

        Malicious prompts that bypass your agent's safety instructions

    .. grid-item-card:: 📊 Training Data Extraction
        :class-card: sd-border-1

        Attempts to expose sensitive data from your model's training

    .. grid-item-card:: 🔍 Internal Information Exposure
        :class-card: sd-border-1

        Leakage of system configurations or internal data

    .. grid-item-card:: 🛡️ Data Privacy & Exfiltration
        :class-card: sd-border-1

        Unauthorized access to user data or privacy violations

Safety Risks
============

.. grid:: 2

    .. grid-item-card:: ⚠️ Harmful Content Generation
        :class-card: sd-border-1

        Toxic, offensive, or policy-violating content creation

    .. grid-item-card:: 🚫 Excessive Agency
        :class-card: sd-border-1

        Actions beyond intended scope or authority level

    .. grid-item-card:: 💥 Denial of Service
        :class-card: sd-border-1

        Resource exhaustion attacks that disable your system

Business Risks
==============

.. grid:: 2

    .. grid-item-card:: 🤔 Hallucination & Misinformation
        :class-card: sd-border-1

        False or misleading information that damages trust

    .. grid-item-card:: 📉 Brand Damaging & Reputation
        :class-card: sd-border-1

        Outputs that harm your brand or public perception

    .. grid-item-card:: ⚖️ Legal & Financial Risk
        :class-card: sd-border-1

        Content leading to legal liability or financial harm

    .. grid-item-card:: 💼 Misguidance & Unauthorized Advice
        :class-card: sd-border-1

        Advice outside your agent's intended expertise
