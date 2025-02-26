==================
Set access rights
==================

This section provides guidance on managing users in the Hub.

The Hub allows you to set access rights at two levels: global and scoped. To begin, click on the "Settings" icon on the left panel, then select "Users".

click the "Account" icon in the upper right corner of the screen, then select "Settings." From the left panel, choose "User Management."

.. image:: /_static/images/hub/access-settings.png
   :align: center
   :alt: "Access rights"
   :width: 800

Global permissions apply access rights across all projects. You can configure Create, Read, Edit, and Delete permissions for each page or entity. This is available in the following pages: Project, Dataset, Model, Knowledge Base, and Evaluation. Additionally, for features like the Playground, API Key Authentication, and Permission, you can enable or disable the users’ right to use it.

The rights are as follows:

- **Create**: users can create a new item specific to the page.

- **Read**: users can see the items created in the page.

- **Edit**: users can modify the items in the page.

- **Delete**: users can permanently remove the items in the page.

- **Use**: users can use the feature.

.. image:: /_static/images/hub/access-permissions.png
   :align: center
   :alt: "Set permissions"
   :width: 800

Scoped permissions allow for more granular control. For each project, you can specify which pages or entities users are allowed to access. An example of where this may be useful is if you want your users to read everything in a project but only allow a few people to edit the dataset.

.. image:: /_static/images/hub/access-scope.png
   :align: center
   :alt: "Set scope of permissions"
   :width: 800

.. note::

    Users need to first login before an admin can give them any permissions in the Hub.