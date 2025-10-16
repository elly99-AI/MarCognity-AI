# © 2025 Elena Marziali — Code released under Apache 2.0 license.
# See LICENSE in the repository for details.
# Removal of this copyright is prohibited.

# This section manages the system's memory, allowing efficient storage and
# retrieval of scientific content. Embeddings are generated using models
# specialized for academic texts.

def safe_encode(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Il testo da codificare è vuoto o non valido.")
    try:
        return embedding_model.encode([text])
    except Exception as e:
        print(f"Errore durante l'embedding: {e}")
        return np.zeros((1, 768), dtype=np.float32)  # fallback neutro


# === Load Specter model ===
word_embedding_model = models.Transformer("allenai/specter")
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
embedding_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])