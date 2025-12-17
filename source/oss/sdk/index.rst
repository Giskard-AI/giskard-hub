:og:title: Giskard Open Source - Free LLM Agent Testing Library
:og:description: Test and evaluate your LLM agents with our free Python library. Detect security vulnerabilities and business logic failures with LLM Scan and RAGET.

Quickstart & setup
==================

**Giskard Open Source is a Python library for LLM testing and evaluation.** It provides a solid foundation for developers to generate AI security and business tests. You can check our :doc:`/start/comparison` to learn how it differs from our enterprise offering. It is available on `GitHub <https://github.com/Giskard-AI/giskard>`_ and formed the basis for our course on Red Teaming LLM Applications on `Deeplearning.AI <https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/>`_.

We support two main use cases:

.. grid:: 1 1 2 2

   .. grid-item-card:: Detect Security Vulnerabilities by Generating Synthetic Tests using LLM Scan
      :link: security
      :link-type: doc

      Detect security failures, by generating synthetic test cases to detect security failures, like *stereotypes & discrimination* or *prompt injection*, using adversarial queries.

   .. grid-item-card:: Detect Business Failures by Generating Synthetic Tests using RAGET
      :link: business
      :link-type: doc

      Detect business failures, by generating synthetic test cases to detect business failures, like *hallucinations* or *denial to answer questions*, using document-based queries and knowledge bases.

.. tip::
   **🚀 Love Giskard Open Source?**

   Try it to the next level with **Giskard Hub** - featuring a friendly UI, team collaboration, continuous red teaming, enterprise security, and a **free trial**!

   `Explore our features to Giskard Hub </start/comparison.html>`_ and learn how it can help you with enterprise-grade AI testing.

This guide will walk you through installing the library, configuring your agents and finding security and business failures in your LLM.

Installation
------------

Install Giskard using pip:

.. code-block:: bash

   pip install "giskard[llm]"

For development installations, including LLM support:

.. code-block:: bash

   pip install "giskard[dev,llm]"

Configure your AI models
------------------------

Giskard Open Source supports a wide range of LLMs by using `LiteLLM providers <https://docs.litellm.ai/docs/providers/>`_.
If you don't want to configure anything, we will simply use the default model, which is ``openai/gpt-4o`` and ``openai/text-embedding-3-small``.

.. tab-set::

   .. tab-item:: Existing Provider

        For existing providers, you can set the model and embedding model by passing the provider name and model name, like ``openai/gpt-4o`` or ``anthropic/claude-3-5-sonnet``, as shown in the `LiteLLM docs <https://docs.litellm.ai/docs/providers/>`_.
        Simply replace the provider name and model name with the ones you want to use.

        .. code-block:: python

            import os
            import giskard

            os.environ["OPENAI_API_KEY"] = "" # "my-api-key"

            # Optional, setup a model (default LLM is gpt-4o, default embedding model is text-embedding-3-small)
            giskard.llm.set_llm_model("openai/gpt-4o")
            giskard.llm.set_embedding_model("openai/text-embedding-3-small")

   .. tab-item:: Custom Provider

        Similarly, we can define a custom provider by subclassing the ``litellm.CustomLLM`` class and registering it with LiteLLM, as shown in the `LiteLLM documentation <https://docs.litellm.ai/docs/providers/custom_llm_server>`_.

        .. code-block:: python

            import os
            import requests
            from typing import Optional

            import litellm
            import giskard


            class MyCustomLLM(litellm.CustomLLM):
                def completion(self, messages: str, api_key: Optional[str] = None, **kwargs) -> litellm.ModelResponse:
                    api_key = api_key or os.environ.get("MY_SECRET_KEY")
                    if api_key is None:
                        raise litellm.AuthenticationError("`api_key` was not provided")

                    response = requests.post(
                        "https://www.my-custom-llm.ai/chat/completion",
                        json={"messages": messages},
                        headers={"Authorization": api_key},
                    )

                    return litellm.ModelResponse(**response.json())

            os.environ["MY_SECRET_KEY"] = "" # "my-secret-key"

            my_custom_llm = MyCustomLLM()

            litellm.custom_provider_map = [  # 👈 KEY STEP - REGISTER HANDLER
                {"provider": "my-custom-llm-endpoint", "custom_handler": my_custom_llm}
            ]

            api_key = os.environ["MY_SECRET_KEY"]

            giskard.llm.set_llm_model("my-custom-llm-endpoint/my-custom-model", api_key=api_key)

Detect security vulnerabilities
--------------------------------

We can now use the configured model to evaluate security vulnerabilities in your LLM API calls using LLM Scan.

The LLM scan combines both heuristics-based and LLM-assisted detectors.
The heuristics-based detectors use known techniques and patterns to test for vulnerabilities which are not specific to the agent.
The LLM-assisted detectors are designed to detect vulnerabilities that are specific to your business case. They use another LLM model to probe your LLM system.

Create a Giskard model
______________________

We define a simple function that takes a Pandas DataFrame with features as input and returns a list of strings as responses.
In the following example, we create a simple function `model_predict` that takes a Pandas DataFrame with a single feature ``question``, forwards it to ``llm_api``, and returns a list of strings as responses.
This function should contain the logic of the LLM API you would like to call.

