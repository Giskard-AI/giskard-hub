.. mermaid::
   :align: center

   graph LR
       B[<a href="scan/index.html" target="_self">Red Team Scan</a>] -->  D[<a href="datasets/index.html" target="_self">Create Test Cases</a>]
       D --> F[<a href="annotate/index.html" target="_self">Annotate & Assign Checks</a>]
       F --> G[<a href="evaluations/index.html" target="_self">Run Evaluations</a>]
       G --> H[<a href="evaluations/index.html" target="_self">Review Results</a>]
       H --> F
       H --> B
