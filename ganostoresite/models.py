from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Додаткові поля для користувача
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_blocked = models.BooleanField(default=False)  # Поле для відстеження статусу блокування
    secret_question = models.CharField(max_length=255, blank=True, null=True)
    secret_answer = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='programs')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='programs')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_programs')
    program_file = models.FileField(upload_to='programs/')
    image = models.ImageField(upload_to='program_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.program.title}'


class Complaint(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='complaints')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f'Complaint by {self.author.username} on {self.program.title}'


class Rating(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField()

    def __str__(self):
        return f'Rating {self.score} for {self.program.title} by {self.user.username}'
