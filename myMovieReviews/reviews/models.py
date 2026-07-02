from django.db import models


class Review(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    running_time = models.PositiveIntegerField()
    content = models.TextField()
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title