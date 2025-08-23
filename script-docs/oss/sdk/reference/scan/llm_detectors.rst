:og:description: LLM Detectors Reference - Documentation for security detectors in LLM Scan. Learn about prompt injection, data leakage, and other security threat detection mechanisms.

Detectors for LLM models
========================


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