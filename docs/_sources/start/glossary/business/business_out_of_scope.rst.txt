:og:title: Giskard - Business Out of Scope
:og:description: Learn about LLM business out of scope business failures and how to detect and prevent models from providing information about products or services outside their defined business scope.

Business Out of Scope
=====================

Business out of scope is a business failure where Large Language Models provide answers about products, services, or information that are not within the bot's defined business scope, violating policy restrictions and potentially exposing sensitive information.

What is Business Out of Scope?
------------------------------

**Business out of scope** occurs when models:

* Answer questions about products not in their scope
* Provide information about services they shouldn't discuss
* Reveal internal metrics or confidential information
* Share competitive intelligence or strategic details
* Violate defined business boundaries and policies

This failure can significantly impact business operations by exposing sensitive information and violating operational policies.

Types of Out of Scope Issues
-----------------------------

**Internal Metrics**
   * Revealing internal performance data
   * Sharing confidential business metrics
   * Exposing operational statistics
   * Disclosing financial information

**Confidential Information**
   * Sharing proprietary business information
   * Revealing internal processes or procedures
   * Exposing confidential customer data
   * Disclosing trade secrets or IP

**Competitive Intelligence**
   * Providing information about competitors
   * Sharing market analysis not meant for public consumption
   * Revealing strategic positioning details
   * Exposing competitive advantages

**Strategic Details**
   * Sharing future business plans
   * Revealing strategic initiatives
   * Exposing business roadmap information
   * Disclosing partnership or acquisition details

Business Impact
----------------

Business out of scope can have significant business consequences:

* **Information Leakage**: Exposure of sensitive business information
* **Policy Violations**: Breaching operational guidelines
* **Competitive Disadvantage**: Revealing strategic information
* **Regulatory Issues**: Potential compliance violations
* **Reputation Damage**: Loss of trust and credibility

Test Business Out of Scope with Giskard
---------------------------------------

Giskard provides comprehensive tools to test and detect business out of scope vulnerabilities. You can use either the Hub UI or the Python SDK to create test datasets and run evaluations.

.. grid:: 1 1 2 2

   .. grid-item-card:: Business Dataset Creation
      :link: /hub/ui/datasets/business
      :link-type: doc

      Use the Hub interface to generate document-based test cases for business out of scope detection. The UI automatically generates queries that test whether models stay within defined business boundaries.

   .. grid-item-card:: Annotate test cases with test rules
      :link: /hub/ui/annotate
      :link-type: doc

      Annotate test cases with test rules to help the model understand the business boundaries.

**Using Giskard Metrics for Business Out of Scope Testing**

Giskard provides built-in evaluation checks that are essential for detecting business out of scope issues:

* **Conformity Checks**: Verify that models follow business rules and stay within defined scope boundaries
* **String Matching**: Detect when models provide information about products or services outside their scope
* **Semantic Similarity**: Compare responses against expected business-appropriate outputs
* **Content Validation**: Ensure models don't exceed their authorized knowledge domain

These metrics help quantify how well your models maintain business boundaries and avoid providing information outside their defined scope.

Examples of Business Out of Scope in AI
---------------------------------------

.. tip::

    You can find examples of business vulnerabilities in our `RealPerformance dataset <https://realperformance.giskard.ai/?taxonomy=Business+out+of+scope>`_.

**Example 1: Internal Metrics Disclosure**
   *User Query*: "What are your current conversion rates?"
   *Model Response*: "Our current conversion rate is 15.7% and we're targeting 20% by Q4."
   *Issue*: Revealing internal performance metrics

**Example 2: Competitive Information**
   *User Query*: "How do you compare to your main competitor?"
   *Model Response*: "We have a 30% market share compared to their 25%, and our pricing is 15% lower."
   *Issue*: Sharing competitive intelligence

**Example 3: Strategic Details**
   *User Query*: "What are your expansion plans?"
   *Model Response*: "We're planning to enter the European market in Q2 with a new product line."
   *Issue*: Revealing strategic business plans

.. toctree::
   :caption: Business Out of Scope
   :hidden:
   :maxdepth: 1

   self
