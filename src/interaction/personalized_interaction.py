# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# This cell analyzes the user's question and adapts the response
# based on subject, skill level, language, and preferences.

# Analyze the question to extract intent and context
def analyze_question(question):
    question_lower = question.lower()
    if re.search(r"\d+|equation|formula|calculate|solve", question_lower):
        return "mathematical problem"
    elif re.search(r"anatomy|biology|description|organ|function|system", question_lower):
        return "descriptive-biological problem"
    elif re.search(r"experiment|measurement|test|observation", question_lower):
        return "experimental problem"
    else:
        return "theoretical problem"

# Extract semantic and conceptual characteristics
def extract_features(problem):
    problem_lower = problem.lower()
    if re.search(r"\d+|equation|formula|energy|speed", problem_lower):
        return "Chart"
    elif re.search(r"principle|theory|model|experiment", problem_lower):
        return "Conceptual diagram"
    elif re.search(r"pressure|volume|temperature|transformation", problem_lower):
        return "State diagram"
    else:
        return "Plain text"

# Reformulate the question to make it clearer for the model
def reformulate_question(question):
    prompt = f"""Reformulate this question in a technical and precise way for a scientific AI assistant.

Question: "{question}"

Return only the reformulated question, without explanations."""
    response = generate_response(prompt, temperature=0.5).strip()

    for prefix in [
        "The generated response to the question",
        "Return only the reformulated question",
        "Question:"
    ]:
        if response.lower().startswith(prefix.lower()):
            response = response[len(prefix):].strip(": .\"'\n")

    if "\n" in response:
        response = response.split("\n")[0].strip()

    return response

# === File upload ===
try:
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]
    file_text = extract_text(file_name)

    if not file_text or file_text == "Empty or non-textual file.":
        raise ValueError("The uploaded file does not contain valid text.")
except Exception as e:
    logging.error(f"File upload error: {e}")
    file_text = input("Manually enter the problem: ").strip()

# Save
with open(INDEX_FILE, "wb") as f:
    pickle.dump(index, f)

# Load
with open(INDEX_FILE, "rb") as f:
    index = pickle.load(f)


# Generate intelligent report
async def example_search():
    query = "quantum physics"
    articles = await search_multi_database(query)
    print(articles)

# Execute the function directly with await
await example_search()

# === User input ===
import asyncio

# Validate that input is correct and coherent
async def get_valid_input(message, valid_options=None):
    """ Asynchronous function to handle validated input. """
    while True:
        value = await asyncio.to_thread(input, message.strip())
        value = value.strip()

        if not value:
            print("Error! Please enter a valid value.")
        elif valid_options and value.lower() not in valid_options:
            print(f"Error! You must choose from: {', '.join(valid_options)}")
        else:
            return value

example_problem = ""

while not example_problem:
    example_problem = file_text.strip() if file_text.strip() else await get_valid_input("Enter the problem manually:")

subject = input("Enter the subject (e.g., physics, biology, etc.): ").strip().lower() or "general subject"
level = input("Choose the level (basic/advanced/expert): ").strip().lower()
while level not in ["basic", "advanced", "expert"]:
    level = input("Error! Enter basic/advanced/expert: ").strip().lower()

topic = input("Enter the scientific problem or topic: ").strip()

chart_choice = input("Do you want a chart for the explanation? (yes/no): ").strip().lower()
while chart_choice not in ["yes", "no"]:
    chart_choice = input("Error! Please answer 'yes' or 'no': ").strip().lower()

chart_requested = chart_choice == "yes"

fig = None
caption = ""

if chart_requested:
    try:
        fig, caption = generate_interactive_chart(example_problem)
        fig.show()
        logging.info("Chart successfully generated.")
    except Exception as e:
        logging.error(f"Chart generation error: {e}")
        fig = None
else:
    logging.info("Chart not requested by the user.")

available_languages = ["en", "fr", "de", "es", "zh", "ja", "ar", "it"]

target_language = input("Which language do you want the translation in? (" + ", ".join(available_languages) + "): ").strip().lower()
while target_language not in available_languages:
    target_language = input("Error! Choose a valid language from: " + ", ".join(available_languages) + ": ").strip().lower()

#Secure Translation and Protected Embedding Storage
save_multilingual_journal(
    journal_text=example_problem,
    journal_id=0,
    target_language=target_language
)

#Secure Translation and Protected Embedding Retrieval
similar_entries = search_similar_journals(
    query=example_problem,
    target_language=target_language
)

for s in similar_entries:
    print("Similar journal:", s)