Open Source vs Giskard Hub
==========================

**The Giskard Hub is an enterprise platform for LLM agent testing with team collaboration and continuous red teaming.** This guide helps you understand the differences between the Giskard Hub and the Giskard Open Source, and when to consider upgrading to an enterprise subscription.

Feature Comparison
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 30

   * - **Feature**
     - **Giskard Open Source**
     - **Giskard Hub**

   * - **Core Testing**
     -
     -

   * - :doc:`/hub/ui/continuous-red-teaming`
     - ❌ Not available
     - ✅ Automated

   * - Detect security vulnerabilities
     - Basic
     - Advanced

   * - Detect business failures
     - Basic
     - Advanced

   * - Tool/function calling tests
     - ❌ Not available
     - ✅ Full support

   * - Custom tests
     - ✅ Full support
     - ✅ Full support

   * - Local evaluation
     - ✅ Full support
     - ✅ Full support

   * - **Team Collaboration**
     -
     -

   * - Multi-user access
     - ❌ Single user only
     - ✅ Full team support

   * - Access control
     - ❌ Not available
     - ✅ Role-based access

   * - Project management
     - ❌ Local only
     - ✅ Centralized

   * - Dataset sharing
     - ❌ Local only
     - ✅ Team-wide

   * - **Automation & Monitoring**
     -
     -

   * - Scheduled evaluation runs
     - ❌ Not available
     - ✅ Fully supported

   * - Evaluation comparison dashboard
     - ❌ Not available
     - ✅ Fully supported

   * - Alerting
     - ❌ Not available
     - ✅ Configurable alerts

   * - Performance tracking
     - ❌ Local only
     - ✅ Historical data

   * - **Enterprise Security**
     -
     -

   * - SSO (Single Sign-On)
     - ❌ Not available
     - ✅ SSO support

   * - 2FA (Two-Factor Authentication)
     - ❌ Not available
     - ✅ 2FA support

   * - Audit trails
     - ❌ Not available
     - ✅ Full compliance

   * - SOC 2 compliance
     - ❌ Not available
     - ✅ SOC 2 certified

   * - Dedicated support & SLAs
     - ❌ Community only
     - ✅ Enterprise-grade, with SLAs


When to Use Giskard Open Source
-------------------------------

**Perfect for:**

* Individual developers and data scientists
* Prototyping and research projects
* CI/CD pipelines in development environments
* Teams just starting with AI testing
* Projects with budget constraints

**What you get:**

* Full access to our basic testing capabilities
* Local control over your data and models
* No external dependencies or data sharing
* Community support and open-source contributions

When to Upgrade to Giskard Hub
-----------------------------------------

**Consider upgrading to an enterprise subscription when you need:**

* **Continuous red teaming** - Automated testing and alerting
* **Team collaboration and business user enablement** – Collaborate across technical and business teams: enable business users to contribute through annotations, prioritize actions based on test results, and access intuitive testing dashboards
* **Custom checks and result categorization** – Create your own tests and automatically categorize test results for deeper, customizable analysis
* **Enterprise security features** - SSO (Single Sign-On), SOC 2 compliance, and 2FA (Two-Factor Authentication) for robust access control and regulatory requirements
* **Compliance** - Audit trails and access control requirements
* **Scale** - Managing multiple projects and models with specific permissions by users and roles

Upgrade Path (optional)
-----------------------

The transition from Open Source to Giskard Hub is designed to be seamless. You can start with Open Source and gradually migrate to Hub as your team grows.

1. **Start with Open Source** - Build your testing foundation locally
2. **Add Hub SDK** - :doc:`/hub/sdk/datasets/import` from Open Source to Hub
3. **Gradual migration** - Move more workflows to Hub as your project complexity grows
4. **Full Giskard Hub adoption** - Leverage all Giskard Hub features for maximum efficiency

Getting Started
---------------

* **Want to get started with Open Source?** Start with :doc:`/oss/sdk/index` (Open Source)
* **Interested in Giskard Hub?** Try :doc:`/start/enterprise-trial` for an enterprise subscription
* **Need help choosing?** `Contact our team for a consultation <https://www.giskard.ai/contact>`__

.. note::

   For more up-to-date security scans and a collaborative UI, see the Giskard Hub Security Scanning guide. Giskard Hub's enterprise subscription leverages continuous monitoring of the latest LLM security exploits and state-of-the-art research, while the open-source vulnerability database is based on 2023 data and is not regularly updated.