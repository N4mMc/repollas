from django.shortcuts import render
from django.db.models import Sum
from purchase.models import Purchase
from production.models import Production
from order.models import Order
from ingredient.models import Ingredient

def dashboard_view(request):
    # Totales generales
    total_orders = Order.objects.count()
    total_purchases = Purchase.objects.aggregate(total_quantity=Sum('quantity'), total_cost=Sum('cost'))
    total_production = Production.objects.aggregate(
        total_repollas=Sum('repollas'),
        total_boxes=Sum('boxes'),
        total_sales=Sum('sales')
    )

    # Datos para gráficos
    ingredients = Ingredient.objects.all()
    ingredient_names = [f"{i.name} ({i.measurament})" for i in ingredients]
    ingredient_stocks = [i.stock for i in ingredients]

    # Top 5 ingredientes más comprados
    top_ingredients = Purchase.objects.values('ingredient__name').annotate(
        total_bought=Sum('quantity')
    ).order_by('-total_bought')[:5]

    top_names = [f"{item['ingredient__name']}" for item in top_ingredients]
    top_quantities = [item['total_bought'] for item in top_ingredients]

    context = {
        'total_orders': total_orders,
        'total_purchases': total_purchases,
        'total_production': total_production,
        'ingredient_names': ingredient_names,
        'ingredient_stocks': ingredient_stocks,
        'top_names': top_names,
        'top_quantities': top_quantities,
    }

    return render(request, 'reports/dashboard.html', context)
