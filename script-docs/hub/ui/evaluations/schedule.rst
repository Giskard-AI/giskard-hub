
:og:title: Giskard Hub UI - Scheduled Evaluations
:og:description: Schedule evaluations to run automatically at regular intervals. Detect regressions in agent performance over time with automated testing workflows and comprehensive monitoring.

Schedule evaluations
====================

You can schedule evaluations to run automatically at regular intervals. This is useful to detect regressions in your agent's performance over time.

On the Evaluations page, click on the "Schedule" tab. This will display a list of all the scheduled evaluations.

.. image:: /_static/images/hub/evaluation-schedule-list.png
   :align: center
   :alt: "Evaluation schedule list"
   :width: 800

To create a new scheduled evaluation, click on the "Schedule Evaluation" button in the upper right corner of the screen.

.. image:: /_static/images/hub/evaluation-schedule.png
   :align: center
   :alt: "Evaluation schedule"
   :width: 800

Next, set the parameters for the evaluation:

- ``Name``: Give your evaluation a name.

- ``Agent``: Select the agent you want to evaluate.

- ``Dataset``: Choose the dataset you want to use for the evaluation.

- ``Tags`` (optional): Limit the evaluation to a specific subset of the dataset by applying tags.

- ``Number of runs``: Select the number of runs that need to pass for each evaluation entry.

- ``Frequency``: Select the frequency for the evaluation.

- ``Time``: Select the time for the evaluation. (This time is based on the time zone of the server where the Giskard Hub is installed.)

After filling the form, click on the "Schedule evaluation" button, which will create the evaluation run and schedule it to run at the specified frequency and time.

