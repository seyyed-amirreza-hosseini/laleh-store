from django.shortcuts import render
from store.models import Product, Customer, Collection, Order, OrderItem

def say_hello(request):
    # Customers with .com account
    queryset = Customer.objects.filter(email__icontains='.com')

    # Collections that don't have a featured product
    queryset = Collection.objects.filter(featured_product__isnull=True) 

    # Products with low inventory (less than 10)
    queryset = Product.objects.filter(inventory__lt=10)

    # Orders placed by customer with id=1
    queryset = Order.objects.filter(customer__id=1)

    # Order items for products in collection 3
    queryset = OrderItem.objects.filter(product__collection_id=3)

    return render(request, 'hello.html', {'name': 'Amirreza', 'products': list(queryset)})
