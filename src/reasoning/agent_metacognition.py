# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# === metacognitive_cycle ===
# Executes an iterative cycle of evaluation and improvement of the generated response.
# Combines qualitative feedback and semantic coherence score to decide whether to reformulate.
# Useful for simulating reflective and adaptive behavior.

def generate_objective_from_input(user_input):
    """
    Generates a high-level operational objective based on the user's input.
    Useful for AGI-style planning and decision-making.
    """
    prompt = f"""
    You are an autonomous scientific agent. Based on the following input:
    "{user_input}"

    Define a clear and actionable objective that guides the agent's next steps.
    """
    try:
        response = llm.invoke(prompt.strip())
        return getattr(response, "content", str(response)).strip()
    except Exception as e:
        logging.error(f"Error generating objective: {e}")
        return "Objective generation failed."


async def metacognitive_cycle(question, level, max_iter, context_docs):
    response = llm.invoke(question)
    response_text = extract_text_from_ai(response)

    for i in range(max_iter):
        feedback = auto_feedback_response(question, response_text, level)
        score = evaluate_coherence(question, response_text)

        print(f"\nIteration {i+1} – Coherence: {score:.3f}")
        print("Feedback:", extract_text_from_ai(feedback))

        if score < 0.7:
            response_text = extract_text_from_ai(improve_response(question, response_text, level))
        else:
            break

    # SKEPTICAL AGENT INTEGRATION
    # The skeptic steps in now that the response is coherent
    print("\n[Skeptical Agent] Analyzing epistemic traceability...")
    skeptical_report = skeptical_agent(question, response_text, context_docs)

    # Citation Verification (Bibliographic Cross-check) ---
    verified_refs = await verify_citations(response_text)

    # 3. Final Report Assembly
    full_output = response_text
    full_output += "\n\n" + "="*40
    full_output += "\n## SKEPTICAL AGENT REPORT (Critical Analysis)\n"
    full_output += skeptical_report                                                        #
    full_output += "\n" + "="*40

    full_output += "\n\n## VERIFIED BIBLIOGRAPHIC REFERENCES\n"
    if verified_refs:
        for r in verified_refs:
            status = "verified" if r["verified"] else "unverified"
            full_output += f"- {r['citation']} ({status})\n"
    else:
        full_output += "No citations found or verifiable in the text."

    return full_output


# Evaluate response with self-assessment and interactive improvement
# Evaluates the response and reformulates it if poorly constructed
def evaluate_responses_with_ai(question, generate_response_fn, n_variants=3, reformulation_threshold=0.6):
    temperature_values = [0.7, 0.4, 0.9][:n_variants]
    responses = [generate_response_fn(question, temperature=t) for t in temperature_values]

    scores = [evaluate_coherence(question, r) for r in responses]
    idx = scores.index(max(scores))
    confidence = scores[idx]
    best_response = responses[idx]

    if confidence < reformulation_threshold:
        new_question = reformulate_question(question)
        return evaluate_responses_with_ai(new_question, generate_response_fn)

    return {
        "response": best_response,
        "confidence": round(confidence, 3),
        "note": generate_note(confidence)
    }

