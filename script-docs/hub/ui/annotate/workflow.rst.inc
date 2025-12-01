.. mermaid::
   :align: center

   graph LR
       C{Persona?} -->|Business| D[<a href="review_test_results.html" target="_self">Review Test Results</a>]
       D --> F{Agree?}
       C -->|Product Owner| E[<a href="modify_test_cases.html" target="_self">Modify Test Cases</a>]
       F -->|Yes| G[<a href="task_management.html" target="_self">Close Task</a>]
       F -->|No| H[<a href="task_management.html" target="_self">Assign to PO</a>]
       H --> E
