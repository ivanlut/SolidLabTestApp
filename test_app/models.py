from django.db import models


class Content(models.Model):
    text = models.TextField(null=False, default='')

    class Meta:
        db_table = 'contents'


class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, default='')

    class Meta:
        db_table = 'tags'


class Note(models.Model):
    title = models.CharField(max_length=255, null=False, default='')
    content = models.OneToOneField(
        Content, on_delete=models.PROTECT, null=False, blank=False)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        db_table = 'notes'

    def delete(self, using=None, keep_parents=False):
        content = self.content
        super().delete()
        if content:
            content.delete()

