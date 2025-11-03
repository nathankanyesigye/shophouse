from django.shortcuts import render
from django.db.models import Count, Sum, F, Avg, Max, Min, Case, When, Value, CharField
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate
from shophouse.models import Order, Product, Categories
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def format_currency(amount):
    if amount is None:
        return "UGX 0"
    return f"UGX {amount:,.0f}"

def dashboard(request):
    # Total Orders and Revenue
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

    # 1. Monthly Revenue Trend
    try:
        orders = Order.objects.all()
        monthly_data = {}
        
        for order in orders:
            date_key = f"{order.orderDate.year}-{order.orderDate.month:02d}"
            revenue = order.product.price * order.quantity
            monthly_data[date_key] = monthly_data.get(date_key, 0) + revenue
        
        if monthly_data:
            monthly_revenue_data = [
                {'date': k, 'revenue': v} 
                for k, v in sorted(monthly_data.items())
            ]
            
            fig_monthly = px.line(
                monthly_revenue_data,
                x='date',
                y='revenue',
                title='Monthly Revenue Trend',
                labels={'revenue': 'Revenue (UGX)', 'date': 'Month'}
            )
            monthly_chart = fig_monthly.to_html(full_html=False)
        else:
            monthly_chart = "No monthly revenue data available"
    except Exception as e:
        monthly_chart = "Error generating monthly revenue chart"

    # 2. Top Products by Revenue
    popular_products = (
        Order.objects
        .values('product__name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('product__price') * F('quantity'))
        )
        .order_by('-total_revenue')[:5]
    )
    
    if popular_products:
        df_products = pd.DataFrame(popular_products)
        df_products['formatted_revenue'] = df_products['total_revenue'].apply(format_currency)
        fig_products = px.bar(
            df_products,
            x='product__name',
            y='total_revenue',
            title='Top 5 Products by Revenue',
            labels={'product__name': 'Product', 'total_revenue': 'Revenue (UGX)'},
            text='formatted_revenue'
        )
        fig_products.update_traces(textposition='outside')
        products_chart = fig_products.to_html(full_html=False)
    else:
        products_chart = "No product data available"

    # 3. Category Distribution
    try:
        orders = Order.objects.select_related('product', 'product__Category')
        category_revenue = {}
        
        for order in orders:
            if order.product and order.product.Category:
                category_name = order.product.Category.name
                revenue = order.product.price * order.quantity
                category_revenue[category_name] = category_revenue.get(category_name, 0) + revenue
        
        if category_revenue:
            category_data = [
                {'category': k, 'revenue': v} 
                for k, v in category_revenue.items()
            ]
            
            fig_categories = px.pie(
                category_data,
                values='revenue',
                names='category',
                title='Revenue Distribution by Category'
            )
            categories_chart = fig_categories.to_html(full_html=False)
        else:
            categories_chart = "No category data available"
    except Exception as e:
        categories_chart = "Error generating category chart"

    # 4. Daily Order Volume
    try:
        orders = Order.objects.values_list('orderDate', flat=True)
        daily_counts = {}
        
        for order_date in orders:
            date_str = order_date.strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        if daily_counts:
            daily_data = [
                {'date': k, 'order_count': v} 
                for k, v in sorted(daily_counts.items())
            ]
            
            fig_daily = px.bar(
                daily_data,
                x='date',
                y='order_count',
                title='Daily Order Volume',
                labels={'date': 'Date', 'order_count': 'Number of Orders'}
            )
            daily_orders_chart = fig_daily.to_html(full_html=False)
        else:
            daily_orders_chart = "No daily order data available"
    except Exception as e:
        daily_orders_chart = "Error generating daily orders chart"

    # 5. Product Price Range Distribution
    try:
        products = Product.objects.all()
        price_ranges_dict = {
            'Under 10k': 0,
            '10k-50k': 0,
            '50k-100k': 0,
            'Over 100k': 0
        }
        
        for product in products:
            if product.price < 10000:
                price_ranges_dict['Under 10k'] += 1
            elif product.price < 50000:
                price_ranges_dict['10k-50k'] += 1
            elif product.price < 100000:
                price_ranges_dict['50k-100k'] += 1
            else:
                price_ranges_dict['Over 100k'] += 1

        price_data = [{'price_range': k, 'count': v} for k, v in price_ranges_dict.items()]
        
        if any(price_ranges_dict.values()):
            fig_prices = px.pie(
                price_data,
                values='count',
                names='price_range',
                title='Product Price Range Distribution'
            )
            price_range_chart = fig_prices.to_html(full_html=False)
        else:
            price_range_chart = "No price range data available"
    except Exception as e:
        price_range_chart = "Error generating price range chart"

    # 6. Order Status Distribution
    delivered_count = Order.objects.filter(status=True).count()
    pending_count = Order.objects.filter(status=False).count()
    
    status_data = [
        {'status': 'Delivered', 'count': delivered_count},
        {'status': 'Pending', 'count': pending_count}
    ]

    if delivered_count > 0 or pending_count > 0:
        fig_status = px.pie(
            status_data,
            values='count',
            names='status',
            title='Order Status Distribution',
            color_discrete_map={'Delivered': 'green', 'Pending': 'yellow'}
        )
        fig_status.update_traces(
            textinfo='percent+label',
            hovertemplate='Status: %{label}<br>Count: %{value}<br>Percentage: %{percent}'
        )
        status_chart = fig_status.to_html(full_html=False)
    else:
        status_chart = "No status data available"

    # 7. Average Order Value Trend
    try:
        orders = Order.objects.select_related('product').all()
        monthly_values = {}
        monthly_counts = {}
        
        for order in orders:
            date_key = f"{order.orderDate.year}-{order.orderDate.month:02d}"
            order_value = order.product.price * order.quantity
            monthly_values[date_key] = monthly_values.get(date_key, 0) + order_value
            monthly_counts[date_key] = monthly_counts.get(date_key, 0) + 1
        
        avg_data = []
        for date_key in sorted(monthly_values.keys()):
            if monthly_counts[date_key] > 0:
                avg_value = monthly_values[date_key] / monthly_counts[date_key]
                avg_data.append({
                    'date': date_key,
                    'avg_value': avg_value
                })
        
        if avg_data:
            fig_avg = px.line(
                avg_data,
                x='date',
                y='avg_value',
                title='Average Order Value Trend',
                labels={'avg_value': 'Average Order Value (UGX)', 'date': 'Month'}
            )
            avg_order_chart = fig_avg.to_html(full_html=False)
        else:
            avg_order_chart = "No average order value data available"
    except Exception as e:
        avg_order_chart = "Error generating average order value chart"

    # 8. Quantity per Product
    try:
        orders = Order.objects.select_related('product').all()
        product_quantities = {}
        
        for order in orders:
            if order.product:
                product_name = order.product.name
                product_quantities[product_name] = product_quantities.get(product_name, 0) + order.quantity
        
        # Sort and get top 10
        sorted_products = sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)[:10]
        quantity_data = [
            {'product_name': name, 'total_quantity': qty} 
            for name, qty in sorted_products
        ]
        
        if quantity_data:
            fig_quantity = px.bar(
                quantity_data,
                x='product_name',
                y='total_quantity',
                title='Top 10 Products by Quantity Sold',
                labels={'product_name': 'Product', 'total_quantity': 'Units Sold'}
            )
            quantity_chart = fig_quantity.to_html(full_html=False)
        else:
            quantity_chart = "No quantity data available"
    except Exception as e:
        quantity_chart = "Error generating quantity chart"

    # Recent Orders
    try:
        recent_orders = (
            Order.objects
            .select_related('product', 'customer', 'customer__UserName')
            .order_by('-orderDate', '-id')[:5]
        )
        
        # Calculate total amounts in Python
        for order in recent_orders:
            order.total_amount = order.product.price * order.quantity if order.product else 0
    except Exception as e:
        recent_orders = []

    context = {
        'total_orders': total_orders,
        'total_revenue': format_currency(total_revenue),
        'monthly_chart': monthly_chart,
        'products_chart': products_chart,
        'categories_chart': categories_chart,
        'daily_orders_chart': daily_orders_chart,
        'price_range_chart': price_range_chart,
        'status_chart': status_chart,
        'avg_order_chart': avg_order_chart,
        'quantity_chart': quantity_chart,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
