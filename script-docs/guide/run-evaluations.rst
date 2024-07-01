===============
Run evaluations
===============

In this section, we will show how to start programmatically evaluation runs in
the Hub. For example, you may want to systematically launch evaluation runs
every time you deploy an updated model in a pre-production or staging
environment. In this way, you can collaborate with your team to ensure that the
model is performing as expected.


.. note:: In this section we will run evaluation against models configured in
    the Hub. If you want to evaluate a local model that is not yet exposed with
    an API, check the :doc:`local-evaluation`.

As usual, let's initialize the Hub client and set our current project ID:

.. code-block:: python

    import os
    from giskard_hub import HubClient

    hub = HubClient()

    project_id = os.getenv("HUB_PROJECT_ID")


Configure the model
-------------------

First, we need to configure the model that we want to evaluate. The model will
need to be accessible from a remote API endpoint.

We can configure the model endpoint in the Hub:

.. code-block:: python

    model = hub.models.create(
        project_id=project_id,
        name="MyBot (staging)",
        description="A chatbot that answers questions about the weather",
        url="https://my-bot.staging.example.com/chat",
        supported_languages=["en"],

        # if your model endpoint needs special headers:
        headers={"X-API-Key": "SECRET_TOKEN"},
    )


You can test that everything is working by sending a test request to the model

.. code-block:: python

    response = model.chat(messages=[{
        "role": "user",
        "content": "What's the weather like in Rome?"
    }])

    print(response)
    # ModelOutput(message=ChatMessage(role='assistant', content='It is sunny!'))


Launch a remote evaluation
--------------------------

Now that the model is configured, we can launch an evaluation run. We first need
to know which dataset we will run the evaluation on. If you are running this in
the CI/CD pipeline, we recommend setting the dataset ID in the environment.

.. code-block:: python

    dataset_id = os.getenv("HUB_EVAL_DATASET_ID")


We can now launch the evaluation run:

.. code-block:: python

    eval_run = hub.evaluate(
        model=model.id,
        dataset=dataset_id
        # optionally, specify a name
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


.. figure:: ../_static/quickstart/metrics_output.png
    :alt: Evaluation metrics output

    Evaluation metrics output

Once the evaluation is completed, may want to compare the results with some
thresholds to decide whether to promote the model to production or not.

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
this code in your CI/CD pipeline to automatically evaluate your models every
time you deploy a new version.

.. note:: If you want to run evaluations on a local model that is not yet
    exposed with an API, check the :doc:`local-evaluation`.