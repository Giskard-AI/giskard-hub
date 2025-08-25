:og:title: Giskard Open Source - Test Suite Reference
:og:description: Documentation for test suite classes and utilities in Giskard open source library. Learn how to organize and run comprehensive test suites for LLM agent evaluation.

Test suite
==============

.. autoclass:: giskard.Suite

   .. automethod:: __init__
   .. automethod:: run
   .. automethod:: add_test
   .. automethod:: add_test
   .. automethod:: save
   .. automethod:: load
   .. automethod:: to_unittest
   .. automethod:: remove_test
   .. automethod:: upgrade_test
   .. automethod:: update_test_params

.. autoclass:: giskard.core.suite.SuiteInput

.. autoclass:: giskard.core.suite.DatasetInput

.. autoclass:: giskard.core.suite.ModelInput

.. autoclass:: giskard.core.suite.TestSuiteResult

.. autoclass:: giskard.core.test_result.TestResult