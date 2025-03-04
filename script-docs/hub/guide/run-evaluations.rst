==============================
Run and compare evaluations
==============================

This section guides you through evaluating your agent using a given dataset. For example, you might want to run evaluations systematically whenever you deploy an updated agent in a pre-production or staging environment. This approach allows you to collaborate with your team to ensure the agent performs as expected.

.. tip:: 
   
   **💡 When to execute your tests?**

   Depending on your AI lifecycle, you may have different reasons to execute your tests:

   - **Development time:** Compare model versions during development and identify the right correction strategies for developers.
   - **Deployment time:** Perform non-regression testing in the CI/CD pipeline for DevOps.
   - **Production time:** Provide high-level reporting for business executives to stay informed about key vulnerabilities in a running bot.


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

.. tip:: 
   
   **💡 How to use your test results to correct your AI agent?**

   During the development phase, it is essential to diagnose issues and implement corrections to improve the bot’s performance.

   - **Failure rate per check:** Identifying the checks with the highest failure rate makes it easier to apply targeted corrections. For example, if you created a custom check to verify whether the bot starts with "I’m sorry," it is useful to know how many conversations fail this requirement. If the failure rate is high, you can develop mitigation strategies such as prompt engineering, implementing guardrails, or using routers to address the issue.
   - **Failure rate per tag:** Measuring failure rates across different vulnerability categories (e.g., hallucination, prompt injection) helps prioritize mitigation strategies for the AI agent.


When you click on a conversation in the Evaluation Runs, you’ll see detailed information on the metrics, along with the reason for the result.

.. image:: /_static/images/hub/evaluation-detail.png
   :align: center
   :alt: "Evaluation detail"
   :width: 800

Compare several evaluations
-------------------------------

Comparing evaluations enables you to make sure you don't have any regression between your model versions. On the Evaluations page, select at least two evaluations to compare, then click the "Compare" button in the top right corner of the table. The page will display a comparison of the selected evaluations.

.. image:: /_static/images/hub/comparison-overview.png
   :align: center
   :alt: "Compare evaluation runs"
   :width: 800

First, it shows the success rate - the percentage of conversations that the checks passed in each evaluation. It also displays the percentage of each specific check. Then it presents a table listing the conversations, which can be filtered by results, such as whether the conversations in both evaluations passed or failed the checks.

Clicking on a conversation will show a detailed comparison.

.. image:: /_static/images/hub/comparison-detail.png
   :align: center
   :alt: "Comparison details"
   :width: 800

Get notified at production time with alerting
-----------------------------------------------

At production time, it is important to provide regular reports to business executives to identify key vulnerabilities in the bot. Test results may vary with each execution due to the stochastic nature of the bot. Therefore, it is crucial to run tests regularly (e.g., once a week) to monitor for new vulnerabilities over time. 

Regular reports can be sent via email to notify teams of newly detected vulnerabilities.

.. image:: /_static/images/hub/alerting.png
   :align: center
   :alt: "Alterting"
   :width: 500