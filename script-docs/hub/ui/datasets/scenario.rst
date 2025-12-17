:og:title: Giskard Hub UI - Scenario-Based Dataset Generation
:og:description: Create targeted, business-specific test cases using scenario-based dataset generation. Test your agents with specific personas and business rules without editing your agent's core functionality.

==============================================================
Generate scenario-based tests
==============================================================

Scenario-based dataset generation allows you to create more targeted, business-specific tests without ever needing to edit your agent's core description and functionality. This is super useful if you want to move beyond general testing and simulate how your agents handle specific personas and complex business logic.

Scenario-based generations are a powerful way to ensure your agent is prepared for real-world user scenarios and personas. They are:

- **Fully customizable**: Tailored to whatever kind of personas you envision and are important for your departments
- **Rule-driven**: Move from generic stress testing to rule-driven scenarios
- **Higher quality**: Get higher quality datasets that are more reliable for evaluations
- **Business-focused**: Ultimately, an agent that truly understands your business boundaries

By moving from generic stress testing to rule-driven scenarios, you get higher quality datasets that are more reliable for evaluations, and ultimately, an agent that truly understands your business boundaries.

.. raw:: html

   <iframe width="100%" height="400" src="https://www.youtube.com/embed/g_fsrGyJF4E?si=6ohbPagZyCNU7OCp&amp;controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Getting started
---------------

To begin, navigate to the Datasets page and click **Generate** in the upper-right corner of the screen. This will open a modal with three options: Knowledge Base, and Scenario. Select the **Scenario** option.

.. image:: /_static/images/hub/scenario-select.png
   :align: center
   :alt: "Select scenario option from generation modal"
   :width: 800

Select or create a persona
---------------------------

You'll see a subset of all the personas that you've defined—the user personas that might interact with your bots. You can select an existing one or create a new one.

.. image:: /_static/images/hub/scenario-persona-choose.png
   :align: center
   :alt: "Select or create a persona"
   :width: 800

When creating a new persona scenario, it's always nice to have:
- **A descriptive name**: This helps identify the persona quickly
- **A description**: This helps with the generation understanding and ensures the generated test cases align with your intended persona

Define rules
------------

You can then add specific rules, and these rules help evaluate different persona scenarios and will be used for the generation of these different scenarios.

.. image:: /_static/images/hub/scenario-persona-create.png
   :align: center
   :alt: "Configure persona with rules"
   :width: 800

For example:
- **Persona**: Customer using slang/emojis asking about loans
- **Rules**: Enforce professional tone and refusal to do interest calculations

After defining a set of rules, you can add them to the scenario.

Generate test cases
-------------------

Once you've configured your persona and rules, you can:
- **Select your agent**: Choose the agent you want to test (e.g., Zephyr Bank multilingual agent)
- **Set the number of test cases**: Specify how many test cases you want to generate

.. image:: /_static/images/hub/scenario-generate.png
   :align: center
   :alt: "Select agent and number of test cases to generate"
   :width: 800

Start running the generation, which will be relatively quick. After running the generation, you'll have high-quality evaluated datasets.

Review and evaluate
-------------------

You can see that you have a generated user message that adheres to the persona. You can generate an answer so that you can actually evaluate your agent's response and see if the rules adhere.

After generating an example response, you can also test the evaluation. If the evaluation passes, you have a meaningful test example. This specific example can then be used for a specific evaluation dataset and for evaluation runs where you would need to iterate on a high-quality dataset.

Next steps
----------

* **Review test cases** - Make sure to :doc:`/hub/ui/annotate/index`
* **Generate knowledge base tests** - Try :doc:`/hub/ui/datasets/knowledge_base`
* **Agentic vulnerability detection** - Try :doc:`/hub/ui/scan/index`
