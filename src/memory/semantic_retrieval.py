# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# Function to retrieve similar responses
def retrieve_context(question, top_k=2):
    """ Searches for similar responses in FAISS memory. """
    emb_question = embedding_model.encode([question])
    _, indices = index.search(np.array(emb_question, dtype=np.float32), top_k)
    return [f"Previous response {i+1}" for i in indices[0]] if indices[0][0] != -1 else []

# **Usage example**
add_to_memory("What is general relativity?", "General relativity is Einstein's theory of gravity.")
similar_responses = retrieve_context("Can you explain relativity?")
print("Related responses:", similar_responses)

# Retrieve multi-turn context
def retrieve_multiturn_context(question, top_k=5):
    """ Searches for related previous responses to build a broader context. """
    emb_question = embedding_model.encode([question])
    _, indices = index.search(np.array(emb_question, dtype=np.float32), top_k)

    context = [f"Previous turn {i+1}" for i in indices[0] if i != -1]
    return " ".join(context) if context else ""