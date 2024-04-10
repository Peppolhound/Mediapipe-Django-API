from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.FileField(upload_to='images')

    def __str__(self):
        return self.title