from vector import simple_retrieve
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

def run_agent(question: str, module: str = "All"):
    docs = simple_retrieve(question, module)

    if not docs:
        return {
            "answer": "No relevant information found in the internal CSV knowledge base.",
            "sources": []
        }

    context = "\n\n".join(d["content"] for d in docs)
    sources = list({d["module"] for d in docs})

    prompt = f"""
You are a Microsoft Dynamics 365 Finance & Operations expert.

Answer the question strictly based on the context.

Question:
{question}

Context:
{context}

Provide a clear step-by-step answer.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }
