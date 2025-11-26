:og:title: Giskard Hub UI - Task Management and Work Distribution
:og:description: Manage and distribute work among team members with Tasks. Assign tasks for reviewing scan results, evaluation runs, and test cases to ensure quality and collaboration.

====================================================
Distribute tasks to organize your review work
====================================================

Tasks allow you to manage and distribute work among you and your coworkers. 

|

.. raw:: html

   <iframe width="100%" height="400" src="https://www.youtube.com/embed/u5ctBhfArNY?si=76o_0VIQzdPXFELk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


Tasks provide several key benefits for managing evaluation workflows:

* **Quality assurance** - Ensure all test cases are reviewed before being used in evaluations
* **Team collaboration** - Distribute work among team members based on their expertise
* **Traceability** - Track who is responsible for what and when work is completed
* **Dataset reliability** - Prevent biased evaluation metrics by ensuring conversations are properly reviewed
* **Workflow control** - Manage the review process systematically without missing any evaluations

This feature is particularly useful when you need to:

* Ask an AI developer to correct the agent if there's a failure
* Ask business experts to review the rules of a check
* Coordinate review workflows for scan results and evaluation runs
* Ensure quality control before publishing test cases

Two personas, two workflows
----------------------------

The annotation workflow involves two distinct personas with different responsibilities:

**Business Persona (Review Workflow):**

- Reviews test results from evaluation runs or tasks
- Understands check results and failure reasons
- Reviews conversation flow and metadata
- Takes action: closes tasks if results are acceptable, or assigns modification work to the product owner

**Product Owner Persona (Modification Workflow):**

- Modifies test cases based on review feedback
- Drafts/undrafts test cases
- Enables/disables checks
- Modifies check requirements
- Validates checks and structures test cases

Find your tasks
-----------------

The Hub UI provides a comprehensive overview of all your tasks, including:

* **Priority** - Set and view task priorities to manage workload
* **Status** - Track task progress (e.g., open, in progress, completed)
* **Creation date** - See when tasks were created
* **Description** - Understand what needs to be done
* **Assignees** - Know who is responsible for each task
* **Filters** - Filter tasks by your own tasks or unassigned tasks

.. image:: /_static/images/hub/tasks-overview.png
   :align: center
   :alt: "Tasks overview"
   :width: 800

Create a task
-------------

You can create tasks from two main sources: evaluation runs and scan results. Tasks help you track and assign work items to the appropriate team members.

.. note::

   Tasks can be linked to test cases (conversations) from datasets. For information on creating and managing datasets, see :doc:`/hub/ui/datasets/index`.

.. tip::

   **💡 When to create tasks**

   Create tasks when you need to:
   
   * Track work items that require review or modification
   * Assign specific test cases or scan results to team members
   * Coordinate review workflows across your team
   * Ensure quality control before publishing test cases
   
From scan results
__________________

When reviewing scan results, you can create tasks to track and assign work items. This is useful for organizing the review of vulnerabilities and issues found during scans.

.. note::

   To create a task from scan results, you first need to launch a scan. For information on how to launch scans, see :doc:`/hub/ui/scan/launch-scan`. For information on reviewing scan results, see :doc:`/hub/ui/scan/review-scan-results`.

To create a task from a scan result:

1. Open a scan result
2. Navigate to a specific item you want to review
3. While reviewing the item, you can see any assigned task
4. Create a new task by pressing "Create linked task" on the right side of the screen:

   * **Priority** - Set the task priority level
   * **Status** - Set the initial status
   * **Assignees** - Select one or more team members
   * **Description** - Provide a clear description of what needs to be done

.. image:: /_static/images/hub/tasks-from-probe.png
   :align: center
   :alt: "Create a task from a probe evaluation"
   :width: 800

From evaluation runs
_____________________

You can create tasks when reviewing evaluation runs. This is useful for tracking test cases that need attention after an evaluation.

.. note::

   To create a task from an evaluation run, you first need to run an evaluation. For information on how to run evaluations, see :doc:`/hub/ui/evaluations/create`.

To create a task from an evaluation run:

1. Open an evaluation run
2. Navigate to a specific test case in the evaluation run and opening it
3. Create a new task by pressing "Add task" on the top right corner of the screen:

   * **Priority** - Set the task priority level
   * **Status** - Set the initial status
   * **Assignees** - Select one or more team members
   * **Description** - Provide a clear description of what needs to be done
   * **Draft** - Chose to set the linked failed test case to draft status, excluding it from the evaluation run.

