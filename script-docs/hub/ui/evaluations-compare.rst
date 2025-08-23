:og:description: Compare Evaluations (UI) - Analyze and compare multiple evaluation runs to detect regressions, identify patterns, and track improvements in your LLM agent performance over time.

.. _compare-evaluations:

===============================================
Compare Evaluations
===============================================

Comparing evaluations enables you to make sure you don't have any regression between your agent versions. To do this, it is essential to diagnose issues and implement corrections to improve the agent's performance.


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
