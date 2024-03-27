from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField()
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to="images/pet/")
    price = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name="categories")
    adopter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="adopted_pets",
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_pets",
    )

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed By {self.user.first_name} {self.user.last_name}"
