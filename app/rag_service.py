import os
from google import genai
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.models import DocumentChunk, ChatHistory

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )
    return response.embeddings[0].values

def ingest_document(text: str, db: Session) -> int:
    # Split text into chunks by double newlines (paragraphs)
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    for chunk in chunks:
        vector = get_embedding(chunk)
        db_chunk = DocumentChunk(content=chunk, embedding=vector)
        db.add(db_chunk)
    db.commit()
    return len(chunks)

def generate_support_reply(user_id: int, question: str, db: Session) -> str:
    # 1. Embed user question & retrieve top 3 matching document chunks
    query_vector = get_embedding(question)
    top_chunks = (
        db.query(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_vector))
        .limit(3)
        .all()
    )
    context_text = "\n---\n".join([c.content for c in top_chunks])

    # 2. Fetch last 6 messages of user's chat history for memory
    past_messages = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(6)
        .all()
    )
    history_text = "\n".join(
        [f"{m.role.capitalize()}: {m.message}" for m in reversed(past_messages)]
    )

    # 3. Build grounded prompt and call LLM
    prompt = f"""You are a helpful customer support assistant.
Answer the customer's question using ONLY the Company Knowledge Base below.
If the answer is not in the knowledge base, politely say you don't have that information and offer to connect them with a human agent.

Company Knowledge Base:
{context_text if context_text else "No knowledge base documents available."}

Recent Conversation:
{history_text}

Customer Question: {question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    reply = response.text

    # 4. Save user question and AI reply to PostgreSQL
    db.add(ChatHistory(user_id=user_id, role="user", message=question))
    db.add(ChatHistory(user_id=user_id, role="assistant", message=reply))
    db.commit()

    return reply
