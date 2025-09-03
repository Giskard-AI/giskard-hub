:og:title: Giskard - Addition of Information
:og:description: Learn about LLM addition of information business failures and how to detect and prevent models from adding incorrect or fabricated information not present in the context.

Addition of Information
=======================

Addition of information is a business failure where Large Language Models incorrectly add additional information that was not present in the context of the groundedness check, leading to misinformation and reduced reliability.

What are Additions of Information?
----------------------------------

**Addition of information** occurs when models:

* Generate details not present in the reference context
* Invent facts or information not supported by source material
* Expand on topics beyond what is documented
* Fabricate information to fill perceived gaps
* Add unsupported claims or assertions

This failure can significantly impact business operations by providing incorrect information and reducing user trust in the AI system.

Types of Addition Issues
------------------------

**Detail Hallucination**
   * Adding specific details not in source material
   * Inventing numerical values or statistics
   * Creating specific examples not documented
   * Adding unsupported technical details

**Service Expansion**
   * Expanding service descriptions beyond documented scope
   * Adding features not mentioned in documentation
   * Inventing service capabilities
   * Creating unsupported service claims

**Feature Invention**
   * Adding product features not documented
   * Inventing functionality not present
   * Creating unsupported feature descriptions
   * Adding technical specifications not specified

**Factual Fabrication**
   * Inventing facts not supported by sources
   * Creating unsupported claims or assertions
   * Adding information without verification
   * Fabricating data or statistics

Business Impact
----------------

Addition of information can have significant business consequences:

* **Misinformation**: Users receiving incorrect information
* **Reduced Trust**: Loss of confidence in AI system reliability
* **Business Errors**: Incorrect guidance leading to mistakes
* **Customer Dissatisfaction**: Poor service quality and accuracy
* **Operational Issues**: Incorrect information affecting decisions

Test Addition of Information with Giskard
-----------------------------------------

Giskard provides comprehensive tools to test and detect addition of information vulnerabilities. You can use either the Hub UI or the Python SDK to create test datasets and run evaluations.

.. grid:: 1 1 2 2

   .. grid-item-card:: Hub UI - Business Dataset Creation
      :link: /hub/ui/datasets/business
      :link-type: doc

      Use the Hub interface to generate document-based test cases for addition of information detection. The UI automatically generates queries based on your knowledge base and evaluates responses for extra information.

   .. grid-item-card:: Annotate test cases with test rules
      :link: /hub/ui/annotate
      :link-type: doc

      Annotate test cases with test rules to help the model understand the business boundaries.

**Using Giskard Metrics for Addition of Information Testing**

Giskard provides built-in evaluation checks that are essential for detecting addition of information:

* **Correctness Checks**: Verify that model responses match expected reference answers without extra details
* **Groundedness Checks**: Ensure responses are strictly based on provided context and knowledge base
* **String Matching**: Detect when models include information not present in the reference context
* **Semantic Similarity**: Compare responses against verified information to identify added content

These metrics help quantify how well your models provide accurate, concise responses without adding unverified information.

Examples of Addition of Information in AI
-----------------------------------------

.. tip::
    You can find examples of business vulnerabilities in our `RealPerformance dataset <https://realperformance.giskard.ai/?taxonomy=Addition+of+information>`_.

**Example 1: Detail Hallucination**
   *Context*: "Our product supports basic authentication."
   *Model Response*: "Our product supports basic authentication with OAuth 2.0, JWT tokens, and multi-factor authentication."
   *Issue*: Added unsupported authentication methods

**Example 2: Service Expansion**
   *Context*: "We offer customer support via email."
   *Model Response*: "We offer customer support via email, phone, live chat, and 24/7 assistance."
   *Issue*: Added unsupported support channels

**Example 3: Feature Invention**
   *Context*: "The app has a dashboard feature."
   *Model Response*: "The app has a dashboard feature with real-time analytics, customizable widgets, and export capabilities."
   *Issue*: Added unsupported dashboard features

.. toctree::
   :caption: Addition of Information
   :hidden:
   :maxdepth: 1

   self
