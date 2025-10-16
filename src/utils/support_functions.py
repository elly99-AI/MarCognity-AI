# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Evaluate the structure of the AI response from the LLM
def validate_ai_structure(response, expected_fields=("title", "abstract", "url")):
    if not isinstance(response, list):
        return []
    valid_items = []
    for item in response:
        if isinstance(item, dict) and all(k in item for k in expected_fields):
            valid_items.append(item)
    return valid_items

import math

# Compute semantic score of the response
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def evaluate_score(model_output):
    try:
        score = float(model_output[0])
        return round(sigmoid(score), 3)
    except:
        return 0.0

# Extract text from selected file
def extract_text(file_name, max_chars=5000):
    """
    Extracts text from supported formats (.pdf, .docx, .tsv, .csv).
    Returns only the first max_chars characters.
    """
    extension = file_name.lower().split(".")[-1]

    try:
        if extension == "pdf":
            with pdfplumber.open(file_name) as pdf:
                text = "\n".join([p.extract_text() or "" for p in pdf.pages]).strip()

        elif extension == "docx":
            doc = Document(file_name)
            text = "\n".join([p.text for p in doc.paragraphs]).strip()

        elif extension in ["csv", "tsv"]:
            sep = "," if extension == "csv" else "\t"
            df = pd.read_csv(file_name, sep=sep)
            text = df.to_string(index=False)

        else:
            raise ValueError(f"Unsupported format: .{extension}")

        return text[:max_chars] if text else "No text extracted."

    except Exception as e:
        return f"Error during text extraction: {e}"

# Safely extract textual content from an AIMessage
def extract_text_from_ai(obj):
    """ Safely extracts textual content from an AIMessage object. """
    return getattr(obj, "content", str(obj)).strip()

# Extract figure captions from text
def extract_captions_from_text(text):
    pattern = r"(Figure|Fig\.?)\s*\d+[:\.\-–]?\s*[^\n]+"
    return re.findall(pattern, text, re.IGNORECASE)

# Extract images and captions from a file
def extract_images_with_captions(file_path, output_folder="extracted_figures"):
    os.makedirs(output_folder, exist_ok=True)
    extension = file_path.lower().split(".")[-1]
    images = []
    captions = []

    try:
        if extension == "pdf":
            doc = fitz.open(file_path)
            full_text = "\n".join([p.get_text("text") for p in doc])
            extracted_captions = extract_captions_from_text(full_text)
            count = 0

            for i, page in enumerate(doc):
                for j, img in enumerate(page.get_images(full=True)):
                    base = doc.extract_image(img[0])
                    ext = base["ext"]
                    path = f"{output_folder}/page{i+1}_img{j+1}.{ext}"
                    with open(path, "wb") as f:
                        f.write(base["image"])
                    images.append(path)
                    captions.append(extracted_captions[count] if count < len(extracted_captions) else f"Figure {i+1}.{j+1}")
                    count += 1

        elif extension == "docx":
            doc = Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
            extracted_captions = extract_captions_from_text(text)
            count = 0

            for i, rel in enumerate(doc.part._rels):
                relation = doc.part._rels[rel]
                if "image" in relation.target_ref:
                    img_data = relation.target_part.blob
                    name = f"{output_folder}/docx_image_{i+1}.png"
                    with open(name, "wb") as f:
                        f.write(img_data)
                    images.append(name)
                    captions.append(extracted_captions[count] if count < len(extracted_captions) else f"Figure {i+1}")
                    count += 1

        else:
            print(f"Unsupported extension: .{extension}")

        print(f"{len(images)} image(s) extracted.")
        return images, captions

    except Exception as e:
        print(f"Error extracting images: {e}")
        return [], []

# Generate semantic coherence note based on score
def generate_note(score):
    if score > 0.85:
        return "High semantic coherence. The response is likely solid and relevant."
    elif score > 0.6:
        return "Moderate coherence. The response is understandable but may contain approximations."
    else:
        return "Low coherence. It may be helpful to rephrase the question or provide more context."

# Simulate LLM response generation
def generate_response(question, temperature=0.7):
    if "Rephrase" in question:
        return "How does enthalpy change during a phase transition?"
    return f"[Simulated response at temperature {temperature} for: {question}]"