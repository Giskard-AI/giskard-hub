:og:title: Giskard Hub UI - Evaluation Creation and Execution
:og:description: Run and manage LLM agent evaluations through the user interface. Execute tests, schedule automated evaluations, and analyze results with comprehensive reporting and detailed metrics.

==============================================
Run evaluations
==============================================

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

- **Metadata**: Verifies the presence of specific (tool calls, user information, etc.) metadata in the agent's response.

- **Semantic Similarity**: Verifies that the agent's response is semantically similar to the expected output.

.. note::

   For detailed information about these checks, including examples and how they work, see :doc:`/hub/ui/annotate/checks`.

The pie chart below displays the number of evaluations that passed, failed, or were unexecuted.

.. image:: /_static/images/hub/evaluation-metrics.png
   :align: center
   :alt: "Evaluation metrics"
   :width: 800

.. tip::

   **💡 How to use your test results to correct your AI agent?**

   During the development phase, it is essential to diagnose issues and implement corrections to improve the agent’s performance.

   - **Failure rate per check:** Identifying the checks with the highest failure rate makes it easier to apply targeted corrections. For example, if you created a custom check to verify whether the agent starts with "I’m sorry," it is useful to know how many conversations fail this requirement. If the failure rate is high, you can develop mitigation strategies such as prompt engineering, implementing guardrails, or using routers to address the issue.
   - **Failure rate per category:** Measuring failure rates across different vulnerability categories (e.g., hallucination, prompt injection) helps prioritize mitigation strategies for the AI agent.
   - **Failure rate per tag:** Measuring failure rates across different tags (e.g., customer-support, technical-support) helps prioritize mitigation strategies for the AI agent.

When you click on a conversation in the Evaluation Runs, you’ll see detailed information on the metrics, along with the reason for the result.

.. image:: /_static/images/hub/evaluation-detail.png
   :align: center
   :alt: "Evaluation detail"
   :width: 800
