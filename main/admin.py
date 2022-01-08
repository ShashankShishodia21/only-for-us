from django.contrib import admin
from .models import Students, Tutorials, ContactQueries, Polls, PollSubmitted
from .models import Semester, Subjects, Course, AdminData


admin.site.register(Students)
admin.site.register(Tutorials)
admin.site.register(ContactQueries)
admin.site.register(PollSubmitted)
admin.site.register(Polls)
admin.site.register(Semester)
admin.site.register(Subjects)
admin.site.register(Course)
admin.site.register(AdminData)
