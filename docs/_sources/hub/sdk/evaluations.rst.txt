:og:title: Giskard Hub - Enterprise Agent Testing - Evaluations Management
:og:description: Run and manage LLM agent evaluations programmatically. Execute tests, schedule automated evaluations, and analyze results through the Python SDK.

============================
Run and schedule evaluations
============================

Evaluations are the core of the testing process in Giskard Hub. They allow you to run your test datasets against your agents and evaluate their performance using the checks that you have defined.

The Giskard Hub provides a comprehensive evaluation system that supports:

* **Synchronous evaluations**: Run evaluations immediately and get results in real-time
* **Asynchronous evaluations**: Schedule evaluations to run in the background
* **Batch evaluations**: Run multiple evaluations simultaneously
* **Scheduled evaluations**: Automatically run evaluations at specified intervals

In this section, we will walk you through how to run and manage evaluations using the SDK.

- An **evaluation** is a run of an agent on each chat test case (conversation) of a dataset using a set of checks.

We recommend to systematically launch evaluation runs every time you deploy an updated agent in a pre-production or staging environment. In this way, you can collaborate with your team to ensure that the agent is performing as expected.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to define the agent and dataset you want to evaluate, and run or schedule evaluations.

Run evaluations
~~~~~~~~~~~~~~~

There are two types of evaluations:

- **Remote evaluations** - In production, you will want to run evaluations against agents that are configured in the Hub and exposed with an API.
- **Local evaluations** - During the development phase, you may want to evaluate a local agent that is not yet exposed with an API before deploying it.


Run remote evaluations
----------------------

In production, you will want to run evaluations against agents that are configured in the Hub and exposed with an API.

Configure an agent
__________________

First, we need to configure the agent that we want to evaluate. The agent will
need to be accessible from a remote API endpoint.

We can configure the agent endpoint in the Hub:

.. code-block:: python

    agent = hub.models.create(
        project_id=project_id,
        name="MyAgent (staging)",
        description="An agent that answers questions about the weather",
        url="https://my-agent.staging.example.com/chat",
        supported_languages=["en"],

        # if your agent endpoint needs special headers:
        headers={"X-API-Key": "SECRET_TOKEN"},
    )

You can test that everything is working by sending a test request to the agent

.. code-block:: python

    response = model.chat(messages=[{
        "role": "user",
        "content": "What's the weather like in Rome?"
    }])

    print(response)
    # ModelOutput(message=ChatMessage(role='assistant', content='It is sunny!'))

Create a evaluation
___________________


Now that the agent is configured, we can launch an evaluation run. We first need
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


.. figure:: /_static/images/cli/metrics_output.png
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

.. note::

    If you want to run evaluations on a local model that is not yet exposed with an API, check :ref:`local-evaluation`.

Compare evaluations
___________________

After running evaluations, you can compare them to see if there are any regressions. We do not offer a built-in comparison tool in the SDK, but you can :ref:`use the Hub UI to compare evaluations <hub/ui/evaluations-compare>`.

.. _local-evaluation:

Run local evaluations
---------------------

During the development phase, you may want to **evaluate a local model** that is not yet exposed with an API.

Running the evaluation will allow you to compare the performance of your local
model with the one that is already in production, or with other models that you
use as a baseline. You will also be able to debug performance issues by
checking each chat test case (conversation) in the Hub inteface.

As usual, let's initialize the Hub client and set our current project ID:

.. code-block:: python

    import os
    from giskard_hub import HubClient


    hub = HubClient()

    project_id = os.getenv("HUB_PROJECT_ID")

Configure a model
_________________

To execute a local model, you just need to define a Python function. This
function should take a list of messages and return an output message.

Here is an example of a simple model that just echoes the last user message:

.. code-block:: python

    from typing import List
    from giskard_hub.data import ChatMessage


    def my_local_agent(messages: List[ChatMessage]) -> str:
        """A simple agent that echoes the last user message."""
        msg = messages[-1].content
        return f"You said: '{msg}'"

There are a few things to note here:

- The function takes a list of :class:`~giskard_hub.data.ChatMessage` objects as
  input. This object has two fields: `role` (e.g. "user" or "assistant") and
  `content` (the message content).

- The function should return a string or an instance of
  :class:`~giskard_hub.data.ModelOutput` (if you want more control)

- Include a **docstring that describes what the model does**. This is equivalent
  to the description of the model in the Hub and will be used to improve the
  reliability of evaluations.

- The name of the function (e.g. ``my_local_agent``) will be used as the model
  name when showing the evaluation run in the Hub.


You can check that everything works simply by running the function:

.. code-block:: python

    my_local_agent([ChatMessage(role="user", content="Hello")])
    # Output: "You said: 'Hello'"

Create a local evaluation
_________________________

