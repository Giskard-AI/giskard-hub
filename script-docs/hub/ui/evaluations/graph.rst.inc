.. mermaid::
   :align: center

   graph LR
       A([<a href="create.html" target="_self">Run Evaluation</a>]) --> B([<a href="index.html" target="_self">Review Results</a>])
       B --> C{Analysis}
       C -->|Compare Versions| D([<a href="compare.html" target="_self">Compare Evaluations</a>])
       C -->|Schedule Automation| E([<a href="schedule.html" target="_self">Schedule Evaluation</a>])
       D --> F{Next Steps}
       E --> F
       F -->|Iterate| A
       F -->|Fix Issues| G[<a href="../annotate/index.html" target="_self">Update Test Cases</a>]
       G --> A

