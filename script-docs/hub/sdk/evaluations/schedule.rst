:og:title: Giskard Hub SDK - Scheduled Evaluations
:og:description: Schedule evaluations to run automatically at regular intervals. Detect regressions in agent performance over time with automated testing workflows using the Python SDK.

Schedule evaluations
----------------------

You can schedule evaluations to run automatically at regular intervals. This is useful to detect regressions in your agent's performance over time.

As usual, let's initialize the Hub client and set our current project ID:

.. code-block:: python

    import os
    from giskard_hub import HubClient


    hub = HubClient()

    project_id = os.getenv("HUB_PROJECT_ID")

You can schedule evaluations using the ``hub.scheduled_evaluations.create()`` method. Example:

.. code-block:: python

    # Create a scheduled evaluation that runs every Monday at 9 AM (UTC)
    scheduled_eval = hub.scheduled_evaluations.create(
        name="Weekly Performance Check",
        project_id=project_id,
        model_id=model.id,
        dataset_id=dataset_id,
        frequency="weekly", # 'daily', 'weekly' or 'monthly'
        time="09:00", # HH:MM (24h format)
        day_of_week=1, # 1-7 (1 is Monday)
    )

.. note::

    The time of the evaluation is specified in the UTC timezone.

For detailed information about scheduled evaluations, see the :doc:`/hub/sdk/reference/resources/index` section.