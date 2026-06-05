from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Document

import json
import traceback

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from .services.qa_service import answer_question


def home_page(request):

    return render(
        request,
        "index.html"
    )



def list_documents(request):

    documents = Document.objects.all()

    data = []

    for document in documents:

        data.append(
            {
                "id": document.id,
                "title": document.title,
                "pdf": document.pdf.name if document.pdf else None,
                "file_size": document.file_size,
                "page_count": document.page_count,
                "status": document.status
            }
        )

    return JsonResponse(
        data,
        safe=False
    )


@csrf_exempt
def upload_pdf(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "POST request required"
            },
            status=405
        )

    pdf_file = request.FILES.get("file")

    if not pdf_file:

        return JsonResponse(
            {
                "error": "No PDF uploaded"
            },
            status=400
        )

    document = Document.objects.create(
        title=pdf_file.name,
        pdf=pdf_file,
        file_size=pdf_file.size,
        status="uploaded"
    )

    return JsonResponse(
        {
            "message": "PDF uploaded successfully",
            "document_id": document.id,
            "filename": document.title
        }
    )


def get_document(request, id):

    try:

        document = Document.objects.get(
            id=id
        )

        return JsonResponse(
            {
                "id": document.id,
                "title": document.title,
                "pdf": document.pdf.name if document.pdf else None,
                "file_size": document.file_size,
                "page_count": document.page_count,
                "status": document.status
            }
        )

    except Document.DoesNotExist:

        return JsonResponse(
            {
                "error": "Document not found"
            },
            status=404
        )


@csrf_exempt
def ask_question_api(request):

    try:

        print("STEP 1: Request received")

        if request.method != "POST":

            return JsonResponse(
                {
                    "error": "POST request required"
                },
                status=405
            )

        body = json.loads(
            request.body
        )

        print("STEP 2: JSON parsed")

        question = body.get(
            "question"
        )

        print(f"STEP 3: Question = {question}")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print("STEP 4: Embeddings loaded")

        vector_store = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

        print("STEP 5: FAISS loaded")

        results = vector_store.similarity_search(
            question,
            k=5
        )

        print(f"STEP 6: Retrieved {len(results)} chunks")

        answer = answer_question(
            question,
            results
        )

        print("STEP 7: Gemini answer generated")

        return JsonResponse(
            {
                "question": question,
                "answer": answer
            }
        )

    except Exception as e:

        print("\n========== ERROR ==========")
        print(traceback.format_exc())
        print("===========================\n")

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )