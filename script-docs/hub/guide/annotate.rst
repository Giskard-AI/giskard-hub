======================
Annotate test dataset
======================

Conversations are a collection of messages with evaluation parameters (i.e. the expected answer, rules that the agent must comply with, etc.). These conversations are the ones you eventually evaluate your model against. 

The Annotation Studio provides an interface for reviewing and assigning evaluation criteria (checks) to conversations. 

Since bot outputs are non-deterministic (they may vary at each execution of the bot), writing expected outputs and rules requires generating multiple bot outputs and testing evaluations against them. Refining test cases is then a **trial-and-error process** that demands proper iterative solutions, hence the need for a studio to design test requirements (ex: expected outputs, rules, contexts, etc.).

Write a message
================

A message is the user conversation with the bot that you want to test. 

.. image:: /_static/images/hub/annotation-studio.png
   :align: center
   :alt: "Iteratively design your test cases using a business-centric & interactive interface."
   :width: 800

A message contains two key components:

- **User message**: This is the prompt written by the user. It can be a query from a user.
- **Assistant message**: This is the bot's answer to the user message. There are different ways to write an assistant message:

  1. You can import your bot's answer while uploading your dataset.
  2. Dynamically generate the bot's answer by clicking on the three-dot button and selecting "Replace the assistant message".
  3. You can also write your own bot message from scratch.

If you haven't written an assistant message, by default, the Hub populates the assistant message with the bot's answer generated during the evaluation of your dataset.

For multi-turn interactions with the bot, you can easily add more interactions by clicking on "Add message".


Assign a check to a conversation
==================================

Assigning checks to a conversation enables you to set the right requirements for your conversation. Various checks are available at Giskard:


Correctness Check
------------------

Check whether all information from the reference answer is present in the model answer without contradiction. Unlike the groundedness check, the correctness check is sensitive to omissions but tolerant of additional information in the agent’s answer.

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
------------------

Given a rule or criterion, check whether the model answer complies with this rule. This can be used to check business specific behavior or constraints. A conformity check may have several rules. Each rule should check a unique and unambiguous behavior. Here are a few examples of rules:

- The model should not talk about {{competitor company}}.
- The model should only answer in English.
- The model should always keep a professional tone.

.. admonition:: Example

   **Rule**: The model should not give any financial advice or personalized recommendations.
   
   **Failure example**:
   
   - You should definitely invest into bitcoin in addition to your saving plan, since you want to buy a flat quickly, the yield is much higher with bitcoin. 

     - *Reason: The model answer contradicts the rule which states that the model should not give any financial advice or personalized recommendations.*
   
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
     - *Examples of generic rules that are likely to be used more than once*: "The agent should not discriminate based on gender, sexual orientation, religion, or profession." "The bot should answer in English."

Groundedness Check
--------------------

Check whether all information from the bot’s answer is present in the given context without contradiction. Unlike the correctness check, the groundedness check is tolerant of omissions but sensitive to additional information in the agent’s answer. The groundedness check is useful for detecting potential hallucinations in the agent’s answer.

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


String Matching
---------------

Check whether the given keyword or sentence is present in the model answer.

.. admonition:: Example

   **Keyword**: "Hello"
   
   **Failure example**:
   
   - Hi, can I help you?

     - *Reason: The model answer does not contain the keyword 'Hello'*
   
   **Success example**:
   
   - Hello, how may I help you today?

Custom Check
---------------

Custom checks are built on top of the built-in checks (Conformity, Correctness, Groundedness and String matching) and can be used to evaluate the quality of your agent's responses. 

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
    - ``Correctness``: The output of the model should match the reference.
    - ``Conformity``: The conversation should follow a set of rules.
    - ``Groundedness``: The output of the model should be grounded in the conversation.
    - ``String matching``: The output of the model should contain a specific string (keyword or sentence).
- And a set of parameters specific to the check type. For example, for a ``Correctness`` check, you would need to provide the ``Expected response`` parameter, which is the reference answer.

.. image:: /_static/images/hub/create-checks-detail.png
   :align: center
   :alt: "Create a new check"
   :width: 800

Once you have created a custom check, you can apply it to conversations in your dataset. When you run an evaluation, the custom check will be executed along with the built-in checks that are enabled.


Assign a tag to a conversation
================================

Tags are optional but highly recommended for better organization. They allow you to filter the conversations later on and manage your chatbot's performance more effectively.


How to choose the right tag?
-------------------------------

To choose a tag, it is good to stick to a naming convention that you agreed on beforehand. Ensure that similar conversations based on categories, business functions, and other relevant criteria are grouped together. For example, if your team is located in different regions, you can have tags for each, such as "Normandy" and "Brittany".

.. admonition:: Categories of Tags

   - **Issue-Related Tags**: These tags categorize the types of problems that might occur during a conversation.
     
     Examples: "Hallucination", "Misunderstanding", "Incorrect Information"

   - **Attack-Oriented Tags**: These tags relate to specific types of adversarial testing or attacks.
     
     Examples: "SQL Injection Attempt", "Phishing Query", "Illegal Request"

   - **Legitimate Question Tags**: These tags categorize standard, everyday user queries.
     
     Examples: "Balance Inquiry", "Loan Application", "Account Opening"

   - **Context-Specific Tags**: These tags pertain to specific business contexts or types of interactions.
     
     Examples: "Caisse d'Epargne", "Banco Popular", "Corporate Banking"

   - **User Behavior Tags**: These tags describe the nature of the user's behavior or the style of interaction.
     
     Examples: "Confused User", "Angry Customer", "New User"

   - **Temporal Tags**: Depending on the life cycle of the testing process of the model.
     
     Examples: "red teaming phase 1", "red teaming phase 2"


.. tip::

   - **Use Multiple Tags if Necessary**: Apply multiple tags to a single conversation to cover all relevant aspects.
     
     Example: A conversation with a confused user asking about loan applications could be tagged with "Confused User", "Loan Application", and "Misunderstanding".
   
   - **Hierarchical Tags**: Implement a hierarchy in your tags to create a structured and clear tagging system.
     
     Example: Use "User Issues > Hallucination" to show the relationship between broader categories and specific issues.
   
   - **Stick to Agreed Naming Conventions**: Ensure that your team agrees on and follows a consistent naming convention for tags to maintain organization and clarity.
     
     Example: Decide on using either plural or singular forms for all tags and stick to it.
