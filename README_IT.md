# MarCognity-AI  
**Un framework di ricerca per sistemi IA riflessivi ed epistemicamente trasparenti**

---

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)  

---

## Indice

- [Panoramica](#panoramica)
- [Motivazione della Ricerca](#motivazione-della-ricerca)
- [Moduli e Funzioni](#moduli-e-funzioni)
- [Funzionalità Core](#funzionalità-core)
- [Interazioni Iniziali della Community](#interazioni-iniziali-della-community-non-endorsement)
- [Pubblicazione Ufficiale e Citazione](#pubblicazione-ufficiale-e-citazione)
- [Limitazioni Strutturali e Scopo della Ricerca](#limitazioni-strutturali-e-scopo-della-ricerca)
- [Modelli IA Integrati](#modelli-ia-integrati)

---

## Panoramica

**MarCognity-AI** è un framework di ricerca open-source modulare progettato per studiare le limitazioni strutturali della metacognizione basata su LLM (Large Language Models) e introdurre livelli espliciti di verifica epistemica.

Invece di limitarsi a generare risposte, il sistema:
- Produce output strutturati
- Valuta la coerenza semantica
- Verifica le affermazioni confrontandole con fonti recuperate
- Archivia la memoria semantica
- Genera report epistemici strutturati

L'obiettivo non è "migliorare le risposte", ma analizzare la frattura strutturale tra la coerenza linguistica e la consapevolezza epistemica nei modelli linguistici di grandi dimensioni.

---

## Motivazione della Ricerca

I modelli linguistici di grandi dimensioni ottimizzano la probabilità linguistica, non la verità fattuale. MarCognity-AI indaga la seguente domanda fondamentale:

> **L'incertezza epistemica può essere resa esplicita all'interno di un sistema basato su LLM?**

Questo framework non pretende di risolvere le "allucinazioni" degli LLM. Al contrario, espone e documenta le modalità di fallimento della metacognizione artificiale in modo riproducibile.

---

## Moduli e Funzioni

| Modulo | Funzione |
| :--- | :--- |
| **Problem Classification** | Rilevamento automatico del tipo di input |
| **Academic Prompting** | Prompting multidisciplinare strutturato |
| **Scientific Retrieval** | Recupero asincrono da fonti open-access |
| **Semantic Evaluation** | Punteggio logico e semantico delle risposte |
| **Skeptical Agent** | Verifica puntuale delle affermazioni rispetto alle fonti |
| **FAISS Memory** | Archiviazione e confronto degli output passati |
| **Cognitive Visualization** | Rappresentazione concettuale strutturata |

---

## Funzionalità Core

- Generazione scientifica assistita da LLM
- Integrazione e recupero di fonti (arXiv, PubMed, Zenodo, OpenAlex)
- Valutazione metacognitiva multilivello
- Verifica epistemica a livello di singola frase
- Analisi dei rischi etici e dei bias
- Memoria semantica persistente (FAISS)
- Report riflessivi esportabili in Markdown

---

## Limitazioni Strutturali e Scopo della Ricerca

MarCognity-AI è un framework di ricerca esplorativo e **non è destinato all'uso in produzione**.

Durante lo sviluppo è emersa una limitazione strutturale ricorrente: i livelli metacognitivi basati su LLM ottimizzano in modo affidabile la coerenza linguistica, ma falliscono nel far emergere l'incertezza epistemica come segnale esplicito.

In pratica, il sistema può valutare *come* una risposta è scritta (chiarezza, struttura, allineamento semantico), ma non può determinare intrinsecamente se le affermazioni sottostanti siano realmente conosciute, verificabili o epistemicamente giustificate. Il modello può segnalare che una risposta è poco chiara, ma non che manca di conoscenza fondata.

Questa discrepanza è l'oggetto principale dello studio: il framework serve a esporre e analizzare questo "punto di rottura" in modo osservabile.

---

## Interazioni Iniziali della Community (Non-Endorsement)

È stata aperta una discussione riguardo al livello di mappatura semantica. Membri della community di Hugging Face e relativi esperti hanno partecipato tecnicamente alla proposta.

- 🔗 [Hugging Face Discussion](https://huggingface.co/elly99/MarCognity-AI/discussions)  
- 🔗 [DeepSeek Community Thread](https://huggingface.co/elly99/MarCognity-AI/discussions)  
- 🔗 [Google org Response Snapshot](https://huggingface.co/google/gemma-2b-it/discussions/70#68ecace9e79b11c589bcead9)

---
## Benchmark Epistemico Cross-Domain

Per valutare il comportamento epistemico dell’architettura, è stato condotto un benchmark cross-domain su otto domini scientifici e tecnici.

### Domini inclusi

- Medicina
- Neuroscienze
- Biologia
- Statistica
- Linguistica
- Informatica
- Fisica
- Diritto

Il benchmark consiste in **72 task di valutazione (9 per dominio)**.

### Configurazioni valutate

Sono state valutate due configurazioni:

- un **modello linguistico di grandi dimensioni (LLM) baseline**, operante senza verifica epistemica
- l’**architettura MarCognity-AI**, che integra il ciclo metacognitivo e lo Skeptical Agent

Ogni risposta generata dai due sistemi è stata valutata tramite un **protocollo strutturato di valutazione epistemica basato su prompt**, applicato da un LLM indipendente che funge da valutatore.

### Metriche di affidabilità epistemica

- Epistemic Score
- Hallucination Exposure Rate
- Evidence Support Rate
- Overconfidence Index
- Cautious Response Ratio
- Contradiction Rate
- Claim Verification Accuracy

I task del benchmark, i prompt di valutazione e i risultati sono disponibili nella directory `/benchmark`.

### Pipeline di generazione dei task

I task del benchmark sono stati generati utilizzando file di argomenti specifici per dominio, elaborati dal sistema MarCognity.

Il sistema ha estratto i nomi dei topic e ha generato domande scientifiche esplicative basate su tali argomenti.

Le domande generate sono state poi revisionate e curate manualmente per garantire chiarezza, diversità concettuale e rilevanza disciplinare.

I task finali del benchmark sono disponibili nella directory `/benchmark_tasks`.

---
### Analisi dei Fallimenti

Un'analisi qualitativa dei casi di fallimento rappresentativi è fornita in:

`benchmark/failure_analysis`

L'analisi identifica schemi ricorrenti di fallimento epistemico, tra cui:

* **Ambiguità della fonte**
* **Perdita di contesto** durante la segmentazione delle asserzioni
* **Inferenza non autorizzata**
* **Falsi negativi del valutatore**
* **Ambiguità semantica**
* **Corpus di conoscenza incompleto**

Queste osservazioni suggeriscono la presenza di un **confine epistemico** nei sistemi di verifica basati su testo.

---

### Epistemic Boundary

Analisi concettuale dell’incertezza irreducibile osservata nel benchmark.

➡️ `benchmark/Epistemic_Boundary.md`

---

## Pubblicazione Ufficiale e Citazione

La versione ufficiale del codice e il paper di ricerca completo sono stati archiviati su Zenodo.

| MarCognity-AI | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17855185.svg)](https://doi.org/10.5281/zenodo.19020581) |
| :--- | :--- |
| **DOI Permanente** | `https://doi.org/10.5281/zenodo.19020581` |
| **Accesso** | [Paper di Ricerca & Codice (Zenodo)](https://doi.org/10.5281/zenodo.19020581) |

---

## Modelli IA Integrati

| Modelli Integrati | Licenza | Restrizioni |
| :--- | :--- | :--- |
| **meta-llama/llama-4-scout-17b-16e-instruct* | LLaMA 4 Community | Uso conforme alla AUP di Meta |
| **allenai/specter** | Apache 2.0 | Libero con attribuzione |
| **scibert_scivocab_uncased** | Apache 2.0 | Libero con attribuzione |
| **Helsinki-NLP (OPUS-MT)** | CC-BY-4.0 | Citazione obbligatoria |
| **RandomForest Model** | Nessuna | Algoritmo classico |
| **CrossEncoder (DeBERTa)** | Varia (MIT/Apache) | Libero se rispettata la licenza |

---

## Come Contribuire

1. Fai un **Fork** della repository
2. Crea un branch (`git checkout -b improvement`)
3. Modifica i file `.py` o `.ipynb`
4. **Nota:** È necessaria una API key di Groq per l'esecuzione
5. Apri una **Pull Request** descrittiva

---

## Licenza

Rilasciato sotto licenza **Apache 2.0**. I modelli di terze parti integrati seguono le rispettive licenze.
