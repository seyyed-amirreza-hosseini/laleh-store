from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Sum, Avg, Max, Min
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.mail import mail_admins, send_mail, BadHeaderError, EmailMessage
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage
from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem
from tags.models import TaggedItem
from .tasks import notify_customers
import requests


# @cache_page(5 * 60)
# def say_hello(request):
    # # Customers with .com account
    # queryset = Customer.objects.filter(email__icontains='.com')

    # # Collections that don't have a featured product
    # queryset = Collection.objects.filter(featured_product__isnull=True) 

    # # Products with low inventory (less than 10)
    # queryset = Product.objects.filter(inventory__lt=10)

    # # Orders placed by customer with id=1
    # queryset = Order.objects.filter(customer__id=1)

    # # Order items for products in collection 3
    # queryset = OrderItem.objects.filter(product__collection_id=3)

    # # Products: inventory < 10 OR price < 20
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    # # Products: inventory = price
    # queryset = Product.objects.filter(inventory=F('unit_price'))

    # queryset = Product.objects.order_by('title')
    # queryset = Product.objects.order_by('-title')

    # queryset = Product.objects.order_by('unit_price', '-title')
    # queryset = Product.objects.order_by('unit_price', '-title').reverse()

    # queryset = Product.objects.filter(collection_id=1).order_by('unit_price')

    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')

    # queryset = Product.objects.all()[:5]
    # queryset = Product.objects.all()[5:10]
    
    # queryset = Product.objects.values_list('id', 'title', 'collection__title')

    # # Select products that have been ordered and sort them by title
    # queryset = OrderItem.objects.values_list('product_id').distinct()
    # queryset = Product.objects.filter(id__in=queryset).order_by('title')

    # queryset = Product.objects.only('id', 'title')
    # queryset = Product.objects.defer('description')

    # # select_related(1) --> each product has only ONE collection
    # # prefetch_related(n) --> each product has MANY promotions
    # queryset = Product.objects.select_related('collection').all()
    # queryset = Product.objects.prefetch_related('promotions')
    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # # Get the last 5 orders with their customer and items (including product)
    # queryset = Order.objects.order_by('-placed_at')[:5].select_related('customer').prefetch_related('orderitem_set__product')

    # result = Product.objects.filter(collection_id=3).aggregate(numbers=Count('id'), min_price=Min('unit_price'))  
    
    # # How many orders do we have?
    # result = Order.objects.aaggregate(count=Count('id'))

    # # How many units of product 1 have we sold?
    # result = OrderItem.objects \
    #     .filter(product_id=1) \
    #     .aaggregate(units_sold=Sum('quantity'))
    
    # # How many orders has customer 1 placed?
    # result = Order.objects.filter(customer_id=1).aggregate(count=Count('id'))

    # # What is the min, max and average price of the products in collection 3?
    # result = Product.objects.filter(collection_id=3) \
    #     .aggregate(min=Min('unit_price'), max=Max('unit_price'), avg=Avg('unit_price'))
    
    # queryset = Customer.objects.annotate(is_new=Value(True))
    # queryset = Customer.objects.annotate(new_id=F('id') + 1)

    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )
    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # )

    # queryset = Customer.objects.annotate(orders_count=Count('order'))

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())    
    # queryset = Product.objects.annotate(
    #     discount_price=discounted_price
    # )

    # # Customers with their last order ID
    # queryset = Customer.objects.annotate(last_order_id=Max('order__id'))

    # # Collections and count of their products
    # queryset = Collection.objects.annotate(products=Count('product'))

    # # Customers with more than 5 orders  
    # queryset = Customer.objects.annotate(orders=Count('order')).filter(orders__gt=5)

    # # Customers and the total amount they’ve spent
    # queryset = Customer.objects.annotate(total_amount=Sum(
    #     F('order__orderitem__unit_price') * F('order__orderitem__quantity')
    # ))

    # # Top 5 best-selling products and their total sales
    # queryset = Product.objects.annotate(best_selling=Sum(
    #     F('orderitem__unit_price') * F('orderitem__quantity')
    # )).order_by('-best_selling')[:5]
    
    # TaggedItem.objects.get_tags_for(Product, 1)


    # # Create a shopping cart with an item
    # # cart = Cart()
    # # cart.save()

    # # item1 = CartItem()
    # # item1.cart = cart
    # # item1.product_id = 1
    # # item1.quantity = 1

    # # # Update the quantity of an item in a shopping cart 
    # # item1 = CartItem.objects.get(pk=1)
    # # item1.quantity = 2
    # # item1.save()

    # # # Remove a shopping cart with its items
    # # cart = Cart.objects.get(pk=1)
    # # cart.delete()

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # sending emails
    # try:
        # send_mail(
        #     subject='Order Foods',
        #     message='Hello bob! Your order is ready',
        #     from_email='info@amirrezabuy.com',
        #     recipient_list=['bob@amirrezabuy.com']
        # )
         
        # mail_admins(subject='subject', message='message', html_message='message')
        
        # message = EmailMessage(
        #     'subject',
        #     'message',
        #     'from@amirreza.com',
        #     ['cj@gmail.com']
        # )
        # message.attach_file('playground/static/images/jujube.jpg')
        # message.send()
        
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Amirreza'}
    #     )
    #     message.send(['ryder@gta.com'])

    # except BadHeaderError:
    #     pass
    # notify_customers.delay('Hello')
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()

    # return render(request, 'hello.html', {'name': data})

# class-based
class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
            response = requests.get('https://httpbin.org/delay/2')
            data = response.json()
            return render(request, 'hello.html', {'name': data})