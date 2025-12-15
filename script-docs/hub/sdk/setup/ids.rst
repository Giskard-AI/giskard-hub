:og:title: Giskard Hub SDK - Configure API keys and find entity IDs
:og:description: Configure API keys and find entity IDs programmatically. Set up workspaces, configure access controls, and manage team collaboration through the comprehensive Python SDK.

Find API keys and resource IDs
==============================

In this section, we will walk you through how to configure API keys and find entity IDs using the SDK.

Find API keys
-------------

You can find your API key and Hub URL in the Hub UI. After login, click your user badge in the bottom left corner and copy the "API Key" value.

.. image:: /_static/images/sdk/api-key.png
   :align: center
   :alt: "API key"
   :width: 800

You can configure the API key and Hub URL by setting the following environment variables:

.. code-block:: bash

    export GISKARD_HUB_URL="https://your-hub-url"
    export GISKARD_HUB_TOKEN="your-token"

Alternatively, you can pass these values directly to the client:

.. code-block:: python

    hub = HubClient(
        url="https://your-hub-url",
        token="your-token"
    )

Find resource IDs
-----------------

You can find the resource IDs by listing the resources through the SDK like shown below:

.. code-block:: python

    resources = hub.my_resource.list()
    print(resources)

Instead, you can also get a specific resource throught the URL when viewing the resource in the Hub UI.

You would then navigate to the resource URL and copy the ID from the URL.

``https://demo.giskard.cloud/p/<my-uuid-id>/dashboard``

For example: 

``https://demo.giskard.cloud/p/d4893f62-ade9-449a-8684-685e7c954edd/dashboard``     

In this case, the resource ID is ``d4893f62-ade9-449a-8684-685e7c954edd``.