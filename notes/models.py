from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Note(models.Model):
    note_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=255)
    note_content = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
