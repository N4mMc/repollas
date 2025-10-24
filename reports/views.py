from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.http import HttpRequest
import json
from decimal import Decimal

from purchase.models import Purchase
from production.models import Production
from ingredient.models import Ingredient
from payment.models import Payment
from enums.measurament import Measurament


def dashboard_view(request: HttpRequest):
    # --- Ingredients grouped by measurement (querysets) ---
    ingredients_ml = Ingredient.objects.filter(measurament=Measurament.MILILITER).order_by('name')
    ingredients_u = Ingredient.objects.filter(measurament=Measurament.UNIT).order_by('name')
    ingredients_gm = Ingredient.objects.filter(measurament=Measurament.GRAM).order_by('name')

    # --- Aggregates (purchases + payments) ---
    purchases_agg = Purchase.objects.aggregate(total_cost=Sum('cost'))
    payments_agg = Payment.objects.aggregate(total_payment=Sum('amount'))

    total_purchases = purchases_agg.get('total_cost') or Decimal('0.00')
    total_payments = payments_agg.get('total_payment') or Decimal('0.00')

    # Total Expenses = Purchases + Payments
    total_expenses = total_purchases + total_payments
    total_expenses_f = float(total_expenses)

    # --- Income and Production (from Production model) ---
    sales_agg = Production.objects.aggregate(
        total_sales=Sum('sales'),
        total_boxes=Sum('boxes')
    )

    total_income = sales_agg.get('total_sales') or Decimal('0.00')
    total_income_f = float(total_income)

    total_production = sales_agg.get('total_boxes') or 0  # total boxes

    # Net Profit = total_income - total_expenses
    net_profit = float(total_income - total_expenses)

    # --- Stock grouped by measurement (for tables) ---
    grams = list(Ingredient.objects.filter(measurament=Measurament.GRAM).values('name', 'stock').order_by('name'))
    mls = list(Ingredient.objects.filter(measurament=Measurament.MILILITER).values('name', 'stock').order_by('name'))
    units = list(Ingredient.objects.filter(measurament=Measurament.UNIT).values('name', 'stock').order_by('name'))

    # --- Top 5 most purchased ingredients ---
    top_qs = (
        Purchase.objects
        .values('ingredient__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )
    top_names = [item['ingredient__name'] for item in top_qs]
    top_quantities = [item['total_qty'] for item in top_qs]

    # --- Sales and Expenses over time (period grouping) ---
    period = request.GET.get('period', 'day')

    if period == 'week':
        trunc_purchase = TruncWeek('date')
        trunc_payment = TruncWeek('created_at')
        trunc_production = TruncWeek('created_at')
    elif period == 'month':
        trunc_purchase = TruncMonth('date')
        trunc_payment = TruncMonth('created_at')
        trunc_production = TruncMonth('created_at')
    else:
        trunc_purchase = TruncDate('date')
        trunc_payment = TruncDate('created_at')
        trunc_production = TruncDate('created_at')

    sales_by_period_qs = (
        Production.objects
        .annotate(period=trunc_production)
        .values('period')
        .annotate(total_sales=Sum('sales'), total_boxes=Sum('boxes'))
        .order_by('period')
    )

    purchases_by_period_qs = (
        Purchase.objects
        .annotate(period=trunc_purchase)
        .values('period')
        .annotate(total_purchases=Sum('cost'))
        .order_by('period')
    )

    payments_by_period_qs = (
        Payment.objects
        .annotate(period=trunc_payment)
        .values('period')
        .annotate(total_payments=Sum('amount'))
        .order_by('period')
    )

    # Merge purchases + payments into expenses_by_period
    expenses_by_period = {}
    for row in purchases_by_period_qs:
        date = row['period'].date() if hasattr(row['period'], 'date') else row['period']
        expenses_by_period[date] = expenses_by_period.get(date, Decimal('0.00')) + (row['total_purchases'] or Decimal('0.00'))
    for row in payments_by_period_qs:
        date = row['period'].date() if hasattr(row['period'], 'date') else row['period']
        expenses_by_period[date] = expenses_by_period.get(date, Decimal('0.00')) + (row['total_payments'] or Decimal('0.00'))

    # Prepare chart data for sales/expenses over time
    labels, sales_data, expenses_data = [], [], []
    for row in sales_by_period_qs:
        p = row['period']
        label = p.date().isoformat() if hasattr(p, 'date') else p.isoformat()
        labels.append(label)

        total_sales_row = row['total_sales'] or Decimal('0.00')
        sales_data.append(float(total_sales_row))

        expenses_value = expenses_by_period.get(p.date() if hasattr(p, 'date') else p, Decimal('0.00'))
        expenses_data.append(float(expenses_value))

    # --- Datos para los charts de stock por medida (listas JSON-safe) ---
    stock_ml_names = [ing.name for ing in ingredients_ml]
    stock_ml_values = [ing.stock for ing in ingredients_ml]

    stock_u_names = [ing.name for ing in ingredients_u]
    stock_u_values = [ing.stock for ing in ingredients_u]

    stock_gm_names = [ing.name for ing in ingredients_gm]
    stock_gm_values = [ing.stock for ing in ingredients_gm]

    context = {
        'total_expenses': total_expenses_f,
        'total_income': total_income_f,
        'total_boxes': total_production,
        'net_profit': net_profit,
        'production_count': Production.objects.count(),

        # stock tables
        'stock_grams': grams,
        'stock_mls': mls,
        'stock_units': units,

        # top ingredients
        'top_names': json.dumps(top_names),
        'top_quantities': json.dumps(top_quantities),

        # sales/expenses charts
        'sales_labels': json.dumps(labels),
        'sales_data': json.dumps(sales_data),
        'expenses_data': json.dumps(expenses_data),

        # period selector
        'period': period,

        # stock-by-measure charts (JSON strings for insertion into JS)
        'stock_ml_names': json.dumps(stock_ml_names),
        'stock_ml_values': json.dumps(stock_ml_values),
        'stock_u_names': json.dumps(stock_u_names),
        'stock_u_values': json.dumps(stock_u_values),
        'stock_gm_names': json.dumps(stock_gm_names),
        'stock_gm_values': json.dumps(stock_gm_values),
    }

    return render(request, 'reports/dashboard.html', context)
