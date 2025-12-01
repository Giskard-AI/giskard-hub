.. mermaid::
   :align: center

   graph LR
       A[Create Dataset] --> B{Source}
       B -->|Manual| C([<a href="manual.html" target="_self">Create Manually</a>])
       B -->|Import| D([<a href="import.html" target="_self">Import Existing</a>])
       B -->|Generate| E([<a href="business.html" target="_self">Generate Tests</a>])
       B -->|Scan Results| F([<a href="../scan/index.html" target="_self">From Scan</a>])
       C --> H[<a href="../annotate/index.html" target="_self">Iterate on Test Cases</a>]
       D --> H
       E --> H
       F --> H

