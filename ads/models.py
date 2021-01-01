from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

User = get_user_model()


class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=255, null=True,
        help_text="The MIME Type of this file")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
