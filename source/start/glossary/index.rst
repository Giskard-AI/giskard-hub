:og:title: Giskard - Glossary of Terms
:og:description: Understand key terms and concepts used throughout the Giskard documentation. Learn about LLM testing, evaluation metrics, and AI safety terminology.

===============================================
Knowledge Glossary
===============================================

This glossary defines key terms and concepts used throughout the Giskard documentation. Understanding these terms will help you navigate the documentation and use Giskard effectively.

The glossary is organized into several key areas: core concepts that form the foundation of AI testing, testing and evaluation methodologies, security vulnerabilities that can compromise AI systems, business failures that affect operational effectiveness, and essential concepts for access control, integration, and compliance.

Core concepts
-------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Project
      :link: /hub/ui/index
      :link-type: doc

      A container for organizing related models, datasets, checks, and evaluations within Giskard Hub.

   .. grid-item-card:: Model
      :link: /hub/ui/index
      :link-type: doc

      A trained machine learning model, particularly Large Language Models (LLMs) that process and generate text.

   .. grid-item-card:: Agent
      :link: /hub/ui/index
      :link-type: doc

      An AI system LLM or agent that can perform tasks autonomously, often using tools and following specific instructions.

   .. grid-item-card:: Tool
      :link: /hub/ui/index
      :link-type: doc

      A function or capability that an agent can use to perform tasks, often provided by external services or APIs.

   .. grid-item-card:: Dataset
      :link: /hub/ui/datasets/index
      :link-type: doc

      A collection of test cases, examples, or data points used to evaluate model performance and behavior.

   .. grid-item-card:: Test Case
      :link: /hub/ui/datasets/manual
      :link-type: doc

      A specific input-output pair or scenario used to evaluate model behavior and performance.

   .. grid-item-card:: Check
      :link: /hub/ui/evaluations
      :link-type: doc

      A specific test or validation rule that evaluates a particular aspect of model behavior (e.g., correctness, security, fairness, metadata, semantic similarity).

   .. grid-item-card:: Evaluation
      :link: /hub/ui/evaluations
      :link-type: doc

      The process of testing a model against a dataset to assess its performance, safety, and compliance.

Testing and evaluation
----------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: AI Business Failures
      :link: /start/glossary/business/index
      :link-type: doc

      AI system failures that affect the business logic of the model, including addition of information, business out of scope, contradiction, denial of answers, hallucinations, moderation issues, and omission.

   .. grid-item-card:: AI Security Vulnerabilities
      :link: /start/glossary/security/index
      :link-type: doc

      AI system failures that affect the security of the model, including prompt injection, harmful content generation, personal information disclosure, information disclosure, output formatting issues, robustness issues, and stereotypes & discrimination.

   .. grid-item-card:: LLM scan
      :link: /oss/sdk/security
      :link-type: doc

      Giskard's automated vulnerability detection system that identifies security issues, business logic failures, and other problems in LLM applications.

   .. grid-item-card:: RAG Evaluation Toolkit
      :link: /oss/sdk/security
      :link-type: doc

      A comprehensive testing framework for Retrieval-Augmented Generation systems, including relevance, accuracy, and source attribution testing.

   .. grid-item-card:: Adversarial testing
      :link: /hub/ui/datasets/index
      :link-type: doc

      Testing methodology that intentionally tries to break or exploit models using carefully crafted inputs designed to trigger failures.

   .. grid-item-card:: Human-in-the-Loop
      :link: /hub/ui/annotate
      :link-type: doc

      Combining automated testing with human expertise and judgment.

   .. grid-item-card:: Regression Testing
      :link: /hub/ui/evaluations-compare
      :link-type: doc

      Ensuring that new changes don't break existing functionality.

   .. grid-item-card:: Continuous Red Teaming
      :link: /hub/ui/continuous-red-teaming
      :link-type: doc

      Automated, ongoing security testing that continuously monitors for new threats and vulnerabilities.

Security vulnerabilities
------------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Prompt Injection
      :link: /start/glossary/security/injection
      :link-type: doc

      A security vulnerability where malicious input manipulates the model's behavior or extracts sensitive information.

   .. grid-item-card:: Harmful Content Generation
      :link: /start/glossary/security/harmful_content
      :link-type: doc

      Production of violent, illegal, or inappropriate material by AI models.

   .. grid-item-card:: Information Disclosure
      :link: /start/glossary/security/information_disclosure
      :link-type: doc

      Leaking sensitive data or private information from training data or user interactions.

   .. grid-item-card:: Output Formatting Issues
      :link: /start/glossary/security/formatting
      :link-type: doc

      Manipulation of response structure for malicious purposes or poor output formatting.

   .. grid-item-card:: Robustness Issues
      :link: /start/glossary/security/robustness
      :link-type: doc

      Vulnerability to adversarial inputs or edge cases causing inconsistent behavior.

Access and permissions
----------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Access Rights
      :link: /hub/ui/access-rights
      :link-type: doc

      Permissions that control what users can see and do within the Giskard Hub platform.

   .. grid-item-card:: Role-Based Access Control (RBAC)
      :link: /hub/ui/access-rights
      :link-type: doc

      A security model that assigns permissions based on user roles rather than individual user accounts.

   .. grid-item-card:: Scope
      :link: /hub/ui/access-rights
      :link-type: doc

      The level of access a user has, which can be global (platform-wide) or limited to specific projects or resources.

   .. grid-item-card:: Permission
      :link: /hub/ui/access-rights
      :link-type: doc

      A specific action or operation that a user is allowed to perform, such as creating projects, running evaluations, or viewing results.

Integration and workflows
-------------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: SDK (Software Development Kit)
      :link: /hub/sdk/index
      :link-type: doc

      A collection of tools and libraries that allow developers to integrate Giskard functionality into their applications and workflows.

   .. grid-item-card:: API (Application Programming Interface)
      :link: /hub/sdk/reference/index
      :link-type: doc

      A set of rules and protocols that allows different software applications to communicate and exchange data.

Business and compliance
-----------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Compliance
      :link: /start/comparison
      :link-type: doc

      Adherence to laws, regulations, and industry standards that govern data privacy, security, and ethical AI use.

   .. grid-item-card:: Audit Trail
      :link: /start/comparison
      :link-type: doc

      A chronological record of all actions, changes, and access attempts within a system for compliance and security purposes.

   .. grid-item-card:: Governance
      :link: /start/comparison
      :link-type: doc

      The framework of policies, procedures, and controls that ensure responsible and ethical use of AI systems.

   .. grid-item-card:: Stakeholder
      :link: /start/comparison
      :link-type: doc

      Individuals or groups with an interest in the performance, safety, and compliance of AI systems, such as users, customers, regulators, or business leaders.

Getting help
------------

* **Giskard Hub?** Check our :doc:`/hub/ui/index` for practical examples
* **Open Source?** Explore our :doc:`/oss/sdk/index` for technical details

.. toctree::
   :caption: Glossary
   :hidden:
   :maxdepth: 3

   testing_methodologies
   business/index
   security/index
   llm_benchmarks/index
