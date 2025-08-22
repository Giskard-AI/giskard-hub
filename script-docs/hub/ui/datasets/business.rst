======================================================
Detect Business Failures by Generating Synthetic Tests
======================================================

Generative AI agents can face an endless variety of real-world scenarios, making it impossible to manually enumerate all possible test cases. Automated, synthetic test case generation is therefore essential—especially when you lack real user conversations to import as tests. However, a major challenge is to ensure that these synthetic cases are tailored to your business context, rather than being overly generic.

By generating domain-specific synthetic tests, you can proactively identify and address these types of failures before they impact your users or business operations.

In this section, we will walk you through how to generate synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

What are AI business failures?
------------------------------

AI business failures are failures that are related to the business of the AI system. To detect them, we need to generate tests that are designed to trigger failures.

The Giskard Hub provides an interface for the synthetic generation of legitimate queries **with expected outputs**. It automatically clusters the documents from the internal knowledge base into key topics and generates test cases for each topic by applying a set of perturbations.
These clusters and topics are then used to generate dedicated test that challenge the bot to answer questions about the specific topic in a way that might not align with the business rules of your organization.

.. note::

   **Legitimate queries** are normal user inputs without malicious intent. Failure in these test cases often indicates hallucinations or incorrect answers. To automate this process, internal data (e.g., the knowledge base retrieved by the RAG) can be used as a seed to generate expected responses from the bot. A well-structured synthetic data process for legitimate queries should be:

   - **Exhaustive**: Create diverse test cases by ensuring coverage of all documents and/or topics used by the bot. We recommend you create 20 conversations per topic.
   - **Designed to trigger failures**: Synthetic test cases should not be trivial queries, otherwise the chance that your tests fail becomes very low. The Giskard hub applies perturbation techniques (e.g., paraphrasing, adding out-of-scope contexts) to increase the likelihood of incorrect responses from the bot.
   - **Automatable**: A good synthetic test case generator should not only generate queries but also generate the expected outputs so that the evaluation judge can automatically compare them with the bot's responses. This is essential for the LLM-as-a-judge setup.
   - **Domain-specific**: Synthetic test cases should not be generic queries; otherwise, they won’t be truly representative of real user queries. While these test cases should be reviewed by humans, it’s important to add metadata to the synthetic data generator to make it more specific. The Giskard Hub includes the bot's description in the generation process to ensure that the queries are realistic.

.. tip::

   Business failures are different from security failures. While security failures focus on malicious exploitation and system integrity, business failures focus on the model's ability to provide accurate, reliable, and appropriate responses in normal usage scenarios.
   If you want to detect security failures, check out the :doc:`/hub/ui/datasets/security`.


Document-based tests generation
-------------------------------

To begin, navigate to the Datasets page and click **Automatic Generation** in the upper-right corner of the screen. This will open a modal with two options: Adversarial or Document-Based. Select the Document-Based option.

The Document Based tab allows you to generate a dataset with examples based on your knowledge base.

.. image:: /_static/images/hub/generate-dataset-document-based.png
   :align: center
   :alt: "Generate document based dataset"
   :width: 800

In this case, dataset generation requires two additional pieces of information:

- ``Knowledge Base``: Choose the knowledge base you want to use as a reference.
- ``Topics``: Select the topics within the chosen knowledge base from which you want to generate examples.

  .. note::

     Giskard can automatically cluster your knowledge base into topics for you, or, if your knowledge base already includes tags or categories, you can use those existing tags as topics. This flexibility ensures that topic selection aligns with your business context and data organization.

  .. tip::

     Synthetic test case generation in Giskard is designed to provide broad coverage across your knowledge base. While absolute statistical exhaustiveness isn't feasible, Giskard's approach—clustering documents into key topics and generating multiple test cases per topic—helps ensure that all major areas are represented. By recommending the creation of at least 20 conversations per topic and leveraging both automated clustering and your own domain-specific tags, Giskard maximizes the likelihood of uncovering gaps or failures across your business knowledge.

Once you click on "Generate," you receive a dataset where:

- The groundedness check is enabled: the context consists of the knowledge documents relevant to answering the query.
- The correctness check is disabled, but its reference (expected output) is prefilled by the Hub. If you want to execute the dataset with the correctness check, you can either enable it manually or enable it for multiple conversations at once by selecting multiple conversations in the Dataset tab and enabling the correctness check.

Next steps
----------

* **Review test case** - Make sure to :doc:`/hub/ui/annotate`
* **Detect security vulnerabilities** - Try :doc:`/hub/ui/datasets/security`
* **Set-up continuous red teaming** - Understand exhaustive and proactive detection with :doc:`/hub/ui/continuous-red-teaming`






