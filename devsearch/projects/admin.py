from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag


admin.site.register([Project,
                     Review,
                     Tag])


