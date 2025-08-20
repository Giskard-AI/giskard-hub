=============================================================
Detect Business Failures in LLMs using RAGET
=============================================================

What are AI business failures?
------------------------------

Business failures in LLMs are failures that impact the business logic, accuracy, and reliability of your AI system. These include hallucinations, incorrect factual responses, inappropriate content generation, and failures to follow business rules. Giskard Open Source provides powerful tools to automatically detect these issues.

How RAGET Works
---------------

The RAG Evaluation Toolkit (RAGET) is a comprehensive testing framework designed specifically for Retrieval-Augmented Generation (RAG) systems. It helps you:

* **Generate comprehensive test sets** from your knowledge base
* **Evaluate RAG performance** across multiple dimensions
* **Detect business failures** like hallucinations and factual inaccuracies
* **Ensure source attribution** and grounding in your responses

RAGET consists of two main components:

1. **Testset Generation** - Automatically creates diverse test cases from your documents
2. **RAG Evaluation** - Assesses your RAG system's performance on the generated tests

Before starting
--------------

To use RAGET, you'll need:

* A `pandas.DataFrame` that can function as a knowledge base with your documents
* A RAG system to evaluate
* Access to an LLM provider (OpenAI, Azure OpenAI, Ollama, etc.)

Prepare your Knowledge Base
---------------------------

First, create a knowledge base from your documents:

.. code-block:: python

   from giskard.rag import KnowledgeBase
   from giskard.rag.generators import RAGETQuestionGenerator

   # Create knowledge base from documents
   knowledge_base = KnowledgeBase.from_documents(
       documents=[
           "Your document content here...",
           "Another document...",
       ],
       chunk_size=1000,
       chunk_overlap=200
   )

   # Or load from existing files
   knowledge_base = KnowledgeBase.from_files(
       file_paths=["doc1.pdf", "doc2.txt", "doc3.docx"]
   )

Generate a test set
-------------------

Use the `generate_testset` function to create comprehensive test cases:

.. code-block:: python

   from giskard.rag import generate_testset

   # Generate test set with default settings
   testset = generate_testset(
       knowledge_base=knowledge_base,
       num_questions=50
   )

   # View the generated test set
   print(f"Generated {len(testset)} test cases")
   print(testset.head())

The generated test set contains several columns:

* **question**: The generated question
* **reference_context**: Context that can be used to answer the question
* **reference_answer**: Expected answer (generated with GPT-4)
* **conversation_history**: Conversation context (empty for simple questions)
* **metadata**: Additional information about the question type and topic

Advanced configuration of the question generation
-----------------------------------------------

Customize question generation by specifying question types:

.. code-block:: python

   from giskard.rag.question_generators import (
       simple_questions,
       complex_questions,
       double_questions,
       conditional_questions,
       multi_context_questions
   )

   # Generate only complex and double questions
   testset = generate_testset(
       knowledge_base=knowledge_base,
       question_generators=[complex_questions, double_questions],
       num_questions=30
   )

   # Generate questions in specific language
   testset = generate_testset(
       knowledge_base=knowledge_base,
       language="French",
       num_questions=20
   )

Question Types Available
~~~~~~~~~~~~~~~~~~~~~~~~

* **Simple Questions**: Basic factual queries about your documents
* **Complex Questions**: Multi-step reasoning questions
* **Double Questions**: Questions with multiple parts
* **Conditional Questions**: Questions with specific conditions
* **Multi-Context Questions**: Questions requiring information from multiple sources

Custom Question Generators
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create your own question generators by implementing the `QuestionGenerator` interface:

.. code-block:: python

   from giskard.rag.question_generators import QuestionGenerator
   from typing import List, Dict, Any

   class CustomBusinessQuestions(QuestionGenerator):
       def generate_questions(
           self,
           knowledge_base,
           num_questions: int,
           **kwargs
       ) -> List[Dict[str, Any]]:
           # Your custom question generation logic
           questions = []
           # ... implementation ...
           return questions

   # Use your custom generator
   testset = generate_testset(
       knowledge_base=knowledge_base,
       question_generators=[CustomBusinessQuestions()],
       num_questions=25
   )

Evaluate your RAG system
------------------------

Once you have a test set, evaluate your RAG system using the `evaluate` function:

