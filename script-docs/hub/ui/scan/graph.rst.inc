.. mermaid::
   :align: center

   graph LR
       A([<a href="launch-scan.html" target="_self">Launch Scan</a>]) --> C([<a href="review-scan-results.html" target="_self">Review Vulnerabilities</a>])
       C --> D{Take Action}
       D -->|Convert to Test| E[Send to Dataset]
       D -->|Create Task| F[<a href="../annotate/distribute_tasks.html" target="_self">Distribute Task</a>]
       E --> H[<a href="../annotate/modify_test_cases.html" target="_self">Review Test Cases</a>]
       F --> H
       H --> A

