:og:title: Giskard Hub UI - Check Assignment and Custom Validation Rules
:og:description: Assign checks to test cases and create custom validation rules. Use correctness, conformity, groundedness, and other evaluation metrics to ensure comprehensive LLM agent testing.

Assigning checks to tests
=========================

.. raw:: html

   <iframe width="100%" height="400" src="https://www.youtube.com/embed/VLejoLvDy-o?si=MHhUR4NTc-Nk5MjM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Assigning checks to a conversation enables you to set the right requirements for your conversation. Various checks are available at Giskard.

Correctness Check
-----------------

Check whether all information from the reference answer is present in the agent answer without contradiction. Unlike the groundedness check, the correctness check is sensitive to omissions but tolerant of additional information in the agent's answer.

.. admonition:: Example

   **Reference Answer**: Paris is the capital of France, it was founded around 200 BC.

   **Failure examples**:

   - The capital of France is Paris.

     - *Reason: The answer does not specify when the city of Paris was founded*
   - The capital of France is Paris, it was founded in 200 AD.

     - *Reason: The answer contradicts the reference which states that Paris was founded around 200 BC, and not 200 AD*

   **Success example**:

   - The capital of France is Paris, the first settlement dates from 200 BC.



Conformity Check
-----------------

Given a rule or criterion, check whether the agent answer complies with this rule. This can be used to check business specific behavior or constraints. A conformity check may have several rules. Each rule should check a unique and unambiguous behavior. Here are a few examples of rules:

- The agent should not talk about {{competitor company}}.
- The agent should only answer in English.
- The agent should always keep a professional tone.

.. admonition:: Example

   **Rule**: The agent should not give any financial advice or personalized recommendations.

   **Failure example**:

   - You should definitely invest into bitcoin in addition to your saving plan, since you want to buy a flat quickly, the yield is much higher with bitcoin.

     - *Reason: The agent answer contradicts the rule which states that the agent should not give any financial advice or personalized recommendations.*

   **Success example**:

   - I'm sorry, I cannot give you specific financial advice, to get personalized recommandation I suggest that you contact our dedicated customer service.


.. tip::

   To write effective rules, remember the following best practices:

   - **Avoid General Rules Unrelated to the Conversation**

     - *Example of wrong usage:* "The agent should not discriminate based on gender, sexual orientation, religion, or profession" when responding to a user question that has no connection to biases and discrimination.
     - *Reason:*  Unit test logic helps with diagnostics (1 test = 1 precise behavior). Having many non relevant  tests that pass has low value because a failing test provides more useful information than a passing test.
     - *Best Practice:* Minimize the number of rules per conversation and only choose rules likely to cause the test to fail.

   - **Break Down Policies into Multiple Ones**

     - *Example of wrong usage:* "The agent should not respond to requests about illegal topics and should focus on banking and insurance-related questions."
     - *Reason:*  Long rules with large scope are difficult to maintain and interpret for the evaluator and they make it harder the debugging process.
     - *Best Practice:* Add multiple rules within the same check to ensure the entire set is interpreted globally.

   - **Write Custom Checks when your rules apply to multiple conversations**

     - Creating and enabling a custom check for multiple conversations is useful when you want to display the evaluation results for all conversations where the custom check is enabled.
     - *Examples of generic rules that are likely to be used more than once*: "The agent should not discriminate based on gender, sexual orientation, religion, or profession." "The agent should answer in English."

Groundedness Check
------------------

Check whether all information from the agent's answer is present in the given context without contradiction. Unlike the correctness check, the groundedness check is tolerant of omissions but sensitive to additional information in the agent's answer. The groundedness check is useful for detecting potential hallucinations in the agent's answer.

.. admonition:: Example

   **Reference Context**: Sir Edmund Hillary, a New Zealand mountaineer, became famous for being one of the first people to reach the summit of Mount Everest with Tenzing Norgay on May 29, 1953.

   **Failure examples**:

   - Edmund Hillary, born in 1919, was a great mountaineer who climb Mount Everest first.

     - *Reason: The reference context does not specify that Hillary was born in 1919*
   - Edmund Hillary reached the summit of Mount Everest in 1952.

     - *Reason: The reference context states that Hillary reached the summit of Mount Everest in 1953, and not in 1952*

   **Success examples**:

   - Edmund Hillary was the first person to reach the summit of Mount Everest in 1953.
   - Edmund Hillary, a renowned New Zealander, gained fame as one of the first climbers to summit Mount Everest alongside Tenzing Norgay on May 29, 1953.


String Matching Check
---------------------

Check whether the given keyword or sentence is present in the agent answer.

