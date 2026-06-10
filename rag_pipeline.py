import os

from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
from supabase import create_client

from prompts import build_prompt, FALLBACK_RESPONSE

# Load environment variables for service connections
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Initialize the Supabase client for vector lookups
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Load the embedding model (runs locally, no API calls needed)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize the Groq LLM for response generation
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=1,
    max_tokens=1024,
)

# Similarity thresholds for retrieval quality control
MATCH_THRESHOLD = 0.30
MATCH_COUNT = 5

def embed_query(query: str) -> list[float]:
    # Convert the user's question into a 384-dim vector
    embedding = embedding_model.encode(query)
    return embedding.tolist()


def retrieve_chunks(query_embedding: list[float]) -> list[dict]:
    # Call the Supabase match_documents RPC for cosine similarity search
    result = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_threshold": MATCH_THRESHOLD,
            "match_count": MATCH_COUNT,
        },
    ).execute()

    return result.data if result.data else []

def get_rag_response(query: str, session_history: list[dict]) -> dict:
    # Step 1: Embed the user query
    query_embedding = embed_query(query)
    # Step 2: Retrieve matching chunks from the vector store
    chunks = retrieve_chunks(query_embedding)

    # If no chunks matched at all, return the fallback immediately
    if not chunks:
        return {
            "response": FALLBACK_RESPONSE,
            "sources": [],
            "confidence": 0.0,
        }

    # Step 3: Calculate the highest similarity score among retrieved chunks
    max_similarity = max(
        1 - chunk.get("embedding_distance", 1.0) for chunk in chunks
    ) if chunks else 0.0

    # If even the best chunk is below the threshold, skip the LLM
    if max_similarity < MATCH_THRESHOLD:
        return {
            "response": FALLBACK_RESPONSE,
            "sources": [],
            "confidence": max_similarity,
        }

    # Step 4: Build the prompt with context and history, then call the LLM
    prompt = build_prompt(
        query=query,
        context_chunks=chunks,
        session_history=session_history,
    )

    response = llm.invoke(prompt)

    # Step 5: Extract source metadata for attribution
    sources = [
        {
            "page_source": chunk.get("page_source", "Unknown"),
            "section_title": chunk.get("section_title", "Unknown"),
        }
        for chunk in chunks
    ]

    return {
        "response": response.content,
        "sources": sources,
        "confidence": max_similarity,
    }
