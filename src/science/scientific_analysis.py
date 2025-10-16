# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# === Asynchronous Functions ===
MAX_REQUESTS = 5
API_SEMAPHORE = asyncio.Semaphore(MAX_REQUESTS)

async def safe_api_request(url):
    async with API_SEMAPHORE:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    return await response.json()
            except Exception as e:
                logging.error(f"API request error: {e}")
                return None

# Connection pooling
async def safe_api_request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logging.error(f"API request error: {e}")
            return None

# Smart timeout
import asyncio

async def timeout_handler(task, timeout=20):
    try:
        return await asyncio.wait_for(task, timeout)
    except asyncio.TimeoutError:
        logging.error("API request timed out")
        return None

import requests

url = "http://export.arxiv.org/api/query?search_query=all:physics&start=0&max_results=1"
response = requests.get(url, timeout=50)

if response.status_code == 200:
    print("Connection to arXiv OK")
else:
    print(f"Connection error: {response.status_code}")

# Advanced parallelization
async def fetch_multiple_data(urls):
    tasks = [safe_api_request(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Retrieve scientific sources from Zenodo
async def search_zenodo_async(query, max_results=5):
    """
    Searches for open access articles and resources from Zenodo using their public API.
    """
    url = f"https://zenodo.org/api/records/?q={query}&size={max_results}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()

                articles = []
                for hit in data.get("hits", {}).get("hits", []):
                    title = hit.get("metadata", {}).get("title", "Title not available")
                    authors = ", ".join([c.get("name", "") for c in hit.get("metadata", {}).get("creators", [])])
                    abstract = hit.get("metadata", {}).get("description", "Abstract not available")
                    link = hit.get("links", {}).get("html", "No link")

                    articles.append({
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "url": link
                    })

                return articles if articles else [{"error": "No results found on Zenodo."}]

        except Exception as e:
            return []

# Retrieve scientific sources from PubMed
async def search_pubmed_async(query, max_results=5):
    """ Asynchronously retrieves scientific articles from PubMed. """
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=xml"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                content = await response.text()
                root = ET.fromstring(content)

                articles = []
                for id_element in root.findall(".//Id"):
                    pubmed_id = id_element.text
                    articles.append(f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/")  # Article links
                return articles
        except Exception as e:
            return f"PubMed error: {e}"


# Function to handle asynchronous responses from arXiv
def parse_arxiv_response(content):
    """ Extracts titles and abstracts from arXiv articles. """
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        logging.error("Error parsing arXiv XML.")
        return []

    articles = []
    for entry in root.findall(".//entry"):
        title = entry.find("title").text if entry.find("title") is not None else "Title not available"
        abstract = entry.find("summary").text if entry.find("summary") is not None else "Abstract not available"
        articles.append({"title": title, "abstract": abstract})

    return articles

# === Asynchronous search on arXiv ===
# Queries the arXiv API to retrieve scientific articles.
async def search_arxiv_async(query, max_results=3, retry_attempts=3, timeout=20):
    """ Retrieves scientific articles from arXiv with advanced error handling. """
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

    async with aiohttp.ClientSession() as session:
        for attempt in range(retry_attempts):
            try:
                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()
                    content = await response.text()

                    if not content.strip():
                        raise ValueError("Error: Empty response from arXiv.")

                    return parse_arxiv_response(content)

            except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
                wait_time = min(2 ** attempt + np.random.uniform(0, 1), 10)  # Max wait time: 10 seconds
                logging.error(f"Attempt {attempt+1}: Error - {e}. Retrying in {wait_time:.1f} seconds...")
                await asyncio.sleep(wait_time)

    logging.error("Error: Unable to retrieve data from arXiv after multiple attempts.")
    return []

# === Asynchronous search on OpenAlex ===
# Retrieves scientific articles with complete metadata (title, authors, abstract, DOI)
async def search_openalex_async(query, max_results=5):
    """ Safely retrieves scientific articles from OpenAlex. """
    url = f"https://api.openalex.org/works?filter=title.search:{query}&per-page={max_results}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()

                articles = []
                for record in data.get("results", []):
                    title = record.get("title", "Title not available")

                    authors = ", ".join([
                        aut.get("display_name", "Unknown author")
                        for aut in record.get("authorships", [])
                    ])

                    abstract = record.get("abstract", "Abstract not available")
                    article_url = record.get("doi") or record.get("id", "No link")

                    articles.append({
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "url": article_url
                    })

                return articles

        except Exception as e:
            return f"OpenAlex error: {e}"


# === Synchronous search on BASE ===
# Queries the BASE engine for open-access articles.
def search_base(query, max_results=5):
    url = f"https://api.base-search.net/cgi-bin/BaseHttpSearchInterface?q={query}&num={max_results}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        results = []
        for record in data.get("docs", []):
            title = record.get("dcTitle", ["Title not available"])[0]
            link = record.get("link", ["No link available"])[0]
            results.append(f"**{title}**\n[Link to article]({link})\n")

        return "\n\n".join(results) if results else "No results found."

    except Exception as e:
        return f"Error during BASE search: {e}"

# === Distributed search across multiple databases ===
# Executes parallel queries on arXiv, OpenAlex, PubMed, Zenodo.
async def search_multi_database(query):
    try:
        tasks = [
            search_arxiv_async(query),
            search_openalex_async(query),
            search_pubmed_async(query),
            search_zenodo_async(query)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        articles = []
        for source in results:
            if isinstance(source, list):
                articles += source
            else:
                logging.warning(f"Invalid source: {type(source)} → {source}")

        # Normalize immediately after
        articles = normalize_articles(articles)

        if isinstance(articles, list) and all(isinstance(a, dict) for a in articles):
            formatted_search = format_articles(articles)
        else:
            logging.error(f"Error: 'articles' is not a valid list. Type received: {type(articles)} - Value: {repr(articles)}")
            formatted_search = "Unable to format search: response not properly structured."

        return articles, formatted_search

    except Exception as e:
        logging.error(f"Error during multi-database search: {e}")
        return [], "Internal error"


# === Scientific Source Integration ===
# Selects the first N valid articles and formats them as Markdown references.
async def integrate_sources_from_database(concept, max_sources=5):
    articles, formatted_search = await search_multi_database(concept)

    if not isinstance(articles, list) or not all(isinstance(a, dict) for a in articles):
        logging.warning("Invalid 'articles' structure. No sources will be displayed.")
        return "No valid sources available."

    references = []
    for a in articles[:max_sources]:
        title = a.get("title", "Title not available")
        url = a.get("url", "#")
        if url and isinstance(url, str):
            references.append(f"- [{title}]({url})")

    return "\n".join(references) if references else "No relevant sources found."


# === Data Normalization ===
# Converts heterogeneous input (dicts, strings, links) into a consistent list of articles.
def normalize_source(source):
    if isinstance(source, list) and all(isinstance(x, dict) for x in source):
        return source
    elif isinstance(source, dict):  # Single article as dictionary
        return [source]
    elif isinstance(source, str):  # Unstructured string
        logging.warning(f"Ignored textual source: {source[:50]}...")
        return []
    else:
        logging.warning(f"Invalid source type: {type(source)}")
        return []

def normalize_articles(article_list):
    valid_articles = []
    for a in article_list:
        if isinstance(a, dict):
            valid_articles.append(a)
        elif isinstance(a, str) and "pubmed.ncbi.nlm.nih.gov" in a:
            valid_articles.append({
                "title": "PubMed Link",
                "abstract": "Not available",
                "url": a,
                "authors": "Unknown"
            })
        else:
            logging.warning(f"Ignored: {repr(a)}")
    return valid_articles

articles, formatted_search = await search_multi_database("quantum physics")
print(formatted_search)


# === Async Task Protection Wrapper ===
# Handles timeouts and errors during asynchronous function execution.
def protect_async_task(func):
    async def wrapper(*args, **kwargs):
        try:
            return await asyncio.wait_for(func(*args, **kwargs), timeout=20)
        except asyncio.CancelledError:
            logging.warning("Task cancelled.")
            return None
        except Exception as e:
            logging.error(f"Error during execution of {func.__name__}: {e}")
            return None
    return wrapper

# === Asynchronous Scientific Explanation Generation ===
# Builds the prompt and invokes the LLM model.
async def generate_explanation_async(problem, level, concept, topic):
    """Generates the explanation using the LLM asynchronously."""
    prompt = prompt_template.format(
        problem=problem,
        concept=concept,
        topic=topic,
        level=level
    )
    try:
        response = await asyncio.to_thread(llm.invoke, prompt.strip())
        return response
    except Exception as e:
        logging.error(f"LLM API error: {e}")
        return "Error generating the response."

# === Conditional Interactive Chart Generation ===
# Generates a chart based on the analyzed problem if requested.
def generate_conditional_chart(problem, chart_choice):
    """Generates an interactive chart if requested."""
    fig = None
    if chart_choice.lower() in ["yes", "y"]:
        try:
            fig = generate_interactive_chart(problem)
            if fig is None:
                raise ValueError("Chart not generated correctly.")
            print("Chart generated successfully!")
        except Exception as e:
            logging.error(f"Chart error: {e}")
    return fig

# === Structured Output: Text + Chart ===
# Combines the generated explanation with the graphical visualization.
async def generate_complete_result(problem, level, concept, topic, chart_choice):
    """Combines explanation and chart to generate a structured output."""
    response = await generate_explanation_async(problem, level, concept, topic)
    chart = generate_conditional_chart(problem, chart_choice)
    return {
        "response": response,
        "chart": chart
    }


# === Scientific Article Validation ===
# Checks that each article has a title, abstract, and URL.
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