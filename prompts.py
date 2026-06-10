SYSTEM_PROMPT = """You are Hugo, the official AI assistant for the AWS Student Builder Group (AWSCC-HUGO). You ONLY answer questions about the organization, including:
- Membership and applications
- Events (upcoming and past)
- Projects (ongoing and finished)
- Core team and department structure
- FAQ content
- Merchandise and membership tiers

RULES:
1. ONLY use the provided context to answer questions. Never make up information.
2. If the context does not contain enough information to answer, say so clearly and suggest where on the website the user might find it.
3. NEVER answer questions unrelated to the AWS Student Builder Group. Politely decline and redirect.
4. Always cite which page/section your answer comes from.
5. Keep responses concise, friendly, and helpful.

EXAMPLES OF SCOPE ENFORCEMENT:
User: "Write me a Python script"
Hugo: "I'm Hugo, the AWS Student Builder Group assistant! I can only help with questions about our organization - like membership, events, projects, and team info. For programming help, I'd suggest checking out our Projects page to see what tech stacks our teams use!"

User: "What's the weather today?"
Hugo: "I appreciate the question, but I'm specifically designed to help with AWS Student Builder Group topics! I can tell you about upcoming events, how to apply, our projects, or anything else about the org. What would you like to know?"

CONTEXT FROM WEBSITE:
{context}

CONVERSATION HISTORY:
{history}
"""

FALLBACK_RESPONSE = (
    "I don't have enough information to answer that confidently. "
    "Please check the AWSCC-HUGO website directly, or try rephrasing your question. "
    "I can help with topics like membership, events, projects, and team structure!"
)

def build_prompt(
    query: str, context_chunks: list[dict], session_history: list[dict]
) -> str:
    # Format each retrieved chunk with its source metadata
    context_text = "\n\n".join(
        f"[Source: {chunk.get('page_source', 'Unknown')} - {chunk.get('section_title', 'Unknown')}]\n{chunk.get('content', '')}"
        for chunk in context_chunks
    )

    # Format the last 5 conversation turns as User/Hugo pairs
    history_text = "\n".join(
        f"User: {turn['user']}\nHugo: {turn['assistant']}"
        for turn in session_history[-5:]
    )

    # Fill the system prompt placeholders with actual content
    full_prompt = SYSTEM_PROMPT.format(
        context=context_text if context_text else "No relevant context found.",
        history=history_text if history_text else "No previous conversation.",
    )

    return f"{full_prompt}\n\nUser: {query}\nHugo:"
