from django.db import models
import uuid

class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(on_delete=models.CASCADE) # TODO: User 테이블에서 Foreginkey 연결
    account_number = models.CharField(max)