<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# Build a Production RAG Chatbot Backend

**Project Link:** [View Project](https://learn.nextwork.org/projects/8c6ba6f3-b8de-48b3-82cf-da43478c6872)

**Author:** Nurmid Mayo  
**Email:** mayonurmid@gmail.com

---

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_on918ceh)

## What I Built and Why

### Project overview

In this project, I'm building a RAG pipeline so that it can be integrated to a website 

## Deploying Hugo AI to Production

### Deployment strategy

In this step, I'm deploying configuration files so that the web team can actually call it.

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_on918ceh)

### Live endpoint verification

I sent a question about how to join and received a response that mentioned refer to the website with sources from /apply

## Building the FastAPI Endpoints

### API design goals

In this step, I'm building a chat post endpoint with pydantic request/response models, add a healh get endpint and cors middle wair and test the full rag flow locally usin gswagger ui and curl so that the web team can call the pipeline easily.

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_92u2vs5a)

### Response structure and confidence scoring

The response includes responses, sources, and confidence.The confidence score matters because it determines how much data it recognize and answers.

## Constructing the RAG Pipeline

### Pipeline architecture

In this step, I'm building the embedding model and groq llm clinet and retrieval funcitons so that Hugo can query Supabase vectore store and implement confidence thresholding to prevent low-quality answers

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_qobezdjz)

### Confidence thresholding logic

When the similarity score is below the threshold, Hugo will say that the question is out of its scope instead of giving irrelevant information and hallucinating

## Engineering the System Prompt and Scope Enforcement

### Prompt design goals

In this step, I'm writing a system prompt so that Hugo can enforce examples, formats context and history, and declines off-topic queries

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_qjb75ued)

### Handling off-topic queries

When an off-topic query comes in, the pipeline returns with 0 confidence because the confidence is below the minimum threshold

## Adding Session Memory and Source Attribution

### Memory and attribution goals

In this step, I'm setting up a session memory class so that I can store conversation which turns with automatic expiry, review how source attribution provides page and section references in every response, and test multi-turn conversations to verify follow-up questions resolve correctly.

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_kqzfyq65)

### How session memory resolves follow-up questions

Session memory stores the previous prompts and answers so the prompt includes the necessary data which lets Hugo resolve the insufficient prompt.

## Configuring Supabase pgvector and Seeding Data

### Vector database setup

In this step, I'm setting up pgvector so that Hugo can search functions that ranks documents by relevance and seed the database with sample website content using a python script

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_fehh2bbp)

### How match_documents works

The match_documents function do is to search and compares datas.The threshold ensures all the answers are relevant and not includes any unrelated information

## Setting Up the Development Environment

### Environment setup goals

In this step, I'm setting up python, groq, and supabase so that I can start building my RAG Pipeline

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_z1rua103)

### Environment variables and service connections

I configured groq, supabase url, & supabase service key which connects to groq llm and supabase

## Bonus: Feedback Logging for Continuous Improvement

![Image](https://learn.nextwork.org/sympathetic_purple_adorable_sow/uploads/8c6ba6f3-b8de-48b3-82cf-da43478c6872_dbv8r7uh)

### Feedback stats and quality tracking

In this project extension, the stats endpoint returns whether the user thumbs up or down the response of the chatbot.This helps because it can provide new data on what response is the best

## Reflections and Takeaways

### Tools and concepts learned

The key tools I used include supabase, groq api, render, and github. Key concepts I learnt include pipelining, seeding data, data management.

### Time and challenges

This project took me approximately 2 days. The most challenging part was trying to optimize the storage use so that I can have the free tier of render.

I did this project today to learn how to set up a feeback response. Another skill I want to learn is improving the data and reducing the hallucination well.

---

*Built with [NextWork](https://learn.nextwork.org) - [View this project](https://learn.nextwork.org/projects/8c6ba6f3-b8de-48b3-82cf-da43478c6872)*
