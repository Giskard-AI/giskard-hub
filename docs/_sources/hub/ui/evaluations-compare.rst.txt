:og:title: Giskard Hub - Enterprise Agent Testing - Compare Evaluations
:og:description: Compare evaluation results across different agent versions, datasets, and time periods. Identify regressions, track improvements, and maintain quality standards.

.. compare-evaluations::

==============================================
Compare evaluation results
==============================================

Comparing evaluations is a crucial part of maintaining and improving your LLM agents over time. By comparing results across different versions, datasets, or time periods, you can:

* **Detect regressions**: Identify when agent performance has degraded
* **Track improvements**: Measure the impact of changes and optimizations
* **Maintain quality standards**: Ensure consistent performance across deployments
* **Make data-driven decisions**: Use metrics to guide development priorities

In this section, we will walk you through how to compare evaluations in Giskard Hub.


On the Evaluations page, select at least two evaluations to compare, then click the "Compare" button in the top right corner of the table. The page will display a comparison of the selected evaluations.

.. image:: /_static/images/hub/comparison-overview.png
   :align: center
   :alt: "Compare evaluation runs"
   :width: 800

First, it shows the success rate - the percentage of conversations that the checks passed in each evaluation. It also displays the percentage of each specific check. Then it presents a table listing the conversations, which can be filtered by results, such as whether the conversations in agenth evaluations passed or failed the checks.

Clicking on a conversation will show a detailed comparison.

.. image:: /_static/images/hub/comparison-detail.png
   :align: center
   :alt: "Comparison details"
   :width: 800

Within this comparison you can explore the performance of the agent on a specific conversation and metrics.

.. tip:: **💡 How to use your test results to correct your AI agent?**

   During this process you might uncover patterns and issues that you can address in your agent.

   For example, if you created a custom check to verify whether the agent starts with "I’m sorry," it is useful to know how many conversations fail this requirement.
   If the failure rate is high, you can chose to adjust the evaluation, create more representative test cases or adjust your Agent deployment.

   If you need more information on setting up efficient evaluationsfor your agent, check out the :doc:`/hub/ui/annotate` section.
