from django.db import models

# Create your models here.
class KbEntry(models.Model):
    id = models.CharField(primary_key=True, max_length = 1024)
    text = models.CharField(blank = True, max_length = 1024)
    expiraton = models.DateTimeField(null=False, blank=False, db_index=True)
