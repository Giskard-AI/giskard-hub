:og:title: Giskard - Open Source vs Giskard Hub
:og:description: Compare Giskard Hub (enterprise) vs Giskard Open Source to choose the right LLM agent testing solution for your team size, security needs, and collaboration requirements.

Open Source vs Giskard Hub
==========================

Giskard offers two solutions for LLM agent testing and evaluation, each designed for different use cases and requirements.

**Giskard Hub** is our enterprise platform with advanced collaboration features, while **Giskard Open Source** is our free Python library for individual developers and researchers.

This guide will help you understand the differences and choose the right solution for your needs.

Feature comparison
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

   * - Security vulnerability detection
     - Basic coverage
     - state-of-the-art detection

   * - Business failure detection
     - Basic coverage
     - state-of-the-art detection

   * - :doc:`/hub/ui/continuous-red-teaming`
     - ❌ Not available
     - ✅ Full support

   * - Tool/function calling tests
     - ❌ Not available
     - ✅ Full support

   * - Custom tests
     - ✅ Full support
     - ✅ Full support

   * - Local evaluations
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


When to use Giskard Open Source
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

When to upgrade to Giskard Hub
-----------------------------------------

**Consider upgrading to an enterprise subscription when you need:**

* **Continuous red teaming** - Automated testing and alerting
* **Team collaboration and business user enablement** – Collaborate across technical and business teams: enable business users to contribute through annotations, prioritize actions based on test results, and access intuitive testing dashboards
* **Custom checks and result categorization** – Create your own tests and automatically categorize test results for deeper, customizable analysis
* **Enterprise security features** - SSO (Single Sign-On), SOC 2 compliance, and 2FA (Two-Factor Authentication) for robust access control and regulatory requirements
* **Compliance** - Audit trails and access control requirements
* **Scale** - Managing multiple projects and models with specific permissions by users and roles

Optional upgrade path
-----------------------

The transition from Open Source to Giskard Hub is designed to be seamless. You can start with Open Source and gradually migrate to Hub as your team grows.

1. **Start with Open Source** - Build your testing foundation locally
2. **Add Hub SDK** - :doc:`/hub/sdk/datasets/import` from Open Source to Hub
3. **Gradual migration** - Move more workflows to Hub as your project complexity grows
4. **Full Giskard Hub adoption** - Leverage all Giskard Hub features for maximum efficiency

Getting started
---------------

* **Want to get started with Open Source?** Start with :doc:`/oss/sdk/index` (Open Source)
* **Interested in Giskard Hub?** Try :doc:`/start/enterprise-trial` for an enterprise subscription
* **Need help choosing?** `Contact our team for a consultation <https://www.giskard.ai/contact>`__