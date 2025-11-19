:og:title: Giskard Hub UI - Human-in-the-Loop Annotation and Review
:og:description: Review and refine test cases with domain expertise. Use collaborative annotation workflows to improve test quality and ensure comprehensive coverage with intuitive visual tools.

====================================================
Iterate on tests and metrics
====================================================

The annotation workflow in Giskard Hub enables you to continuously improve your test cases and evaluation metrics through an iterative, collaborative process. 

Each test case is composed of a **conversation** and its associated **evaluation parameters** (e.g., an expected answer, rules that the agent must respect, etc.).

The annotation workflow follows these steps:

1. **Review results** - Review test cases and evaluation runs to identify issues  
2. **Assign evaluation criteria** - Define checks and tags to measure quality (correctness, groundedness, conformity, etc.)  
3. **Structure your dataset** - Use tags to organize your test cases and evaluate them efficiently  
4. **Distribute tasks** - Use tasks to coordinate team reviews and ensure quality (review scan results, evaluation runs, and test cases)  

This section guides you through reviewing results, creating and refining test cases, assigning evaluation criteria, and managing team workflows.

Getting started
---------------

.. grid:: 1 1 2 2

   .. grid-item-card:: Review test cases
      :link: conversations
      :link-type: doc

      Create and manage test cases (conversations). Design multi-turn dialogues, add answer examples, and build comprehensive test scenarios.

   .. grid-item-card:: Create and assign checks
      :link: checks
      :link-type: doc

      Define evaluation criteria with checks. Create custom validation rules to measure correctness, conformity, groundedness, and other metrics.

   .. grid-item-card:: Create and assign tags
      :link: tags
      :link-type: doc

      Organize and categorize test cases with tags. Filter conversations, manage performance metrics, and maintain structured test datasets.

   .. grid-item-card:: Distribute review tasks among your team
      :link: tasks
      :link-type: doc

      Coordinate team workflows with tasks. Assign review work for scan results, evaluation runs, and test cases to ensure quality and collaboration.

High-level workflow
-------------------

.. mermaid::
   :align: center

   graph LR
    X[Scan Results] --> A["Iterate on test cases"]
    KB[Generated Test] --> A
     A --> D["Distribute Tasks"]
     D --> A
     A --> C1["Assign Checks"]
     A --> C2["Assign Tags"]
     C1 --> E["Run Evaluations"]
     C2 --> E
     E --> A

Next steps
----------

Now that you understand the annotation workflow, explore the specific features:

* **Start with reviewing results** - Review scan results or evaluation runs to identify areas for improvement
* **Create test cases** - Build conversations that represent your test scenarios
* **Define evaluation criteria** - Assign checks to measure agent performance
* **Organize your dataset** - Use tags to structure and filter your test cases
* **Coordinate team work** - Use tasks to distribute review work and ensure quality

.. toctree::
   :hidden:
   :maxdepth: 3

   conversations
   checks
   tags
   tasks
   
