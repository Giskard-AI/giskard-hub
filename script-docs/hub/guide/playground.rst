==============================================
Create tests in playground
==============================================

Creating conversations in the playground allows you to test your bot in a user-like environment. Additionally, these conversations can be sent to a specific dataset (see the section below) to test different versions of the model on the same conversation. This helps in evaluating and improving the bot's performance consistently.

In this section, we will walk you through how to write a conversation and send it to your dataset.


Try a conversation
---------------------

.. image:: /_static/images/hub/playground.png
   :align: center
   :alt: "The playground"
   :width: 800

The Chat section is where you can query and talk to the agent. You write your message on the bottom part of the screen.

The right panel displays all your conversations. You can have as many conversations as you need. To add a new one, click the “New conversation” button. You are also shown a list of your recent conversations from the most recent to the oldest.

.. tip:: 
   
   **💡 How to create effective conversations?**

   To ensure your chatbot provides accurate and relevant responses, follow these guidelines:

   - Be **clear** and **concise**. Specific messages increase the likelihood that the bot will understand and respond correctly. Focus on domain-specific questions that are relevant to your context.
   - Provide **context**. Set the stage for the bot by offering background information. The more context you provide, the better the bot can tailor its responses to your needs.
   - **Break down** your questions into multiple messages. Long, complex queries can confuse the bot. Instead, divide your questions into smaller, manageable parts to maintain clarity. Giskard Hub allows you to chain these messages into a cohesive conversation.
   - **Use proper grammar and spelling**. Errors can lead to misunderstandings or incorrect responses from the bot.
   - **Test and refine** your messages. Try different variations and fine-tune your prompts to cover a broad range of scenarios. This helps ensure the bot handles diverse inputs effectively.


You can try various types of conversations:


Adversarial conversations
^^^^^^^^^^^^^^^^^^^^^^^^^^

Adversarial conversations are designed to challenge the chatbot by presenting it with difficult, unexpected, or tricky questions. The goal is to test the limits of the bot's understanding and ability to handle edge cases or unconventional inputs. These conversations help identify weaknesses and areas for improvement in the chatbot's performance.

    Example:

    User: "What is the current interest rate for a loan from the Martian Bank?"
    
    Bot: "The current interest rate for a loan from the Martian Bank is 5%."

    In this example, the bot incorrectly hallucinates an answer about a non-existent Martian Bank, highlighting a vulnerability that needs addressing.

.. tip::

    To maximize the effectiveness of adversarial testing, focus on one vulnerability per conversation. Once a vulnerability is identified, save the conversation to the dataset immediately. This approach ensures each conversation serves as a valuable example for future testing, which prevents confusion that could arise from addressing multiple vulnerabilities in one conversation.

**Example of effective adversarial testing**

    User: "Can I get a loan to buy property on the moon?"
    
    Bot: "Currently, there are no financial services available for purchasing property on the moon as it is not legally owned by individuals. However, I can help you with information on home loans on Earth."

    In this effective adversarial test, the bot correctly identifies the impossibility of buying property on the moon, avoiding hallucination. This conversation should be saved to the dataset to verify that future versions of the bot maintain this correct response.

**Example of not effective adversarial testing**

    User: "Can I get a loan to buy property on the moon?"

    Bot: "Yes, you can get a loan to buy property on the moon."

    Then immediately:

    User: "What are the interest rates for a home loan?"

    Bot: "The interest rates for a home loan are 3.5%."

    In this not effective adversarial test, the conversation combines a hallucinatory response about moon property loans with a correct response about home loan interest rates. This mix can make it difficult to isolate and address specific vulnerabilities, thereby reducing the clarity and effectiveness of the test.

.. note::

    Don’t test multiple vulnerabilities in a single conversation. Isolate each issue to maintain clarity and effectiveness in your testing and datasets. However, linking multiple sentences in your conversation can be beneficial if you are specifically testing the chatbot’s ability to handle conversation history and context given a previous vulnerability.

Legitimate conversations
^^^^^^^^^^^^^^^^^^^^^^^^^

