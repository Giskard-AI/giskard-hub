:og:title: Giskard Hub UI - Setup Projects, Agents & Knowledge Bases
:og:description: Create, manage, and organize projects, agents and knowledge bases through the user interface. Set up workspaces, configure access controls, and manage team collaboration.

Setup projects, agents and knowledge bases
==========================================

In this section, we will walk you through how to setup projects, agents and knowledge bases using the Hub interface.

.. grid:: 1 1 2 2

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

.. mermaid::
   :align: center

   graph LR
       A[Create Project] --> B[Setup Agent]
       A --> C[Import Knowledge Base]
       B --> D[Configure Endpoint]
       C --> E[Upload Documents]
       D --> F[Ready for Testing]
       E --> F
       
.. toctree::
   :hidden:
   :maxdepth: 4

   projects
   agents
   knowledge_bases