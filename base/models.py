from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_learned = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    source_language = models.TextField(max_length=50, default="Deutsch")
    target_language = models.TextField(max_length=50, default="Englisch")

    def __str__(self):
        return self.name

    

class Vocab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_word = models.CharField(max_length=20)
    target_word = models.CharField(max_length=20)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="vocabs")
    is_learned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source_word
    


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"



