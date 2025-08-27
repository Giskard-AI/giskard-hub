:og:title: Giskard Open Source - Models Reference
:og:description: Learn about the Model class in Giskard Open Source. Understand how to wrap and test different types of LLM models and AI systems.

==============================================
Models reference
==============================================

The Model class is a core component of Giskard Open Source that wraps different types of LLM models and AI systems for testing and evaluation.

.. automodule:: giskard.models

Integrations
------------

.. automodule:: giskard.models.langchain
    :members: LangchainModel

The :class:`giskard.Model` class
--------------------------------

.. autoclass:: giskard.Model

   .. automethod:: __new__
   .. automethod:: save_model
   .. automethod:: model_predict
   .. automethod:: load_model
