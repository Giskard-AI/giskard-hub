Open Source vs Giskard Hub
==========================

This guide helps you understand the differences between Giskard Open Source and Giskard Hub, and when to consider upgrading to an enterprise subscription.

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

   * - Detect security vulnerabilities
     - Basic
     - Advanced

   * - Detect business failures
     - Basic
     - Advanced

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

   * - Continuous red teaming
     - ❌ Manual runs only
     - ✅ Automated

   * - Alerting
     - ❌ Not available
     - ✅ Configurable alerts

   * - Performance tracking
     - ❌ Local only
     - ✅ Historical data

   * - Audit trails
     - ❌ Not available
     - ✅ Full compliance

   * - **Advanced Security**
     -
     -

   * - Continuous red teaming
     - ❌ Manual only
     - ✅ Automated

   * - Threat detection
     - ❌ Basic scanning
     - ✅ Advanced detection

   * - Vulnerability management
     - ❌ Local tracking
     - ✅ Centralized

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
* **Custom checks and result categorization** – Create your own tests and automatically categorize test results for deeper, customizable analysis
* **Team collaboration and business user enablement** – Collaborate across technical and business teams: enable business users to contribute through annotations, prioritize actions based on test results, and access intuitive testing dashboards
* **Scale** - Managing multiple projects and models with specific permissions by users and roles
* **Compliance** - Audit trails and access control requirements
* **Scale** - Managing multiple projects and models with specific permissions by users and roles

**Key benefits:**

* **Stronger coverage with less effort** - Advanced adversarial dataset generation and comparison
* **Team access control and automated security testing** - Manage user permissions and enable continuous red teaming to proactively identify risks
* **Greater customization for developers** - Create custom datasets and advanced tests with the Hub SDK

Upgrade Path
------------

The transition from Open Source to Giskard Hub is designed to be seamless. You can start with Open Source and gradually migrate to Hub as your team grows.

1. **Start with Open Source** - Build your testing foundation locally
2. **Add Hub SDK** - :doc:`/hub/sdk/datasets/import` from Open Source to Hub
3. **Gradual migration** - Move more workflows to Hub as your team grows
4. **Full GiskardHub adoption** - Leverage all Giskard Hub features for maximum efficiency

Getting Started
---------------

* **Want to get started with Open Source?** Start with :doc:`/oss/sdk/index` (Open Source)
* **Interested in Giskard Hub?** Try :doc:`/start/enterprise-trial` for an enterprise subscription
* **Need help choosing?** `Contact our team for a consultation <https://www.giskard.ai/contact>`__