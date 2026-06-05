from django.db import models


class Document(models.Model):

    title = models.CharField(max_length=255)

    pdf = models.FileField(
    upload_to="pdfs/",
    null=True,
    blank=True
)
    file_size = models.IntegerField(default=0)

    page_count = models.IntegerField(default=0)

    status = models.CharField(
        max_length=50,
        default="uploaded"
    )

    def __str__(self):
        return self.title