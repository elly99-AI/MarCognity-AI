# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# This cell simulates AGI (Artificial General Intelligence) behavior,
# with capabilities for planning, reasoning, generation, and self-assessment.

# Interactive loop simulating a complete cognitive cycle
async def agi_interactive_loop(user_input):
    context = retrieve_multiturn_context(user_input, top_k=3)
    planning = decompose_task(user_input)
    results = []

    for subtask in planning:
        response = await generate_agi_response(subtask, context)
        results.append(response)
        update_memory(subtask, response)

    return synthesize_final(results)


cross_encoder = CrossEncoder("cross-encoder/nli-deberta-base")

# Simulated historical archive for the question
memory_archive = {}

# Evaluate and version the generated response
def evaluate_and_version_response(question, new_response, level="basic", acceptance_threshold=0.75):
    """
    Evaluates a new response using CrossEncoder,
    compares it with previous versions,
    and decides whether to keep or discard it.

    Returns a dictionary with:
    - evaluation outcome
    - version details (if accepted)
    - confidence and note (if discarded)
    """

    question_id = question.strip().lower()

    # Step 1: Semantic evaluation of the new response
    new_score = float(cross_encoder.predict([(question, new_response)])[0])

    new_version = {
        "id": str(uuid.uuid4()),
        "response": new_response,
        "coherence_score": round(new_score, 3),
        "level": level,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "model_version": "LLM_v1",
        "improvable": new_score < acceptance_threshold
    }

    # Step 2: Retrieve previous versions
    previous_memory = memory_archive.get(question_id, [])

    # If no previous versions exist, save the first one
    if not previous_memory:
        memory_archive[question_id] = [new_version]
        return {
            "outcome": "New question saved.",
            "total_versions": 1,
            "response_accepted": True,
            "details": new_version
        }

    # Step 3: Compare with the best saved version
    best_version = max(previous_memory, key=lambda v: v["coherence_score"])
    best_score = best_version["coherence_score"]

    if new_score > best_score:
        memory_archive[question_id].append(new_version)
        return {
            "outcome": "New version saved (more coherent than previous).",
            "total_versions": len(memory_archive[question_id]),
            "response_accepted": True,
            "details": new_version
        }

    # Version discarded: less coherent
    return {
        "outcome": "Version discarded: less coherent than existing ones.",
        "response_accepted": False,
        "confidence": round(new_score, 3),
        "note": "The proposed version is less coherent than the previous one.",
        "new_score": round(new_score, 3),
        "best_score": round(best_score, 3)
    }


# === Main function: hypothesis generation and creative analysis ===
def simulate_scientific_creativity(concept, subject, style="generative", level="advanced", language="it"):
    prompt = f"""
You are a cognitive scientific assistant with autonomous creative capabilities.

Subject: {subject}
Central concept: {concept}
Requested creative style: {style}
Level: {level}

Objective: Generate an innovative scientific proposal.

Respond with:
1. An **original hypothesis** related to "{concept}".
2. A **conceptual model** that can be visually described.
3. A proposal for a **novel experiment** to test it.
4. Possible **interdisciplinary applications**.
5. A reflection on the degree of verifiability and impact.

Translate everything into language: **{language}**
"""
    try:
        response = llm.invoke(prompt.strip())
        hypothesis_text = getattr(response, "content", str(response)).strip()
        return hypothesis_text
    except Exception as e:
        logging.error(f"[simulate_creativity] Generation error: {e}")
        return "Error during creative simulation."

# === Classifications ===
problem_type = analyze_question(example_problem)
diagram_type_ml = extract_features(example_problem)
print(f"Problem type: {problem_type}")
print(f"Recommended representation: {diagram_type_ml}")

logging.info(f"Identified problem type: {problem_type}")
logging.info(f"Recommended representation type: {diagram_type_ml}")

# === Assign concept from the 'topic' variable ===
concept = topic.strip()

# === Retrieve articles from arXiv with error handling ===
try:
    arxiv_articles = await search_arxiv_async(concept)
    logging.info(f"arXiv: {len(arxiv_articles)} articles found.")
except Exception as e:
    logging.error(f"Error during arXiv search: {e}")
    arxiv_articles = []

# === Retrieve from other databases ===
try:
    pubmed_results = await search_pubmed_async(concept)
    openalex_results = await search_openalex_async(concept)

    logging.info("Search completed across all databases.")
except Exception as e:
    logging.error(f"Error in multi-database search: {e}")
    pubmed_results = openalex_results = doaj_results = []

