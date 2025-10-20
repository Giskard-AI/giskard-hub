:og:title: Giskard Hub SDK - Evaluations Management
:og:description: Run and manage LLM agent evaluations programmatically. Execute tests, schedule automated evaluations, and analyze results through the comprehensive Python SDK.

======================================
Run, schedule and compare evaluations
======================================

In this section, we will walk you through how to run and manage evaluations using the SDK.

Evaluations are the core of the testing process in Giskard Hub. They allow you to run your test datasets against your agents and evaluate their performance using the checks that you have defined. We recommend to systematically launch evaluation runs every time you deploy an updated agent in a pre-production or staging environment. In this way, you can collaborate with your team to ensure that the agent is performing as expected.

.. grid:: 1 1 2 2

    .. grid-item-card:: Run local evaluations
        :link: local
        :link-type: doc

        Run evaluations against a local agent.

    .. grid-item-card:: Run remote evaluations
        :link: remote
        :link-type: doc

        Run evaluations against a remote agent.

    .. grid-item-card:: Schedule evaluations
        :link: schedule
        :link-type: doc

        Schedule evaluations to run automatically.

    .. grid-item-card:: Compare evaluations
        :link: compare
        :link-type: doc

        Compare evaluations to see if there are any regressions.

.. toctree::
   :hidden:
   :maxdepth: 1

   local
   remote
   schedule
   compare