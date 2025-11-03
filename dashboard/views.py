from django.shortcuts import render
from django.db.models import Count, Sum
from shophouse.models import Order, Product, Categories
import plotly.express as px
import pandas as pd

def dashboard(request):
    # Total Orders and Revenue
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('product__price'))['total'] or 0

    # Popular Products
    popular_products = (
        Order.objects
        .values('product__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    
    if popular_products:
        fig_products = px.bar(
            popular_products,
            x='product__name',
            y='count',
            title='Top 5 Popular Products'
        )
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

    # Recent Orders
    recent_orders = Order.objects.select_related('product', 'customer').order_by('-orderDate')[:5]

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products_chart': products_chart,
        'categories_chart': categories_chart,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
    
    sales_df = pd.DataFrame(sales_data)
    if not sales_df.empty:
        fig_sales = px.line(
            sales_df,
            x='date',
            y='total_sales',
            title='Daily Sales'
        )
        sales_chart = fig_sales.to_html(full_html=False)
    else:
        sales_chart = "No sales data available"

    # Popular Products
    popular_products = (
        Order.objects
        .values('product__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )
    
    if popular_products:
        fig_products = px.bar(
            popular_products,
            x='product__name',
            y='total_quantity',
            title='Top 5 Popular Products'
        )
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

    # Recent Orders
    recent_orders = Order.objects.order_by('-orderDate')[:5]

    context = {
        'sales_chart': sales_chart,
        'products_chart': products_chart,
        'categories_chart': categories_chart,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
