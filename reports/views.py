# from django.shortcuts import render
# from django.db.models import Sum
# from purchase.models import Purchase
# from production.models import Production
# from order.models import Order
# from ingredient.models import Ingredient

# def dashboard_view(request):
#     # Totales generales
#     total_orders = Order.objects.count()
#     total_purchases = Purchase.objects.aggregate(total_quantity=Sum('quantity'), total_cost=Sum('cost'))
#     total_production = Production.objects.aggregate(
#         total_repollas=Sum('repollas'),
#         total_boxes=Sum('boxes'),
#         total_sales=Sum('sales')
#     )

#     # Datos para gráficos
#     ingredients = Ingredient.objects.all()
#     ingredient_names = [f"{i.name} ({i.measurament})" for i in ingredients]
#     ingredient_stocks = [i.stock for i in ingredients]

#     # Top 5 ingredientes más comprados
#     top_ingredients = Purchase.objects.values('ingredient__name').annotate(
#         total_bought=Sum('quantity')
#     ).order_by('-total_bought')[:5]

#     top_names = [f"{item['ingredient__name']}" for item in top_ingredients]
#     top_quantities = [item['total_bought'] for item in top_ingredients]

#     context = {
#         'total_orders': total_orders,
#         'total_purchases': total_purchases,
#         'total_production': total_production,
#         'ingredient_names': ingredient_names,
#         'ingredient_stocks': ingredient_stocks,
#         'top_names': top_names,
#         'top_quantities': top_quantities,
#     }

#     return render(request, 'reports/dashboard.html', context)


# dashboard/views.py
from django.shortcuts import render
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from django.http import HttpRequest
import json
from decimal import Decimal

from purchase.models import Purchase
from production.models import Production
from ingredient.models import Ingredient
from purchase.models import Purchase  # ya listado
# Asumo que los modelos están en estos módulos; ajusta imports si tus apps usan otros names.

# Si tienes un enum Measurament definido, puedes importarlo si lo necesitas
from enums.measurament import Measurament


def dashboard_view(request: HttpRequest):
    # --- Totales monetarios y contadores ---
    purchases_agg = Purchase.objects.aggregate(total_cost=Sum('cost'))
    total_purchases = purchases_agg.get('total_cost') or Decimal('0.00')
    # convertir a float para serializar JSON si es necesario en el template
    total_purchases_f = float(total_purchases)

    sales_agg = Production.objects.aggregate(total_sales=Sum('sales'), total_repollas=Sum('repollas'), total_boxes=Sum('boxes'))
    total_sales = sales_agg.get('total_sales') or Decimal('0.00')
    total_sales_f = float(total_sales)
    total_repollas = sales_agg.get('total_repollas') or 0
    total_boxes = sales_agg.get('total_boxes') or 0

    production_count = Production.objects.count()

    # Ganancias netas = ventas (dinero) - compras (dinero)
    net_profit = float(total_sales - total_purchases)

    # --- Stock agrupado por medida (listas de dicts para mostrar en tablas) ---
    # Obtener ingredientes clasificados por measurament
    grams = list(Ingredient.objects.filter(measurament=Measurament.GRAM).values('name', 'stock').order_by('name'))
    mls = list(Ingredient.objects.filter(measurament=Measurament.MILILITER).values('name', 'stock').order_by('name'))
    units = list(Ingredient.objects.filter(measurament=Measurament.UNIT).values('name', 'stock').order_by('name'))

    # --- Top 5 ingredientes más comprados (por cantidad total comprada) ---
    # Asumo que Purchase.quantity es la cantidad comprada (por Purchase.ingredient)
    top_qs = (Purchase.objects
              .values('ingredient__name')
              .annotate(total_qty=Sum('quantity'))
              .order_by('-total_qty')[:5])
    top_names = [item['ingredient__name'] for item in top_qs]
    top_quantities = [item['total_qty'] for item in top_qs]

    # --- Gráfico de ventas por fecha (agrupar por día/semana/mes) ---
    period = request.GET.get('period', 'day')  # 'day' | 'week' | 'month'
    if period == 'week':
        trunc = TruncWeek('created_at')
    elif period == 'month':
        trunc = TruncMonth('created_at')
    else:
        trunc = TruncDate('created_at')

    sales_by_period_qs = (Production.objects
                          .annotate(period=trunc)
                          .values('period')
                          .annotate(total_sales=Sum('sales'), total_boxes=Sum('boxes'))
                          .order_by('period'))

    # preparar etiquetas y datos (formatos de fecha)
    labels = []
    sales_data = []
    boxes_data = []
    for row in sales_by_period_qs:
        p = row['period']
        if hasattr(p, 'date'):
            # TruncWeek/TruncMonth may return date-like objects; ensure string conversion
            label = p.date().isoformat()
        else:
            # p is date
            label = p.isoformat()
        labels.append(label)
        # convertir Decimal a float
        total = row['total_sales'] or Decimal('0.00')
        sales_data.append(float(total))
        boxes_data.append(int(row.get('total_boxes') or 0))

    context = {
        # monetarios
        'total_purchases': total_purchases_f,
        'total_sales_money': total_sales_f,
        'total_repollas': total_repollas,
        'total_boxes': total_boxes,
        'production_count': production_count,
        'net_profit': net_profit,

        # stock por medida (listas de dicts)
        'stock_grams': grams,
        'stock_mls': mls,
        'stock_units': units,

        # top ingredientes
        'top_names': json.dumps(top_names),
        'top_quantities': json.dumps(top_quantities),

        # ventas por periodo (chart)
        'sales_labels': json.dumps(labels),
        'sales_data': json.dumps(sales_data),
        'boxes_data': json.dumps(boxes_data),
        'period': period,
    }

    return render(request, 'reports/dashboard.html', context)
