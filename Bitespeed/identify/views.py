from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Contact
from django.db.models import Q
from datetime import datetime

@api_view(['POST'])
def identify(request):
    email = request.data.get('email')
    phoneNumber = request.data.get('phoneNumber')

    # Find existing contacts that share either email or phoneNumber
    contacts = Contact.objects.filter(
        Q(email=email) | Q(phoneNumber=phoneNumber)
    )

    if not contacts.exists():
        # No existing contact, create new primary contact
        new_contact = Contact.objects.create(
            email=email, phoneNumber=phoneNumber, linkPrecedence='primary', createdAt=datetime.now(), updatedAt=datetime.now()
        )
        response = {
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
                "secondaryContactIds": []
            }
        }
        
    else:
       # To handle linking of contacts properly
        primary_contact = None
        secondary_contacts = []
        seen_contacts = set()

        for contact in contacts:
            if contact.linkPrecedence == 'primary':
                if primary_contact is None or contact.createdAt < primary_contact.createdAt:
                    if primary_contact:
                        secondary_contacts.append(primary_contact)
                    primary_contact = contact
            else:
                secondary_contacts.append(contact)
            seen_contacts.add(contact.id)

        if primary_contact is None:
            primary_contact = contacts.first()
            primary_contact.linkPrecedence = 'primary'
            primary_contact.save()

        # Ensure all other contacts are linked to the primary contact
        for contact in contacts:
            if contact != primary_contact:
                if contact.linkPrecedence == 'primary':
                    contact.linkPrecedence = 'secondary'
                    contact.linkedId = primary_contact.id
                    contact.save()
                elif contact.linkedId != primary_contact.id:
                    contact.linkedId = primary_contact.id
                    contact.save()

        # Handle additional linking through linked contacts
        additional_contacts = Contact.objects.filter(
            Q(linkedId=primary_contact.id) |
            Q(email=primary_contact.email) |
            Q(phoneNumber=primary_contact.phoneNumber)
        ).exclude(id__in=seen_contacts)

        for contact in additional_contacts:
            if contact.linkPrecedence == 'primary':
                secondary_contacts.append(contact)
                contact.linkPrecedence = 'secondary'
                contact.linkedId = primary_contact.id
                contact.save()
            elif contact.linkedId != primary_contact.id:
                contact.linkedId = primary_contact.id
                contact.save()
            seen_contacts.add(contact.id)

        # Check if new information should be added as secondary contact
        if (email and email not in [c.email for c in contacts]) or (phoneNumber and phoneNumber not in [c.phoneNumber for c in contacts]):
            new_secondary = Contact.objects.create(
                email=email, phoneNumber=phoneNumber, linkedId=primary_contact.id, linkPrecedence='secondary', createdAt=datetime.now(), updatedAt=datetime.now()
            )
            secondary_contacts.append(new_secondary)

        # Consolidate all emails and phone numbers
        emails = list(set([primary_contact.email] + [c.email for c in secondary_contacts if c.email]))
        phoneNumbers = list(set([primary_contact.phoneNumber] + [c.phoneNumber for c in secondary_contacts if c.phoneNumber]))
        secondaryContactIds = [c.id for c in secondary_contacts]

        response = {
            "contact": {
                "primaryContactId": primary_contact.id,
                "emails": emails,
                "phoneNumbers": phoneNumbers,
                "secondaryContactIds": secondaryContactIds
            }
        }

    return Response(response)