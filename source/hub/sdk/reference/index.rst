:og:title: Giskard Hub - Enterprise Agent Testing - SDK Reference
:og:description: Access complete API documentation for the enterprise Hub Python SDK. Find detailed information about all classes, methods, and resources for programmatic LLM agent testing.

===============================================
API reference
===============================================

These docs are automatically generated from the ``giskard_hub`` library.

.. toctree::
   :hidden:
   :maxdepth: 1

   client
   entities/index
   resources/index

.. card:: Client
   :link: client
   :link-type: doc

   The client is the main entry point for interacting with the Giskard API.

.. card:: Entities
   :link: entities/index
   :link-type: doc

   The data representation of the Hub entities, such as projects, datasets, and evaluations.

.. card:: Resources
   :link: resources/index
   :link-type: doc

   The resource classes providing access to the various entities from the :class:`~giskard_hub.client.HubClient` e.g. ``client.projects``.

.. card:: Server endpoints

   Our API relies on FastAPI and is documented using OpenAPI. You can access the interactive API documentation directly in your browser at:

   `https://your-hub-url/_api/docs <https://your-hub-url/_api/docs>`__