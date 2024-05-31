Quick start
===========

Installation
------------

The library is compatible with Python 3.9 to 3.12.

.. code-block:: bash
   :caption: Shell

   pip install giskard-hub


Getting an API key
------------------

Head over to your Giskard Hub instance and click on the user icon in the top right corner. You will find your personal
API key, click on the button to copy it.

.. image:: /_static/quickstart/api_key.png
   :width: 779px
   :scale: 50%
   :align: center
   :alt: ""

.. note::

   If you don't see your API key in the UI, it means your administrator has not enabled API keys. Please contact them to get one. 


Configuring your environment
----------------------------

You can set the following environment variables to avoid passing them as arguments to the client:

.. code-block:: bash
   :caption: Shell

   export GSK_API_KEY=your_api_key
   export GSK_HUB_URL=https://your-giskard-hub-instance.com/



Interact with the Hub programmatically
--------------------------------------

@TODO:
- Create a dataset
- Add a conversation
- Setting up a model


You can now configure the client to interact with the Hub. Start by initializing a client:

.. code-block:: python

    from giskard_hub.client import HubClient

    client = HubClient()

If you didn't set up the environment variables, you can provide the API key and Hub URL directly:

.. code-block:: python

    client = HubClient(
        api_key="YOUR_GSK_API_KEY",
        hub_url="THE_GSK_HUB_URL",
    )

You can retrieve projects, models, or datasets from the server:

.. code-block:: python

    projects = client.get_projects()
    models = client.get_models(project.id)
    dataset = client.get_datasets(project.id)


You can launch an evaluation programmatically:

.. code-block:: python

    evaluation = client.evaluate(
        project_id=project.id,
        model_id=model.id,
        dataset_id=dataset.id,
    )

    print(evaluation)

