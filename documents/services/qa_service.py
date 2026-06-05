from langchain_google_genai import ChatGoogleGenerativeAI
import os


def answer_question(question, chunks):

    context = "\n\n".join(
        chunk.page_content
        for chunk in chunks
    )

    print("API KEY =", os.getenv("GOOGLE_API_KEY"))

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = f"""
Use only the context below to answer the question.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(
        prompt
    )

    return response.content