.. code-block:: python

    import pandas as pd
    from giskard import Model

    def model_predict(df: pd.DataFrame) -> list[str]:
        """Wraps the LLM call in a simple Python function."""
        return [llm_api(question) for question in df["question"].values]

    # Create a giskard.Model object with security-focused description
    giskard_model = Model(
        model=model_predict,
        model_type="text_generation",
        name="Customer Service Assistant",
        description="AI assistant for customer support with strict security requirements",
        feature_names=["question"]
    )

    # Create a test dataset with a single feature "question"
    scan_results = giskard.scan(giskard_model)
    # Save the scan results to a file
    display(scan_results)

.. image:: /_static/images/oss/scan.png
   :align: center
   :alt: "LLM Scan Example"
   :width: 800

Generate a test suite
_____________________

We can then turn the issues you found into actionable tests that you can save and reuse in further iterations.

.. code-block:: python

    # Generate a test suite from the scan results
    test_suite = scan_results.generate_test_suite("My first test suite")

    # Save the test suite to a folder
    test_suite.save("my_test_suite")

Evaluate the test suite
_______________________

We can now evaluate the test suite against another model.

.. code-block:: python

    from giskard import Model, Suite

    # Load the test suite
    test_suite = Suite.load("my_test_suite")

    # Create a different model
    giskard_model_2 = Model(...)

    # Run the test suite with the new model
    test_suite.run(model=giskard_model_2)

.. tip::
   **🚀 Looking for SOTA security testing?**

   Try our enterprise-grade solution with a **free trial**. Get access to advanced security detection, team collaboration, continuous red teaming, and more.

   `Request your free enterprise trial today </start/enterprise-trial.html>`_ and see the difference for yourself!

Detect business failures
------------------------

We can also use the configured model to evaluate business failures using RAG Evaluation Toolkit (RAGET).

RAGET can automatically generate a list of ``question``, ``reference_answer`` and ``reference_context`` from a knowledge base.
It relies on a chain of LLM operations to generate realistic questions across different types.
You can then use this generated test set to evaluate your RAG agent.

Create a knowledge base
_______________________

Before we can use RAGET, we need to create a knowledge base.

.. code-block:: python

    import pandas as pd
    from giskard.rag import KnowledgeBase

    # Load your data and initialize the KnowledgeBase
    df = pd.DataFrame({
        "samples": [
            "Giskard is a great tool for testing and evaluating LLMs.",
            "Giskard Hub offers a comprehensive suite of tools for testing and evaluating LLMs.",
            "Giskard was founded in France by ex-Dataiku employees."
        ]
    })

    knowledge_base = KnowledgeBase.from_pandas(df, columns=["samples"])

Generate a test set
___________________

We can now use the knowledge base to generate a test set of ``question``, ``reference_answer`` and ``reference_context``.

.. code-block:: python

    from giskard.rag import generate_testset

    testset = generate_testset(
        knowledge_base,
        num_questions=60,
        # optionally, we'll auto detect the language if not provided
        language='en',
        # optionally, provide a description of the agent to help generating better questions
        agent_description="A customer support agent for company X",
    )

    # Save the test set to a file
    testset.save("my_testset.jsonl")

Evaluate the test set
_____________________

We will use the ``evaluate`` function to evaluate the test set with the results a provided by the ``predict_fn`` function.
This will return a report object that contains the evaluation results.

.. code-block:: python

    from giskard.rag import evaluate, QATestset

    # Load the test set
    testset = QATestset.load("my_testset.jsonl")

    # Load the original knowledge base
    knowledge_base = KnowledgeBase.from_pandas(df, columns=["samples"])

    # Define a predict function
    def predict_fn(question: str, history=None) -> str:
        """A function representing your RAG agent."""
        # Format appropriately the history for your RAG agent
        messages = history if history else []
        messages.append({"role": "user", "content": question})

        # Get the answer using your preferred framework
        # could be langchain, llama_index, etc.
        answer = get_answer_from_agent(messages)

        return answer

    # Run the evaluation and get a report
    report = evaluate(predict_fn, testset=testset, knowledge_base=knowledge_base)
    display(report)

.. image:: /_static/images/oss/raget.webp
   :align: center
   :alt: "RAGET Example"
   :width: 800

.. tip::
   **🚀 Is every single business failure too much for you?**

   Try our enterprise-grade solution with a **free trial**. Get access to advanced business logic validation, team collaboration, continuous red teaming, and more.

   `Request your free enterprise trial today </start/enterprise-trial.html>`_ and see the difference for yourself!

Next steps
----------

* **Explore Security Vulnerabilities** - :doc:`security` for security logic validation
* **Explore Business Failures** - :doc:`business` for business logic validation

Need help?
----------

* **Documentation**: Explore our :doc:`/oss/sdk/reference/index` for detailed API information
* **Examples**: Check our GitHub repository for more examples
* **Community**: Join our Discord for support and discussions
* **Upgrade**: Ready for team collaboration? Try :doc:`/start/enterprise-trial` for an enterprise subscription