def evaluate_responses_with_ai_simple(question, response, level="basic"):
    """
    Evaluates the quality of the generated response relative to the question.
    Returns a dictionary with:
    - semantic coherence score
    - reason for weakness
    - suggested reformulation
    - reflection on reasoning
    - flag for auto-improvement
    """

    evaluation_prompt = f"""
    User question: "{question}"
    Generated response: "{response}"
    Required level: {level}

    Evaluate the response in 5 points:
    1. Semantic coherence (0–1)
    2. Conceptual completeness
    3. Argumentative structure
    4. Adequacy to the required level
    5. Ability to stimulate new questions

    If the response is weak:
    - Explain the reason
    - Suggest a reformulation
    - Reflect on how the system reasoned

    Return everything in structured format.
    """

    try:
        ai_evaluation = llm.invoke(evaluation_prompt)
        raw_output = getattr(ai_evaluation, "content", str(ai_evaluation))
    except Exception as e:
        print("Evaluation error:", e)
        return {
            "semantic_score": 0.0,
            "weakness_reason": "System error",
            "new_formulation": None,
            "self_reflection": None,
            "requires_improvement": True
        }

    # Simplified parsing functions (can be enhanced with regex or LLM)
    def extract_score(text):
        match = re.search(r"Semantic coherence\s*[:\-]?\s*(0\.\d+)", text)
        return float(match.group(1)) if match else 0.0

    def extract_reason(text):
        match = re.search(r"Reason\s*[:\-]?\s*(.+)", text)
        return match.group(1).strip() if match else "Reason not found."

    def extract_reformulation(text):
        match = re.search(r"Reformulation\s*[:\-]?\s*(.+)", text)
        return match.group(1).strip() if match else None

    def extract_reflection(text):
        match = re.search(r"Reflection\s*[:\-]?\s*(.+)", text)
        return match.group(1).strip() if match else None

    # Actual parsing
    score = extract_score(raw_output)
    reason = extract_reason(raw_output)
    reformulation = extract_reformulation(raw_output)
    reflection = extract_reflection(raw_output)

    return {
        "response": response,
        "semantic_score": score,
        "weakness_reason": reason,
        "new_formulation": reformulation,
        "self_reflection": reflection,
        "requires_improvement": score < 0.7
    }

def generate_metacognitive_content(question, response, evaluation):
    return f"""
    [Question] {question}
    [Response] {response}
    [Coherence Score] {evaluation['semantic_score']}
    [Weakness Reason] {evaluation['weakness_reason']}
    [Suggested Reformulation] {evaluation['new_formulation']}
    [Cognitive Reflection] {evaluation['self_reflection']}
    [Needs Improvement] {evaluation['requires_improvement']}
    """.strip()

def add_metacognitive_memory(question, response):
    # Cognitive evaluation of the response
    evaluation = evaluate_responses_with_ai(question, response)

    # Generate textual content with all metacognitive data
    textual_content = generate_metacognitive_content(question, response, evaluation)

    # Generate semantic embedding from the full content
    embedding = embedding_model.encode([textual_content])

    # Add to FAISS index
    index.add(np.array(embedding, dtype=np.float32))

    # Save updated index
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index, f)

    print("Metacognitive memory updated!")

def search_similar_reasoning(query, top_k=5):
    """
    Searches the FAISS metacognitive memory for reasoning most similar to the input query.
    Returns a list of the most relevant textual contents.
    """
    # Encode the query
    query_vector = embedding_model.encode([query])

    # Search for top-K nearest
    distances, indices = index.search(np.array(query_vector, dtype=np.float32), top_k)

    results = []
    for idx in indices[0]:
        try:
            with open("meta_diary.json", "r", encoding="utf-8") as f:
                archive = json.load(f)
                content = archive.get(str(idx))
                if content:
                    results.append(content)
        except Exception as e:
            print(f"Memory retrieval error: {e}")

    return results

def add_metacognition_to_response(response, evaluation):
    reflection = evaluation.get("self_reflection", "")
    note = evaluation.get("weakness_reason", "")
    return f"{response.strip()}\n\n*Metacognitive note:* {note}\n*Agent's reflection:* {reflection}"

def auto_feedback(question, response, level):
    return f"""Analyze the response in relation to the question: "{question}".
Evaluate the content according to the level '{level}' and suggest improvements.
"""

# === Full flow example ===
async def scientific_creativity_flow(concept, subject, language="en", level="advanced"):
    creative_hypothesis = simulate_scientific_creativity(concept, subject, language=language, level=level)
    articles, _ = await search_multi_database(concept)  # Retrieve existing scientific sources
    novelty_evaluation = evaluate_hypothesis_novelty(creative_hypothesis, articles)

    return {
        "hypothesis": creative_hypothesis,
        "novelty": novelty_evaluation

    }
