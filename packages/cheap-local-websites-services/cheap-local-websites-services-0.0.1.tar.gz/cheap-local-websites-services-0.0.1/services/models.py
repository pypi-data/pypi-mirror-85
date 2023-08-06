from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    img = models.ImageField(upload_to='uploads/services')
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=100)
    body = models.TextField(max_length=1000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)