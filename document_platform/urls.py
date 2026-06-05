from django.contrib import admin
from django.urls import path

from documents.views import (
    home_page,
    list_documents,
    get_document,
    upload_pdf,
    ask_question_api
)

urlpatterns = [

    path(
        "",
        home_page
    ),

    path(
        "documents/",
        list_documents
    ),

    path(
        "upload-pdf/",
        upload_pdf
    ),

    path(
        "documents/<int:id>/",
        get_document
    ),

    path(
        "ask/",
        ask_question_api
    ),

    path(
        "admin/",
        admin.site.urls
    ),
]