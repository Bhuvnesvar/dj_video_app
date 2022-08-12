from django.db import models
import time
from django.contrib.auth.models import User
# Create your models here.


# class ChatRequest(models.Model):
#     requested_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="requested_by")
#     requested_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="requested_to")
#     requested_at = models.FloatField(default=time.time())
#     requested_message = models.CharField(null=False, max_length=250)
#     request_status = models.BooleanField(default=False)
#     # unfollowed_at = models.FloatField(default=None, null=True)
#
#     def __str__(self):
#         return str(self.requested_by)


class ChatTable(models.Model):
    message_from = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="message_from")
    message_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name="message_to")
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
