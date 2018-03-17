from django.db import models

class Place(models.Model):
    address = models.TextField(max_length=256, default="", help_text="The full address")
    zip_code = models.CharField(max_length=16, default="")
    city = models.CharField(max_length=128, default="")

    class Meta:
        abstract: True

class Person(Place):
    PERSON_CIV = (
        ("M.", "Monsieur"),
        ("Mme", "Madame"),
        ("M. Mme", "Monsieur et Madame"),
        ("SCI", "Société Civile"),
    )
    civilite = models.CharField(choices=PERSON_CIV, max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=128, unique=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Apartment(Place):
    building = models.CharField(max_length=64, help_text="Building's name")
    reference = models.CharField(max_length=16, help_text="Give a short identifier tag to this apartment")
    number = models.SmallIntegerField(help_text="Apartment number")
    floor = models.SmallIntegerField()
    persons = models.ManyToManyField(Person)

    class Meta:
        ordering = ['reference', 'building']

    def __str__(self):
        return '(' + self.reference + ') ' + self.building

class Ticket(models.Model):
    TICKET_STATE = (
        ("O", "Open"),
        ("C", "Closed"),
        ("S", "Solved"),
        ("R", "Rejected"),
    )
    TICKET_PRIORITY = (
        ("L", "Low"),
        ("N", "Normal"),
        ("H", "high"),
        ("E", "Emergency"),
    )
    title: models.CharField(max_length=64, help_text="Be strait forward")
    description: models.TextField(help_text="Give all the details here")
    history: models.TextField(help_text="Write here all the actions for answer this problem")
    state: models.CharField(max_length=16, choices=TICKET_STATE)
    priority: models.CharField(max_length=16, choices=TICKET_PRIORITY)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    created_at: models.DateField(auto_now_add=True)
    updated_at: models.DateField(auto_now=True)
    
    class Meta:
        get_latest_by = ['-updated_at', '-created_at']
        #ordering = 'id'
        order_with_respect_to = 'apartment'

    def __str__(self):
        return '#' + self.id + ' - ' + self.title

class Bill(models.Model):
    number = models.SmallIntegerField(unique=True)
    created_at= models.DateField(auto_now_add=True)
    is_paid= models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        ordering = ['number']
        get_latest_by = 'created_at'

    def __str__(self):
        return self.number

class Item(models.Model):
    title: models.CharField(max_length=45)
    code: models.CharField(max_length=16)
    price: models.FloatField()

#    class Meta:
#        ordering = ['code', 'title']

    def __str__(self):
        return '(' + self.code + ') ' + self.title

class TicketItem(models.Model):
    ticket: models.ForeignKey(Ticket, on_delete=models.CASCADE)
    item: models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity: models.SmallIntegerField()

    def __str__(self):
        return self.ticket + ' - ' + self.item + 'x' + self.quantity