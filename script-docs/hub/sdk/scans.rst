:og:title: Giskard Hub SDK - Vulnerability Scanning and Red Teaming
:og:description: Launch comprehensive red teaming attacks to find vulnerabilities in your agents. Automated security scanning with OWASP LLM Top 10 compliance using the Python SDK.

==========================
Launch vulnerability scans
==========================

Security scanning is a critical component of AI agent testing that allows you to automatically probe your models for vulnerabilities and security issues using Giskard Hub's integrated red teaming capabilities.

The Giskard Hub provides a comprehensive scanning system that enables you to:

* **Automated vulnerability detection**: Run scans that automatically test for common AI vulnerabilities
* **Targeted threat assessment**: Focus on specific vulnerability types using tags and filtering
* **Knowledge base integration**: Use domain-specific knowledge to generate more relevant security tests
* **OWASP LLM Top 10 compliance**: Test against industry-standard security classifications
* **CI/CD integration**: Integrate scans into your deployment pipeline

In this section, we will walk you through how to run and manage scans using the SDK.

- A **scan** is a security assessment that runs various red teaming attacks against your agent to identify potential vulnerabilities and security weaknesses.

We recommend systematically launching scans every time before deploying an updated agent in a pre-production or staging environment. This allows you to collaborate with your team to ensure that your agent is secure and resilient against potential attacks.

.. important::
   
   Scans can only be launched with agents that are configured in the Hub and exposed via an API endpoint. Local agents are not currently supported for scanning.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

First, you need to have an agent configured in the Hub. If you haven't created an agent yet, check the Create an agent section in the Projects guide.

Attack overview
---------------

The vulnerability scan test suite includes various attack patterns designed to test for specific vulnerabilities in your agent. 
We recommend running a full scan regularly but you can also run targeted scans for specific vulnerability types during development. 

.. note::
    
    For a full overview of the attacks, see the :doc:`/hub/ui/scan/vulnerability-categories/index` section.

Launch a basic scan
-------------------

Once you have an agent configured in the Hub, you can launch a security scan. If you are running this in a CI/CD pipeline, we recommend setting the model ID in the environment.

.. code-block:: python

    model_id = os.getenv("GISKARD_HUB_MODEL_ID")  # or use agent.id

We can now launch the scan:

.. code-block:: python

    # All the OWASP LLM Top 10 vulnerabilities
    tags = [f"owasp:llm-top-10-2025='LLM{i:02d}'" for i in range(1, 11)]

    scan_result = hub.scans.create(
        model_id=model_id,
        tags=tags,
    )

.. note::

    Running scans with all OWASP LLM Top 10 categories can be token-intensive and may take significant time to complete. Consider running targeted scans for specific vulnerability types during development.

The security scan will be queued and processed by the Hub. The ``create`` method will immediately return a scan object while the scan is running. Note that this object will not contain the scan results until the scan is completed.

You can wait until the scan has finished running with the ``wait_for_completion`` method:

.. code-block:: python

    scan_result.wait_for_completion(
        # optionally, specify a timeout in seconds (10 min by default)
        timeout=600
    )

This will block until the scan is completed and update the ``scan_result`` object in-place. The method will wait for up to 10 minutes for the scan to complete.

Then, you can check the results:

.. code-block:: python

    print(f"Scan completed with ID: {scan_result.id}")
    print(f"Model ID: {scan_result.model.id}")
    print(f"Scan grade: {scan_result.grade.value}")

View scan metrics
_________________

You can view a detailed breakdown of the scan results using the ``print_metrics()`` method:

.. code-block:: python

    scan_result.print_metrics()

This will display a formatted table showing:

* **Category**: The security vulnerability category (e.g., "Prompt Injection", "Hallucination / Misinformation")
* **Probe Name**: The specific probe that was run
* **Severity**: The highest severity level found (CRITICAL, MAJOR, MINOR, SAFE)
* **Results**: Number of issues found and total number of attacks performed

.. image:: /_static/images/sdk/scan-metrics-output.png
   :alt: Scan metrics output
   :align: center


Advanced scan configuration
---------------------------

Knowledge base integration
__________________________

Provide a ``knowledge_base_id`` to generate more targeted security tests based on your domain-specific knowledge:

.. code-block:: python

    scan_result = hub.scans.create(
        model_id="<GISKARD_HUB_MODEL_ID>",
        knowledge_base_id="<GISKARD_HUB_KNOWLEDGE_BASE_ID>",
        tags=["owasp:llm-top-10-2025='LLM09'"],
    )

Vulnerability type filtering
____________________________

Similarly to the OWASP LLM Top 10 tags, you can use the ``gsk:threat-type`` tags to focus on specific vulnerability types:

.. code-block:: python

    # Scan for specific vulnerabilities
    scan_result = hub.scans.create(
        model_id="<GISKARD_HUB_MODEL_ID>",
        tags=["gsk:threat-type='prompt-injection'"],
    )

    # Scan for multiple vulnerability types
    scan_result = hub.scans.create(
        model_id="<GISKARD_HUB_MODEL_ID>",
        knowledge_base_id="<GISKARD_HUB_KNOWLEDGE_BASE_ID>",
        tags=[
            "gsk:threat-type='hallucination'",
            "gsk:threat-type='prompt-injection'",
            "gsk:threat-type='harmful-content-generation'",
        ],
    )

    # Scan for all vulnerability types
    categories = hub.scans.list_categories()
    scan_result = hub.scans.create(
        model_id="<GISKARD_HUB_MODEL_ID>",
        knowledge_base_id="<GISKARD_HUB_KNOWLEDGE_BASE_ID>",
        tags=[category.id for category in categories],
    )

Complete workflow example
-------------------------

Here's a complete CI/CD scanning workflow:

.. code-block:: python

    import os
    import sys
    from giskard_hub import HubClient

    hub = HubClient(...)
    model_id = os.getenv("GISKARD_HUB_MODEL_ID")

    # Run security scan with specific tags
    scan_result = hub.scans.create(
        model_id=model_id,
        tags=[
            "gsk:threat-type='prompt-injection'",
            "owasp:llm-top-10-2025='LLM01'",
        ],
    )

    # Wait for completion and check result metrics
    scan_result.wait_for_completion(timeout=1200)
    scan_result.print_metrics()

    # Check if the grade is worse than A or B (C, D or N/A)
    if scan_result.grade not in ["A", "B"]:
        print(f"❌ Security check failed: Scan with Grade {scan_result.grade.value}")
        sys.exit(1)
    
    print(f"✅ Security check passed: Scan with Grade {scan_result.grade.value}")

API Reference
==============

For detailed information about scan management methods and parameters, see the :doc:`/hub/sdk/reference/index` section.
