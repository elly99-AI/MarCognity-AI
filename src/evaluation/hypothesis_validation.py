# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Generate an automatic report
def generate_markdown_report(
    title="Automatic Report",
    description="Automatically generated scientific summary.",
    articles=None,
    images=None,
    captions=None,
    filename="report.md"
):
    """
    Generates a Markdown file with:
    - Title and description
    - Scientific articles with abstract and link
    - Images and associated captions (if available)

    All arguments are optional. A coherent structure is created regardless.
    """

    # Safe fallback for each parameter
    articles = articles if isinstance(articles, list) else []
    images = images if isinstance(images, list) else []
    captions = captions if isinstance(captions, list) else []

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"{description}\n\n")

            f.write("## Scientific Articles\n\n")
            if articles:
                for i, art in enumerate(articles[:5]):
                    article_title = art.get("titolo", f"Article {i+1}")
                    abstract = art.get("abstract", "Abstract not available.")
                    url = art.get("url", "#")
                    f.write(f"**{i+1}. {article_title}**\n")
                    f.write(f"{abstract}\n\n[Link to article]({url})\n\n")
            else:
                f.write("No articles available.\n\n")

            if images:
                f.write("## Figures\n\n")
                for i, img_path in enumerate(images):
                    caption = captions[i] if i < len(captions) else f"Figure {i+1}"
                    f.write(f"![{caption}]({img_path})\n\n*{caption}*\n\n")

        print(f"Markdown report successfully generated: {filename}")
    except Exception as e:
        print(f"Error during report generation: {e}")

# === Markdown report generation ===
def generate_markdown_report(title, description, articles, filename="report.md"):
    if not isinstance(articles, list):
        logging.error(f"[generate_markdown_report] 'articles' is not a valid list: {type(articles)}")
        print("Error: unable to generate report. Invalid article format.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{description}\n\n## Scientific Articles\n\n")
        for i, art in enumerate(articles[:5]):
            if isinstance(art, dict) and all(k in art for k in ["titolo", "abstract", "url"]):
                f.write(f"**{i+1}. {art['titolo']}**\n{art['abstract']} ([Link]({art['url']}))\n\n")
            else:
                f.write(f"**{i+1}. Article data not available or incomplete.**\n\n")
    print(f"Markdown report generated: {filename}")