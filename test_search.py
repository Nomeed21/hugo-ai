import os
from dotenv import load_dotenv

# 1. Load environment variables FIRST before importing your local pipeline!
load_dotenv()

from rag_pipeline import embed_query, supabase

print("--- 1. Checking Database Embeddings ---")
rows = supabase.table("documents").select("section_title", "embedding").execute().data
if rows:
    for r in rows:
        emb = r.get("embedding")
        print(f"Row: {r.get('section_title')} | Embedding Length: {len(emb) if emb else 'NULL'}")
else:
    print("No rows found in the database.")

print("\n--- 2. Running Search with 0.1 Threshold ---")
q_emb = embed_query("How do I apply to AWSCC-HUGO?")
res = supabase.rpc("match_documents", {
    "query_embedding": q_emb,
    "match_threshold": 0.1,
    "match_count": 5
}).execute()

print(f"Matches found: {len(res.data) if res.data else 0}")
for r in (res.data or []):
    dist = r.get("embedding_distance", 1.0)
    similarity = 1 - dist
    print(f"- {r.get('section_title')} | Calculated Similarity: {similarity:.4f}")
