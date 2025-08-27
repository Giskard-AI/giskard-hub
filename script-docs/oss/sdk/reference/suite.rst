:og:title: Giskard Open Source - Test Suite Reference
:og:description: Learn about the TestSuite class in Giskard Open Source. Understand how to create, run, and manage comprehensive test suites for LLM evaluation.

=============
Test suite reference
=============

The TestSuite class is a core component of Giskard Open Source that allows you to organize and run multiple tests together.

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