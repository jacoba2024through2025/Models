from django.db import models





class Contacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    is_favorite = models.BooleanField(default=False)
    

def create_contact(name, email, phone, is_favorite=False):
    contact = Contacts.objects.create(name=name, email=email, phone=phone, is_favorite=is_favorite)
    return contact

def all_contacts():
    return Contacts.objects.all()

def find_contact_by_name(name):
    try:
        return Contacts.objects.get(name=name)
    
    except Contacts.DoesNotExist:
        return None

def favorite_contacts():
    return Contacts.objects.filter(is_favorite=True)

def update_contact_email(name, new_email):
    try:
        contact = find_contact_by_name(name)
        if contact:
            contact.email = new_email
            contact.save()
            return contact
    except Exception as error:
        return str(error)
    
def delete_contact(name):
    try:
        contact = find_contact_by_name(name)
        if contact:
            contact.delete()
            return True
    except Exception as error:
        return str(error)