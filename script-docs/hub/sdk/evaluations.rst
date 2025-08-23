:og:description: Run Evaluations (SDK) - Run and schedule LLM evaluations programmatically. Execute tests in the Hub or locally, analyze results, and manage evaluation workflows through the Python SDK.

=============================
Run and Schedule Evaluations
=============================

In this section, we will show how to start programmatically evaluation runs in the Hub.

- An **evaluation** is a run of an agent on each conversation of a dataset using a set of checks.

We recommend to systematically launch evaluation runs every time you deploy an updated agent in a pre-production or staging environment. In this way, you can collaborate with your team to ensure that the agent is performing as expected.

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to define the agent and dataset you want to evaluate, and run or schedule evaluations.

Run Evaluations
~~~~~~~~~~~~~~~

There are two types of evaluations:

- **Remote evaluations** - In production, you will want to run evaluations against agents that are configured in the Hub and exposed with an API.
- **Local evaluations** - During the development phase, you may want to evaluate a local agent that is not yet exposed with an API before deploying it.


Run remote evaluations
----------------------

In production, you will want to run evaluations against agents that are configured in the Hub and exposed with an API.

Configure an Agent
__________________

First, we need to configure the agent that we want to evaluate. The agent will
need to be accessible from a remote API endpoint.

We can configure the agent endpoint in the Hub:

.. code-block:: python

    agent = hub.agents.create(
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

    response = agent.chat(messages=[{
        "role": "user",
        "content": "What's the weather like in Rome?"
    }])

    print(response)
    # ModelOutput(message=ChatMessage(role='assistant', content='It is sunny!'))


Run an evaluation
_________________

Now that the agent is configured, we can launch an evaluation run. We first need
to know which dataset we will run the evaluation on. If you are running this in
the CI/CD pipeline, we recommend setting the dataset ID in the environment.

.. code-block:: python

    dataset_id = os.getenv("HUB_EVAL_DATASET_ID")


We can now launch the evaluation run:

.. code-block:: python

    eval_run = hub.evaluate(
        model=agent.id,  # Note: parameter is still named 'model' for backward compatibility
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

.. note:: If you want to run evaluations on a local model that is not yet
    exposed with an API, check :ref:`local-evaluation`.

Compare evaluations
___________________

After running evaluations, you can compare them to see if there are any regressions. We do not offer a built-in comparison tool in the SDK, but you can :ref:`use the Hub UI to compare evaluations <compare-evaluations>`.

.. _local-evaluation:

Run local evaluations
---------------------

During the development phase, you may want to **evaluate a local model** that is not yet exposed with an API.

Running the evaluation will allow you to compare the performance of your local
model with the one that is already in production, or with other models that you
use as a baseline. You will also be able to debug performance issues by
checking each conversation in the Hub inteface.

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

Run an evaluation
_________________

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

.. hint::  You may also want to use this method in your CI/CD pipeline, to
    perform checks when the code or the prompts of your agent get updated.

Schedule Evaluations
~~~~~~~~~~~~~~~~~~~~

At the moment, scheduling evaluations is not supported with the SDK, we recommend using the Giskard Hub UI for doing this.