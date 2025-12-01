:og:title: Giskard Hub SDK - Remote Model Evaluation
:og:description: Run evaluations against remote agents configured in the Hub. Execute comprehensive tests against production APIs and analyze performance metrics using the Python SDK.

Run remote evaluations
----------------------

This section will guide you through running evaluations against a remote model.

In production, you will want to run evaluations against agents that are configured in the Hub and exposed with an API.

As usual, let's initialize the Hub client and set our current project ID:

.. code-block:: python

    import os
    from giskard_hub import HubClient


    hub = HubClient()

    project_id = os.getenv("HUB_PROJECT_ID")


First, we need to configure the agent that we want to evaluate. The agent will
need to be accessible from a remote API endpoint. For more information about how to configure an agent, see :doc:`/hub/sdk/setup/agents`.

After configuring the agent, we can launch an evaluation run. We first need
to know which dataset we will run the evaluation on. If you are running this in
the CI/CD pipeline, we recommend setting the dataset ID in the environment.

.. code-block:: python

    dataset_id = os.getenv("HUB_EVAL_DATASET_ID")

We can now launch the evaluation run:

.. code-block:: python

    eval_run = hub.evaluations.create(
        model_id=model.id,
        dataset_id=dataset_id,
        # optionally,
        tags=["staging", "build"],
        run_count=1, # number of runs per case
        name="staging-build-a4f321",
    )

The evaluation run will be queued and processed by the Hub. The ``evaluate``
method will immediately return an :class:`~giskard_hub.data.EvaluationRun` object
while the evaluation is running. Note however that this object will not contain
the evaluation results until the evaluation is completed.

You can wait until the evaluation run has finished running with the
``wait_for_completion`` method:

.. code-block:: python

    eval_run.wait_for_completion(
        # optionally, specify a timeout in seconds (10 min by default)
        timeout=600
    )

This will block until the evaluation is completed and update the ``eval_run``
object in-place. The method will wait for up to 10 minutes for the
evaluation to complete. If the evaluation takes longer, the method will raise a
``TimeoutError``.

Then, you can print the results:

.. code-block:: python

    # Let's print the evaluation results
    eval_run.print_metrics()


.. figure:: /_static/images/sdk/evaluation-metrics-output.png
    :alt: Evaluation metrics output

    Evaluation metrics output

Once the evaluation is completed, may want to compare the results with some
thresholds to decide whether to promote the agent to production or not.

You can retrieve the metrics from ``eval_run.metrics``: this will contain a list
of :class:`~giskard_hub.data.Metric` objects.

For example:

.. code-block:: python
    :caption: CI/CD pipeline example

    import sys

    # make sure to wait for completion or the metrics may be empty
    eval_run.wait_for_completion()

    for metric in eval_run.metrics:
        print(metric.name, metric.percentage})

        if metric.percentage < 90:
            print(f"FAILED: {metric.name} is below 90%.")
            sys.exit(1)

That covers the basics of running evaluations in the Hub. You can now integrate
this code in your CI/CD pipeline to automatically evaluate your agents every
time you deploy a new version.

.. tip::

    If you want to run evaluations on a local model that is not yet exposed with an API, check :doc:`/hub/sdk/evaluations/local`.

