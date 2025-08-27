:og:title: Giskard Hub - Enterprise Agent Testing - Access Rights
:og:description: Configure role-based access control, manage user permissions, and ensure secure collaboration across your organization's LLM agent testing projects.

==================
Set access rights
==================

This section provides guidance on managing users in the Hub.

The Hub allows you to set access rights at two levels: global and scoped for both users and groups. To begin, click on the "Settings" icon on the left panel, then select "Users".

Configure users and groups
--------------------------

.. tab-set::

   .. tab-item:: User-level permissions

      To manage user-level permissions, click the "Account" icon in the upper right corner of the screen, then select "Settings." From the left panel, choose "Users" and then press "Users" in the dropdown.

      .. image:: /_static/images/hub/access-settings.png
         :align: center
         :alt: "Access rights"
         :width: 800

   .. tab-item:: Group-level permissions

      To manage group-level permissions, click the "Account" icon in the upper right corner of the screen, then select "Settings." From the left panel, choose "Users" and then press "Groups" in the dropdown.

      .. image:: /_static/images/hub/access-settings-group.png
         :align: center
         :alt: "Access rights"
         :width: 800

      After creating a group and users, you can then navigate back to the "Users" tab from the left panel. You can then select a user you want to add to a group, click the three vertical dots on the right side of the user box, and click on "Edit Group".

      .. image:: /_static/images/hub/access-settings-group-user.png
         :align: center
         :alt: "Access rights"
         :width: 800

      This will open a pop up where you can select the group you want to add the user to.

      .. image:: /_static/images/hub/access-settings-group-assign.png
         :align: center
         :alt: "Access rights"
         :width: 800



Configure Global Permissions
____________________________

Global permissions apply access rights across all projects. You can configure Create, Read, Edit, and Delete permissions for each page or entity. This is available in the following pages: Project, Dataset, Agent, Knowledge Base, and Evaluation. Additionally, for features like the Playground, API Key Authentication, and Permission, you can enable or disable the users’ right to use it.

The rights are as follows:

- **Create**: users can create a new entity of the given type.

- **Read**: users can see entities of the given type.

- **Edit**: users can modify entities of the given type.

- **Delete**: users can permanently remove entities of the given type.

- **Use**: users can use the given feature.

.. image:: /_static/images/hub/access-permissions.png
   :align: center
   :alt: "Set permissions"
   :width: 800

Configure Scoped Permissions
____________________________

Scoped permissions allow for granular control. For each project, you can specify which pages or entities users are allowed to access. An example of where this may be useful is if you want your users to read everything in a project but only allow a few people to edit the dataset.

.. image:: /_static/images/hub/access-scope.png
   :align: center
   :alt: "Set scope of permissions"
   :width: 800

.. note::

    Users need to log in first before an admin can give them any permissions in the Hub.