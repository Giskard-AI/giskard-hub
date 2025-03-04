====================
Create custom checks
====================

This section guides you through creating custom checks. 

Custom checks are built on top of the built-in checks (Conformity, Correctness, Groundedness and String matching) and can be used to evaluate the quality of your agent's responses. 

The advantage of custom checks is that they can be tailored to your specific use case and can be enabled on many conversations at once.

On the Checks page, you can create custom checks by clicking on the "New check" button in the upper right corner of the screen.

.. image:: /_static/images/hub/create-checks-list.png
   :align: center
   :alt: "List of checks"
   :width: 800

Next, set the parameters for the check:

- ``Name``: Give your check a name.
- ``Identifier``: A unique identifier for the check. It should be a string without spaces.
- ``Description``: A brief description of the check.
- ``Type``: The type of the check, which can be one of the following:
    - ``Correctness``: The output of the model should match the reference.
    - ``Conformity``: The conversation should follow a set of rules.
    - ``Groundedness``: The output of the model should be grounded in the conversation.
    - ``String match``: The output of the model should contain a specific string (keyword or sentence).
- And a set of parameters specific to the check type. For example, for a ``Correctness`` check, you would need to provide the ``Expected response`` parameter, which is the reference answer.

.. image:: /_static/images/hub/create-checks-detail.png
   :align: center
   :alt: "Create a new check"
   :width: 800

Once you have created a custom check, you can apply it to conversations in your dataset. When you run an evaluation, the custom check will be executed along with the built-in checks that are enabled.

