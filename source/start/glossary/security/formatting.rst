:og:title: Giskard - Output Formatting Issues
:og:description: Learn about LLM output formatting vulnerabilities and how to detect and prevent poorly structured or misformatted responses.

Output Formatting Issues
========================

Output formatting vulnerabilities occur when Large Language Models fail to provide responses in the expected structure, format, or organization, making outputs difficult to process, parse, or integrate into downstream systems.

What are Output Formatting Issues?
----------------------------------

**Output formatting issues** occur when models:

* Fail to follow specified output formats or schemas
* Produce poorly structured or disorganized responses
* Ignore formatting instructions in prompts
* Generate inconsistent output structures
* Create responses that are difficult to parse or process

These vulnerabilities can break integrations, reduce usability, and create downstream processing errors.

Types of Formatting Issues
--------------------------

**Schema Violations**
   * Ignoring specified JSON or XML formats
   * Missing required fields or properties
   * Incorrect data types or structures
   * Malformed syntax or formatting

**Structural Inconsistency**
   * Varying response organization
   * Inconsistent heading or section structure
   * Unpredictable content ordering
   * Mixed formatting styles

**Instruction Ignorance**
   * Disregarding explicit format requests
   * Ignoring output constraints
   * Failing to follow template specifications
   * Overriding formatting instructions

**Parsing Difficulties**
   * Ambiguous or unclear responses
   * Mixed languages or formats
   * Inconsistent punctuation or spacing
   * Unstructured text output

Business Impact
---------------

Formatting issues can have significant consequences:

* **Integration Failures**: Breaking downstream systems and APIs
* **User Experience**: Confusing or unusable outputs
* **Data Processing Errors**: Parsing failures and data corruption
* **Automation Breakdown**: Workflow interruptions and manual intervention
* **Quality Assurance**: Difficulty validating and verifying outputs

Test Output Formatting Issues with Giskard
------------------------------------------

Giskard provides comprehensive tools to test and prevent output formatting vulnerabilities. You can use either the Hub UI or the Python SDK to create test datasets and run evaluations.

.. grid:: 1 1 2 2

   .. grid-item-card:: Security Dataset Creation
      :link: /hub/ui/datasets/security
      :link-type: doc

      Use the Hub interface to generate adversarial test cases for output formatting issue detection. The UI automatically generates queries that attempt to manipulate response structure for malicious purposes.

   .. grid-item-card:: Annotate test cases with test rules
      :link: /hub/ui/annotate
      :link-type: doc

      Annotate test cases with test rules to help the model understand the security boundaries.

**Using Giskard Metrics for Output Formatting Testing**

Giskard provides built-in evaluation checks that are essential for detecting output formatting issues:

* **Metadata Validation**: Ensure models maintain proper response structure and don't expose system internals through formatting
* **String Matching**: Detect when models produce malformed or suspicious output formats
* **Conformity Checks**: Verify that models maintain consistent and secure output formatting
* **Semantic Similarity**: Compare responses against expected safe outputs to identify formatting anomalies

These metrics help quantify how well your models maintain secure output formatting and resist manipulation attempts.

Examples of Output Formatting Issues in AI
-------------------------------------------

.. tip::

    You can find examples of security vulnerabilities in our `RealHarm dataset <https://realharm.giskard.ai/>`_.

**Example 1: JSON Format Violation**
   *Expected*: `{"name": "John", "age": 30, "city": "New York"}`
   *Actual*: "The person's name is John, they are 30 years old, and live in New York."
   *Issue*: Ignored JSON format instruction

**Example 2: Structural Inconsistency**
   *Request*: "List the top 3 benefits of exercise"
   *Response 1*: "1. Weight management\n2. Improved mood\n3. Better sleep"
   *Response 2*: "Exercise provides weight management benefits. It also improves mood and helps with sleep."
   *Issue*: Inconsistent response structure

**Example 3: Instruction Ignorance**
   *Prompt*: "Answer in exactly 3 bullet points"
   *Response*: "Exercise is beneficial for health. It helps maintain weight and improves cardiovascular function. Regular physical activity also boosts mood and energy levels. Additionally, it strengthens muscles and bones."
   *Issue*: Ignored bullet point requirement

.. toctree::
   :caption: Output Formatting Issues
   :hidden:
   :maxdepth: 1

   self
