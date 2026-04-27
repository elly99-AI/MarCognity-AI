# MarCognity-AI
Un framework modulare per l’analisi strutturata e la verifica basata su fonti nei sistemi LLM  
**Licenza:** Apache 2.0

## Table of Contents
- Overview
- Research Motivation
- Modules and Functions
- Core Capabilities
- Early Community Interactions (Non-Endorsement)
- Cross-Domain Epistemic Benchmark
- Official Publication and Citation
- Structural Limitation & Research Scope
- Integrated AI Models

---

## Overview
MarCognity-AI è un framework open-source modulare progettato per analizzare le limitazioni dell’elaborazione informativa basata su LLM e introdurre livelli di verifica strutturata.

Il sistema:

- Produce output strutturati  
- Scompone le risposte in singole affermazioni  
- Verifica le affermazioni contro fonti recuperate  
- Valuta la coerenza semantica  
- Genera report analitici strutturati  

Il framework è pensato per sperimentazione metodologica e riproducibilità.

---

## Research Motivation
I Large Language Models ottimizzano la probabilità linguistica — non la verità fattuale.

MarCognity-AI indaga la seguente domanda centrale:

**Come rendere osservabile l’incertezza a livello di singola affermazione negli output generati da LLM?**

Il framework non pretende di risolvere le allucinazioni dei LLM.  
Documenta invece i pattern di fallimento della metacognizione artificiale in modo riproducibile.

L’architettura cognitiva è composta da moduli indipendenti.

---

## Modules and Functions

| Modulo | Funzione |
|--------|----------|
| Problem Classification | Riconoscimento automatico del tipo di input |
| Academic Prompting | Prompting strutturato multidisciplinare |
| Scientific Retrieval | Retrieval asincrono da fonti open-access |
| Semantic Evaluation | Valutazione logica e semantica delle risposte |
| Skeptical Agent | Verifica claim-by-claim contro le fonti |
| Factual Grounding | Estrazione di evidenze dalle fonti recuperate |
| FAISS Memory | Archiviazione e confronto di output precedenti |
| Cognitive Visualization | Rappresentazione concettuale strutturata |

---

## Core Capabilities
- Generazione scientifica assistita da LLM  
- Retrieval e integrazione di fonti (arXiv, PubMed, Zenodo, OpenAlex)  
- Valutazione metacognitiva multilivello  
- Verifica epistemica a livello di frase  
- Analisi di rischio etico e bias  
- Memoria semantica persistente (FAISS)  
- Report riflessivi esportabili in Markdown  

---

## Structural Limitation & Research Scope
MarCognity-AI è un framework di ricerca esplorativa e non è destinato all’uso in produzione.

Durante lo sviluppo è emersa una limitazione strutturale ricorrente:  
i livelli metacognitivi basati su LLM ottimizzano la coerenza linguistica, ma non riescono a rendere l’incertezza epistemica un segnale esplicito.

In pratica, il sistema può valutare *come* è scritta una risposta (chiarezza, struttura, allineamento semantico), ma non può determinare se le affermazioni siano realmente conosciute, verificabili o giustificate.  
Il modello può dire che una risposta è poco chiara, ma non che manca di conoscenza fondata.

Questa frattura tra coerenza linguistica e consapevolezza epistemica non è trattata come un bug, ma come un fenomeno strutturale da studiare.  
Il framework serve a esporre, analizzare e documentare questa limitazione in modo riproducibile.

La demo e il diario cognitivo inclusi nel repository rendono osservabile questo pattern di fallimento — non presentano un sistema risolto.

---

## Early Community Interactions (Non-Endorsement)
È stata aperta una discussione sul livello di mappatura semantica.  
Membri della community Hugging Face e discussioni correlate hanno interagito tecnicamente con la proposta.

Thread disponibili:
- 🔗 Hugging Face Discussion  
- 🔗 DeepSeek Community Thread  
- 🔗 Google org Response Snapshot  

*(Le interazioni non costituiscono endorsement.)*

---

## Cross-Domain Epistemic Benchmark

Per valutare il comportamento epistemico dell’architettura è stato condotto un benchmark cross-domain su otto domini scientifici e tecnici.

### Domini inclusi
- Medicina  
- Neuroscienze  
- Biologia  
- Statistica  
- Linguistica  
- Informatica  
- Fisica  
- Diritto  

Il benchmark consiste in **72 task di valutazione** (9 per dominio).

### Configurazioni valutate
1. Un LLM baseline senza verifica epistemica  
2. L’architettura MarCognity-AI con ciclo metacognitivo e Skeptical Agent  

