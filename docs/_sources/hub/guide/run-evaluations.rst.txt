================
Run evaluations
================

This section guides you through evaluating your model using a given dataset. For example, you might want to run evaluations systematically whenever you deploy an updated model in a pre-production or staging environment. This approach allows you to collaborate with your team to ensure the model performs as expected.


Create a new evaluation
------------------------

On the Evaluations page, click the "Run Evaluation" button in the upper right corner of the screen.

.. image:: /_static/images/hub/evaluation-list.png
   :align: center
   :alt: "List of evaluations"
   :width: 800

Next, set the parameters for the evaluation:

- ``Model``: Select the model you wish to evaluate.

- ``Dataset``: Choose the dataset you want to use for the evaluation.

- ``Tags`` (optional): Limit the evaluation to a specific subset of the dataset by applying tags.

.. image:: /_static/images/hub/evaluation-run.png
   :align: center
   :alt: "New evaluation run"
   :width: 800

The evaluation run is automatically named and assessed against the Correctness and Conformity metrics for each conversation.

- **Correctness**: Verifies if the agent's response matches the expected output.

- **Conformity**: Ensures the agent's response adheres to the rules, such as "The agent must be polite."

The pie chart below displays the number of evaluations that passed, failed, or were unexecuted.

.. image:: /_static/images/hub/evaluation-metrics.png
   :align: center
   :alt: "Evaluation metrics"
   :width: 800

When you click on a conversation in the Evaluation Runs, you’ll see detailed information on the Correctness and/or Conformity metrics, along with the reason for the result.

.. image:: /_static/images/hub/evaluation-detail.png
   :align: center
   :alt: "Evaluation detail"
   :width: 800