# === Formatting for prompt or report ===
async def retrieve_and_normalize_articles(concept):
    """
    Retrieves articles from multiple scientific sources and normalizes them.

    Sources: arXiv, PubMed, OpenAlex, Zenodo

    Returns:
    - list of normalized articles
    """
    articles = []

    try:
        arxiv_articles = await search_arxiv_async(concept)
    except Exception as e:
        logging.error(f"[arxiv] Error: {e}")
        arxiv_articles = []

    try:
        pubmed_articles = await search_pubmed_async(concept)
    except Exception as e:
        logging.error(f"[pubmed] Error: {e}")
        pubmed_articles = []

    try:
        openalex_articles = await search_openalex_async(concept)
    except Exception as e:
        logging.error(f"[openalex] Error: {e}")
        openalex_articles = []

    try:
        zenodo_articles = await search_zenodo_async(concept)
    except Exception as e:
        logging.error(f"[zenodo] Error: {e}")
        zenodo_articles = []

    sources = {
        "arxiv": arxiv_articles,
        "pubmed": pubmed_articles,
        "openalex": openalex_articles,
        "zenodo": zenodo_articles
    }

    for name, source in sources.items():
        if isinstance(source, list) and all(isinstance(a, dict) for a in source):
            articles += normalize_source(raw_articles=source, source_name=name)
        else:
            logging.warning(f"[{name}] Invalid data or unrecognized structure.")

    logging.info(f"Total normalized articles: {len(articles)}")
    return articles

# Check if articles exist and format the text
example_query = "quantum physics"  # Define the query
articles = await search_multi_database(example_query)
zenodo_articles = await search_zenodo_async(example_query)

# === Prompt construction and response ===
# Perform academic database search
pubmed_results = await search_pubmed_async(concept)
openalex_results = await search_openalex_async(concept)
arxiv_results = await search_arxiv_async(concept)
zenodo_results = await search_zenodo_async(concept)

chart_choice_text = "Chart included" if chart_choice.lower() in ["yes"] else "Text only"

paper_text = ""  # Or provide a predefined text

# Modify language handling in the prompt to avoid errors
prompt = prompt_template.format(
    problem=example_problem,
    topic=topic,
    concept=concept,
    level=level,
    subject=subject,
    arxiv_search=arxiv_results,
    paper_text=paper_text,
    pubmed_search=pubmed_results,
    zenodo_search=zenodo_results,
    openalex_search=openalex_results,
    chart_choice=chart_choice_text,
    target_language=target_language
)

try:
    # Generate response
    response = llm.invoke(prompt.strip())
    response_content = getattr(response, "content", str(response))

    if not response_content or "Error" in response_content:
        raise ValueError("Invalid AI model response")
    logging.info("Response successfully generated.")

    # Reasoning explanation (metacognition)
    reasoning_explanation = explain_reasoning(prompt, response_content)
    print("Reasoning explanation:\n", getattr(reasoning_explanation, "content", reasoning_explanation))

    # Operational decision (AGI Point 5)
    objective = generate_objective_from_input(example_problem)
    decision = llm.invoke(f"Objective: {objective}\nPrompt: {prompt.strip()}")
    action = getattr(decision, "content", str(decision)).strip()
    print(f"Agent's autonomous decision: {action}")

except Exception as e:
    logging.error(f"General error in AGI operational block: {e}")


# This cell executes a generation + metacognition cycle

final_response = metacognitive_cycle(example_problem, level)

# Generates and evaluates the response for coherence and potential improvement
def generate_and_evaluate(generation_prompt, question, level):
    response = llm.invoke(generation_prompt)
    evaluation_prompt = f"""
    You received the following response: "{getattr(response, 'content', response)}".
    - Is it coherent with the question: "{question}"?
    - Is the tone appropriate for the '{level}' level?
    - How would you improve the response?
    """
    feedback = llm.invoke(evaluation_prompt)
    return response, feedback

import time

def execute_with_retry(function, max_attempts=3, base_delay=2):
    for attempt in range(max_attempts):
        try:
            return function()
        except InternalServerError as e:
            logging.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(base_delay * (attempt + 1))
        except Exception as e:
            logging.error(f"Unhandled error: {e}")
            break
    return "Persistent error: unable to complete the operation."


# === Visualization (optional) ===
if chart_requested and diagram_type_ml in ["Chart", "Conceptual diagram", "State diagram"]:
    logging.info("Generating interactive chart...")
    try:
        fig, caption = generate_interactive_chart(example_problem)
        fig.show()
        logging.info("Chart successfully generated!")
    except Exception as e:
        logging.error(f"Error during chart generation: {e}")
else:
    logging.info("Chart not requested or not necessary.")


from IPython.display import FileLink
FileLink(file_name)