Running the evaluation is similar to what we have seen for remote evaluations. Instead of passing a remote model ID to the
``evaluate`` method of the Hub client, we will pass the function we defined
above. The evaluation will be run locally, but the results will be stored in the
Hub.

Let's select the dataset we want to use for the evaluation.

.. code-block:: python

    dataset_id = os.getenv("HUB_EVAL_DATASET_ID")  # or directly set the ID

We can now launch the evaluation run:

.. code-block:: python

    eval_run = hub.evaluate(
        model=my_local_agent,
        dataset=dataset_id,
        # optionally, specify a name
        name="test-run",
    )

The evaluation run will be queued and processed by the Hub. As usual, wait for
the evaluation run to complete and then print the results:

.. code-block:: python

    # This will block until the evaluation is completed
    eval_run.wait_for_completion()

    # Print the metrics
    eval_run.print_metrics()

.. figure:: /_static/images/cli/metrics_output.png
    :alt: Evaluation metrics output

    Evaluation metrics output

You can also check the results in the Hub interface and compare it with other
evaluation runs.

.. hint::

    You may also want to use this method in your CI/CD pipeline, to perform checks when the code or the prompts of your agent get updated.

Evaluations
~~~~~~~~~~~

Create an evaluation
--------------------

You can create a new evaluation using the ``hub.evaluations.create()`` method.

.. code-block:: python

    eval_run = hub.evaluations.create(
        model_id=model.id,
        dataset_id=dataset.id,
        tags=["nightly", "regression"],
        run_count=1,
        name="nightly-regression-1"
    )

Retrieve an evaluation
----------------------

You can retrieve an evaluation using the ``hub.evaluations.retrieve()`` method.

.. code-block:: python

    eval_run = hub.evaluations.retrieve(eval_run.id)

Update an evaluation
--------------------

You can update an evaluation using the ``hub.evaluations.update()`` method.

.. code-block:: python

    eval_run = hub.evaluations.update(eval_run.id, tags=["staging", "build"])

Delete an evaluation
--------------------

You can delete an evaluation using the ``hub.evaluations.delete()`` method.

.. code-block:: python

    hub.evaluations.delete(eval_run.id)

List evaluations
----------------

You can list evaluations using the ``hub.evaluations.list()`` method.

.. code-block:: python

    eval_runs = hub.evaluations.list(project_id=project_id)

List evaluation results
-----------------------

You can list evaluation results using the ``hub.evaluations.list_entries()`` method.

.. code-block:: python

    eval_results = hub.evaluations.list_entries(eval_run.id)

Each evaluation entry contains detailed information about the test case execution, including the chat test case, model output, evaluation results, and optionally a failure category:

.. code-block:: python

    for entry in eval_results:
        print(f"Chat Test Case ID: {entry.chat_test_case.id}")

        # Check if there's a failure category assigned
        if entry.failure_category:
            category = entry.failure_category.category
            if category:
                print(f"Failure Category: {category.title}")
                print(f"Description: {category.description}")
            if entry.failure_category.error:
                print(f"Categorization Error: {entry.failure_category.error}")

        # Check evaluation results
        if not entry.results:
            print("No checks were run for this chat test case")
        for result in entry.results:
            print("-" * 50)
            print(f"Check: {result['name']}")
            print(f"Passed: {result['passed']}")
            print(f"Reason: {result['reason']}")
        print("*" * 50)





Scheduled evaluations
~~~~~~~~~~~~~~~~~~~~~

Create a scheduled evaluation
-----------------------------

You can create a scheduled evaluation using the ``hub.scheduled_evaluations.create()`` method. Here's a basic example:

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

List scheduled evaluations
--------------------------

You can list all scheduled evaluations using the ``hub.scheduled_evaluations.list()`` method. Here's a basic example:

.. code-block:: python

    scheduled_evals = hub.scheduled_evaluations.list(project_id=project_id)

    for scheduled_eval in scheduled_evals:
        print(f"{scheduled_eval.name}: {scheduled_eval.to_dict()}")

Update a scheduled evaluation
-----------------------------

To update a scheduled evaluation, you need to specify the model, dataset, and a cron expression for the schedule:

.. code-block:: python

    # Update a scheduled evaluation to pause it
    scheduled_eval = hub.scheduled_evaluations.update(
        scheduled_eval.id,
        paused=True
    )

Delete a scheduled evaluation
-----------------------------

You can delete a scheduled evaluation using the ``hub.scheduled_evaluations.delete()`` method.

.. code-block:: python

    hub.scheduled_evaluations.delete(scheduled_eval.id)

List evaluation runs linked to a scheduled evaluation
-----------------------------------------------------

Track the runs of your scheduled evaluations:

.. code-block:: python

    # Check run history
    evaluations = hub.scheduled_evaluations.list_evaluations(scheduled_eval.id)