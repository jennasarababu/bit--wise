from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user1 = models.ForeignKey(User, related_name='user1_notes', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2_notes', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    last_editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='last_edited_notes')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note on {self.date} by {self.last_editor}"
    

    