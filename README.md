# Bitespeed Backend Task: Identity Reconciliation

This project is part of an assessment given by BiteSpeed for the position of Backend Developer. The task involves designing a web service to identify and keep track of a customer's identity across multiple purchases, linking different orders made with different contact information to the same person.

## Project Description

Dr. Emmett Brown, known as Doc, is using different email addresses and phone numbers for each purchase to avoid drawing attention to his project. FluxKart.com, an online store, wants to integrate Bitespeed into their platform to reward loyal customers and provide a personalized experience. Bitespeed needs a way to link different contact information to the same customer.

## Requirements

- Design a web service with an endpoint `/identify` that receives HTTP POST requests with a JSON body containing "email" or "phoneNumber".
- The service should return a consolidated contact with primary and secondary contacts.

### Example

**Request:**

```json
{
  "email": "mcfly@hillvalley.edu",
  "phoneNumber": "123456"
}
```

### Stack Used

- Backend Framework: Django with Django REST Framework (DRF)
- Database: PostgreSQL
- Deployment: Hosted on Render.com

### Live Endpoint

The application is hosted on Render.com. You can access the backend using the following URL:
- Base URL: https://bitespeed-assessment-1t33.onrender.com/
- Endpoint: https://bitespeed-assessment-1t33.onrender.com/identify/

### Testing the Endpoint

Use Postman or any other API client to test the /identify endpoint. Make sure to send a POST request with a JSON body containing either "email" or "phoneNumber".
