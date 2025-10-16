# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Verify citations and update them
def verify_citations(paper_text):
    prompt = f"Analyze the citations and check whether they are relevant and up-to-date:\n{paper_text}"
    return llm.invoke(prompt.strip())

# Source validation and citation quality

# Verify citations extracted from the text
async def verify_citations(paper_text):
    """ Checks the quality and relevance of citations. """
    citations = extract_citations(paper_text)  # Function that extracts citations from the text
    verified_sources = []

    for citation in citations:
        pubmed_res = await search_pubmed_async(citation)
        arxiv_res = await search_arxiv_async(citation)
        openalex_res = await search_openalex_async(citation)
        zenodo_res = await search_zenodo_async(citation)

        verified_sources.append({
            "citation": citation,
            "valid_pubmed": bool(pubmed_res),
            "valid_arxiv": bool(arxiv_res),
            "valid_openalex": bool(openalex_res),
            "is_obsolete": check_obsolescence(citation)
        })

    return verified_sources

# Generate asynchronous LLM explanations
async def generate_explanation_async(problem, level, concept, topic):
    """ Generates an explanation using the LLM asynchronously. """
    prompt = prompt_template.format(problem=problem, concept=concept, topic=topic, level=level)
    try:
        return await asyncio.to_thread(llm.invoke, prompt.strip())  # Parallel LLM call
    except Exception as e:
        logging.error(f"LLM API error: {e}")
        return "Error generating the response."

# Format retrieved articles
def format_articles(articles):
    if isinstance(articles, list) and all(isinstance(a, dict) for a in articles):
        return "\n\n".join([
            f"**{a.get('title', 'Untitled')}**: {a.get('abstract', 'No abstract')}"
            for a in articles
        ]) if articles else "No articles available."
    else:
        logging.error(f"Error: 'articles' is not a valid list. Type received: {type(articles)} - Value: {repr(articles)}")
        return "Unable to format search results: unrecognized structure."

# Generate BibTeX citations for scientific articles
def generate_bibtex_citation(title, authors, year, url):
    """ Generates a BibTeX citation for a scientific article. """
    return f"""
@article{{{title.lower().replace(' ', '_')}_{year},
    title={{"{title}"}},
    author={{"{', '.join(authors)}"}},
    year={{"{year}"}},
    url={{"{url}"}}
}}
    """

# Validate scientific articles
def validate_articles(raw_articles, max_articles=5):
    """
    Validates and filters the list of articles received from an AI or API source.
    Returns a clean list of dictionaries containing at least 'title', 'abstract', and 'url'.
    """
    if not isinstance(raw_articles, list):
        logging.warning(f"[validate_articles] Invalid input: expected list, received {type(raw_articles)}")
        return []

    valid_articles = []
    for i, art in enumerate(raw_articles):
        if not isinstance(art, dict):
            logging.warning(f"[validate_articles] Invalid element at position {i}: {type(art)}")
            continue

        title = art.get("title")
        abstract = art.get("abstract")
        url = art.get("url")

        if all([title, abstract, url]):
            valid_articles.append({
                "title": str(title).strip(),
                "abstract": str(abstract).strip(),
                "url": str(url).strip()
            })
        else:
            logging.info(f"[validate_articles] Article discarded due to incomplete data (i={i}).")

    if not valid_articles:
        logging.warning("[validate_articles] No valid articles after filtering.")

    return valid_articles[:max_articles]