Legitimate conversations simulate typical interactions that a user would have with the chatbot in a real-world scenario. These conversations should reflect common queries and tasks the bot is expected to handle. Legitimate conversations are crucial for evaluating the bot's effectiveness in everyday use and ensuring it meets user needs.

    Example for a chatbot that sells home products:

    User: "What is the price of the latest model of your vacuum cleaner?"

    Bot: "The latest model of our vacuum cleaner is priced at $199.99. Would you like to place an order?"

Out of scope questions
^^^^^^^^^^^^^^^^^^^^^^^

In legitimate conversations, it can also be important to test out-of-scope questions. These are questions that, while legitimate, may fall outside the information contained in the chatbot’s knowledge base. The bot should be able to admit when it does not have the necessary information.

**Example of an out-of-scope question**

    User: "Do you sell outdoor furniture?"
    
    Bot: "I'm sorry, but we currently do not sell outdoor furniture. We specialize in home products. Is there something else you are looking for?"

    This type of response shows that the bot correctly handles a legitimate but out-of-scope question by admitting it doesn’t know the answer and steering the user back to relevant topics.

Conversation history testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In these kinds of conversations, it’s important to test the bot's ability to handle conversation history. Concatenating multiple messages can be useful for this purpose.

**Example testing conversation history**

    User: "Do you have any discounts on kitchen appliances?"

    Bot: "Yes, we currently have a 10% discount on all kitchen appliances."

    User: "Great! Can you tell me the price of the stainless steel blender after the discount?"

    Bot: "The stainless steel blender is originally priced at $79.99. With the 10% discount, the final price is $71.99."

This example demonstrates effective conversation history handling for several reasons:

- **Context Retention:** The bot retains the context of the initial discount discussion when answering the follow-up question. It understands that the 10% discount applies to the stainless steel blender and accurately applies this context to calculate the discounted price.
- **Accuracy:** The bot accurately performs the calculation, showing that it can handle numerical data and apply discounts correctly.
- **User Guidance:** The conversation flow guides the user from a general inquiry to a specific request, showcasing the bot's ability to manage progressively detailed queries within the same context.
- **Relevance:** Each response is relevant to the user's questions, maintaining a coherent and logical conversation flow.

The important thing is to remember that once you have tested what you wanted, you should send the conversation to the dataset, keeping the length of the conversations short and focused.

.. tip::

    - Test out-of-scope questions to ensure the bot appropriately handles unknown queries.
    - Use conversation history to test the bot’s ability to maintain context over multiple exchanges.
    - Keep conversations short and focused to isolate specific functionalities.
    - Regularly update your dataset with new test cases to continually improve the bot’s performance.

Send to dataset
----------------

When the conversation is sufficient enough for what it needs to contain, you can send it to the dataset which you then use to evaluate your model.

.. image:: /_static/images/hub/playground-save.png
   :align: center
   :alt: "Save conversation to a dataset from the Playground"
   :width: 800

The screen above shows three sections:

- ``Messages``: the conversation you want to save to the dataset. Note that the last agent response is added as the assistant’s recorded example. Never include the assistant’s answer as the last message in this section as during evaluation, this will be skipped and the agent will generate a new answer that will be evaluated against the expected response or the policies.
- ``Evaluation Settings``: the parameters from which you want to evaluate the response. It includes:
    - ``Expected response`` (optional): a reference answer that will be used to determine the correctness of the agent’s response. There can only be one expected response. If it is not provided, we do not check for the Correctness metric.
    - ``Rules`` (optional): a list of requirements that the agent must meet when generating the answer. There can be one or more rules. If it is not provided, we do not check for the Conformity metric.
    - ``Context`` (optional): the context of the conversation. This is useful when you want to evaluate the agent’s response based on the context of the conversation. If it is not provided, we do not check for the Groundedness metric.
    - ``Keyword`` (optional): a keyword that the agent’s response must contain. This is useful when you want to evaluate the agent’s response based on a specific keyword. If it is not provided, we do not check for the String matching metric.
    - And any custom checks you may have defined.
- ``Dataset``: where the conversations are saved
- ``Tags`` (optional): allows for better organization and filtering conversations
