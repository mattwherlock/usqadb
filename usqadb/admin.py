from django.contrib import admin
from .models import *

admin.site.register(Audit)
admin.site.register(AuditProbe)
admin.site.register(Machine)
admin.site.register(Location)
admin.site.register(NameModel)
admin.site.register(Manufacturer)
admin.site.register(Gateway)
admin.site.register(Subnet)
admin.site.register(Port)