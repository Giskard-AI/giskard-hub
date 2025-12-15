:og:title: Giskard Hub SDK - Projects, Agents & Knowledge Bases Management
:og:description: Create, manage, and organize projects programmatically. Set up workspaces, configure access controls, and manage team collaboration through the comprehensive Python SDK.

=====================================================
Setup API keys, projects, agents and knowledge bases
=====================================================

In this section, we will walk you through how to setup keys, IDs, projects, agents and knowledge bases using the SDK.

* **Projects**: Projects are the top-level organizational units in Giskard Hub. They provide a workspace for your team to collaborate on LLM agent testing and evaluation.
* **Agents**: The AI systems, LLMs or agents you want to test and evaluate
* **Knowledge bases**: Domain-specific information sources we can use to test your agents

.. grid:: 1 1 2 2

   .. grid-item-card:: Configure API keys and find entity IDs
      :link: keys
      :link-type: doc

      Retrieve API keys and entity IDs programmatically

   .. grid-item-card:: Setup projects
      :link: projects
      :link-type: doc

      Setup and organize projects

   .. grid-item-card:: Setup agents
      :link: agents
      :link-type: doc

      Setup and organize your deployed agents

   .. grid-item-card:: Setup knowledge bases
      :link: knowledge_bases
      :link-type: doc

      Setup and organize knowledge bases we can use to test your agents

High-level workflow
-------------------

.. include:: ../../ui/setup/graph.rst.inc
   
.. toctree::
   :hidden:
   :maxdepth: 4

   keys
   projects
   agents
   knowledge_bases