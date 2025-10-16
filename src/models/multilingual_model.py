# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# === Text Translation ===

# Caching dictionary for previously translated texts
translation_cache = {}


def detect_language(text):
    """Detects the language of the loaded text."""
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return "unknown"

def translate_text(text, source_lang, target_lang):
    """ Translates the text with debug output to verify correctness. """
    translation_model = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"

    print(f"Using translation model: {translation_model}")

    translator = pipeline("translation", model=translation_model)

    translation = translator(text)[0]['translation_text']
    print(f"Original text: {text}")
    print(f"Translated text: {translation}")

    return translation

def extract_text_pdf(file_name):
    """ Extracts text from a PDF file. """
    text = ""
    with pdfplumber.open(file_name) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_docx(file_name):
    """ Extracts text from a DOCX file. """
    doc = Document(file_name)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text.strip()

def save_docx(text, output_file_name):
    """ Saves translated text into a DOCX document. """
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_file_name)

def extract_text_csv(file_name):
    """ Extracts textual content from a CSV file. """
    df = pd.read_csv(file_name)
    text = df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep='\n')
    return text.strip()

def extract_text_tsv(file_name):
    """ Extracts textual content from a TSV file. """
    df = pd.read_csv(file_name, sep='\t')
    text = df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep='\n')
    return text.strip()

def handle_file(file_name):
    """ Loads the file, detects its language, and lets the user choose a target language for translation. """
    extension = file_name.split('.')[-1].lower()

    if extension == "pdf":
        text = extract_text_pdf(file_name)
    elif extension == "docx":
        text = extract_text_docx(file_name)
    elif extension == "csv":
        text = extract_text_csv(file_name)
    elif extension == "tsv":
        text = extract_text_tsv(file_name)
    else:
        return "Unsupported format! Use PDF, DOCX, CSV, or TSV."

    original_language = detect_language(text)
    print(f"The file was detected in **{original_language}**.")

    # List of available languages
    available_languages = ["en", "fr", "de", "es", "zh", "ja", "ar", "it"]

    # Ask the user for the target language
    print(f"Available languages for translation: {', '.join(available_languages)}")
    target_language = input("Which language do you want the explanation in? (e.g., 'en' for English, 'fr' for French): ").strip()

    if target_language not in available_languages:
        print("Error: Unsupported language!")
    else:
        print(f"The explanation will be translated into {target_language}.")

    # Ensure translation is performed
    translated_text = translate_text(text, original_language, target_language)

    # Save the translated file
    translated_file_name = f"translated_{target_language}_{file_name}"
    if extension == "pdf":
        with open(translated_file_name, "w", encoding="utf-8") as f:
            f.write(translated_text)
    elif extension == "docx":
        save_docx(translated_text, translated_file_name)

    return f"Translation completed! Download the file: {translated_file_name}"

# Initialize the dictionary to store journals
journal_store = {}

def save_multilingual_journal(journal_text, journal_id, target_language):
    source_language = detect_language(journal_text)

    if source_language != target_language:
        translated_text = translate_long_text(journal_text, source_lang=source_language, target_lang=target_language)
    else:
        translated_text = journal_text

    journal_store[journal_id] = {
        "original": journal_text,
        target_language: translated_text
    }

    embedding = safe_encode(translated_text)
    index.add(np.array(embedding, dtype=np.float32))



def translate_long_text(text, source_lang="it", target_lang="en", max_chars=400):
    translation_model = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    translator = pipeline("translation", model=translation_model)

    blocks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    translated = []

    for block in blocks:
        try:
            output = translator(block)[0]['translation_text']
            translated.append(output)
        except Exception as e:
            print(f"Error translating block: {e}")
            translated.append("[Translation error]")

    return "\n".join(translated)

def search_similar_journals(query, target_language, top_k=3):
    query_language = detect_language(query)

    if query_language != target_language:
        translated_query = translate_long_text(query, source_lang=query_language, target_lang=target_language)
    else:
        translated_query = query

    query_emb = safe_encode(translated_query)
    query_emb = np.array(query_emb, dtype=np.float32)

    if hasattr(index, "is_trained") and not index.is_trained:
        print("FAISS index is not trained.")
        return []

    D, I = index.search(query_emb, top_k)
    results = []
    for i in I[0]:
        journal = journal_store.get(i, {})
        results.append(journal.get(target_language, ""))
    return results

# === Valid Input Function ===
def get_valid_input(message, valid_options=None):
    while True:
        value = input(message).strip().lower()
        if not value:
            print("Error! Please enter a valid value.")
        elif valid_options and value not in valid_options:
            print(f"Error! You must choose from: {', '.join(valid_options)}")
        else:
            return value