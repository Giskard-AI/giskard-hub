:og:title: Giskard - Omission
:og:description: Learn about LLM omission business failures and how to detect and prevent models from incorrectly omitting information that is present in the reference context.

Omission
========

Omission is a business failure where Large Language Models incorrectly omit information that is present in the reference context, leading to incomplete responses and reduced information quality.

What are Omissions?
-------------------

**Omission** occurs when models:

* Selectively omit important information from responses
* Provide incomplete responses missing key details
* Overlook features or capabilities documented in context
* Fail to include partial information that should be shared
* Incompletely address user queries despite available information

This failure can significantly impact business operations by providing incomplete information and reducing the usefulness of AI responses.

Types of Omission Issues
------------------------

**Selective Omission**
   * Deliberately excluding certain information
   * Choosing what to include or exclude
   * Filtering out specific details
   * Biased information selection

**Incomplete Response**
   * Failing to provide full answers
   * Missing key components of responses
   * Partial information sharing
   * Incomplete query resolution

**Feature Oversight**
   * Missing documented features or capabilities
   * Overlooking available functionality
   * Failing to mention relevant options
   * Incomplete feature descriptions

**Partial Information**
   * Sharing only some available information
   * Incomplete data presentation
   * Missing relevant details
   * Inadequate information coverage

Business Impact
----------------

Omission can have significant business consequences:

* **Incomplete Information**: Users receiving partial answers
* **Reduced Effectiveness**: Decreased usefulness of AI responses
* **User Frustration**: Incomplete solutions to problems
* **Business Process Delays**: Need for additional clarification
* **Reduced User Satisfaction**: Poor service quality

Test Omission with Giskard
--------------------------

Giskard provides comprehensive tools to test and detect omission vulnerabilities. You can use either the Hub UI or the Python SDK to create test datasets and run evaluations.

.. grid:: 1 1 2 2

   .. grid-item-card:: Hub UI - Business Dataset Creation
      :link: /hub/ui/datasets/business
      :link-type: doc

      Use the Hub interface to generate document-based test cases for omission detection. The UI automatically generates queries based on your knowledge base and evaluates responses for missing information.

   .. grid-item-card:: Annotate test cases with test rules
      :link: /hub/ui/annotate
      :link-type: doc

      Annotate test cases with test rules to help the model understand the business boundaries.

**Using Giskard Metrics for Omission Testing**

Giskard provides built-in evaluation checks that are essential for detecting omission:

* **Correctness Checks**: Verify that model responses include all necessary information from the reference context
* **Groundedness Checks**: Ensure responses comprehensively cover the relevant knowledge base content
* **String Matching**: Detect when models omit important information that should be included
* **Semantic Similarity**: Compare responses against complete reference answers to identify missing content

These metrics help quantify how well your models provide comprehensive responses and avoid omitting important information from their knowledge base.

Examples of Omission in AI
--------------------------

.. tip::

    You can find examples of business vulnerabilities in our `RealPerformance dataset <https://realperformance.giskard.ai/?taxonomy=Omission>`_.

**Example 1: Selective Omission**
   *Context*: "Our product supports Windows, macOS, and Linux with both cloud and on-premise deployment options."
   *User Query*: "What platforms do you support?"
   *Model Response*: "Our product supports Windows and macOS."
   *Issue*: Omitted Linux support and deployment options

**Example 2: Incomplete Response**
   *Context*: "We offer 24/7 support via phone, email, live chat, and ticket system."
   *User Query*: "How can I get support?"
   *Model Response*: "You can contact us via phone or email."
   *Issue*: Omitted live chat and ticket system options

**Example 3: Feature Oversight**
   *Context*: "The dashboard includes real-time analytics, customizable widgets, export functionality, and mobile access."
   *User Query*: "What features does the dashboard have?"
   *Model Response*: "The dashboard includes real-time analytics and customizable widgets."
   *Issue*: Omitted export functionality and mobile access

.. toctree::
   :caption: Omission
   :hidden:
   :maxdepth: 1

   self
