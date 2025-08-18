===============
Manage Projects
===============

In this section, we will show how to manage projects programmatically using the SDK.

- A **project** is a collection of models, datasets, and evaluations

Let's start by initializing the Hub client or take a look at the :doc:`/hub/sdk/index` section to see how to install the SDK and connect to the Hub.

.. code-block:: python

    from giskard_hub import HubClient

    hub = HubClient()

You can now use the ``hub`` client to create, update, and delete projects.

Create a project
________________

You can create a project using the ``hub.projects.create()`` method. Here's a basic example:

.. code-block:: python

    project = hub.projects.create(
        name="My first project",
        description="This is a test project to get started with the Giskard Hub client library",
    )

Retrieve a project
__________________

You can retrieve a project using the ``hub.projects.retrieve()`` method. Here's a basic example:

.. code-block:: python

    project = hub.projects.retrieve("<PROJECT_ID>")

Update a project
________________

You can update a project using the ``hub.projects.update()`` method. Here's a basic example:

.. code-block:: python

    project = hub.projects.update("<PROJECT_ID>", name="My updated project")

Delete a project
________________

You can delete a project using the ``hub.projects.delete()`` method. Here's a basic example:

.. code-block:: python

    hub.projects.delete("<PROJECT_ID>")

List projects
_____________

You can list all projects using the ``hub.projects.list()`` method. Here's a basic example:

.. code-block:: python

    projects = hub.projects.list()

    for project in projects:
        print(project.name)