.. admonition:: Example

   **Keyword**: "Hello"

   **Failure example**:

   - Hi, can I help you?

     - *Reason: The agent answer does not contain the keyword 'Hello'*

   **Success example**:

   - Hello, how may I help you today?

Metadata Check
---------------

Check whether the agent answer contains the expected value at the specified JSON path. This check is useful to verify that the agent answer contains the expected metadata (e.g. whether a tool is called). The metadata check can be used to check for specific values in the metadata of agent answer, such as a specific date or a specific name.

.. tip::

    We recommend using a tool like `json-path-evaluator <https://mockoon.com/tools/json-object-path-evaluator/>`_ to evaluate the JSON path rules.

.. admonition:: Example - string value

   **JSON Path rule**: Expecting ``John`` (string) at ``$.user.name``

   **Failure examples**:

   - Metadata: ``{"user": {"name": "Doe"}}``

     - *Reason: Expected* ``John`` *at* ``$.user.name`` *but got* ``Doe``

   **Success examples**:

   - Metadata: ``{"user": {"name": "John"}}``
   - Metadata: ``{"user": {"name": "John Doe"}}``

.. admonition:: Example - boolean value

   **JSON Path rule**: Expecting ``true`` (boolean) at ``$.output.success``

   **Failure examples**:

   - Metadata: ``{"output": {"success": false}}``

     - *Reason: Expected* ``true`` *at* ``$.output.success`` *but got* ``false``

   - Metadata: ``{"output": {}}``

     - *Reason: JSON path* ``$.output.success`` *does not exist in metadata*

   **Success example**:

   - Metadata: ``{"output": {"success": true}}``

Semantic Similarity Check
-------------------------

Check whether the agent's response is semantically similar to the reference. This is useful when you want to allow for some variation in wording while ensuring the core meaning is preserved.

.. admonition:: Example

   **Reference Answer**: "The capital of France is Paris, which is located in the northern part of the country."

   **Threshold**: 0.8

   **Failure example**:

   - The capital of France is Paris, which is located in the southern part of the country.


Custom Check
------------

Custom checks are built on top of the built-in checks (Conformity, Correctness, Groundedness, String Matching, Metadata, and Semantic Similarity) and can be used to evaluate the quality of your agent's responses.

The advantage of custom checks is that they can be tailored to your specific use case and can be enabled on many conversations at once.

On the Checks page, you can create custom checks by clicking on the "New check" button in the upper right corner of the screen.

.. image:: /_static/images/hub/create-checks-list.png
   :align: center
   :alt: "List of checks"
   :width: 800

Next, set the parameters for the check:

- ``Name``: Give your check a name.
- ``Identifier``: A unique identifier for the check. It should be a string without spaces.
- ``Description``: A brief description of the check.
- ``Type``: The type of the check, which can be one of the following:
    - ``Correctness``: The output of the agent should match the reference.
- ``Conformity``: The conversation should follow a set of rules.
- ``Groundedness``: The output of the agent should be grounded in the conversation.
- ``String matching``: The output of the agent should contain a specific string (keyword or sentence).
- ``Metadata``: The metadata output of the agent should match a list of JSON path rules.
- ``Semantic Similarity``: The output of the agent should be semantically similar to the reference.
- And a set of parameters specific to the check type. For example, for a ``Correctness`` check, you would need to provide the ``Expected response`` parameter, which is the reference answer.

.. image:: /_static/images/hub/create-checks-detail.png
   :align: center
   :alt: "Create a new check"
   :width: 800

Once you have created a custom check, you can apply it to conversations in your dataset. When you run an evaluation, the custom check will be executed along with the built-in checks that are enabled.

How to choose the right check?
-------------------------------

The choice of check depends on the type of vulnerability you're testing for and ultimately depends on the your business requirements, however, we do provide some guidelines to help you choose the right check for various business failures and security vulnerabilities.

.. grid:: 1 1 2 2

   .. grid-item-card:: Business Failures
      :link: /start/glossary/business/index
      :link-type: doc

      Hallucination is one of the most critical vulnerabilities affecting Large Language Models. It occurs when a model generates false, misleading, or fabricated information that appears plausible but is incorrect.

   .. grid-item-card:: Security Vulnerabilities
      :link: /start/glossary/security/index
      :link-type: doc

      Prompt injection is a critical security vulnerability where malicious users manipulate input prompts to bypass content filters, override model instructions, or extract sensitive information.

Next steps
----------

Now that you have created a custom check, you can apply it to conversations in your dataset. When you run an evaluation, the custom check will be executed along with the built-in checks that are enabled.

* **Evaluate tests** - :doc:`/hub/ui/annotate/conversations`
* **Assign tags to tests** - :doc:`/hub/ui/annotate/tags`
* **Run evaluations** - :doc:`/hub/ui/evaluations/create`