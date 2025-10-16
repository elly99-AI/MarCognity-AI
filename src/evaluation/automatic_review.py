# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Verify the methodology of the text using an LLM
def verify_methodology(paper_text):
    prompt = f"Analyze the 'Methods' section and check whether the experiment is replicable:\n{paper_text}"
    return llm.invoke(prompt.strip())

# Enrich the context of the response
async def enrich_context(query):
    """ Retrieves scientific data to enrich the LLM's context. """
    articles = await search_multi_database(query)

    context = "\n".join([f"**{a['title']}** - {a['abstract']}" for a in articles[:3]])  # Select the first 3 articles
    return context if context else "No relevant scientific articles found."

# Automated review of scientific papers
async def review_paper(paper_text):
    """ Analyzes the paper's methodology and citations. """
    methodology = await verify_methodology(paper_text)
    citations = await verify_citations(paper_text)

    review = {
        "methodology_analysis": methodology,
        "citation_validation": citations,
        "improvement_suggestions": suggest_improvements(paper_text)
    }

    return review

# === Asynchronous function for scientific search and analysis using SciBERT ===
async def search_arxiv_async(query):
    # TODO: Implement asynchronous API call to arXiv or other repository
    return []  # Placeholder article list

async def analyze_scientific_text(problem, concept):
    articles = await search_arxiv_async(concept)
    context = "\n".join([f"{a.get('title', '')}: {a.get('abstract', '')[:300]}..." for a in articles])
    scibert_response = scibert_model(question=problem, context=context)
    return scibert_response.get("answer", "")

# === Function to search for experimental data ===
def search_experimental_data(query):
    url = f"https://api.openphysicsdata.org/search?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return "No experimental data found."