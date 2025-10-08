===========
Run scans
===========

Security scanning allows you to automatically test your AI models for vulnerabilities and security issues using the Giskard Hub's integrated scanning capabilities.

.. note::
   
   The scanning functionality is currently in development. Advanced features like result monitoring, status checking, and detailed result analysis will be available in a future version.

Overview
========

The Giskard Hub client provides a ``scans`` resource that allows you to run security scans on your models with optional filtering and knowledge base integration.

Quick Start
===========

To run a security scan on your model:

.. code-block:: python

    from giskard_hub import HubClient

    # Initialize the client
    hub = HubClient()

    # Run a basic scan
    scan_result = hub.scans.create(
        model_id="your-model-id"
    )

    print(f"Scan created with ID: {scan_result.id}")


Configuration Options
=====================

You can customize your scans with additional parameters:

Knowledge Base Integration
--------------------------

When you provide a ``knowledge_base_id``, the scan will use the knowledge base content to generate more targeted and context-aware security tests:

.. code-block:: python

    scan_result = hub.scans.create(
        model_id="customer-service-bot",
        knowledge_base_id="company-policies-kb"
    )

Tag Filtering
-------------

Use tags to focus your scan on specific types of vulnerabilities:

.. code-block:: python

    # Scan for hallucination vulnerabilities
    scan_result = hub.scans.create(
        model_id="your-model-id",
        tags=["gsk:threat-type='hallucination'"]
    )

    # Scan for prompt injection vulnerabilities
    scan_result = hub.scans.create(
        model_id="your-model-id",
        tags=["gsk:threat-type='prompt-injection'"]
    )

    # Scan for multiple vulnerability types
    scan_result = hub.scans.create(
        model_id="your-model-id",
        tags=[
            "gsk:threat-type='hallucination'",
            "gsk:threat-type='prompt-injection'",
            "gsk:threat-type='denial-of-service'"
        ]
    )

    # Use OWASP LLM Top 10 classifications
    scan_result = hub.scans.create(
        model_id="your-model-id",
        tags=["owasp:llm-top-10-2025='LLM10'"]
    )

Complete Example
================

Here's a complete example with all available options:

.. code-block:: python

    from giskard_hub import HubClient

    # Initialize the client
    hub = HubClient()

    # Run a comprehensive scan
    scan_result = hub.scans.create(
        model_id="your-model-id",
        knowledge_base_id="your-kb-id",  # Optional: use a knowledge base
        tags=[
            "gsk:threat-type='hallucination'",
            "gsk:threat-type='prompt-injection'",
            "gsk:threat-type='denial-of-service'",
            "owasp:llm-top-10-2025='LLM10'"
        ],
    )

    print(f"Scan started with ID: {scan_result.id}")
    print(f"Model ID: {scan_result.model_id}")
    print(f"Project ID: {scan_result.project_id}")

    # Optional: wait for the completion of the running scan
    scan.wait_for_completion()

    print(f"Scan finished with grade: {scan_result.grade}")

