:og:title: Giskard Hub UI - Task Management and Work Distribution
:og:description: Manage and distribute work among team members with Tasks. Assign tasks for reviewing scan results, evaluation runs, and test cases to ensure quality and collaboration.

====================================================
Distribute review tasks for probes and tests
====================================================

Tasks allow you to manage and distribute work among you and your coworkers. 

|

.. raw:: html

   <iframe width="100%" height="400" src="https://www.youtube.com/embed/u5ctBhfArNY?si=76o_0VIQzdPXFELk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

This feature is particularly useful when you need to:

* Ask an AI developer to correct the agent if there's a failure
* Ask business experts to review the rules of a check
* Coordinate review workflows for scan results and evaluation runs
* Ensure quality control before publishing test cases

Tasks overview
--------------

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

Create tasks from scan results
_______________________________

When reviewing scan results, you can create tasks to track and assign work items.

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

Create tasks from evaluation runs
__________________________________

Similar to scan results, you can create tasks when reviewing evaluation runs.

To create a task from an evaluation run by:

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

Setting conversations to draft
------------------------------

An important feature related to tasks is the ability to set conversations to draft. This ensures that conversations are not reused in subsequent evaluation runs before they are properly reviewed and approved.

When you go to the conversation linked to an evaluation run and create a task, you can set the linked failed test case to draft status. Before using it again, you need to resolve all associated tasks. 
Similarly, you can select a conversation from a dataset and set it to draft status. 

.. image:: /_static/images/hub/tasks-draft.png
   :align: center
   :alt: "Set a conversation to draft status"
   :width: 800

This workflow ensures that:

* Subsequent evaluation runs don't reuse conversations before they're published
* Your evaluation metrics remain unbiased
* Quality control is maintained throughout the review process

How to iterate on tasks?
------------------------

Tasks are designed to help team members review datasets without needing to modify technical test configurations. This workflow enables team members to contribute to quality assurance even if they don't understand the technical details of checks, evaluation metrics, or LLM-as-a-judge configurations.

Analyze the failures
____________________

When reviewing evaluation results, start by analyzing the failed test cases:

1. Review the **Results** - Understand what the agent output was
2. Review the **Explanation** - See why the test failed
3. Review the **Checks** - Understand what evaluation criteria were applied

Open tasks
__________

Based on your analysis, determine if the failed test case is relevant:

**If the failed test case is relevant (true positive):**

- Assign it to a **Data Scientist**: They can fix the agent or improve the model
- Assign it to a **Knowledge Base Manager**: They can update the knowledge base if information is missing or incorrect

**If the failed test case is not relevant (false positive):**

1. If you do have the required knowledge and you are sure, open a task and put the test case in **draft** and start the review process
2. If you don'thave the required knowledge or you are sure, describe the issue of the test case and assign it to the **Data Scientist** so they can change the test case

   The Data Scientist has two options:

   a. **Remove the test case** - If it's not relevant to your use case

   b. **Rewrite the test case** - If the test case concept is valid but needs adjustment:

      i. If you agree with the check: rewrite only the requirements of the test (expected outputs, etc.), then test it

      ii. If you don't agree with the check: change the check itself:

         * Create a new check that better matches your requirements
         * Test the new check

.. mermaid::
   :align: center

   graph TD
       A[Failed Test Case] --> B{Is it relevant?}
       B -->|True Positive| C[Assign to DS]
       B -->|True Positive| D[Assign to KB Manager]
       B -->|False Positive| E[Set to Draft]
       E --> F{Have business knowledge?}
       F -->|No| G[Assign to Business Expert]
       F -->|Yes| H[Describe Issue]
       H --> I[Assign to DS]
       I --> J{Action Needed}
       J --> K[Remove Test Case]
       J --> L[Rewrite Test Case]
       L --> M{Agree with Check?}
       M -->|Yes| N[Rewrite Requirements]
       M -->|No| O[Change Check]
       N --> P[Test]
       O --> Q[Create New Check]
       Q --> P

Follow the review
_________________

Once tasks are created, follow the review process:

1. **Open the task and view it** - Check the current status and any updates
2. **Add your input** - Provide feedback, comments, or additional context
3. **Assign the right people** - Make sure the task is assigned to the appropriate team members
4. **Close the task** - When the work is complete
5. **Undraft the conversation** - Once all tasks are resolved, you can undraft the conversation to make it available for future evaluation runs

Progressively add the test cases you put in draft back to your dataset as they are reviewed and approved.

.. mermaid::
   :align: center

   graph LR
       A[Task Created] --> B[Review Task]
       B --> C[Add Input]
       C --> D[Assign People]
       D --> E[Work Completed]
       E --> F[Close Task]
       F --> G{All Tasks Resolved?}
       G -->|No| B
       G -->|Yes| H[Undraft Conversation]
       H --> I[Available for Evaluations]


Benefits of using tasks
-----------------------

Tasks provide several key benefits for managing evaluation workflows:

* **Quality assurance** - Ensure all test cases are reviewed before being used in evaluations
* **Team collaboration** - Distribute work among team members based on their expertise
* **Traceability** - Track who is responsible for what and when work is completed
* **Dataset reliability** - Prevent biased evaluation metrics by ensuring conversations are properly reviewed
* **Workflow control** - Manage the review process systematically without missing any evaluations

Best practices
--------------

* **Set clear priorities** - Use task priorities to help team members focus on the most important work first
* **Provide detailed descriptions** - Include enough context in task descriptions so assignees understand what needs to be done
* **Assign appropriately** - Match tasks to team members based on their expertise (DS for technical issues, business experts for domain knowledge)
* **Resolve before publishing** - Always resolve all tasks before undrafting conversations to maintain dataset quality
* **Regular review** - Check task status regularly to ensure the review process is progressing

Next steps
----------

Now that you understand how to use tasks, you can:

* **Create tasks for scan results** - Assign work items when reviewing scan results
* **Create tasks for evaluation runs** - Track review work for evaluation test cases
* **Manage draft conversations** - Ensure quality before publishing test cases
* **Coordinate team reviews** - Distribute work among team members effectively

For more information about related features, see:

* :doc:`/hub/ui/annotate/conversations` - Learn about test cases and conversations
* :doc:`/hub/ui/annotate/checks` - Understand evaluation checks and validation rules
* :doc:`/hub/ui/evaluations/index` - Explore evaluation workflows

