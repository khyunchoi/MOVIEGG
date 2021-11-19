from django.contrib import admin
from .models import Review, ReviewComment, FreeBoard, FreeComment

# Register your models here.
admin.site.register([Review, ReviewComment, FreeBoard, FreeComment])