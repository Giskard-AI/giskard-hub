AI Business Failures
========================

Business vulnerabilities are failures that affect the business logic, accuracy, and reliability of AI systems. These include issues that impact the model's ability to provide accurate, reliable, and appropriate responses in normal usage scenarios.

Understanding Business Failures
---------------------------------

Business vulnerabilities differ from security vulnerabilities in that they focus on the model's ability to provide correct and grounded responses with respect to a knowledge base taken as ground truth. These failures can occur in Retrieval-Augmented Generation (RAG) systems and other AI applications where accuracy and reliability are critical for business operations.

.. tip::

    You can find examples of business vulnerabilities in our `RealPerformance dataset <https://realperformance.giskard.ai/>`_.

Types of Business Failures
---------------------------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Addition of Information
      :link: addition_of_information
      :link-type: doc

      The AI incorrectly adds information that was not present in the context of the groundedness check.

   .. grid-item-card:: Business Out of Scope
      :link: business_out_of_scope
      :link-type: doc

      The AI provides answers about products or services outside their defined business scope.

   .. grid-item-card:: Denial of answers
      :link: denial_of_answers
      :link-type: doc

      The AI incorrectly refuses to answer legitimate questions that are in scope.

   .. grid-item-card:: Hallucinations
      :link: hallucination
      :link-type: doc

      The AI generates information not present in your knowledge base.

   .. grid-item-card:: Moderation issues
      :link: moderation_issues
      :link-type: doc

      The AI incorrectly provides the wrong default moderation answer.

   .. grid-item-card:: Omission
      :link: omission
      :link-type: doc

      The AI incorrectly omits information that is present in the reference context.

Getting Started with Business Testing
-------------------------------------

To begin testing your AI systems for business failures:

.. grid:: 1 1 2 2

   .. grid-item-card:: Giskard Hub UI Business Dataset
      :link: /hub/ui/datasets/business
      :link-type: doc

      Our state-of-the-art enterprise-grade business failure testing.

   .. grid-item-card:: RAGET: RAG Evaluation Toolkit
      :link: /oss/sdk/business
      :link-type: doc

      Our open-source toolkit for business failure testing.

.. toctree::
   :maxdepth: 1
   :hidden:
   :glob:

   /start/glossary/business/*