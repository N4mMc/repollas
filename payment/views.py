from django.shortcuts import render, redirect
from .services import get_all_payments, create_payment, get_payment_by_id
from .forms import PaymentForm

def payment_list(request):
    payments = get_all_payments()
    return render(request, 'payment/payment_list.html', {'payments': payments})


def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return render(request, 'payment/payment_created.html', {'payment': payment})
    else:
        # Si es GET, mostramos el formulario vacío
        form = PaymentForm()

    # En ambos casos devolvemos un render
    return render(request, 'payment/payment_form.html', {'form': form})
