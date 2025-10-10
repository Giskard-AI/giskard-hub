:og:title: Giskard Hub - Enterprise Agent Testing - Scan Vulnerabilities in your agents
:og:description: Launch several red teaming attacks to find vulnerabilities in your agents.

==========================
Launch vulnerability scans
==========================

Security scanning is a critical component of AI agent testing that allows you to automatically probe your models for vulnerabilities and security issues using Giskard Hub's integrated red teaming capabilities.

The Giskard Hub provides a comprehensive security scanning system that enables you to:

* **Automated vulnerability detection**: Run security scans that automatically test for common AI vulnerabilities
* **Targeted threat assessment**: Focus on specific vulnerability types using tags and filtering
* **Knowledge base integration**: Use domain-specific knowledge to generate more relevant security tests
* **OWASP LLM Top 10 compliance**: Test against industry-standard security classifications
* **CI/CD integration**: Integrate security scans into your deployment pipeline

In this section, we will walk you through how to run and manage security scans using the SDK.

- A **scan** is a security assessment that runs various red teaming attacks against your agent to identify potential vulnerabilities and security weaknesses.

We recommend systematically launching security scans every time you deploy an updated agent in a pre-production or staging environment. This allows you to collaborate with your team to ensure that your agent is secure and resilient against potential attacks.

.. important::
   
   Security scans can only be launched with agents that are configured in the Hub and exposed via an API endpoint. Local agents are not currently supported for security scanning.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

Run security scans
~~~~~~~~~~~~~~~~~~

First, you need to have an agent configured in the Hub. If you haven't created an agent yet, check the :ref:`Create an agent <projects:Create an agent>` section in the :doc:`/hub/sdk/projects` guide.

Launch a basic scan
-------------------

Once you have an agent configured in the Hub, you can launch a security scan. If you are running this in a CI/CD pipeline, we recommend setting the model ID in the environment.

.. code-block:: python

    model_id = os.getenv("GISKARD_HUB_MODEL_ID")  # or use agent.id

We can now launch the security scan:

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

Once the scan is completed, you may want to compare the results with some security thresholds to decide whether to promote the agent to production or not.

For example:

.. code-block:: python
    :caption: CI/CD pipeline security check example

    import sys

    # Make sure to wait for completion or the results may be incomplete
    scan_result.wait_for_completion()

    if scan_result.grade > "B":
        print(f"FAILED: Security scan grade {scan_result.grade} is below acceptable threshold.")
        print("Please review the security vulnerabilities before deploying.")
        sys.exit(1)
    
    print(f"PASSED: Security scan grade {scan_result.grade} meets security requirements.")

That covers the basics of running security scans in the Hub. You can now integrate this code in your CI/CD pipeline to automatically scan your agents for security vulnerabilities every time you deploy a new version.

Advanced scan configuration
---------------------------

Knowledge base integration
__________________________

Provide a ``knowledge_base_id`` to generate more targeted security tests based on your domain-specific knowledge:

.. code-block:: python

    scan_result = hub.scans.create(
        model_id="<GISKARD_HUB_MODEL_ID>",
        knowledge_base_id="<GISKARD_HUB_KNOWLEDGE_BASE_ID>",
        tags=["owasp:llm-top-10-2025='LLM08'"],
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

Here's a complete CI/CD security scanning workflow:

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

    # Wait for completion and check results
    scan_result.wait_for_completion(timeout=1200)

    # Check if the grade is worse than B (C, D or N/A)
    if scan_result.grade and scan_result.grade > "B":
        print(f"❌ Security check failed: Scan with Grade {scan_result.grade.value}")
        sys.exit(1)
    
    print(f"✅ Security check passed: Scan with Grade {scan_result.grade.value}")

Scan management
~~~~~~~~~~~~~~~

The SDK also provides other methods to manage your scans beyond the ``create`` method.

Retrieve a scan
---------------

You can retrieve a security scan using the ``hub.scans.retrieve()`` method:

.. code-block:: python

    scan_result = hub.scans.retrieve(scan_id)

List scans
----------

You can list security scans using the ``hub.scans.list()`` method:

.. code-block:: python

    scans = hub.scans.list(project_id=project_id)
    
    for scan in scans:
        print(f"Scan ID: {scan.id} - Grade: {scan.grade.value} - Status: {scan.progress.status.value}")

Delete a scan
-------------

You can delete a security scan using the ``hub.scans.delete()`` method:

.. code-block:: python

    hub.scans.delete(scan_id)

Best practices
~~~~~~~~~~~~~~

1. **Regular scanning**: Run security scans before every deployment, not just major releases
2. **Comprehensive coverage**: Test multiple vulnerability types and OWASP categories
3. **Knowledge base integration**: Use domain-specific knowledge bases when available
4. **Threshold management**: Set clear security grade thresholds in your CI/CD pipeline
5. **Result analysis**: Review scan results in the Hub UI for detailed vulnerability insights