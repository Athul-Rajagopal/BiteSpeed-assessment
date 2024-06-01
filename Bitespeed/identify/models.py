from django.db import models

# Create your models here.

class Contact(models.Model):
    LINKPRECEDENCE_CHOICES = [('primary', 'primary'), 
                              ('secondary', 'secondary')]
    
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length=10, choices=LINKPRECEDENCE_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} - {self.phoneNumber}"
    
