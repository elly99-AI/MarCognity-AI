# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Sample data for ranking
data = np.array([
    [120, 45, 1, 2023],  # Citations, h-index, peer review, year
    [50, 30, 1, 2020],
    [10, 15, 0, 2018]
])

labels = [95, 70, 30]  # Academic impact score

# Model training
ranking_model = RandomForestRegressor(n_estimators=100)
ranking_model.fit(data, labels)

# **Ranking prediction**
def calculate_impact_score(citations, h_index, peer_review, publication_year):
    paper_data = np.array([[citations, h_index, peer_review, publication_year]])
    score = ranking_model.predict(paper_data)
    return max(0, score[0])  # Ensure non-negative

# Usage example
impact_score = calculate_impact_score(80, 40, 1, 2024)
print(f"Estimated score: {impact_score}")

# Ranking model
from sklearn.ensemble import RandomForestRegressor

# Sample data for ranking
data = np.array([
    [120, 45, 1, 2023],  # Citations, h-index, peer review, year
    [50, 30, 1, 2020],
    [10, 15, 0, 2018]
])

labels = [95, 70, 30]  # Academic impact score

# Model training
ranking_model = RandomForestRegressor(n_estimators=100)
ranking_model.fit(data, labels)

# Ranking prediction
new_paper = np.array([[80, 40, 1, 2024]])
score = ranking_model.predict(new_paper)
print(f"Estimated score: {score[0]}")

# === Scientific originality evaluation ===
def evaluate_hypothesis_novelty(hypothesis, existing_articles, threshold=0.7):
    """
    Compares the hypothesis with existing articles using semantic embeddings.
    Returns:
    - average similarity score
    - similar articles
    - qualitative assessment of originality
    """
    try:
        emb_hypothesis = model_embedding.encode([hypothesis])
        emb_articles = model_embedding.encode([a["abstract"] for a in existing_articles if "abstract" in a])

        similarity = np.dot(emb_hypothesis, emb_articles.T) / (
            np.linalg.norm(emb_hypothesis) * np.linalg.norm(emb_articles, axis=1)
        )
        average = round(float(np.mean(similarity)), 3)

        similar_articles = [
            existing_articles[i]["title"]
            for i, score in enumerate(similarity[0]) if score > threshold
        ]

        if average < 0.4:
            assessment = "High originality: hypothesis is rarely present in the literature."
        elif average < 0.7:
            assessment = "Moderate originality: related concepts exist."
        else:
            assessment = "Low originality: hypothesis is already widely discussed."

        return {
            "novelty_score": average,
            "similar_articles": similar_articles,
            "assessment": assessment
        }

    except Exception as e:
        logging.error(f"[evaluate_novelty] Error during originality evaluation: {e}")
        return {
            "novelty_score": 0.0,
            "similar_articles": [],
            "assessment": "Error during originality evaluation."
        }

# Automated paper review with AI
async def review_paper(paper_text):
    """ Checks the methodology and citation quality of a paper. """
    methodology = await verify_methodology(paper_text)
    citations = await verify_citations(paper_text)
    return {"methodology": methodology, "citations": citations}

async def validate_hypothesis(hypothesis):
    sources = await search_multi_database(hypothesis)
    score = calculate_impact_score(sources)  # Based on citations, year, h-index, etc.
    summary = summarize_evidence(sources)
    return score, summary

def summarize_evidence(sources):
    return "\n".join([
        f"- {a['title'][:80]}…" for a in sources if isinstance(a, dict) and 'title' in a
    ]) if sources else "No evidence found."
