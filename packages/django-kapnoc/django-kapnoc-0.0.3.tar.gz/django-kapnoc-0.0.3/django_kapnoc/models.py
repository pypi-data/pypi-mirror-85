from django.db import models
from django.utils import timezone
from martor.models import MartorField
from easy_thumbnails.fields import ThumbnailerImageField


class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'"{self.name}" (tag {self.pk})'


class MarkdownPage(models.Model):
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    body = MartorField(verbose_name='body')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField()

    def __str__(self):
        return f'"{self.title}" (page {self.pk})'

    class Meta:
        abstract = True


class Image(models.Model):
    name = models.CharField(max_length=255)
    name_unique = models.CharField(max_length=255, editable=False)
    description = models.TextField(blank=True, default='')
    image = ThumbnailerImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'"{self.name_unique}" (image {self.pk})'

    def save(self, *args, **kwargs):
        i = 0
        name_unique = self.name
        while True:
            try:
                img = Image.objects.get(name_unique=name_unique)
                if img.pk == self.pk:
                    break
                i += 1
                name_unique = f"{self.name} {i}"
            except self.DoesNotExist:
                break
        self.name_unique = name_unique
        super().save(*args, **kwargs)
