:og:title: Giskard Hub - Enterprise Agent Testing - Continuous Red Teaming
:og:description: Implement proactive threat detection and continuous vulnerability assessment for your LLM agents. Monitor for emerging security risks and maintain robust AI safety.

======================
Continuous red teaming
======================

Continuous red teaming is a proactive approach to AI security that involves continuously testing your LLM agents for new vulnerabilities and emerging threats.

Unlike traditional security testing that focuses on known vulnerabilities, continuous red teaming:

* **Adapts to new threats**: Automatically detects and responds to emerging attack patterns
* **Enables proactive defense**: Identifies vulnerabilities before they can be exploited

In this section, we will walk you through how to set up and use continuous red teaming in Giskard Hub.

Once your test cases are generated, refined with business knowledge, and automatically executed, it is essential to maintain them over time. As AI applications interact with real-world data, new vulnerabilities emerge, and your test dataset may miss critical test cases. New vulnerabilities can arise when:

- **Company content changes:** Updates to the RAG knowledge base or modifications to the company’s products.
- **News evolves:** Events not included in the foundational model’s training data (e.g., the 2024 Olympic Games, a new CEO appointment, U.S. elections, etc.).
- **Cybersecurity research advances:** Newly discovered prompt injections or other vulnerabilities identified by the scientific community.
- **New model versions are introduced:** Changes in prompts, updates to foundational models, or modifications in AI behavior.

Upon request, Giskard can offer a continuous red teaming service that constantly enriches your datasets with new test cases. These new test cases are generated from:

- **Internal data** (e.g., RAG knowledge base)
- **External data** (e.g., social media, news articles)
- **Security research**

.. image:: /_static/images/hub/continuous-red-teaming.png
   :align: center
   :alt: "Continuous red teaming"
   :width: 800