Ogni risposta è stata valutata tramite un protocollo strutturato di valutazione epistemica, applicato da un LLM indipendente.

L’uso di un LLM come valutatore introduce una limitazione metodologica nota:  
il valutatore può condividere bias epistemici con il sistema valutato.

---

## Epistemic Reliability Metrics
- Epistemic Score  
- Hallucination Exposure Rate  
- Evidence Support Rate  
- Overconfidence Index  
- Cautious Response Ratio  
- Contradiction Rate  
- Claim Verification Accuracy  

I task, i prompt di valutazione e i risultati sono disponibili nella directory `/benchmark`.

---

## Task Generation Pipeline
I task del benchmark sono stati generati usando file di argomenti specifici per dominio, elaborati dal sistema MarCognity.

Il sistema ha estratto i nomi dei topic e generato domande scientifiche esplicative.  
Le domande sono state poi riviste manualmente per garantire chiarezza e rilevanza.

I task finali sono disponibili in `/benchmark_tasks`.

---

## Failure Analysis
Un’analisi qualitativa dei casi di fallimento è disponibile in:

`benchmark/failure_analysis`

Pattern ricorrenti osservati:

- Ambiguità delle fonti  
- Perdita di contesto durante la segmentazione dei claim  
- Inferenze non autorizzate  
- Falsi negativi del valutatore  
- Ambiguità semantica  
- Corpus di conoscenza incompleto  

Queste osservazioni suggeriscono la presenza di un *epistemic boundary* nei sistemi di verifica basati su testo.

---

## Epistemic Boundary
Analisi concettuale dell’incertezza irriducibile osservata nel benchmark.

➡️ `benchmark/Epistemic_Boundary.md`

---

## Official Publication and Citation

La versione ufficiale del codice e il paper completo sono archiviati permanentemente su Zenodo.

**MarCognity-AI — DOI**  
Permanent DOI: https://doi.org/10.5281/zenodo.19385060  
Access: Full Research Paper (PDF) & Code (Zenodo)

---

## Usage Examples

### Scientific Question
**Input:** “Spiega il ruolo delle proteine chaperon.”  
**Output:** Risposta + fonti + punteggio semantico + diagramma concettuale

### Epistemic Verification Example
**Input:** “Spiega l’entanglement quantistico.”  
**Output:**  
- Risposta generata  
- Verifica claim-by-claim  
- Report VERIFIED / EPISTEMIC FAILURE  
- Motivazione basata sulle fonti  

---

## Quick Demo
Esempio passo-passo disponibile in:

`marcognity_demo.ipynb`

Mostra:

- Generazione della risposta  
- Integrazione del retrieval  
- Verifica a livello di claim  
- Report epistemico  

---

## Execution Options
MarCognity-AI offre due modalità di esecuzione:

1. **Notebook basato su Groq** (`marcognity_demo.ipynb`)  
   - Richiede una Groq API key  
   - Inference ultra-rapida

2. **Notebook locale** (`marcognity_hf_demo.ipynb`)  
   - Esecuzione completamente locale con modelli GGUF  
   - Ideale per uso offline  

Il framework è model-agnostic: il modello di ragionamento può essere sostituito con qualsiasi modello compatibile GGUF.

---

## Integrated AI Models

| Modello | Licenza | Restrizioni |
|---------|---------|-------------|
| meta-llama/llama-4-scout-17b-16e-instruct | LLaMA 4 Community License | Uso di ricerca e applicativo |
| allenai/specter | Apache 2.0 | Uso commerciale con attribuzione |
| scibert_scivocab_uncased_squad_v2 | Apache 2.0 | Uso commerciale con attribuzione |
| Helsinki-NLP OPUS-MT | CC-BY-4.0 | Citazione obbligatoria |
| RandomForest | Nessuna | Dipende dai dati |
| CrossEncoder (DeBERTa) | MIT/Apache | Uso libero con licenza |

Nota: Llama 4 Maverick è stato usato per il benchmark cross-domain.

---

## How to Contribute
1. Fai un fork del repository  
2. Crea un branch (`git checkout -b improvement`)  
3. Modifica file `.py` o `.ipynb`  
4. Per eseguire il progetto serve una Groq API key  
5. Apri una pull request con descrizione chiara  

Linee guida in `CONTRIBUTING.md`.

---

## License
Rilasciato sotto licenza Apache 2.0.  
I modelli di terze parti seguono le loro licenze.

Contributi benvenuti!  
Apri una pull request o segnala un issue se vuoi migliorare il progetto.
