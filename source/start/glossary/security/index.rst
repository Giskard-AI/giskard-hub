AI Security Vulnerabilities
===========================

Security vulnerabilities in AI systems represent critical weaknesses that can be exploited by malicious actors to compromise system integrity, extract sensitive information, or manipulate model behavior for harmful purposes.

Understanding Security Vulnerabilities
---------------------------------------

Security vulnerabilities differ from business failures in that they focus on malicious exploitation and system integrity rather than accuracy and reliability. These vulnerabilities can lead to data breaches, privacy violations, system manipulation, and other security incidents that pose significant risks to organizations and users.

.. tip::

    You can find examples of security vulnerabilities in our `RealHarm dataset <https://realharm.giskard.ai/>`_.

Types of Security Vulnerabilities
---------------------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Prompt Injection
      :link: injection
      :link-type: doc

      A security vulnerability where malicious input manipulates the model's behavior or extracts sensitive information.

   .. grid-item-card:: Harmful Content Generation
      :link: harmful_content
      :link-type: doc

      Production of violent, illegal, or inappropriate material by AI models.

   .. grid-item-card:: Information Disclosure
      :link: information_disclosure
      :link-type: doc

      Revealing internal system details, training data, or confidential information.

   .. grid-item-card:: Output Formatting Issues
      :link: formatting
      :link-type: doc

      Manipulation of response structure for malicious purposes or poor output formatting.

   .. grid-item-card:: Robustness Issues
      :link: robustness
      :link-type: doc

      Vulnerability to adversarial inputs or edge cases causing inconsistent behavior.

   .. grid-item-card:: Stereotypes & Discrimination
      :link: stereotypes
      :link-type: doc

      Biased responses that perpetuate harmful stereotypes and discriminatory behavior.

Getting Started with Security Testing
-------------------------------------

To begin securing your AI systems:

.. grid:: 1 1 2 2

   .. grid-item-card:: Giskard Hub UI Security Dataset
      :link: /hub/ui/datasets/security
      :link-type: doc

      Our state-of-the-art enterprise-grade security vulnerability testing.

   .. grid-item-card:: LLM Scan
      :link: /oss/sdk/security
      :link-type: doc

      Our open-source toolkit for security vulnerability testing.

.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:

   /start/glossary/security/*