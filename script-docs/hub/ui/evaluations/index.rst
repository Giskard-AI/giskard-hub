:og:title: Giskard Hub UI - Evaluations Management
:og:description: Run and manage LLM agent evaluations through the user interface. Execute tests, schedule automated evaluations, and analyze results with comprehensive reporting and visual analytics.

Run, schedule and compare evaluations
=====================================

Evaluations are the core of the testing process in Giskard Hub. They allow you to run your test datasets against your agents and evaluate their performance using the checks that you have defined.

The Giskard Hub provides a comprehensive evaluation system that supports:

* **Local evaluations**: Run evaluations locally using development agents
* **Remote evaluations**: Run evaluations in the Hub using deployed agents
* **Scheduled evaluations**: Automatically run evaluations at specified intervals

In this section, we will walk you through how to run and manage evaluations using the Hub interface.

.. tip:: **💡 When to execute your tests?**

   Depending on your AI lifecycle, you may have different reasons to execute your tests:

   - **Development time:** Compare agent versions during development and identify the right correction strategies for developers.
   - **Deployment time:** Perform non-regression testing in the CI/CD pipeline for DevOps.
   - **Production time:** Provide high-level reporting for business executives to stay informed about key vulnerabilities in a running agent.

In this section, we will walk you through how to manage evaluations in Giskard Hub.

.. grid:: 1 1 2 2

   .. grid-item-card:: Run evaluations
      :link: /hub/ui/evaluations/create
      :link-type: doc

      Create evaluations

   .. grid-item-card:: Schedule evaluations
      :link: /hub/ui/evaluations/schedule
      :link-type: doc

      Schedule evaluations to run automatically.

   .. grid-item-card:: Compare evaluations
      :link: /hub/ui/evaluations/compare
      :link-type: doc

      Compare evaluations to see if there are any regressions.

High-level workflow
-------------------

.. mermaid::
   :align: center

   graph LR
       A[Run Evaluation] --> B[Evaluation Results]
       B --> C[Review Results]
       C --> D{Action Needed?}
       D -->|Create Task| E[Iterate on Test Cases]
       D -->|Fix Issues| F[Update Test/Agent]
       D -->|No Issues| A
       E --> A
       F --> A

.. note::

   Local evaluations are supported via the SDK. To run evaluations against local development agents, see :doc:`/hub/sdk/evaluations/local`.


.. toctree::
   :hidden:
   :maxdepth: 1

   create
   schedule
   compare