from django.contrib import admin

from api.models import Apartment
from api.models import Person
from api.models import Ticket
from api.models import Bill
from api.models import Item
from api.models import TicketItem

# Define the admin class
class ApartmentAdmin(admin.ModelAdmin):
    fields = [('building', 'reference'), ('number', 'floor'), 'address', ('zip_code', 'city')]

# Register your models here.
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Person)
admin.site.register(Ticket)
admin.site.register(Bill)
admin.site.register(Item)
admin.site.register(TicketItem)