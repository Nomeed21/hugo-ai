import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

# Initialize the Supabase client and embedding model
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

SAMPLE_CONTENT = [
    {
        "content": "The AWS Student Builder Group (AWSCC-HUGO) is a community of students passionate about cloud computing and technology. We host events, build projects, and help members grow their technical skills.",
        "page_source": "/",
        "section_title": "About Us",
        "content_type": "landing_page",
    },
    {
        "content": "To apply, visit our Apply Now page. Applications are open during recruitment periods. You can apply for positions in departments like AI/ML, Web Development, Cloud, and Design. Requirements include being an enrolled student and having enthusiasm for technology.",
        "page_source": "/apply",
        "section_title": "How to Apply",
        "content_type": "apply",
    },
    {
        "content": "Cloud101 is our introductory workshop on AWS services. It covers EC2, S3, and Lambda basics. The next session is scheduled for July 2026. Registration opens one week before the event on our Events page.",
        "page_source": "/events",
        "section_title": "Cloud101 Workshop",
        "content_type": "event",
    },
    {
        "content": "The AI/ML Department builds intelligent applications using machine learning. Current projects include Hugo AI (a RAG-powered chatbot) and a computer vision attendance system. The department is led by the AI/ML Tech Lead.",
        "page_source": "/core-team",
        "section_title": "AI/ML Department",
        "content_type": "core_team",
    },
    {
        "content": "FAQ: What is AWSCC-HUGO? It is the AWS Cloud Club - Holy Angel University student chapter. Who can join? Any enrolled student at the university. Is there a membership fee? No, membership is completely free.",
        "page_source": "/faq",
        "section_title": "Frequently Asked Questions",
        "content_type": "faq",
    },
]

def seed():
    print("Generating embeddings and seeding data...")
    for item in SAMPLE_CONTENT:
        # Convert text content into a 384-dimensional vector
        embedding = embedding_model.encode(item["content"]).tolist()

        # Upsert into Supabase (insert or update if content already exists)
        supabase.table("documents").upsert(
            {
                "content": item["content"],
                "embedding": embedding,
                "page_source": item["page_source"],
                "section_title": item["section_title"],
                "content_type": item["content_type"],
            },
            on_conflict="content",
        ).execute()

        print(f"  Seeded: {item['section_title']}")

    print("Done! All sample content seeded.")


if __name__ == "__main__":
    seed()
