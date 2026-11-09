import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create local vector database
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="campus_knowledge"
)


def load_college_data():

    file_path = Path("data/college_info.txt")

    if not file_path.exists():
        raise FileNotFoundError("college_info.txt not found!")

    text = file_path.read_text(encoding="utf-8")

    if not text.strip():
        raise ValueError("College information file is empty.")

    # Split text into manageable chunks
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) > 500 and current_chunk:
            chunks.append(current_chunk)
            current_chunk = ""

        current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def index_college_data():

    chunks = load_college_data()

    embeddings = model.encode(chunks).tolist()

    ids = [f"college_{i}" for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(chunks)


def retrieve_context(question, top_k=3):

    question_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=min(top_k, collection.count())
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)