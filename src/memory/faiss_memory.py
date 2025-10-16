# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# === FAISS Parameters ===
INDEX_FILE = "faiss_memoria_pq.pkl"
dimension = 768
nlist = 100
m = 32
nbits = 8

# Load or create a FAISS index for vector memory
def load_or_create_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "rb") as f:
            index = pickle.load(f)
        # Verifica che l'indice sia addestrato
        if hasattr(index, "is_trained") and not index.is_trained:
            print("Indice FAISS caricato ma non addestrato. Addestramento in corso...")
            index.train(np.random.rand(5000, dimension).astype(np.float32))
            with open(INDEX_FILE, "wb") as f:
                pickle.dump(index, f)
        return index
    else:
        quantizer = faiss.IndexFlatL2(dimension)
        index = faiss.IndexIVFPQ(quantizer, dimension, nlist, m, nbits)
        index.train(np.random.rand(5000, dimension).astype(np.float32))
        with open(INDEX_FILE, "wb") as f:
            pickle.dump(index, f)
        return index

index = load_or_create_index()

if hasattr(index, "is_trained") and not index.is_trained:
    logging.warning("Indice FAISS non addestrato. Addestramento in corso...")
    index.train(np.random.rand(5000, DIMENSION).astype(np.float32))


# === Semantic coherence check ===
def check_coherence(query, response):
    emb_query = embedding_model.encode([query])
    emb_response = embedding_model.encode([response])
    similarity = np.dot(emb_query, emb_response.T) / (np.linalg.norm(emb_query) * np.linalg.norm(emb_response))
    if similarity < 0.7:
        return "The response is too generic, reformulating with more precision..."
    return response

# === Memory addition ===
# Each document is converted into embeddings and inserted into the index.
def add_to_memory(question, answer):
    emb_question = embedding_model.encode([question])
    if emb_question.shape[1] != index.d:
        raise ValueError(f"Embedding dimension ({emb_question.shape[1]}) not compatible with FAISS ({index.d})")
    index.add(np.array(emb_question, dtype=np.float32))
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index, f)
    print("Memory updated with new question!")

def add_diary_to_memory(diary_text, index):
    embedding = embedding_model.encode([diary_text])
    index.add(np.array(embedding, dtype=np.float32))

def search_similar_diaries(query, index, top_k=3):
    query_emb = embedding_model.encode([query])
    _, indices = index.search(np.array(query_emb, dtype=np.float32), top_k)
    return indices[0]  # You can then map these IDs to files or content

# === Context retrieval ===
def retrieve_context(question, top_k=3):
    emb_question = embedding_model.encode([question])
    _, indices = index.search(np.array(emb_question, dtype=np.float32), top_k)
    return [f"Similar response {i+1}" for i in indices[0]] if indices[0][0] != -1 else []

def retrieve_similar_embeddings(question, top_k=2):
    """
    Retrieves the top-k most similar embeddings to the given question.
    """
    emb = embedding_model.encode([question])
    _, indices = index.search(np.array([emb], dtype=np.float32), top_k)
    return [f"Similar response {i+1}" for i in indices[0]] if indices[0][0] != -1 else []

# === Multi-turn retrieval ===
# Retrieves context from previous conversations
def retrieve_multiturn_context(question, top_k=5):
    emb_question = embedding_model.encode([question])
    _, indices = index.search(np.array(emb_question, dtype=np.float32), top_k)
    context = [f"Previous turn {i+1}" for i in indices[0] if i != -1]
    return " ".join(context) if context else ""

# === Usage example ===
add_to_memory("What is general relativity?", "General relativity is Einstein's theory of gravity.")
similar_responses = retrieve_context("Can you explain general relativity?")
print("Related responses:", similar_responses)