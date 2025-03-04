=======================
Continuous red teaming
=======================

Once your test cases are generated, refined with business knowledge, and automatically executed, it is essential to maintain them over time. As AI applications interact with real-world data, new vulnerabilities emerge, and your test dataset may miss critical test cases. New vulnerabilities can arise when:

- **Company content changes:** Updates to the RAG knowledge base or modifications to the company’s products.
- **News evolves:** Events not included in the foundational model’s training data (e.g., the 2024 Olympic Games, a new CEO appointment, U.S. elections, etc.).
- **Cybersecurity research advances:** Newly discovered prompt injections or other vulnerabilities identified by the scientific community.
- **New model versions are introduced:** Changes in prompts, updates to foundational models, or modifications in AI behavior.

The Giskard Evaluation Hub conducts continuous red teaming by constantly enriching your test dataset by new cases. These new cases are generated from:

- **Internal data** (e.g., RAG knowledge base)
- **External data** (e.g., social media, news articles)
- **Security research**

.. image:: /_static/images/hub/continuous-red-teaming.png
   :align: center
   :alt: "Continuous red teaming"
   :width: 800

Combining email alerts with continuous red teaming allows you to be promptly notified when new vulnerabilities emerge within your AI agents.