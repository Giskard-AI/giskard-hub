.. mermaid::
   :align: center

   graph LR
       A[Create Dataset] --> B{Source}
       B --> C([<a href="manual.html" target="_self">Create Manually</a>])
       B --> D([<a href="import.html" target="_self">Import Existing</a>])
       B --> E([<a href="knowledge_base.html" target="_self">Knowledge Base Tests</a>])
       B --> F([<a href="scenario.html" target="_self">Scenario Tests</a>])
       B --> G([<a href="../scan/index.html" target="_self">From Scan</a>])
       C --> H[<a href="../annotate/index.html" target="_self">Review Test Cases</a>]
       D --> H
       E --> H
       F --> H
       G --> H

