from django.db import models

class Product(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = 'Published', 'Published'
        NOT_PUBLISHED = 'Not Published', 'Not Published'
        NONE = 'None', 'None'

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_PUBLISHED
    )

class Meta :
        indexes = [
            models.Index(fields=['name','id']) ,
            models.Index(fields=['status','created_at']),]



def __str__(self):
        return self.name
