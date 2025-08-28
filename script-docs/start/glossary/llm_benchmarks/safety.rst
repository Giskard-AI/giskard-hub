Safety Benchmarks
==================

Safety and ethics benchmarks evaluate LLMs' ability to avoid harmful content generation, resist manipulation, and maintain ethical behavior across various scenarios. These benchmarks test the model's safety mechanisms and ethical decision-making capabilities.

Overview
--------

These benchmarks assess how well LLMs can:

- Avoid generating harmful or inappropriate content
- Resist prompt injection and manipulation attempts
- Maintain ethical boundaries in responses
- Handle sensitive topics appropriately
- Detect and avoid bias and discrimination
- Provide safe and responsible information

Key Benchmarks
--------------

SafetyBench
~~~~~~~~~~~

**Purpose**: Comprehensive evaluation of LLM safety across multiple categories

**Description**: SafetyBench incorporates over 11,000 multiple-choice questions across seven categories of safety concerns: offensive content, bias, illegal activities, mental health, and more. The benchmark offers data in both Chinese and English.

**Key Features**:
- Multiple safety categories
- Bilingual evaluation (Chinese/English)
- Large dataset (11,000+ questions)
- Comprehensive safety coverage
- Standardized assessment

**Use Cases**: Safety evaluation, bias detection, content moderation assessment, and ethical AI development.

**Resources**: `SafetyBench dataset <https://github.com/thu-coai/SafetyBench>`_ | `SafetyBench Paper <https://arxiv.org/abs/2309.07045>`_

AgentHarm
~~~~~~~~~

**Purpose**: Evaluates the safety of LLM agents in multi-step task execution

**Description**: AgentHarm tests how well LLM agents can maintain safety while executing complex, multi-step tasks. The benchmark assesses whether agents can fulfill user requests without causing harm or violating safety principles.

**Key Features**:
- Multi-step task evaluation
- Agent safety assessment
- Task completion testing
- Safety boundary evaluation
- Harm prevention measurement

**Use Cases**: Agent safety testing, multi-step task evaluation, and safety mechanism validation.

**Resources**: `AgentHarm dataset <https://github.com/THUDM/AgentBench>`_ | `AgentHarm Paper <https://arxiv.org/abs/2308.03688>`_

TruthfulQA
~~~~~~~~~~

**Purpose**: Tests resistance to misinformation and false beliefs

**Description**: TruthfulQA evaluates whether language models can distinguish between true and false information, particularly when dealing with common misconceptions or false beliefs that are frequently repeated online.

**Key Features**:
- Truthfulness testing
- Misinformation resistance
- Factual accuracy assessment
- Common misconception handling
- Multiple-choice format

**Use Cases**: Factual accuracy evaluation, misinformation resistance testing, and truthfulness assessment.

**Resources**: `TruthfulQA dataset <https://github.com/sylinrl/TruthfulQA>`_ | `TruthfulQA Paper <https://arxiv.org/abs/2109.07958>`_

Safety evaluation is also included in other benchmarks such as BigBench, which covers various reasoning types including safety and ethical considerations, and domain-specific benchmarks that evaluate safety within specific professional contexts.

Phare
~~~~~

**Purpose**: Evaluates the safety of LLMs across key safety & security dimensions, including hallucination, factual accuracy, bias, and potential harm.

**Description**: Phare is a multilingual benchmark to evaluate LLMs across key safety & security dimensions, including hallucination, factual accuracy, bias, and potential harm.

**Key Features**:
- Multilingual evaluation
- Comprehensive safety coverage
- Hallucination testing
- Bias and potential harm assessment
- Standardized scoring

**Use Cases**: Safety evaluation, bias detection, content moderation assessment, and ethical AI development.

**Resources**: `Phare dataset <https://phare.giskard.ai/>`_ | `Phare Paper <https://arxiv.org/abs/2505.11365>`_

Related Topics
--------------

- :doc:`conversation_and_chatbot`
- :doc:`domain_specific`
