.. mermaid::
   :align: center

   graph LR
       A([<a href="projects.html" target="_self">Create Project</a>]) --> B([<a href="agents.html" target="_self">Create Agent</a>])
       A --> C([<a href="knowledge_bases.html" target="_self">Create Knowledge Base</a>])
       C --> E[Upload Documents]
       B --> F[<a href="../scan/index.html" target="_self">Ready for Testing</a>]
       E --> F