.. code-block:: python

   from giskard.rag import evaluate
   from giskard.rag.models import RAGModel

   # Define your RAG model
   class MyRAGModel(RAGModel):
       def retrieve(self, question: str, top_k: int = 5):
           # Your retrieval logic
           return ["retrieved_context_1", "retrieved_context_2"]

       def generate(self, question: str, contexts: List[str]) -> str:
           # Your generation logic
           return "Generated answer based on contexts"

   # Create RAG model instance
   rag_model = MyRAGModel()

   # Evaluate your RAG system
   evaluation_results = evaluate(
       model=rag_model,
       testset=testset,
       metrics=["relevance", "faithfulness", "answer_relevancy"]
   )

   # View results
   print(f"Overall Score: {evaluation_results.overall_score}")
   print(f"Relevance: {evaluation_results.relevance_score}")
   print(f"Faithfulness: {evaluation_results.faithfulness_score}")

Available Metrics
~~~~~~~~~~~~~~~~

* **Relevance**: How well the retrieved context matches the question
* **Faithfulness**: Whether the generated answer is faithful to the retrieved context
* **Answer Relevancy**: How relevant the answer is to the question
* **Context Precision**: Precision of the retrieved context
* **Context Recall**: Recall of relevant information in retrieved context

Integration with Giskard Hub
----------------------------

For team collaboration and centralized management, you can integrate with Giskard Hub:

.. code-block:: python

   from giskard_hub import HubClient

   # Connect to Giskard Hub
   client = HubClient(
       url="https://your-hub-instance.com",
       api_key="your-api-key"
   )

   # Upload your test set
   dataset = client.datasets.create(
       name="Business Validation Test Set",
       data=testset,
       project_id="your-project-id"
   )

   # Run evaluation on the hub
   evaluation = client.evaluate(
       dataset=dataset,
       model="your-rag-model",
       name="Business Validation Run"
   )

Business Failure Detection Examples
----------------------------------

Detect common business failures in your RAG system:

.. code-block:: python

   # Test for hallucinations
   def test_no_hallucination(model, testset):
       """Test that the model doesn't generate information not in the context."""
       results = []
       for _, row in testset.iterrows():
           answer = model.generate(row['question'], [row['reference_context']])
           # Check if answer contains information not in context
           # Implementation depends on your specific requirements
           results.append(not contains_hallucination(answer, row['reference_context']))

       return sum(results) / len(results)

   # Test for factual accuracy
   def test_factual_accuracy(model, testset):
       """Test that the model provides factually correct answers."""
       results = []
       for _, row in testset.iterrows():
           answer = model.generate(row['question'], [row['reference_context']])
           # Compare with reference answer
           accuracy = calculate_similarity(answer, row['reference_answer'])
           results.append(accuracy)

       return sum(results) / len(results)

Continuous Monitoring
--------------------

Set up continuous monitoring for business failures:

.. code-block:: python

   import schedule
   import time

   def run_business_validation():
       """Run business validation tests regularly."""
       testset = generate_testset(knowledge_base, num_questions=20)
       results = evaluate(rag_model, testset)

       if results.overall_score < 0.8:
           print("Warning: Business validation score below threshold!")
           # Send alert, log issue, etc.

   # Schedule regular validation
   schedule.every().day.at("09:00").do(run_business_validation)
   schedule.every().hour.do(run_business_validation)

   while True:
       schedule.run_pending()
       time.sleep(60)

Best Practices
--------------

* **Generate diverse test cases**: Ensure coverage across all document topics
* **Use realistic questions**: Make test cases representative of actual user queries
* **Regular evaluation**: Run tests frequently to catch regressions
* **Monitor key metrics**: Focus on relevance, faithfulness, and accuracy
* **Iterate and improve**: Use results to enhance your RAG system

Troubleshooting
---------------

Common issues and solutions:

* **Low relevance scores**: Check your retrieval system and document chunking
* **High hallucination rates**: Verify context retrieval and generation logic
* **Poor answer quality**: Ensure sufficient context is provided to the generator

For additional support, join the `Giskard Discord community <https://discord.gg/giskard>`_ and ask questions in the #support channel.

Next Steps
----------

* **Explore Security Testing** - :doc:`/oss/sdk/security` for security vulnerability detection
* **Advance your Business Failure Testing** - Integrate tests into your CI/CD pipeline
