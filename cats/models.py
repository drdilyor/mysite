from django.core.validators import MinLengthValidator
from django.db import models


class Breed(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Breed must longer than a character")])

    def __str__(self):
        return self.name


class Cat(models.Model):
    nickname = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Nickname must be longer than a character")]
    )
    weight = models.PositiveIntegerField()
    foods = models.CharField(max_length=200)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
