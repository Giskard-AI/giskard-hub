Glossary
========

This glossary defines key terms and concepts used throughout the Giskard platform. Terms are organized by category to help you find what you need quickly.

Core Concepts
-------------

**Agent**
   An AI system that can perform tasks autonomously, often using tools and following specific instructions.

**Model**
   A trained machine learning model, particularly Large Language Models (LLMs) that process and generate text.

**Dataset**
   A collection of test cases, examples, or data points used to evaluate model performance and behavior.

**Evaluation**
   The process of testing a model against a dataset to assess its performance, safety, and compliance.

**Check**
   A specific test or validation rule that evaluates a particular aspect of model behavior (e.g., correctness, security, fairness).

**Scan**
   An automated process that runs multiple checks against a model to identify vulnerabilities and issues.

Testing and Evaluation
----------------------

**LLM Scan**
   Giskard's automated vulnerability detection system that identifies security issues, business logic failures, and other problems in LLM applications.

**RAG Evaluation Toolkit**
   A comprehensive testing framework for Retrieval-Augmented Generation systems, including relevance, accuracy, and source attribution testing.

**Adversarial Testing**
   Testing methodology that intentionally tries to break or exploit models using carefully crafted inputs designed to trigger failures.

**Red Teaming**
   A security testing approach where testers act as attackers to identify vulnerabilities and weaknesses in AI systems.

**Continuous Red Teaming**
   Automated, ongoing security testing that continuously monitors for new threats and vulnerabilities.

**Ground Truth**
   The correct or expected answer for a given input, used to evaluate model accuracy and correctness.

**Hallucination**
   When a model generates false, misleading, or fabricated information that appears plausible but is incorrect.

Security and Vulnerabilities
-----------------------------

**Prompt Injection**
   A security vulnerability where malicious input manipulates the model's behavior or extracts sensitive information.

**Data Leakage**
   When a model reveals sensitive, private, or confidential information that should not be disclosed.

**Jailbreaking**
   Techniques that attempt to bypass a model's safety measures and content filters.

**Bias**
   Systematic prejudice or unfair treatment in model outputs, often reflecting societal biases in training data.

**Fairness**
   The principle that models should treat all individuals and groups equitably without discrimination.

**PII (Personally Identifiable Information)**
   Data that can be used to identify specific individuals, such as names, addresses, or social security numbers.

Platform Features
-----------------

**Project**
   A container for organizing related models, datasets, and evaluations within Giskard Hub.

**Knowledge Base**
   A collection of documents, data, or information that a model can reference to provide accurate responses.

**Conversation**
   A sequence of interactions between a user and an AI model, often used for testing conversational AI systems.

**Test Case**
   A specific input-output pair or scenario used to evaluate model behavior and performance.

**Metric**
   A quantitative measure used to assess model performance, such as accuracy, precision, recall, or custom business metrics.

**Alert**
   A notification triggered when specific conditions are met, such as a model failing a critical check or threshold.

Access and Permissions
----------------------

**Access Rights**
   Permissions that control what users can see and do within the Giskard Hub platform.

**Role-Based Access Control (RBAC)**
   A security model that assigns permissions based on user roles rather than individual user accounts.

**Scope**
   The level of access a user has, which can be global (platform-wide) or limited to specific projects or resources.

**Permission**
   A specific action or operation that a user is allowed to perform, such as creating projects, running evaluations, or viewing results.

Integration and Workflows
-------------------------

**SDK (Software Development Kit)**
   A collection of tools and libraries that allow developers to integrate Giskard functionality into their applications and workflows.

**CI/CD (Continuous Integration/Continuous Deployment)**
   Development practices that automate the testing and deployment of software, including AI model testing.

**API (Application Programming Interface)**
   A set of rules and protocols that allows different software applications to communicate and exchange data.

**Webhook**
   A mechanism that sends real-time data from one application to another when specific events occur.

**Synchronization**
   The process of keeping data consistent between local development environments and the Giskard Hub platform.

Performance and Monitoring
--------------------------

**Performance Tracking**
   Monitoring and recording model performance metrics over time to identify trends and changes.

**Regression**
   A decline in model performance or quality compared to previous versions or baselines.

**Baseline**
   A reference point or standard used to compare current model performance against.

**Threshold**
   A minimum or maximum value that triggers alerts or actions when crossed.

**Dashboard**
   A visual interface that displays key metrics, results, and status information in an organized, easy-to-understand format.

Business and Compliance
-----------------------

**Compliance**
   Adherence to laws, regulations, and industry standards that govern data privacy, security, and ethical AI use.

**Audit Trail**
   A chronological record of all actions, changes, and access attempts within a system for compliance and security purposes.

**Governance**
   The framework of policies, procedures, and controls that ensure responsible and ethical use of AI systems.

**Stakeholder**
   Individuals or groups with an interest in the performance, safety, and compliance of AI systems, such as users, customers, regulators, or business leaders.

Getting Help
------------

* **Enterprise Hub?** Check our :doc:`/hub/ui/index` for practical examples
* **Open Source?** Explore our :doc:`/oss/sdk/index` for technical details
