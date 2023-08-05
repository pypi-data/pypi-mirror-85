from django.db import models

from django_kapnoc.models import MarkdownPage, Tag


class TestMarkdownPage(MarkdownPage):
    tags = models.ManyToManyField(Tag)

    class Meta:
        app_label = 'django_kapnoc_tests2'
