# MarCognity-AI  
**A modular framework for structured analysis and source-grounded verification in LLM-based systems**
---

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)  

---

## Table of Contents

- [Overview](#overview)
- [Research Motivation](#research-motivation)
- [Modules and Functions](#modules-and-functions)
- [Core Capabilities](#core-capabilities)
- [Early Community Interactions(Non-Endorsement)](#early-community-interactions(non-endorsement))
- [Cross-Domain Epistemic Benchmark](#cross-domain-epistemic-benchmark) 
- [Official Publication and Citation](#official-publication-and-citation)
- [Structural Limitation & Research Scope](#structural-limitation-&-research-scope)
- [Integrated AI Models](#integrated-ai-models)

---

## Overview

MarCognity-AI is a modular open-source framework designed to analyze limitations of LLM-based information processing and introduce structured verification layers.

The system:

- Produces structured outputs

- Decomposes responses into individual claims

- Verifies claims against retrieved sources

- Evaluates semantic coherence

- Generates structured analytical reports

The framework is intended for methodological experimentation and reproducibility.

---

## Research Motivation

Large Language Models optimize linguistic probability — not factual truth.

MarCognity-AI investigates the following core question:

How can claim-level uncertainty be made observable in LLM-generated outputs?

This framework does not claim to solve LLM hallucinations.
Instead, it exposes and documents the failure modes of artificial metacognition in a reproducible way.

The following cognitive architecture is composed of independent modules.

## Modules and Functions

| Module                   | Function                                          |
|--------------------------|---------------------------------------------------|
| Problem Classification   | Automatic input type detection                    |
| Academic Prompting       | Structured multidisciplinary prompting            |
| Scientific Retrieval     | Asynchronous retrieval from open-access sources   |
| Semantic Evaluation      | Logical and semantic scoring of responses         |
| Skeptical Agent          | Claim-by-claim verification against sources       |
| FAISS Memory             | Archiving and comparison of past outputs          |
| Cognitive Visualization  | Structured conceptual representation              |


## Core Capabilities

- LLM-assisted scientific generation  
- Source retrieval and integration (arXiv, PubMed, Zenodo, OpenAlex)  
- Multilevel metacognitive evaluation  
- Sentence-level epistemic verification  
- Ethical risk and bias analysis  
- Persistent semantic memory (FAISS)  
- Markdown-exportable reflective reports  

---

## Structural Limitation & Research Scope

MarCognity-AI is an exploratory research framework and is not intended for production use.

During development, a recurring structural limitation emerged: LLM-based metacognitive layers reliably optimize for linguistic coherence but fail to surface epistemic uncertainty as an explicit signal.

In practice, the system can evaluate how an answer is written (clarity, structure, semantic alignment), yet it cannot inherently determine whether the underlying claims are genuinely known, verifiable, or epistemically justified. The model can express that a response is unclear, but not that it lacks grounded knowledge.

This collapse between linguistic coherence and epistemic awareness is not treated as a bug to be fixed, but as a structural fracture to be studied. The purpose of this framework is to expose, analyze, and document this limitation in a reproducible way.

The demo and cognitive journal included in this repository are designed to make this failure mode observable — not to present a solved system.

---

## Early Community Interactions (Non-Endorsement)

A discussion was opened regarding the semantic mapping layer.
Community members from Hugging Face and related model discussions engaged technically with the proposal.

You can explore the original threads and responses here:  
🔗 [Hugging Face Discussion](https://huggingface.co/elly99/MarCognity-AI/discussions)  
🔗 [DeepSeek Community Thread](https://huggingface.co/elly99/MarCognity-AI/discussions)  
🔗 [Google org Response Snapshot](https://huggingface.co/google/gemma-2b-it/discussions/70#68ecace9e79b11c589bcead9)

---
## Cross-Domain Epistemic Benchmark

To evaluate the epistemic behavior of the architecture, a cross-domain benchmark was conducted across eight scientific and technical domains.

### Domains Included

- Medicine
- Neuroscience
- Biology
- Statistics
- Linguistics
- Computer Science
- Physics
- Law

The benchmark consists of **72 evaluation tasks (9 per domain)**.

### Evaluated Configurations

Two configurations were evaluated:

- a **baseline large language model (LLM)** operating without epistemic verification
- the **MarCognity-AI architecture**, which integrates the metacognitive cycle and the Skeptical Agent

Each response generated by the two systems was evaluated using a **structured prompt-based epistemic assessment protocol**, applied by an independent LLM acting as evaluator.

The use of an LLM as independent evaluator introduces a known methodological limitation: the evaluator may share epistemic biases with the evaluated system. This constraint is acknowledged as a structural open problem in the field of LLM evaluation and is not specific to this framework.

### Epistemic Reliability Metrics

- Epistemic Score
- Hallucination Exposure Rate
- Evidence Support Rate
- Overconfidence Index
- Cautious Response Ratio
- Contradiction Rate
- Claim Verification Accuracy

Benchmark tasks, evaluation prompts, and results are available in the `/benchmark` directory.

### Task Generation Pipeline

Benchmark tasks were generated using domain-specific topic files processed by the MarCognity system.

The system extracted topic names and generated explanatory scientific questions based on those topics.

The generated questions were then manually reviewed and curated to ensure clarity, conceptual diversity, and domain relevance.

The final benchmark tasks are available in the `/benchmark_tasks` directory.

---

### Failure Analysis

A qualitative analysis of representative failure cases is provided in:

benchmark/failure_analysis

The analysis identifies recurring epistemic failure patterns including:

• Source ambiguity  
• Context loss during claim segmentation  
• Unauthorized inference  
• Evaluator false negatives  
• Semantic ambiguity  
• Incomplete corpus of knowledge  

These observations suggest the presence of an epistemic boundary in text-based verification systems.

---

### 📚 Official Publication and Citation

The official version of the code and the full research paper have been permanently archived on Zenodo and are citable using their Digital Object Identifier (DOI).

| **MarCognity-AI** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17855185.svg)](https://doi.org/10.5281/zenodo.18913144) |
|---|---|
| **Permanent DOI** | `https://doi.org/10.5281/zenodo.18913144` |
| **Access Publication** | [Full Research Paper (PDF) & Code (Zenodo)](https://doi.org/10.5281/zenodo.18913144) |

---

## Usage Examples

### Scientific Question  
**Input:** “Explain the role of chaperone proteins.”  
**Output:** Response + sources + semantic score + conceptual diagram

### Epistemic Verification Example
Input: “Explain quantum entanglement.”
Output:

Generated response

Claim-by-claim verification

VERIFIED / EPISTEMIC FAILURE report

Reasoning based on provided sources

--- 
### Quick Demo

A step-by-step execution example is available in:

`marcognity_demo.ipynb`

The notebook illustrates:
- Response generation
- Retrieval integration
- Claim-level verification
- Epistemic reporting

[Meta LLaMA 4 Community License](https://ai.meta.com/llama/license) 

It is intended for inspection and reproducibility, not interactive deployment.

--- 


## Integrated AI Models

| Integrated Models                                            | License                              | Main Restrictions                                                   |
|--------------------------------------------------------------|--------------------------------------|----------------------------------------------------------------------|
| meta-llama/llama-4-maverick-17b-128e-instruct                | LLaMA 4 Community License (Meta)     | Research and application use allowed; must comply with Meta’s AUP   |
| allenai/specter                                              | Apache 2.0                           | Free for commercial use with attribution                            |
| ktrapeznikov/scibert_scivocab_uncased_squad_v2               | Apache 2.0                           | Free for commercial use with attribution                            |
| Helsinki-NLP (OPUS-MT models on HuggingFace)                 | CC-BY-4.0                            | Free use with mandatory citation                                    |
| RandomForest Model                                           | None (classic algorithm)             | No license restrictions; depends on data used                       |
| CrossEncoder (DeBERTa-based)                                 | Varies (often MIT or Apache 2.0)     | Free use if open license is respected                               |

---


## How to Contribute

Got ideas, suggestions, or want to improve a feature?

1. Fork the repository  
2. Create a branch (`git checkout -b improvement`)  
3. Modify `.py` or `.ipynb` files
4. To run this project, you need a Groq API key
5. Open a pull request with a clear description  

See the [CONTRIBUTING.md](Contributing.md) file for contribution guidelines.

---

## License

Released under the Apache 2.0 License.
Third-party integrated models follow their respective licenses.


Contributions are welcome! If you have additional examples or improvements, please feel free to open a pull request or report an issue.



