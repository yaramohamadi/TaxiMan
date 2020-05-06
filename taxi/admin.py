from django.contrib import admin

# Register your models here.
from taxi.models import *

admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Car)
admin.site.register(Commonaddresses)
admin.site.register(Trip)
admin.site.register(Layover)
admin.site.register(Discount)
admin.site.register(Score)
admin.site.register(Moneytransfer)
admin.site.register(Prize)
admin.site.register(Templatecomments)