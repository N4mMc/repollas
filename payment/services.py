from django.shortcuts import get_object_or_404
from .models import Payment

def get_all_payments():
    payments = Payment.objects.all()
    return payments

def get_payment_by_id(id):
    payment = get_object_or_404(Payment, pk=id)
    return payment

def create_payment(data):
    payment = Payment.objects.create(
        amount=data.get('amount', 0),
        description=data.get('description', 'NONE')
    )
    return payment