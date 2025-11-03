from django.shortcuts import render
from django.db.models import Count, Sum, F
from shophouse.models import Order, Product, Categories
import plotly.express as px
import pandas as pd

def format_currency(amount):
    if amount is None:
        return "UGX 0"
    return f"UGX {amount:,.0f}"

def dashboard(request):
    # Total Orders and Revenue
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

    # Popular Products with both quantity and revenue
    popular_products = (
        Order.objects
        .values('product__name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('product__price') * F('quantity'))
        )
        .order_by('-total_quantity')[:5]
    )
    
    if popular_products:
        # Convert to DataFrame for better plotting
        df_products = pd.DataFrame(popular_products)
        df_products['formatted_revenue'] = df_products['total_revenue'].apply(format_currency)
        
        # Create bar chart with quantity
        fig_products = px.bar(
            df_products,
            x='product__name',
            y='total_quantity',
            title='Top 5 Popular Products by Quantity Sold',
            labels={
                'product__name': 'Product Name',
                'total_quantity': 'Units Sold'
            },
            text='formatted_revenue'  # Show revenue on bars
        )
        fig_products.update_traces(textposition='outside')
        products_chart = fig_products.to_html(full_html=False)
    else:
        products_chart = "No product data available"

    # Category Distribution
    category_data = (
        Product.objects
        .values('Category__name')
        .annotate(count=Count('id'))
    )
    
    if category_data:
        fig_categories = px.pie(
            category_data,
            values='count',
            names='Category__name',
            title='Product Distribution by Category'
        )
        categories_chart = fig_categories.to_html(full_html=False)
    else:
        categories_chart = "No category data available"

    # Recent Orders with total amount
    recent_orders = (
        Order.objects
        .select_related('product', 'customer', 'customer__UserName')
        .annotate(
            total_amount=F('product__price') * F('quantity'),
            display_name=F('customer__UserName__user_name')
        )
        .order_by('-orderDate', '-id')[:5]
    )

    context = {
        'total_orders': total_orders,
        'total_revenue': format_currency(total_revenue),
        'products_chart': products_chart,
        'categories_chart': categories_chart,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
