===================
Generate a dataset
===================

This section guides you through generating a test dataset when you don't have one at your disposal.

On the Datasets page, click "Automatic generation" on the upper right corner of the screen. This will open a modal that provides you with two options: Adversarial or Document Based.

In the Adversarial tab, you can generate a dataset specific to testing whether your chatbot abides by the rules.

.. image:: /_static/images/hub/generate-dataset-adversarial.png
   :align: center
   :alt: "Generate adversarial dataset"
   :width: 800

- ``Dataset name``: Provide a name for the dataset.

- ``Model``: Select the model you want to use for evaluating this dataset.

- ``Description``: Provide details about your model to help generate more relevant examples.

- ``Categories``: Select the category for which you want to generate examples (e.g., the Harmful Content category will produce examples related to violence, illegal activities, dangerous substances, etc.).

- ``Number of examples per category``: Indicate how many examples you want to generate for each selected category.

On the other hand, the Document Based tab allows you to generate a dataset with examples based on your knowledge base.

.. image:: /_static/images/hub/generate-dataset-document-based.png
   :align: center
   :alt: "Generate document based dataset"
   :width: 800

However, in this case, dataset generation requires two additional pieces of information:

- ``Knowledge Base``: Choose the knowledge base you want to use as a reference.

- ``Topics``: Select the topics within the chosen knowledge base from which you want to generate examples.