:og:title: Giskard Open Source - Models Reference
:og:description: Documentation for model classes and testing utilities in Giskard open source library. Learn how to wrap, test, and evaluate your LLM agents.

Models
===============================================

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
