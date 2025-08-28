Domain-Specific Benchmarks
===========================

Domain-specific benchmarks evaluate LLMs' performance in specialized fields such as healthcare, finance, law, and medicine. These benchmarks test the model's knowledge, reasoning, and application skills within specific professional domains.

Overview
--------

These benchmarks assess how well LLMs can:

- Apply domain-specific knowledge accurately
- Handle specialized terminology and concepts
- Provide contextually appropriate responses
- Navigate domain-specific constraints and regulations
- Demonstrate professional competence
- Maintain accuracy in specialized fields

Key Benchmarks
--------------

MultiMedQA
~~~~~~~~~~

**Purpose**: Evaluates LLMs' ability to provide accurate medical information and clinical knowledge

**Description**: MultiMedQA combines six existing medical question-answering datasets spanning professional medicine, research, and consumer queries. The benchmark evaluates model answers along multiple axes: factuality, comprehension, reasoning, possible harm, and bias.

**Resources**: `MultiMedQA datasets <https://research.google/pubs/large-language-models-encode-clinical-knowledge/>`_ | `MultiMedQA Paper <https://arxiv.org/abs/2212.13138>`_

FinBen
~~~~~~

**Purpose**: Comprehensive evaluation of LLMs in the financial domain

**Description**: FinBen includes 36 datasets covering 24 tasks in seven financial domains: information extraction, text analysis, question answering, text generation, risk management, forecasting, and decision-making. It's the first benchmark to evaluate stock trading capabilities.

**Resources**: `FinBen dataset <https://github.com/THUDM/FinBen>`_ | `FinBen Paper <https://arxiv.org/abs/2401.09657>`_

LegalBench
~~~~~~~~~~

**Purpose**: Evaluates legal reasoning abilities across multiple legal domains

**Description**: LegalBench consists of 162 tasks crowdsourced by legal professionals, covering six types of legal reasoning: issue-spotting, rule-recall, rule-application, rule-conclusion, interpretation, and rhetorical understanding.

**Use Cases**: Legal AI evaluation, legal reasoning assessment, and legal application development.

**Resources**: `LegalBench datasets <https://github.com/nguha/legalbench>`_ | `LegalBench Paper <https://arxiv.org/abs/2308.11462>`_

Berkeley Function-Calling Leaderboard (BFCL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Evaluates LLMs' function-calling abilities across multiple languages and domains

**Description**: BFCL evaluates function-calling capabilities using 2,000 question-answer pairs in multiple languages including Python, Java, JavaScript, and REST API. The benchmark supports multiple and parallel function calls, as well as function relevance detection.

**Resources**: `BFCL dataset <https://github.com/berkeley-function-calling-leaderboard/bfcl>`_ | `Research <https://berkeley-function-calling-leaderboard.github.io/>`_

Domain-specific evaluation is also included in other benchmarks such as MMLU, which tests knowledge across multiple academic subjects including specialized domains, and BigBench, which covers various reasoning types that can be applied to specific professional contexts.

Related Topics
--------------

- :doc:`reasoning_and_language`
- :doc:`safety`
