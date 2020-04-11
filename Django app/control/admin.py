from django.contrib import admin
from .models import Institutions,Campus,Building,Locks,Rooms,Account,Control,Permission,Carrier,Subject,SubjectSchedule,Permission,UserSubject
from import_export.admin import ImportExportModelAdmin

# Register your models here.
#admin.site.register(Institutions)
#admin.site.register(Campus)
#admin.site.register(Building)
#admin.site.register(Locks)
#admin.site.register(Rooms)
#admin.site.register(Account)
#admin.site.register(Control)
#admin.site.register(Permission)
#admin.site.register(Carrier)
#admin.site.register(Subject)
#admin.site.register(SubjectSchedule)
#admin.site.register(UserSubject)


@admin.register(Institutions)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Campus)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Building)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Locks)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Rooms)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Account)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Control)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Permission)
class ViewAdmin(ImportExportModelAdmin):
    pass

@admin.register(Carrier)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(Subject)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(SubjectSchedule)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(UserSubject)
class ViewAdmin(ImportExportModelAdmin):
    pass