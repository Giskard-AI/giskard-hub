Open Source vs Enterprise
=========================

This guide helps you understand the differences between Giskard Open Source and Giskard Enterprise Hub, and when to consider upgrading.

Feature Comparison
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 30

   * - **Feature**
     - **Giskard Open Source**
     - **Giskard Enterprise Hub**

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

   * - **Operational Features**
     -
     -

   * - Continuous monitoring
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

   * - Vulnerability mgmt
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

When to Upgrade to Giskard Enterprise Hub
----------------------------------------

**Consider upgrading when you need:**

* **Advanced testing** - Advanced testing capabilities
* **Team collaboration** - Multiple people working on testing
* **Compliance** - Audit trails and access control requirements
* **Scale** - Managing multiple projects and models
* **Continuous monitoring** - Automated testing and alerting
* **Enterprise security** - Advanced threat detection and response

**Key benefits:**

* **Stronger coverage with less effort** - Automated adversarial dataset generation and comparison
* **Operational guardrails** - Access rights for teams and continuous red teaming
* **Keep developers happy** - Continue using local testing while syncing to Hub via SDK

Upgrade Path
------------

The transition from Open Source to Enterprise Hub is designed to be seamless. You can start with Open Source and gradually migrate to Hub as your team grows.

1. **Start with Open Source** - Build your testing foundation locally
2. **Add Hub SDK** - :doc:`/hub/sdk/datasets/import` from Open Source to Hub
3. **Gradual migration** - Move more workflows to Hub as your team grows
4. **Full Hub adoption** - Leverage all enterprise features for maximum efficiency

**No code changes required** - Your existing tests and evaluations can be migrated between both environments.

Getting Started
--------------

* **Want to get started with Open Source?** Start with :doc:`/oss/sdk/index` (Open Source)
* **Interested in the Enterprise Hub?** Try :doc:`/start/free-enterprise-trial` (Enterprise Hub)
* **Need help choosing?** `Contact our team for a consultation <https://www.giskard.ai/contact>`__

Next Steps
----------

* Learn about :doc:`/hub/ui/continuous-red-teaming` for ongoing security
* Check out our :doc:`/start/glossary` for key terms and concepts
