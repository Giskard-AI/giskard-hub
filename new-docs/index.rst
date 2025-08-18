Welcome to Giskard
==================

Welcome to Giskard! This section will help you understand what Giskard is, choose the right offering for your needs, and get started quickly.

* **Enterprise Hub** - Our enterprise Hub for team collaboration and continuous red teaming
* **Open Source** - Our open-source Python library for LLM testing and evaluation
* **Open Research** - Our open-source research on AI safety and security

.. tip::

   If you're not sure which Giskard offering is right for you, check out the :doc:`start/comparison` guide.

Enterprise
----------

**Giskard Enterprise Hub** is a platform for team collaboration and continuous red teaming. It provides a set of tools for testing and evaluating LLMs, including:

* Team collaboration - Multiple users working together on testing and evaluation
* Continuous red teaming - Automated threat detection and response
* Access control - Manage who can see what data and run which tests
* Dataset management - Centralized storage and versioning of test cases
* Performance monitoring - Track model performance over time
* Alerting - Get notified when issues are detected

.. grid:: 1 1 2 2

   .. grid-item-card:: Enterprise UI
      :link: hub/ui/index
      :link-type: doc

      As a non-technical user, you can use the Giskard Enterprise Hub to create test datasets, run evaluations, and manage your team.

   .. grid-item-card:: Enterprise SDK
      :link: hub/sdk/index
      :link-type: doc

      As a developer, you can use the Hub SDK to interact with the Giskard Enterprise Hub programmatically.

Open Source
-----------

**Giskard Open Source** is a Python library for LLM testing and evaluation. It is available on `GitHub <https://github.com/Giskard-AI/giskard>`_ and formed the basis for `our course on Red Teaming LLM Applications on Deeplearning.AI <https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/>`_.

The library provides a set of tools for testing and evaluating LLMs, including:

* Automated detection of security vulnerabilities using LLM Scan.
* Automated detection of business logic failures using RAG Evaluation Toolkit.

.. grid:: 1 1 2 2

   .. grid-item-card:: Open Source SDK
      :link: oss/sdk/index
      :link-type: doc

      As a developer, you can use the Open Source SDK to get familiar with basic testset generation for business and security failures.

Open Research
-------------

**Giskard Research** contributes to open research on AI safety and security to showcase and understand the latest advancements in the field. Some work has been funded by the `European Union <https://european-union.europa.eu/>`_, and we've collaborated with leading companies like the `AI Incident Database <https://incidentdatabase.ai/>`_ and `Google DeepMind <https://deepmind.google/>`_.

.. grid:: 1 1 2 2

   .. grid-item-card:: Phare
      :link: https://phare.giskard.ai/

      Phare is a multilingual benchmark to evaluate LLMs across key safety & security dimensions, including hallucination, factual accuracy, bias, and potential harm.

   .. grid-item-card:: Deeplearning.AI
      :link: https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/

      Our course on red teaming LLM applications on Deeplearning.AI helps you understand how to test, red team and evaluate LLM applications.

   .. grid-item-card:: RealHarm
      :link: https://realharm.giskard.ai/

      RealHarm is a dataset of problematic interactions with textual AI agents built from a systematic review of publicly reported incidents.

   .. grid-item-card:: RealPerformance
      :link: https://realperformance.giskard.ai/

      RealPerformance is a dataset of functional issues of language models, that mirrors failure patterns identified through rigorous testing in real LLM agents.

.. toctree::
   :caption: Getting Started
   :hidden:
   :maxdepth: 1

   self
   start/comparison
   start/free-enterprise-trial
   start/glossary

.. toctree::
   :caption: Enterprise UI
   :hidden:
   :maxdepth: 2

   hub/ui/index
   hub/ui/datasets/index
   hub/ui/annotate
   hub/ui/evaluations
   hub/ui/continuous-red-teaming
   hub/ui/access-rights

.. toctree::
   :caption: Enterprise SDK
   :hidden:
   :maxdepth: 4

   hub/sdk/index
   hub/sdk/projects
   hub/sdk/datasets/index
   hub/sdk/checks
   hub/sdk/evaluations
   hub/sdk/reference/index

.. toctree::
   :caption: Open Source SDK
   :hidden:
   :maxdepth: 2

   oss/sdk/index
   oss/sdk/security
   oss/sdk/business
   oss/sdk/outdated
   oss/notebooks/index
   oss/sdk/reference/index
