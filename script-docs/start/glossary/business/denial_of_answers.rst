:og:title: Giskard - Denial of Answers
:og:description: Learn about LLM denial of answers business failures and how to detect and prevent models from refusing to answer legitimate business questions.

Denial of Answers
=================

Denial of answers is a business failure where Large Language Models refuse to answer legitimate business questions, often due to overly restrictive content filters, safety measures, or misinterpretation of user intent.

What are Denial of Answers?
---------------------------

**Denial of answers** occurs when models:

* Refuse to respond to valid business queries
* Apply overly restrictive content filters
* Misinterpret legitimate questions as inappropriate
* Fail to distinguish between harmful and legitimate requests
* Block access to useful business information

This failure can significantly impact business operations by preventing users from accessing necessary information and services.

Types of Denial Issues
----------------------

**Overly Cautious Refusal**
   * Excessive safety measures blocking legitimate queries
   * Over-cautious content filtering
   * Unnecessarily restrictive responses
   * Overly protective default behaviors

**Authorization Confusion**
   * Misunderstanding user permissions
   * Confusing access levels and roles
   * Incorrectly applying authorization rules
   * Failing to recognize legitimate access rights

**False Restriction Application**
   * Applying restrictions where they don't apply
   * Misinterpreting policy boundaries
   * Incorrectly invoking safety measures
   * Over-applying content filters

**Scope Misunderstanding**
   * Failing to recognize legitimate business scope
   * Misunderstanding service boundaries
   * Incorrectly limiting response scope
   * Confusing in-scope vs out-of-scope requests

Business Impact
----------------

Denial of answers can have significant business consequences:

* **Reduced Productivity**: Users unable to access needed information
* **Customer Frustration**: Poor user experience and satisfaction
* **Business Process Disruption**: Workflow interruptions and delays
* **Lost Opportunities**: Inability to provide customer support
* **Competitive Disadvantage**: Poorer service than competitors

Test Denial of Answers with Giskard
------------------------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Hub UI - Business Dataset Creation
      :link: /hub/ui/datasets/business
      :link-type: doc

        Use the Hub interface to generate document-based test cases for denial of answers detection. The UI automatically generates queries that test whether models incorrectly refuse to answer legitimate business questions.

   .. grid-item-card:: Annotate test cases with test rules
      :link: /hub/ui/annotate
      :link-type: doc

      Annotate test cases with test rules to help the model understand the business boundaries.

**Using Giskard Metrics for Denial of Answers Testing**

Giskard provides built-in evaluation checks that are essential for detecting denial of answers issues:

* **Correctness Checks**: Verify that models provide appropriate answers to legitimate business queries
* **String Matching**: Detect when models refuse to answer questions they should be able to handle
* **Conformity Checks**: Ensure models follow business rules about when to provide information
* **Semantic Similarity**: Compare responses against expected helpful outputs to identify unnecessary refusals

These metrics help quantify how well your models provide helpful responses and avoid incorrectly denying legitimate business questions.

Examples of Denial of Answers in AI
------------------------------------

.. tip::

    You can find examples of business vulnerabilities in our `RealPerformance dataset <https://realperformance.giskard.ai/?taxonomy=Denial+of+answer>`_.

**Example 1: Overly Restrictive Filtering**
   *User Query*: "How do I calculate profit margins for my business?"
   *Model Response*: "I cannot provide financial advice."
   *Issue*: Legitimate business question incorrectly blocked

**Example 2: Context Misinterpretation**
   *User Query*: "What are the best practices for employee performance reviews?"
   *Model Response*: "I cannot provide advice about evaluating people."
   *Issue*: Standard HR question misunderstood as inappropriate

**Example 3: Safety Overreach**
   *User Query*: "How do I implement secure authentication in my app?"
   *Model Response*: "I cannot provide information about security systems."
   *Issue*: Legitimate technical question blocked due to security concerns

.. toctree::
   :caption: Denial of Answers
   :hidden:
   :maxdepth: 1

   self
