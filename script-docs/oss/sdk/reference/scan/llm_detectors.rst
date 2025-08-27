:og:title: Giskard Open Source - LLM Detectors Reference
:og:description: Learn about LLM detectors in Giskard Open Source. Understand how to use and configure security detectors for vulnerability detection.

=======================
LLM detectors reference
=======================

LLM detectors are specialized components that identify specific types of security vulnerabilities in LLM models.


Injection attacks
-----------------

.. autoclass :: giskard.scanner.llm.LLMCharsInjectionDetector
   :members:
   :show-inheritance:

.. autoclass :: giskard.scanner.llm.LLMPromptInjectionDetector
   :members:
   :show-inheritance:

Hallucination & misinformation
------------------------------

.. autoclass :: giskard.scanner.llm.LLMBasicSycophancyDetector
   :members:
   :show-inheritance:

.. autoclass :: giskard.scanner.llm.LLMImplausibleOutputDetector
   :members:
   :show-inheritance:


Harmful content generation
--------------------------

.. autoclass :: giskard.scanner.llm.LLMHarmfulContentDetector
   :members:
   :show-inheritance:

Stereotypes
-----------

.. autoclass :: giskard.scanner.llm.LLMStereotypesDetector
   :members:
   :show-inheritance:


Information disclosure
----------------------

.. autoclass :: giskard.scanner.llm.LLMInformationDisclosureDetector
   :members:
   :show-inheritance:

Output formatting
-----------------

.. autoclass :: giskard.scanner.llm.LLMOutputFormattingDetector
   :members:
   :show-inheritance: