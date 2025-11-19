:og:title: Giskard Hub UI - Tag Management and Test Organization
:og:description: Organize and categorize test cases with comprehensive tagging system. Filter conversations, manage performance metrics, and maintain structured test datasets with intuitive visual tools.

Assigning tags to tests
=======================

Tags are optional but highly recommended for better organization. They allow you to filter the conversations later on and manage your agent's performance more effectively.

How to choose the right tag?
-----------------------------

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

   - **Temporal Tags**: Depending on the life cycle of the testing process of the agent.

     Examples: "red teaming phase 1", "red teaming phase 2"


.. tip::

   - **Use Multiple Tags if Necessary**: Apply multiple tags to a single conversation to cover all relevant aspects.

     Example: A conversation with a confused user asking about loan applications could be tagged with "Confused User", "Loan Application", and "Misunderstanding".

   - **Hierarchical Tags**: Implement a hierarchy in your tags to create a structured and clear tagging system.

     Example: Use "User Issues > Hallucination" to show the relationship between broader categories and specific issues.

   - **Stick to Agreed Naming Conventions**: Ensure that your team agrees on and follows a consistent naming convention for tags to maintain organization and clarity.

     Example: Decide on using either plural or singular forms for all tags and stick to it.

Next steps
----------

Now that you have assigned tags to tests, you can run evaluations on them.

* **Evaluate tests** - :doc:`/hub/ui/annotate/conversations`
* **Assign checks to tests** - :doc:`/hub/ui/annotate/checks`
* **Manage tasks** - :doc:`/hub/ui/annotate/tasks`
* **Run evaluations** - :doc:`/hub/ui/evaluations/create`