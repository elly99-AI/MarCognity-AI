# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Load the model only once
cross_encoder = CrossEncoder("cross-encoder/nli-deberta-base")

def evaluate_coherence(question, answer):
    score = cross_encoder.predict([(question, answer)])
    try:
        logit = float(score[0]) if isinstance(score[0], (int, float, np.floating)) else float(score[0][0])
        probability = 1 / (1 + math.exp(-logit))  # Sigmoid function
        return round(probability, 3)
    except Exception:
        return 0.0

# === Scientific reliability score calculation ===
def calculate_impact_score(citations, h_index, peer_review, publication_year):
    score = (citations * 0.4) + (h_index * 0.3) + (peer_review * 0.2) - (2025 - publication_year) * 0.1
    return max(0, score)  # Ensure non-negative

def check_topic_relevance(user_question, extracted_text, threshold=0.7):
    """Checks whether the topic of the question is consistent with the uploaded file content."""
    emb_question = embedding_model.encode([user_question])
    emb_text = embedding_model.encode([extracted_text])

    similarity = np.dot(emb_question, emb_text.T) / (np.linalg.norm(emb_question) * np.linalg.norm(emb_text))
    return round(similarity, 3), similarity >= threshold

def calculate_response_score(question, answer):
    score = cross_encoder.predict([(question, answer)])
    return float(score[0])

def regenerate_if_low_score(question, answer, level, threshold=0.7, iterations=2):
    evaluation = evaluate_responses_with_ai(question, answer, level)
    if evaluation["semantic_score"] < threshold:
        new_question = reformulate_question(question)
        for i in range(iterations):
            new_answer = generate_response(new_question, temperature=0.7)
            new_evaluation = evaluate_responses_with_ai(new_question, new_answer, level)
            if new_evaluation["semantic_score"] >= threshold:
                return new_answer
    return answer

def select_best_version(question, answers):
    scored = [(r, calculate_response_score(question, r)) for r in answers]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0]  # (answer, score)