.. image:: /_static/images/hub/tasks-from-run.png
   :align: center
   :alt: "Create a task from an evaluation run"
   :width: 800

Iterate on a task
-----------------

When iterating on a task, there are various things you can can change. First, you need to open the task and view it.

.. image:: /_static/images/hub/tasks-edit.png
   :align: center
   :alt: "Edit a task"
   :width: 800

When editing a task, you can change the following information:

Assign people
_____________

Select one or more team members to assign the task to. This ensures that the right person with the appropriate expertise handles the work:

* **Data Scientist** - For fixing the agent or improving the model
* **Knowledge Base Manager** - For updating the knowledge base if information is missing or incorrect
* **Product Owner** - For modifying test cases or checks
* **Business Expert** - For reviewing business rules and requirements

Put description
_______________

Provide a clear description of what needs to be done. Include enough context so assignees understand:

* What the issue is
* Why it needs to be addressed
* What the expected outcome should be
* Any relevant context or background information

Open/close
__________

Set the initial status of the task:

* **Open** - Task is created and ready to be reviewed
* **In Progress** - Task is currently being worked on
* **Resolved** - Task has been finished

You can change the status as the task progresses through the review process.

Put a priority
______________

Set the task priority level to help team members focus on the most important work first:

* **High** - Urgent issues that need immediate attention
* **Medium** - Important issues that should be addressed soon
* **Low** - Issues that can be addressed when time permits

Draft/undraft
_____________

An important feature related to tasks is the ability to set conversations to draft. This workflow ensures that:

* Subsequent evaluation runs don't reuse conversations that are not ready to be used again
* Your evaluation metrics remain unbiased
* Quality control of other evaluations is maintained throughout the review process

When you go to the conversation linked to an evaluation run and create a task, you can set the linked failed test case to draft status. Before using it again, you need to resolve all associated tasks. 
Similarly, you can select a conversation from a dataset and set it to draft status. 

.. image:: /_static/images/hub/tasks-draft.png
   :align: center
   :alt: "Set a conversation to draft status"
   :width: 800

Follow the review process
-------------------------

Once tasks are created, follow the review process:

1. **Open the task and view it** - Check the current status and any updates
2. **Add your input** - Provide feedback, comments, or additional context in the description of the task
3. **Assign the right people** - Make sure the task is assigned to the appropriate team members
4. **Close the task** - When the work is complete
5. **Undraft the conversation** - Once all tasks are resolved, you can undraft the conversation to make it available for future evaluation runs

.. note::

   You can find a full example of the review process in the :doc:`/hub/ui/annotate/modify_test_cases` documentation.

Communicate with your team
--------------------------

You can add additional structure and context to your tasks and test cases to better understand the work to be done.

Update task descriptions
________________________

You can add a description to a task to communicate:

* What the work is about
* Why it's important
* What behavior or scenario it represents
* Any special considerations or context

.. note::

   For more information about task descriptions, see :doc:`/hub/ui/annotate/distribute_tasks`.

Comment on a test case
_______________________

Comments allow you to add notes and insights about a test case:

* Review findings and observations
* Document modifications and their reasons
* Share context with team members
* Track the evolution of a test case

To add a comment:

1. Open the test case in the dataset
2. Press the "Add a comment" button in the bottom right corner of the screen
3. Add your comment
4. Press the "Post comment" button

.. image:: /_static/images/hub/comment-create.png
   :align: center
   :alt: "Comment on a test case"
   :width: 800

Best practices
--------------

* **Set clear priorities** - Use task priorities to help team members focus on the most important work first
* **Provide detailed descriptions** - Include enough context in task descriptions so assignees understand what needs to be done
* **Assign appropriately** - Match tasks to team members based on their expertise (DS for technical issues, business experts for domain knowledge, etc.)
* **Resolve before publishing** - Always resolve all tasks before undrafting conversations to maintain dataset quality
* **Regular review** - Check task status regularly to ensure the review process is progressing

Next steps
----------

Now that you understand how to distribute tasks, you can:

* **Review test results** - Follow the business workflow to review evaluation results :doc:`/hub/ui/annotate/review_test_results`
* **Modify test cases** - Follow the product owner workflow to refine test cases :doc:`/hub/ui/annotate/modify_test_cases`

