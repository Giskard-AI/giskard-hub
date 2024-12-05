===================
Generate a dataset
===================

This section guides you through generating a test dataset when you don’t have one at your disposal.

On the Datasets page, click “Automatic generation” on the upper right corner of the screen. This will open a modal that provides you with two options: Conformity or Correctness.

In the Conformity tab, you can generate a dataset specific to testing whether your chatbot abides by the rules.

.. image:: /_static/images/hub/generate-dataset-conformity.png
   :align: center
   :alt: "Generate conformity dataset"

- ``Model``: Select the model you want to use for evaluating this dataset.

- ``Description``: Provide details about your model to help generate more relevant examples.

- ``Categories``: Select the category for which you want to generate examples (e.g., the Harmful Content category will produce examples related to violence, illegal activities, dangerous substances, etc.).

- ``Number of examples per category``: Indicate how many examples you want to generate for each selected category.

Generating a dataset with the Correctness metric is similar to Conformity, but there is no need to select a category, and the number of examples is specified per topic instead.

.. image:: /_static/images/hub/generate-dataset-correctness.png
   :align: center
   :alt: "Generate correctness dataset"

However, dataset generation requires two additional pieces of information:

- ``Knowledge Base``: Choose the knowledge base you want to use as a reference.

- ``Topics``: Select the topics within the chosen knowledge base from which you want to generate examples.