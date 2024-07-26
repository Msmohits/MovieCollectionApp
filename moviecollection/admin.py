from django.contrib import admin
from .models import Movie, Collection, User

# Register your models here.

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Collection)
