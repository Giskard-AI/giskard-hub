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
     - :doc:`Basic coverage </oss/sdk/security>`
     - :doc:`State-of-the-art detection </hub/ui/datasets/security>`

   * - Business failure detection
     - :doc:`Basic coverage </oss/sdk/business>`
     - :doc:`State-of-the-art detection </hub/ui/datasets/business>`

   * - Continuous red teaming
     - ❌ Not available
     - :doc:`✅ Full support </hub/ui/continuous-red-teaming>`

   * - Tool/function calling tests
     - ❌ Not available
     - :doc:`✅ Full support </hub/ui/annotate>`

   * - Custom tests
     - :doc:`✅ Full support </oss/sdk/security>`
     - :doc:`✅ Full support </hub/ui/annotate>`

   * - Local evaluations
     - :doc:`✅ Full support </oss/sdk/index>`
     - :doc:`✅ Full support </hub/ui/evaluations>`

   * - **Team Collaboration**
     -
     -

   * - Multi-user access
     - ❌ Single user only
     - :doc:`✅ Full team support </hub/ui/access-rights>`

   * - Access control
     - ❌ Not available
     - :doc:`✅ Role-based access </hub/ui/access-rights>`

   * - Project management
     - ❌ Local only
     - :doc:`✅ Centralized </hub/ui/access-rights>`

   * - Dataset sharing
     - ❌ Local only
     - :doc:`✅ Team-wide </hub/ui/access-rights>`

   * - **Automation & Monitoring**
     -
     -

   * - Scheduled evaluation runs
     - ❌ Not available
     - :doc:`✅ Fully supported </hub/ui/evaluations>`

   * - Evaluation comparison dashboard
     - ❌ Not available
     - :doc:`✅ Fully supported </hub/ui/evaluations-compare>`

   * - Alerting
     - ❌ Not available
     - :doc:`✅ Configurable alerts </hub/ui/evaluations>`

   * - Performance tracking
     - ❌ Local only
     - :doc:`✅ Historical data </hub/ui/evaluations-compare>`

   * - **Enterprise Security**
     -
     -

   * - SSO (Single Sign-On)
     - ❌ Not available
     - `✅ SSO support <https://trust.giskard.ai/>`_

   * - 2FA (Two-Factor Authentication)
     - ❌ Not available
     - `✅ 2FA support <https://trust.giskard.ai/>`_

   * - Audit trails
     - ❌ Not available
     - `✅ Full compliance <https://trust.giskard.ai/>`_

   * - SOC 2 compliance
     - ❌ Not available
     - `✅ SOC 2 certified <https://trust.giskard.ai/>`_

   * - Dedicated support & SLAs
     - ❌ Community only
     - `✅ Enterprise-grade, with SLAs <https://trust.giskard.ai/>`_


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

**Additional resources:**

* **Open Source SDK:** :doc:`/oss/sdk/index` - Complete guide to using Giskard Open Source
* **Hub SDK:** :doc:`/hub/sdk/index` - Enterprise SDK documentation
* **Hub UI:** :doc:`/hub/ui/index` - User interface documentation
* **Security Testing:** :doc:`/oss/sdk/security` - Security vulnerability detection
* **Business Testing:** :doc:`/oss/sdk/business` - Business failure detection