:og:title: Giskard Hub UI - Track changes with Event logs
:og:description: Track every change made to entities in Giskard Hub with comprehensive event logs. View complete history of modifications to checks, datasets, and test cases for full traceability.

==================================
Track event logs
==================================

Event logs provide full traceability for all changes made to entities within Giskard Hub. This feature allows you to keep track of every change that every person has made on every entity, providing complete audit trails for your evaluation configurations.

|

.. raw:: html

   <iframe width="100%" height="400" src="https://www.youtube.com/embed/W_9MhdmHouk?si=0cW-jUuMaO8lifS5" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

**Why use event logs?**

Event logs are essential for maintaining accountability and understanding the evolution of your evaluation setup. They help you:

* **Track changes** - See what has been modified on any entity
* **Identify authors** - Know who made each change
* **Understand impact** - Recognize how changes affect your evaluations
* **Maintain compliance** - Keep complete audit trails for regulatory requirements
* **Enable rollback** - Understand changes to potentially revert them if needed

Event logs overview
-------------------

To begin, click on the "Settings" icon on the left panel, then select "Event logs".

.. image:: /_static/images/hub/event-logs.png
   :align: center
   :alt: "Event logs"
   :width: 100%

Every entity in Giskard Hub maintains a complete history of all modifications. This includes:

* **Checks** - Custom validation rules and their configurations
* **Datasets** - Test case collections and their metadata
* **Evaluation test cases** - Individual test cases within evaluations
* **Other entities** - All project-related entities track their changes

Each change is recorded with:

* **What changed** - The specific field or property that was modified
* **Who made the change** - The user who performed the action
* **When it changed** - Timestamp of the modification
* **Change details** - Description of the modification

Viewing event history
_____________________

To view the event history for a specific entity in the Event logs overview:

1. Navigate to the entity you want to inspect (e.g., a check, dataset, or test case)
2. Click the **History** button
3. Review the list of changes

.. image:: /_static/images/hub/event-logs-history.png
   :align: center
   :alt: "Event logs history"
   :width: 100%

Event logs for specific entities
--------------------------------

Every entity in Giskard Hub maintains a complete history of all modifications. This includes:

* **Checks** - Custom validation rules and their configurations
* **Datasets** - Test case collections and their metadata
* **Evaluation test cases** - Individual test cases within evaluations
* **Other entities** - All project-related entities track their changes

Viewing event history
_____________________

To view the event history for any entity:

1. Navigate to the entity you want to inspect (e.g., a check, dataset, test case, etc.)
2. Open the entity to view its details
3. Click the **History** button
4. Review the list of all changes

Underneath you can view an example of the event history for a check.

.. image:: /_static/images/hub/event-logs-conversations.png
   :align: center
   :alt: "Event logs history conversations"
   :width: 100%

Best practices
--------------

* **Review history regularly** - Check event logs when investigating evaluation results
* **Monitor critical entities** - Pay special attention to changes in checks and datasets that affect production evaluations
* **Coordinate with team** - Review event logs before making major changes to understand recent modifications

Next steps
----------

Now that you understand event logs, you can:

* **Review entity histories** - Check the history of your checks, datasets, and test cases
* **Investigate changes** - Use event logs to debug evaluation issues
* **Maintain traceability** - Keep complete audit trails of all modifications

For more information about working with specific entity types, see:

* :doc:`/hub/ui/annotate/checks` - Learn about checks and validation rules
* :doc:`/hub/ui/datasets/index` - Understand dataset management
* :doc:`/hub/ui/evaluations/index` - Explore evaluation workflows

