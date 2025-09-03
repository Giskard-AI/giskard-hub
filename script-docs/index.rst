:og:title: Giskard - LLM Agent Testing & Evaluation Platform
:og:description: Your comprehensive guide to LLM agent testing and evaluation. Choose between Giskard Hub (enterprise platform) and Giskard Open Source (Python library) for your AI safety and security needs.

Welcome to Giskard
==================

Welcome to Giskard! This section will help you understand what Giskard is, choose the right offering for your needs, and get started quickly.

* **Giskard Hub** – Our enterprise platform for LLM agent testing with team collaboration and continuous red teaming, offering both a user-friendly UI for business users and a powerful SDK for technical users
* **Giskard Open-Source** - Open-source Python library for LLM testing and evaluation, offering a programmatic interface for technical users, with basic testing capabilities to get started.
* **Giskard Research** - Our research on AI safety & security

Giskard Hub
-----------

**Giskard Hub** is our enterprise platform for LLM agent testing with advanced team collaboration and continuous red teaming. It provides a set of tools for business users and developers to test and evaluate Agents in production environments, including:

* **Team collaboration** - Real-time collaboration with shared workspaces, collaborative annotation workflows, and role-based access control for seamless team coordination
* **Continuous red teaming** - Continuous threat detection for new vulnerabilities with automated scanning and monitoring capabilities
* **Access control** - Manage who can see what data and run which tests across your organization
* **Dataset management** - Centralized storage and versioning of test cases for consistent testing
* **Custom failure categories** - Define and categorize your own failure types beyond standard security and business logic issues
* **Enterprise compliance features** - 2FA, audit logs, SSO, and enterprise-grade security controls
* **Custom business checks** - Create and deploy your own specialized testing logic and validation rules
* **Alerting** - Get notified when issues are detected with configurable notification systems
* **Evaluations** - Agent evaluations with cron-based scheduling for continuous monitoring
* **Knowledge bases** - Store and manage domain knowledge to enhance testing scenarios

.. grid:: 1 1 2 2

   .. grid-item-card:: Giskard Hub UI
      :link: hub/ui/index
      :link-type: doc

      As a business user, you can use the Giskard Hub to create test datasets, run evaluations, and manage your team.

   .. grid-item-card:: Giskard Hub SDK
      :link: hub/sdk/index
      :link-type: doc

      As a developer, you can use an SDK to interact with the Giskard Hub programmatically.

.. tip::
   **🚀 Experience Giskard Hub Today!**

   Ready to unlock the full potential of enterprise-grade AI testing? Try **Giskard Hub** with a free trial and discover advanced team collaboration, continuous red teaming, and enterprise security features.

   `Start your free enterprise trial <start/enterprise-trial.html>`_ and see how Giskard Hub can transform your AI testing workflow.

Open source
-----------

**Giskard Open Source** is a Python library for LLM testing and evaluation. It is available on `GitHub <https://github.com/Giskard-AI/giskard>`_ and formed the basis for our course on Red Teaming LLM Applications on `Deeplearning.AI <https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/>`_.

The library provides a set of tools for testing and evaluating LLMs, including:

* Automated detection of security vulnerabilities using LLM Scan.
* Automated detection of business logic failures using RAG Evaluation Toolkit.

.. grid:: 1 1 2 2

   .. grid-item-card:: Giskard Open Source
      :link: oss/sdk/index
      :link-type: doc

      As a developer, you can use the Open Source SDK to get familiar with basic testset generation for business and security failures.

   .. grid-item-card:: Deeplearning.AI ↗
      :link: https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/

      Our course on red teaming LLM applications on Deeplearning.AI helps you understand how to test, red team and evaluate LLM applications.

.. tip::
   **⚖️ Unsure about the difference between Open Source and Hub?**

   Check out our :doc:`/start/comparison` guide to learn more about the differnt features.

Open research
-------------

**Giskard Research** contributes to research on AI safety and security to showcase and understand the latest advancements in the field.
Some work has been funded by the `the European Commission <https://commission.europa.eu/index_en>`_, `Bpirance <https://www.bpifrance.com/>`_, and we've collaborated with leading companies like the `AI Incident Database <https://incidentdatabase.ai/>`_ and `Google DeepMind <https://deepmind.google/>`_.


.. grid:: 1 1 2 2

   .. grid-item-card:: Phare

      Phare is a multilingual benchmark to evaluate LLMs across key safety & security dimensions, including hallucination, factual accuracy, bias, and potential harm.

      - `Phare website <https://phare.giskard.ai/>`_
      - `Phare arXiv paper <https://arxiv.org/abs/2505.11365>`_

   .. grid-item-card:: RealHarm

      RealHarm is a dataset of problematic interactions with textual AI agents built from a systematic review of publicly reported incidents.

      - `RealHarm website <https://realharm.giskard.ai/>`_
      - `RealHarm arXiv paper <https://arxiv.org/abs/2504.10277>`_

   .. grid-item-card:: RealPerformance

      RealPerformance is a dataset of functional issues of language models that mirrors failure patterns identified through rigorous testing in real LLM agents.

      - `RealPerformance website <https://realperformance.giskard.ai/>`_

.. note::

   Are you interested in supporting our research? Check out our `Open Collective funding page for Phare <https://opencollective.com/phare-llm-benchmark>`_.

.. toctree::
   :caption: Getting Started
   :hidden:
   :maxdepth: 3

   self
   start/comparison
   start/enterprise-trial
   start/glossary/index
   Contact us <https://www.giskard.ai/contact>
   Blogs <https://www.giskard.ai/knowledge-categories/blog>

.. toctree::
   :caption: Giskard Hub UI
   :hidden:
   :maxdepth: 2

   hub/ui/index
   hub/ui/datasets/index
   hub/ui/annotate
   hub/ui/evaluations
   hub/ui/evaluations-compare
   hub/ui/continuous-red-teaming
   hub/ui/access-rights

.. toctree::
   :caption: Giskard Hub SDK
   :hidden:
   :maxdepth: 4

   hub/sdk/index
   hub/sdk/projects
   hub/sdk/datasets/index
   hub/sdk/checks
   hub/sdk/evaluations
   hub/sdk/reference/index
   GitHub <https://github.com/Giskard-AI/giskard-hub>

.. toctree::
   :caption: Giskard Open Source
   :hidden:
   :maxdepth: 4

   oss/sdk/index
   oss/sdk/security
   oss/sdk/business
   oss/sdk/legacy
   oss/notebooks/index
   oss/sdk/reference/index
   GitHub <https://github.com/Giskard-AI/giskard>
