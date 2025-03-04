================
Run evaluations
================

This section guides you through evaluating your agent using a given dataset. For example, you might want to run evaluations systematically whenever you deploy an updated agent in a pre-production or staging environment. This approach allows you to collaborate with your team to ensure the agent performs as expected.


Create a new evaluation
------------------------

On the Evaluations page, click on "Run evaluation" button in the upper right corner of the screen.

.. image:: /_static/images/hub/evaluation-list.png
   :align: center
   :alt: "List of evaluations"
   :width: 800

Next, set the parameters for the evaluation:

- ``Agent``: Select the agent you wish to evaluate.

- ``Dataset``: Choose the dataset you want to use for the evaluation.

- ``Tags`` (optional): Limit the evaluation to a specific subset of the dataset by applying tags.

.. image:: /_static/images/hub/evaluation-run.png
   :align: center
   :alt: "New evaluation run"
   :width: 800

The evaluation run is automatically named and assessed against the checks (built-in and custom ones) that were enabled in each conversation. The built-in checks include:

- **Correctness**: Verifies if the agent's response matches the expected output (reference answer).

- **Conformity**: Ensures the agent's response adheres to the rules, such as "The agent must be polite."

- **Groundedness**: Ensures the agent's response is grounded in the conversation.

- **String matching**: Checks if the agent's response contains a specific string, keyword, or sentence.

The pie chart below displays the number of evaluations that passed, failed, or were unexecuted.

.. image:: /_static/images/hub/evaluation-metrics.png
   :align: center
   :alt: "Evaluation metrics"
   :width: 800

When you click on a conversation in the Evaluation Runs, you’ll see detailed information on the metrics, along with the reason for the result.

.. image:: /_static/images/hub/evaluation-detail.png
   :align: center
   :alt: "Evaluation detail"
   :width: 800