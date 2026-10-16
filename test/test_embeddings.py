
from sentence_transformers import SentenceTransformer

# Load our pretrained AI embedding model.
print("Loading the embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

# Three sentences to experiment with.
sentences = [
    "A neural network learns from training data.",
    "Machine learning models improve by learning patterns.",
    "I enjoy eating pizza."
]

# Convert sentences into numerical vectors.
vectors = model.encode(
    sentences,
    normalize_embeddings=True
)

print("\n--- Embedding Results ---")
print("Number of sentences:", len(sentences))
print("Vector matrix shape:", vectors.shape)
print("First five values of sentence 1:", vectors[0][:5])

# Compare sentence meanings using cosine similarity.
similarity_1_2 = vectors[0] @ vectors[1]
similarity_1_3 = vectors[0] @ vectors[2]

print("\n--- Similarity Results ---")
print(
    "Neural network vs machine learning:",
    round(float(similarity_1_2), 4)
)
print(
    "Neural network vs pizza:",
    round(float(similarity_1_3), 4)
)
