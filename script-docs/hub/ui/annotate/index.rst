:og:title: Giskard Hub UI - Human-in-the-Loop Annotation and Review
:og:description: Review and refine test cases with domain expertise. Use collaborative annotation workflows to improve test quality and ensure comprehensive coverage with intuitive visual tools.

====================================================
Review and refine test cases and metrics
====================================================

The annotation workflow in Giskard Hub enables you to continuously improve your test cases and evaluation metrics through an iterative, collaborative process. 

Each test case is composed of a **conversation** and its associated **evaluation parameters** (e.g., an expected answer, rules that the agent must respect, etc.).

The annotation workflow follows a task-oriented approach with two distinct personas and workflows:

1. **Distribute tasks** - Organize your review work by creating and assigning tasks to team members
2. **Review test results** - Business workflow for reviewing evaluation results and understanding failures
3. **Modify test cases** - Product owner workflow for refining test cases and validation rules

This section guides you through the complete task-oriented workflow from task distribution to test case refinement.

Getting started
---------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Understand metrics, failure categories and tags
      :link: overview
      :link-type: doc

      Understand metrics, failure categories and tags to review test results. 

   .. grid-item-card:: Distribute tasks to organize your review work
      :link: distribute_tasks
      :link-type: doc

      Create and manage tasks to coordinate team reviews. Assign work for scan results, evaluation runs, and test cases to ensure quality and collaboration.

   .. grid-item-card:: Review test results
      :link: review_test_results
      :link-type: doc

      Review evaluation results and understand test failures. Follow the business workflow to analyze check results, understand reasons, and take appropriate actions.

   .. grid-item-card:: Modify test cases
      :link: modify_test_cases
      :link-type: doc

      Refine test cases and validation rules. Follow the product owner workflow to draft/undraft test cases, enable/disable checks, and structure your dataset.

Workflow overview
------------------

The annotation workflow involves two personas with distinct workflows:

**Business Persona (Review Workflow):**

- Reviews test results from evaluation runs or tasks
- Understands check results and failure reasons
- Reviews conversation flow and metadata
- Takes action: closes tasks if results are acceptable, or assigns modification work

**Product Owner Persona (Modification Workflow):**

- Modifies test cases based on review feedback
- Drafts/undrafts test cases
- Enables/disables checks
- Modifies check requirements
- Validates checks and structures test cases

.. include:: workflow.rst.inc

Next steps
----------

Now that you understand the task-oriented annotation workflow, explore the specific workflows:

* **Start with task distribution** - Learn how to create and manage tasks to organize your review work :doc:`distribute_tasks`
* **Review test results** - Follow the business workflow to review evaluation results :doc:`review_test_results`
* **Modify test cases** - Follow the product owner workflow to refine test cases and checks :doc:`modify_test_cases`

.. tip::

   **💡 Getting started with annotation workflows**

   If you're new to Giskard Hub, we recommend starting with:
   
   1. **Run an evaluation** or **review scan results** to identify test cases that need attention
   2. **Create tasks** to organize the review work
   3. **Review test results** following the business workflow
   4. **Modify test cases** as needed following the product owner workflow
   
   For more information, see :doc:`/hub/ui/evaluations/create` and :doc:`/hub/ui/scan/index`.

.. toctree::
   :hidden:
   :maxdepth: 3

   overview
   distribute_tasks
   review_test_results
   modify_test_cases

